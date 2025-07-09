# imports <<<
import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from typing import Any, List
from .utils import list_to_string
# >>>

class BaseSimulator(ABC):
    def __init__(self, *, device_parameters, simulator_path, include_paths, lib_mappings, raw_spice,  mos_spice_symbols, parameters_to_save, temperature):
        self.raw_spice = raw_spice
        self.temperature = temperature
        self.lib_mappings = lib_mappings
        self.include_paths = include_paths
        self.simulator_path = simulator_path
        self.mos_spice_symbols = mos_spice_symbols
        self.device_parameters = device_parameters
        self.parameters_to_save = parameters_to_save
        self.tmp_dir = None
        self._init_config = {
            "raw_spice": raw_spice,
            "temperature": temperature,
            "lib_mappings": lib_mappings,
            "include_paths": include_paths,
            "simulator_path": simulator_path,
            "mos_spice_symbols": mos_spice_symbols,
            "device_parameters": device_parameters,
            "parameters_to_save": parameters_to_save,
        }
        self.validate_paths()
        self.tmp_dir = "/tmp/"
        self.input_file_path = "input"
        self.output_file_path = "output"
        self.log_file_path = "log"

    @abstractmethod
    def make_temp_files(self) -> None:
        pass

    @abstractmethod
    def build_simulation_command(self, verbose) -> List:
        pass

    @abstractmethod
    def setup_op_simulation(self, sweep) -> List:
        return []

    @abstractmethod
    def setup_dc_simulation(self, sweep) -> List:
        pass

    @abstractmethod
    def parse_output(self) -> Any:
        pass

    @abstractmethod
    def save_parameters(self, analysis, transistor_type, length, vbs, lookup_table, n_vgs, n_vds):
        pass

    @abstractmethod
    def extract_parameters(self, analysis, n_vgs, n_vds):
        pass

    def clone(self):
        return self.__class__(**self._init_config)

    def remove_temp_files(self):
        if self.tmp_dir and os.path.isdir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def validate_paths(self):
        paths = []
        if self.include_paths:
            for p in self.include_paths:
                paths.append(p)
        if self.lib_mappings:
            for item in self.lib_mappings:
                paths.append(item[0])
        for path in paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Path {path} not found.")
        if not shutil.which(self.simulator_path):
            raise ValueError(f"Binary '{self.simulator_path}' not accessible.")


    def run_simulation(self, netlist, verbose=False):
        # Write the netlist to the input file.
        with open(self.input_file_path, "w") as f:
            f.write(list_to_string(netlist))

        # Build the command as a list of arguments.
        cmd = self.build_simulation_command(verbose)

        if verbose:
            # Run process and print the output directly.
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as proc:
                for line in proc.stdout:
                    print(line, end="")
        else:
            # Run the process without printing output.
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                with open(self.log_file_path, "r") as log_file:
                    log_contents = log_file.read()
                self.remove_temp_files()
                raise Exception(f"Simulation error: {log_contents}")
