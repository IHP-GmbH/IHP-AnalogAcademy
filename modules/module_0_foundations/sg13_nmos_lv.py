import os
from mosplot.lookup_table_generator.simulators import NgspiceSimulator, HspiceSimulator
from mosplot.lookup_table_generator import LookupTableGenerator, TransistorSweep
# One of `include_paths` or `lib_mappings` must be specified.
# The rest are optional.

# Read environment variables to build model path
PDK_ROOT = os.environ["PDK_ROOT"]
PDK = os.environ["PDK"]

model_path = os.path.join(PDK_ROOT, PDK, "libs.tech/ngspice/models/cornerMOSlv.lib")

ngspice = NgspiceSimulator(
    # Provide path to simulator if simulator is not in system path.
    simulator_path="ngspice",

    # Default simulation temperature. Override if needed.
    temperature=27,

    # All parameters are saved by default. Override if needed.
    parameters_to_save=["id", "vth", "vdsat", "gm","gds","vgs"],


    # Files to include with `.LIB`.
      lib_mappings = [
    (model_path, "mos_tt")
    ],

    # If the transistor is defined inside a subcircuit in
    # the library files, you must specify the symbol used (first entry)
    # and the hierarchical name (second entry). Override if needed.
    mos_spice_symbols = ("XM1", "n.xm1.nsg13_lv_nmos"),

 

    # Specify the width. For devices that do not take a width,
    # you can specify other parameters such as the number of fingers.
    # The keys are exactly those recognized by the model.
    device_parameters = {
        "w": 10e-6,
    }
)

nmos_sweep = TransistorSweep(
    mos_type="nmos",
    vgs=(0, 1.2, 0.1),
    vds=(0, 1.2, 0.1),
    vbs=(0, -1.2, -0.1),
    length = [130e-9,260e-9,520e-9]
    #length = [130e-9, 260e-9, 390e-9, 520e-9, 650e-9, 780e-9, 910e-9, 1040e-9, 1170e-9, 1300e-9, 1430e-9, 1560e-9, 1690e-9, 1820e-9, 1950e-9, 2080e-9, 2210e-9, 2340e-9, 2470e-9, 2600e-9, 2730e-9, 2860e-9, 2990e-9, 3120e-9, 3250e-9, 3380e-9, 3510e-9, 3640e-9, 3770e-9, 3900e-9, 4030e-9, 4160e-9, 4290e-9, 4420e-9, 4550e-9, 4680e-9, 4810e-9, 4940e-9, 5070e-9, 5200e-9, 5330e-9, 5460e-9, 5590e-9, 5720e-9, 5850e-9, 5980e-9, 6110e-9, 6240e-9, 6370e-9, 6500e-9, 6630e-9, 6760e-9, 6890e-9, 7020e-9, 7150e-9, 7280e-9, 7410e-9, 7540e-9, 7670e-9, 7800e-9, 7930e-9, 8060e-9, 8190e-9, 8320e-9, 8450e-9, 8580e-9, 8710e-9, 8840e-9, 8970e-9, 9100e-9, 9230e-9, 9360e-9, 9490e-9, 9620e-9, 9750e-9, 9880e-9]
)


obj = LookupTableGenerator(
    description="sg13_nmos_lv",
    simulator=ngspice,
    model_sweeps={
        "sg13_lv_nmos ": nmos_sweep,
    },
    n_process=2,
)

# obj.op_simulation()
obj.build("./sg13_nmos_lv_LUT")


