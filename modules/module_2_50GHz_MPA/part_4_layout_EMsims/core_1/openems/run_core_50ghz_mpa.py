import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

import modules.util_stackup_reader as stackup_reader
import util_gds_reader as gds_reader
import util_utilities as utilities
import util_simulation_setup as simulation_setup
import util_meshlines

import os
from pylab import *
from CSXCAD import ContinuousStructure
from CSXCAD import AppCSXCAD_BIN
from openEMS import openEMS
from openEMS.physical_constants import *

# Model comments


# ======================== workflow settings ================================

# preview model/mesh only?
# postprocess existing data without re-running simulation?
preview_only = True   
postprocess_only = False

# ===================== input files and path settings =======================

# GDS filename
gds_filename = "../layout_gds/50_ghz_mpa_core_no_BJT.gds"      # geometries
XML_filename = "SG13G2.xml"       # stackup

# preprocess GDSII for safe handling of cutouts/holes?
preprocess_gds = False

# merge polygons with distance less than xxx um, or set to 0 to disable via array merging
merge_polygon_size = 0.5

# get path for this simulation file
script_path = utilities.get_script_path(__file__)

# use script filename as model basename
model_basename = utilities.get_basename(__file__)

# set and create directory for simulation output
sim_path = utilities.create_sim_path (script_path,model_basename)
print('Simulation data directory: ', sim_path)


# ======================== simulation settings ================================

unit   = 1e-6   # geometry is in microns
margin = 100    # distance in microns from GDSII geometry boundary to simulation boundary 

fstart = 0
fstop  = 350e9
numfreq = 401

refined_cellsize = 0.3  # mesh cell size in conductor region

# choices for boundary xmin,xmax,ymin,ymax,zmin,zmax: 
# 'PEC' : perfect electric conductor (default)
# 'PMC' : perfect magnetic conductor, useful for symmetries
# 'MUR' : simple MUR absorbing boundary conditions
# 'PML_8' : PML absorbing boundary conditions
Boundaries = ['PML_4', 'PML_4', 'PML_4', 'PML_4', 'PEC', 'PML_4']

cells_per_wavelength = 20   # how many mesh cells per wavelength, must be 10 or more
energy_limit = -50          # end criteria for residual energy (dB)

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
allpolygons = gds_reader.read_gds(gds_filename, layernumbers, purposelist=[0], metals_list=metals_list, preprocess=preprocess_gds, merge_polygon_size=merge_polygon_size)


# calculate maximum cellsize from wavelength in dielectric
wavelength_air = 3e8/fstop
max_cellsize = (wavelength_air/unit)/(sqrt(materials_list.eps_max)*cells_per_wavelength) 


########### create model, run and post-process ###########


# Create simulation for port 1 .. 4 excitation, return value is data path for that excitation

FDTD = openEMS(EndCriteria=exp(energy_limit/10 * log(10)))
FDTD.SetGaussExcite( (fstart+fstop)/2, (fstop-fstart)/2 )
FDTD.SetBoundaryCond( Boundaries )

excite_ports_list = [[1],[2],[3],[4]]  # list of ports that are excited in the different excitation runs
for excite_ports in excite_ports_list:
    # define excitation and stop criteria and boundaries
    FDTD = simulation_setup.setupSimulation (excite_ports, simulation_ports, FDTD, materials_list, dielectrics_list, metals_list, allpolygons, max_cellsize, refined_cellsize, margin, unit, xy_mesh_function=util_meshlines.create_xy_mesh_from_polygons)
    simulation_setup.runSimulation (excite_ports, FDTD, sim_path, model_basename, preview_only, postprocess_only)


if preview_only==False:

    print('Begin data evaluation')

    # define dB function for S-parameters
    def dB(value):
        return 20.0*np.log10(np.abs(value))        

    # define phase function for S-parameters
    def phase(value):
        return angle(value, deg=True) 

    f = np.linspace(fstart,fstop,numfreq)

    # get results, CSX port definition is read from simulation ports object
    # all S-parameter data is available because we have simulated all port excitations
    s11 = utilities.calculate_Sij (1, 1, f, sim_path, simulation_ports)
    s21 = utilities.calculate_Sij (2, 1, f, sim_path, simulation_ports)
    s31 = utilities.calculate_Sij (3, 1, f, sim_path, simulation_ports)
    s41 = utilities.calculate_Sij (4, 1, f, sim_path, simulation_ports)
    s12 = utilities.calculate_Sij (1, 2, f, sim_path, simulation_ports)
    s22 = utilities.calculate_Sij (2, 2, f, sim_path, simulation_ports)
    s32 = utilities.calculate_Sij (3, 2, f, sim_path, simulation_ports)
    s42 = utilities.calculate_Sij (4, 2, f, sim_path, simulation_ports)
    s13 = utilities.calculate_Sij (1, 3, f, sim_path, simulation_ports)
    s23 = utilities.calculate_Sij (2, 3, f, sim_path, simulation_ports)
    s33 = utilities.calculate_Sij (3, 3, f, sim_path, simulation_ports)
    s43 = utilities.calculate_Sij (4, 3, f, sim_path, simulation_ports)
    s14 = utilities.calculate_Sij (1, 4, f, sim_path, simulation_ports)
    s24 = utilities.calculate_Sij (2, 4, f, sim_path, simulation_ports)
    s34 = utilities.calculate_Sij (3, 4, f, sim_path, simulation_ports)
    s44 = utilities.calculate_Sij (4, 4, f, sim_path, simulation_ports)

    s4p_name = os.path.join(sim_path, model_basename + '.s4p')
    utilities.write_snp (np.array([[s11,s21,s31,s41], [s12,s22,s32,s42], [s13,s23,s33,s43], [s14,s24,s34,s44]]),f, s4p_name)

    print('\nStarting plots')

    figure()
    plot(f/1e9, dB(s21), 'k-',  linewidth=2, label='S11 [dB]')
    grid()
    legend()
    xlabel('Frequency (GHz)')

    figure()
    plot(f/1e9, phase(s21), 'k-',  linewidth=2, label='S11 phase [degree]')
    grid()
    legend()
    xlabel('Frequency (GHz)')


    # Show all plots
    show()



