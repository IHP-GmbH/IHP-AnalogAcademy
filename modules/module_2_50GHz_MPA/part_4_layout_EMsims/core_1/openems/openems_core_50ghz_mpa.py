import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

import modules.util_stackup_reader as stackup_reader
import modules.util_gds_reader as gds_reader
import modules.util_utilities as utilities
import modules.util_simulation_setup as simulation_setup
import modules.util_meshlines as util_meshlines

import os
import matplotlib.pyplot as plt  # pip install matplotlib
import numpy as np
from CSXCAD import ContinuousStructure
from CSXCAD import AppCSXCAD_BIN
from openEMS import openEMS
from openEMS.physical_constants import *


# Model comments
# Changes for IHP Analog Academy in 01/2026:
# Changed to MUR boundary at zmax so that radiation can be absorbed.
# From experience, using MUR can create numerical issue when it touches the lossy silicon, so it is ONLY used at zmax.
# All other boundaries use PEC, for best simulation speed.
# Distance to side walls reduced, we have not much field there because of the Metal1 ground layout.

# This model uses an alternative syntax where are settings are stored in settings dictionary,
# which makes it easier to implement future extensions without touching again the 
# simulation model code


# ======================== workflow settings ================================
settings = {}

settings['preview_only'] = False  # @brief Enable this to preview model/mesh only, without starting simulation
settings['postprocess_only'] = False # @brief Enable this to show existing results only, without starting simulation

# ===================== input files and path settings =======================

# GDS filename
gds_filename = "../layout_gds/50_ghz_mpa_core_no_BJT.gds"      # geometries
XML_filename = "SG13G2.xml"       # stackup

settings['purpose'] = [0] # @brief Which GDSII data type is evaluated? Values in [] can be separated by comma
settings['preprocess_gds'] = False  # @brief  Preprocess GDSII for safe handling of cutouts/holes?
settings['merge_polygon_size'] = 0.5 #  @brief  Merge via polygons with distance less than .. microns, set to 0 to disable via merging.

# get path for this simulation file
script_path = utilities.get_script_path(__file__)

# use script filename as model basename
model_basename = utilities.get_basename(__file__)

# set and create directory for simulation output
sim_path = utilities.create_sim_path (script_path,model_basename)
print('Simulation data directory: ', sim_path)


# ======================== simulation settings ================================


settings['unit']   = 1e-06  # @brief Geometry units, 1E-6 is in microns
settings['margin'] = 20    # @brief Distance from GDSII geometry boundary to simulation boundary, in project units 

settings['fstart']   = 0e9  # @brief start frequency [Hz]
settings['fstop']    = 350e9 # @brief stop frequency [Hz]
settings['numfreq']  = 401  # @brief number of frequency steps [Hz]

settings['refined_cellsize'] = 0.5  # @brief mesh cell size in conductor region, in project units

# choices for boundary:
# 'PEC' : perfect electric conductor (default)
# 'PMC' : perfect magnetic conductor, useful for symmetries
# 'MUR' : simple MUR absorbing boundary conditions
# 'PML_8' : PML absorbing boundary conditions
settings['Boundaries'] = ['PEC', 'PEC', 'PEC', 'PEC', 'PEC', 'MUR']

settings['cells_per_wavelength'] = 20   # @brief how many mesh cells per wavelength, must be 10 or more
settings['energy_limit'] = -50          # @brief end criteria for residual energy (dB), default is -40


# ports from GDSII Data, polygon geometry from specified special layer
# note that for multiport simulation, excitations are switched on/off in simulation_setup.createSimulation below
simulation_ports = simulation_setup.all_simulation_ports()
# instead of in-plane port specified with target_layername, we here use via port specified with from_layername and to_layername. GND means bottom of simulation box
simulation_ports.add_port(simulation_setup.simulation_port(portnumber=1, voltage=1, port_Z0=50, source_layernum=201, from_layername='Metal3', to_layername='TopMetal2', direction='z'))
simulation_ports.add_port(simulation_setup.simulation_port(portnumber=2, voltage=1, port_Z0=50, source_layernum=202, from_layername='Metal3', to_layername='TopMetal2', direction='z'))
simulation_ports.add_port(simulation_setup.simulation_port(portnumber=3, voltage=1, port_Z0=50, source_layernum=203, target_layername='Metal2', direction='-x'))
simulation_ports.add_port(simulation_setup.simulation_port(portnumber=4, voltage=1, port_Z0=50, source_layernum=204, target_layername='Metal2', direction='x'))

