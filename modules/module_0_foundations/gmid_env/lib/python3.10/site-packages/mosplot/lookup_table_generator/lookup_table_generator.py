# imports <<<
import os

import numpy as np

from .simulators.spice_simulators.mosfet_simulation import MosfetSimulation
from .table_cleanup import LookupTableCleaner

# >>>

class LookupTableGenerator:
    def __init__(
        self,
        *,
        simulator,
        model_sweeps,
        n_process=1,
        description="gmid lookup table",
    ):
        self.model_sweeps = model_sweeps
        self.simulator = simulator
        self.description = description
        self.n_process = n_process

    def op_simulation(self):
        simulation = MosfetSimulation(
            self.simulator,
            self.model_sweeps,
            self.n_process
        )
        simulation.op_simulation()

    def build(self, filepath):
        def range_args(tup):
            n = int(round((tup[1] - tup[0]) / tup[2])) + 1
            return np.linspace(tup[0], tup[1], n)

        # Create MosfetSimulation instance.
        simulation = MosfetSimulation(
            self.simulator,
            self.model_sweeps,
            self.n_process
        )

        # Run all simulation jobs with progress updates.
        simulation.simulate()
        loopup_table = simulation.lookup_table
        parameters_to_save = [key.lower() for key in self.simulator.parameters_to_save]
        device_parameters = {key.lower(): value for key, value in self.simulator.device_parameters.items()}

        # Cleanup table to remove entries for parameters that were not found
        # or parameters that have a constant value throughout.
        cleaner = LookupTableCleaner(loopup_table, parameters_to_save)
        cleaner.clean_lookup_table()

        # Store general and grid information.
        loopup_table["description"] = self.description
        loopup_table["simulator"] = self.simulator.__class__.__name__
        loopup_table["parameter_names"] = parameters_to_save
        loopup_table["device_parameters"] = device_parameters
        for transistor_name, sweep in self.model_sweeps.items():
            loopup_table[transistor_name]["vgs"] = range_args(sweep.vgs)
            loopup_table[transistor_name]["vds"] = range_args(sweep.vds)
            loopup_table[transistor_name]["vbs"] = range_args(sweep.vbs)
            loopup_table[transistor_name]["length"] = np.array(sweep.length)
            loopup_table[transistor_name]["model_name"] = transistor_name
            loopup_table[transistor_name]["parameter_names"] = parameters_to_save
            loopup_table[transistor_name]["device_parameters"] = device_parameters

        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        np.savez_compressed(f"{filepath}.npz", lookup_table=np.array(loopup_table, dtype=object))
        print("Done")
