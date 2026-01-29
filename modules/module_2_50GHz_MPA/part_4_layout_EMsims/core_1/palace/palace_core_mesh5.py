# MODEL FOR GMSH WITH PALACE

import os
import sys
import subprocess

# If gds2palace is NOT installed as a module (pip install), we expect a local copy of 
# gds2palace in the same directory as this model file
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'gds2palace'))) 
from gds2palace import *


# ======================== workflow settings ================================

# preview model/mesh only, without running solver?
start_simulation = False
run_command = ['./run_sim']   

# ===================== input files and path settings =======================

settings = {}

gds_filename = "../layout_gds/50_ghz_mpa_core_no_BJT.gds"      # geometries
XML_filename = "SG13G2_200um.xml"          # stackup

settings['preprocess_gds'] = True  # preprocess GDSII for safe handling of cutouts/holes?
settings['merge_polygon_size'] = 1.2 # merge via polygons with distance less than .. microns, set to 0 to disable via merging.


# get path for this simulation file
script_path = utilities.get_script_path(__file__)
# use script filename as model basename
model_basename = utilities.get_basename(__file__)
# set and create directory for simulation output
sim_path = utilities.create_sim_path (script_path,model_basename)
print('Simulation data directory: ', sim_path)

# change path to models script path
modelDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(modelDir)


# ======================== simulation settings ================================

settings['unit']   = 1e-6  # geometry is in microns
settings['margin'] = 20    # distance in microns from GDSII geometry boundary to stackup boundary
settings['air_around'] = 20    # optional: distance in microns from stackup boundary to simulation boundary (defaults to margin)

settings['fstart']  = 1e9
settings['fstop']   = 350e9
settings['fstep']   = 5e9

settings['refined_cellsize'] = 5  # mesh cell size in conductor region
settings['cells_per_wavelength'] = 10   # how many mesh cells per wavelength, must be 10 or more

settings['meshsize_max'] = 30  # microns, override cells_per_wavelength 
settings['adaptive_mesh_iterations'] = 0

settings['no_preview'] = True # enable to skip gmsh geometry preview before meshing, only show mesh

# Ports from GDSII Data, polygon geometry from specified special layer
# Excitations can be switched off by voltage=0, those S-parameter will be incomplete then

simulation_ports = simulation_setup.all_simulation_ports()
# instead of in-plane port specified with target_layername, we here use via port specified with from_layername and to_layername
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
allpolygons = gds_reader.read_gds(gds_filename, layernumbers, purposelist=[0], metals_list=metals_list, preprocess=settings['preprocess_gds'], merge_polygon_size=settings['merge_polygon_size'])


########### create model ###########

settings['simulation_ports'] = simulation_ports
settings['materials_list'] = materials_list
settings['dielectrics_list'] = dielectrics_list
settings['metals_list'] = metals_list
settings['layernumbers'] = layernumbers
settings['allpolygons'] = allpolygons
settings['sim_path'] = sim_path
settings['model_basename'] = model_basename


# list of ports that are excited (set voltage to zero in port excitation to skip an excitation!)
excite_ports = simulation_ports.all_active_excitations()
config_name, data_dir = simulation_setup.create_palace (excite_ports, settings)

# for convenience, write run script to model directory
utilities.create_run_script(sim_path)


if start_simulation:
    try:
        os.chdir(sim_path)
        subprocess.run(run_command, shell=True)
    except:
        print(f"Unable to run Palace using command ",run_command)