# ======================== simulation ================================

# get technology stackup data
materials_list, dielectrics_list, metals_list = stackup_reader.read_substrate (XML_filename)
# get list of layers from technology
layernumbers = metals_list.getlayernumbers()
layernumbers.extend(simulation_ports.portlayers)

# read geometries from GDSII, only purpose 0
allpolygons = gds_reader.read_gds(gds_filename,
                                  layernumbers,
                                  purposelist=settings['purpose'],
                                  metals_list=metals_list,
                                  preprocess=settings['preprocess_gds'],
                                  merge_polygon_size=settings['merge_polygon_size'])


########### create model, run and post-process ###########

settings['simulation_ports'] = simulation_ports
settings['materials_list'] = materials_list
settings['dielectrics_list'] = dielectrics_list
settings['metals_list'] = metals_list
settings['layernumbers'] = layernumbers
settings['allpolygons'] = allpolygons
settings['sim_path'] = sim_path
settings['model_basename'] = model_basename

# define excitation and stop criteria and boundaries
FDTD = openEMS(EndCriteria=np.exp(settings['energy_limit']/10 * np.log(10)))
FDTD.SetGaussExcite((settings['fstart'] + settings['fstop'])/2,
                    (settings['fstop'] - settings['fstart'])/2)
FDTD.SetBoundaryCond(settings['Boundaries'])


########### create model, run and post-process ###########

# run all port excitations, one after another
for port in simulation_ports.ports:
    settings['excite_portnumbers'] = [port.portnumber]

    # prepare model from GDSII data
    simulation_setup.setupSimulation(FDTD=FDTD, settings=settings)  # must use named parameters when using settings dict!

    # preview model and start simulation
    simulation_setup.runSimulation(FDTD=FDTD, settings=settings)    # must use named parameters when using settings dict!


# Initialize an empty matrix for S-parameters
num_ports = simulation_ports.portcount
s_params = np.empty((num_ports, num_ports, settings['numfreq']), dtype=object)

# Define frequency resolution (postprocessing)
f = np.linspace(settings['fstart'], settings['fstop'], settings['numfreq'])

# Populate the S-parameter matrix with simulation results
for i in range(1, num_ports + 1):
    for j in range(1, num_ports + 1):
        s_params[i-1, j-1] = utilities.calculate_Sij(i, j, f, sim_path, simulation_ports)

# Write to Touchstone *.snp file
snp_name = os.path.join(sim_path, model_basename + '.s' + str(num_ports) + 'p')
utilities.write_snp(s_params, f, snp_name)

print('Created S-parameter output file at ', snp_name)


# ------------------ optional data plots -----------------------------


def dB(value):
    value = np.asarray(value, dtype=np.complex128)
    return 20.0*np.log10(np.abs(value))        

def phase(value):
    value = np.asarray(value, dtype=np.complex128)
    return np.angle(value, deg=True) 

def S(i,j):
    # get S-params from zero-based data array
    return s_params[i-1, j-1]


print('\nStarting plots')

fig, axis = plt.subplots(num="S11", tight_layout=True)
axis.plot(f/1e9, dB(S(1,1)), 'k-',  linewidth=2, label='dB(S11)')
axis.grid()
axis.set_xmargin(0)
axis.set_xlabel('Frequency (GHz)')
axis.set_ylabel('S (dB)')
axis.set_title("Input matching")
axis.legend()

fig, axis = plt.subplots(num="S31", tight_layout=True)
axis.plot(f/1e9, dB(S(2,1)), 'k-',  linewidth=2, label='dB(S21)')
axis.plot(f/1e9, dB(S(3,1)), 'r--', linewidth=2, label='dB(S31)')
axis.grid()
axis.set_xmargin(0)
axis.set_xlabel('Frequency (GHz)')
axis.set_ylabel('S (dB)')
axis.set_title("Transmission")
axis.legend()

# show all plots
plt.show()
