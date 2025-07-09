# imports <<<
import numpy as np
from multiprocessing import Process, Queue
from .spice_mosfet_netlist_generator import SpiceMosfetNetlistGenerator
from .utils import list_to_string
# >>>

# worker <<<
def worker(job_queue, result_queue, simulator, netlist_gen):
    """
    Each worker clones the simulator, creates its temporary files,
    processes jobs from job_queue, and places the results into result_queue.
    """
    # Clone the simulator and initialize temporary files.
    sim = simulator.clone()
    sim.make_temp_files()

    while True:
        job = job_queue.get()
        if job is None:
            break

        # Unpack the job.
        (transistor_name, l_idx, vbs_idx, length, vbs_val, sweep, n_vgs, n_vds) = job

        # Generate netlist and simulation setup.
        netlist = netlist_gen.generate_netlist(transistor_name, length, vbs_val)
        sim_setup = sim.setup_dc_simulation(sweep)
        full_netlist = netlist + sim_setup

        # Run simulation.
        sim.run_simulation(full_netlist, verbose=False)
        analysis = sim.parse_output()
        results = sim.extract_parameters(analysis, n_vgs, n_vds)

        # Put the result into the result queue.
        result_queue.put((transistor_name, l_idx, vbs_idx, results))

   # Remove temporary files after processing all jobs.
    sim.remove_temp_files()
# >>>

class MosfetSimulation:
    def __init__(self, simulator, model_sweeps, n_process):
        """
        simulator   : instance of HspiceSimulator or NgspiceSimulator.
        model_sweeps: dict mapping transistor names to TransistorSweep objects.
        width       : transistor width.
        n_process   : number of parallel processes.
        """
        self.simulator = simulator
        self.sweeps = model_sweeps
        self.n_process = n_process

        # Create a netlist generator.
        self.netlist_generator = SpiceMosfetNetlistGenerator(
            model_sweeps,
            simulator.device_parameters,
            simulator.mos_spice_symbols,
            simulator.include_paths,
            simulator.lib_mappings,
            simulator.raw_spice,
        )

        # Initialize lookup table.
        self.lookup_table = {}
        for mosfet_model, sweep in self.sweeps.items():
            n_vgs = int(round((sweep.vgs[1] - sweep.vgs[0]) / sweep.vgs[2])) + 1
            n_vds = int(round((sweep.vds[1] - sweep.vds[0]) / sweep.vds[2])) + 1
            n_vbs = int(round((sweep.vbs[1] - sweep.vbs[0]) / sweep.vbs[2])) + 1
            self.lookup_table[mosfet_model] = {
                p: np.zeros((len(sweep.length), n_vbs, n_vgs, n_vds), dtype=np.float32)
                for p in simulator.parameters_to_save
            }

    def get_single_netlist(self, sim_type="dc"):
        """
        Return a netlist for printing or op simulation.
        """
        # Select the first transistor sweep for a sample netlist.
        transistor_name, sweep = next(iter(self.sweeps.items()))
        length = sweep.length[0]
        n_vbs = int(round((sweep.vbs[1] - sweep.vbs[0]) / sweep.vbs[2])) + 1
        vbs_val = np.linspace(sweep.vbs[0], sweep.vbs[1], n_vbs)[0]

        # Make netlist.
        netlist = self.netlist_generator.generate_netlist(transistor_name, length, vbs_val)
        if sim_type == "dc":
            sim_setup = self.simulator.setup_dc_simulation(sweep)
        else:
            sim_setup = self.simulator.setup_op_simulation(sweep)

        full_netlist = netlist + sim_setup
        return full_netlist

    def print_netlist(self, netlist=None):
        """
        Print a sample netlist.
        """
        if netlist is None:
            netlist = self.get_single_netlist(sim_type="dc")
        print("----- Sample Netlist -----")
        print(list_to_string(netlist))
        print("--------------------------")

    def op_simulation(self):
        """
        Perform an op simulation, displaying the result.
        """
        self.simulator.make_temp_files()
        netlist = self.get_single_netlist(sim_type="op")
        self.print_netlist(netlist)
        self.simulator.run_simulation(netlist, verbose=True)
        self.simulator.remove_temp_files()

    def simulate(self):
        """
        Build a list of simulation jobs and spawn worker processes.
        """
        # Build job list.
        jobs = []
        for transistor_name, sweep in self.sweeps.items():
            n_vgs = int(round((sweep.vgs[1] - sweep.vgs[0]) / sweep.vgs[2])) + 1
            n_vds = int(round((sweep.vds[1] - sweep.vds[0]) / sweep.vds[2])) + 1
            n_vbs = int(round((sweep.vbs[1] - sweep.vbs[0]) / sweep.vbs[2])) + 1
            vbs_values = np.linspace(sweep.vbs[0], sweep.vbs[1], n_vbs)
            for l_idx, length in enumerate(sweep.length):
                for vbs_idx, vbs_val in enumerate(vbs_values):
                    jobs.append((transistor_name, l_idx, vbs_idx, length, vbs_val, sweep, n_vgs, n_vds))
        self.print_netlist()
        total_jobs = len(jobs)
        print(f"Total simulation jobs: {total_jobs}")

        # Create queues.
        job_queue = Queue()
        result_queue = Queue()

        # Enqueue all jobs.
        for job in jobs:
            job_queue.put(job)

        # Place a sentinel (None) for each worker to know when to stop.
        for _ in range(self.n_process):
            job_queue.put(None)

        # Spawn worker processes.
        processes = []
        for _ in range(self.n_process):
            p = Process(target=worker, args=(job_queue, result_queue, self.simulator, self.netlist_generator))
            p.start()
            processes.append(p)

        # Collect results with progress updates.
        results = []
        for i in range(total_jobs):
            result = result_queue.get()
            print(f"Progress: {i + 1}/{total_jobs} jobs completed")
            results.append(result)

        # Wait for all workers to finish.
        for p in processes:
            p.join()

        # Insert results into the lookup table.
        for transistor_name, l_idx, vbs_idx, result_dict in results:
            for p, res in result_dict.items():
                self.lookup_table[transistor_name][p][l_idx][vbs_idx] = res

