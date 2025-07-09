# imports <<<
import os
import tempfile

import numpy as np

from .base_simulator import BaseSimulator
from .parsers.hspice import parse_file
# >>>

class HspiceSimulator(BaseSimulator):
    def __init__(
        self,
        temperature=27,
        raw_spice=None,
        hdl_paths=None,
        lib_mappings=None,
        include_paths=None,
        simulator_path="hspice",
        device_parameters={"w": 10e-6},
        mos_spice_symbols=("m1", "m1"),
        parameters_to_save=["id", "vth", "vdsat", "gm", "gmbs", "gds", "cgg", "cgs", "cgb", "cgd", "cdd"],
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
        self.hdl_paths = hdl_paths
        self._init_config["hdl_paths"] = hdl_paths

    def make_temp_files(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.input_file_path = os.path.join(self.tmp_dir, "input.txt")
        self.log_file_path = os.path.join(self.tmp_dir, "input.lis")
        self.output_file_path = os.path.join(self.tmp_dir, "input.sw0")
        self.decoded_output_path = os.path.join(self.tmp_dir, "input_sw0.pickle")

    def build_simulation_command(self, verbose):
        if verbose:
            return [self.simulator_path, self.input_file_path]
        return [self.simulator_path, "-i", self.input_file_path, "-o", self.tmp_dir]

    def setup_op_simulation(self, sweep):
        hdl = None
        if self.hdl_paths:
            hdl = "\n".join([f".hdl {p}" for p in self.hdl_paths])
        return [
            hdl,
            f".TEMP = {self.temperature}",
            ".option POST=2",
            ".op",
            ".end",
        ]

    def setup_dc_simulation(self, sweep):
        symbol = self.mos_spice_symbols[1]
        polarity = "-" if sweep.mos_type == "nmos" else ""
        self.parameter_table = {
            "id": [
                f".probe DC m_id = par('{polarity}i(vds)')",
                "m_id"
            ],
            "vth": [
                f".probe DC m_vth = par('vth({symbol})')",
                "m_vth"
            ],
            "vdsat": [
                f".probe DC m_vdsat = par('vdsat({symbol})')",
                "m_vdsat",
            ],
            "gm": [
                f".probe DC m_gm = par('gmo({symbol})')",
                "m_gm"
            ],
            "gmbs": [
                f".probe DC m_gmb = par('gmbso({symbol})')",
                "m_gmb",
            ],
            "gds": [
                f".probe DC m_gds = par('gdso({symbol})')",
                "m_gds",
            ],
            "cgg": [
                f".probe DC m_cgg = par('cggbo({symbol})')",
                "m_cgg",
            ],
            "cgs": [
                f".probe DC m_cgs = par('-cgsbo({symbol})')",
                "m_cgs",
            ],
            "cgd": [
                f".probe DC m_cgd = par('-cgdbo({symbol})')",
                "m_cgd",
            ],
            "cgb": [
                f".probe DC m_cgb = par('cggbo({symbol})-(-cgsbo({symbol}))-(-cgdbo({symbol}))')",
                "m_cgb",
            ],
            "cdd": [
                f".probe DC m_cdd = par('cddbo({symbol})')",
                "m_cdd",
            ],
            "css": [
                f".probe DC m_css = par('-cgsbo({symbol})-cbsbo({symbol})')",
                "m_css",
            ],
        }
        self.parameter_table = { k: v for k, v in self.parameter_table.items() if k in self.parameters_to_save }
        vgs_start, vgs_stop, vgs_step = sweep.vgs
        vds_start, vds_stop, vds_step = sweep.vds
        analysis_string = f".dc VGS {vgs_start} {vgs_stop} {vgs_step} VDS {vds_start} {vds_stop} {vds_step}"
        hdl = None
        if self.hdl_paths:
            hdl = "\n".join([f".hdl {p}" for p in self.hdl_paths])
        return [
            hdl,
            f".TEMP = {self.temperature}",
            ".options probe dccap brief accurate",
            ".option POST=2",
            "\n".join([val[0] for val in self.parameter_table.values()]),
            analysis_string,
            ".end",
        ]

    def parse_output(self):
        return parse_file(self.output_file_path)

    def extract_parameters(self, analysis, n_vgs, n_vds):
        results = {}
        for p in self.parameters_to_save:
            col_name = self.parameter_table[p][1]
            if col_name in analysis.keys():
                res = np.array(analysis[col_name]).T
                results[p] = res
        return results

    def save_parameters(self, analysis, transistor_type, length, vbs, lookup_table, n_vgs, n_vds):
        for p in self.parameters_to_save:
            col_name = self.parameter_table[p][1]
            if col_name in analysis.keys():
                res = np.array(analysis[col_name]).T
                lookup_table[transistor_type][p][length][vbs] = res

