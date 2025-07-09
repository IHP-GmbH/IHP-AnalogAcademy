# imports <<<
import os
import tempfile

import numpy as np

from .base_simulator import BaseSimulator
from .parsers.ngspice import parse_file
# >>>

class NgspiceSimulator(BaseSimulator):
    def __init__(
        self,
        *,
        temperature=27,
        raw_spice=None,
        lib_mappings=None,
        include_paths=None,
        osdi_paths=None,
        simulator_path="ngspice",
        mos_spice_symbols=("m1", "m1"),
        device_parameters={"w": 10e-6},
        parameters_to_save=["weff", "id", "vth", "vdsat", "vdssat", "gm", "gmbs", "gds", "cgg", "cgs", "cgb", "cgd", "cdd"],
    ):
        super().__init__(
                raw_spice=raw_spice,
                temperature=temperature,
                lib_mappings=lib_mappings,
                include_paths=include_paths,
                simulator_path=simulator_path,
                mos_spice_symbols=mos_spice_symbols,
                device_parameters=device_parameters,
                parameters_to_save=parameters_to_save,
        )
        self.osdi_paths = osdi_paths
        self._init_config["osdi_paths"] = osdi_paths

    def make_temp_files(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.input_file_path = os.path.join(self.tmp_dir, "input.txt")
        self.log_file_path = os.path.join(self.tmp_dir, "log.txt")
        self.output_file_path = os.path.join(self.tmp_dir, "output.txt")

    def build_simulation_command(self, verbose):
        if verbose:
            return [self.simulator_path, "-b", self.input_file_path]
        return [self.simulator_path, "-b", "-o", self.log_file_path, self.input_file_path]

    def setup_op_simulation(self, sweep):
        osdi = None
        if self.osdi_paths:
            osdi = "\n".join([f"pre_osdi {p}" for p in self.osdi_paths])
        return [
            f".options TEMP = {self.temperature}",
            f".options TNOM = {self.temperature}",
            ".control",
            osdi,
            "op",
            "show all",
            ".endc",
            ".end",
        ]

    def setup_dc_simulation(self, sweep):
        symbol = self.mos_spice_symbols[1]
        self.parameter_table = {
            "id":     ["save i(vds)",             "i(i_vds)"],
            "weff":   [f"save @{symbol}[weff]",   f"v(@{symbol}[weff])"],
            "vth":    [f"save @{symbol}[vth]",    f"v(@{symbol}[vth])"],
            "vdsat":  [f"save @{symbol}[vdsat]",  f"v(@{symbol}[vdsst])"],
            "vdssat": [f"save @{symbol}[vdssat]", f"v(@{symbol}[vdssat])"],
            "gm":     [f"save @{symbol}[gm]",     f"@{symbol}[gm]"],
            "gmbs":   [f"save @{symbol}[gmbs]",   f"@{symbol}[gmbs]"],
            "gds":    [f"save @{symbol}[gds]",    f"@{symbol}[gds]"],
            "cgg":    [f"save @{symbol}[cgg]",    f"@{symbol}[cgg]"],
            "cgs":    [f"save @{symbol}[cgs]",    f"@{symbol}[cgs]"],
            "cbg":    [f"save @{symbol}[cbg]",    f"@{symbol}[cbg]"],
            "cgd":    [f"save @{symbol}[cgd]",    f"@{symbol}[cgd]"],
            "cdd":    [f"save @{symbol}[cdd]",    f"@{symbol}[cdd]"],
        }
        self.parameter_table = { k: v for k, v in self.parameter_table.items() if k in self.parameters_to_save }
        vgs_start, vgs_stop, vgs_step = sweep.vgs
        vds_start, vds_stop, vds_step = sweep.vds
        analysis_string = f"dc VDS {vds_start} {vds_stop} {vds_step} VGS {vgs_start} {vgs_stop} {vgs_step}"
        osdi = None
        if self.osdi_paths:
            osdi = "\n".join([f"pre_osdi {p}" for p in self.osdi_paths])
        polarity = "-" if sweep.mos_type == "nmos" else ""
        return [
            f".options TEMP = {self.temperature}",
            f".options TNOM = {self.temperature}",
            ".control",
            osdi,
            "\n".join([val[0] for val in self.parameter_table.values()]),
            analysis_string,
            f"let i_vds = {polarity}i(vds)",
            f"write {self.output_file_path} all",
            ".endc",
            ".end",
        ]

    def parse_output(self):
        analysis, _ = parse_file(self.output_file_path)
        return analysis

    def extract_parameters(self, analysis, n_vgs, n_vds):
        results = {}
        column_names = analysis[0].dtype.names
        data = analysis[0]
        for p in self.parameter_table.keys():
            col_name = self.parameter_table[p][1]
            if col_name in column_names:
                res = np.array(data[col_name]).reshape(n_vgs, n_vds)
                results[p] = res
        return results

    def save_parameters(self, analysis, transistor_type, length, vbs, lookup_table, n_vgs, n_vds):
        column_names = analysis[0].dtype.names
        data = analysis[0]
        for p in self.parameter_table.keys():
            col_name = self.parameter_table[p][1]
            if col_name in column_names:
                res = np.array(data[col_name]).reshape(n_vgs, n_vds)
                lookup_table[transistor_type][p][length][vbs] = res
