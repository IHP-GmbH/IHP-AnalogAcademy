########################################################################
#
# Copyright 2025 Volker Muehlhaus and IHP PDK Authors
#
# Licensed under the GNU General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.gnu.org/licenses/gpl-3.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################


import os

from . import util_utilities as utilities
from . import util_meshlines

from CSXCAD import ContinuousStructure
from CSXCAD import AppCSXCAD_BIN
from openEMS import openEMS
from openEMS.physical_constants import *

import numpy as np


class simulation_port:
  """
    port object
    for in-plane port, parameter target_layername is specified
    for via port, parameters from_layername and to_layername are specified for the metals above and below   
  """
  
  def __init__ (self, portnumber, voltage, port_Z0, source_layernum, target_layername=None, from_layername=None, to_layername=None, direction='x'):
    self.portnumber = portnumber
    self.source_layernum = source_layernum        # source for port geometry is a GDSII layer, just one port per layer
    self.target_layername = target_layername      # target layer where we create the port, if specified we create in-plane port
    self.from_layername  = from_layername         # layer on one end of via port, used if target_layername is None
    self.to_layername    = to_layername           # layer on other  end of via port
    self.reversed_direction = ('-' in direction)  # detect reversed port direction
    self.direction  = direction.replace('-', '')  # remove sign that before sending to openEMS
    self.direction  = self.direction.replace('+', '')  # just in case users might specify positive sign in direction string
    
    self.port_Z0 = port_Z0
    self.voltage = voltage
    self.CSXport = None

  def set_CSXport (self, CSXport):
    self.CSXport = CSXport  

  def __str__ (self):
    # string representation 
    mystr = 'Port ' + str(self.portnumber) + ' voltage = ' + str(self.voltage) + ' GDS source layer = ' + str(self.source_layernum) + ' target layer = ' + str(self.target_layername) + ' direction = ' + str(self.direction)
    return mystr
  

class all_simulation_ports:
  """
  all simulation ports object
  """
  
  def __init__ (self):
      self.ports = []
      self.portcount = 0
      self.portlayers = []

  def add_port (self, port):
      self.ports.append(port)
      self.portcount = len(self.ports)
      self.portlayers.append(port.source_layernum)

  def get_port_by_layernumber (self, layernum):  # special GDSII layer for ports only, one port per layer, so we have 1:1 mapping
      found = None
      for port in self.ports:
          if port.source_layernum == layernum:
              found = port
              break
      return found       
  
  def get_port_by_number (self, portnum):
      return self.ports[portnum-1] 
  
  def apply_layernumber_offset (self, offset):
      newportlayers = []    
      for port in self.ports:
          port.source_layernum = port.source_layernum + offset
          newportlayers.append(port.source_layernum)
      self.portlayers = newportlayers        
          

  def all_active_excitations (self):
    """Get all active port excitations, i.e. ports with voltage other than zero
    Returns:
        list of simulation_port: active port instances
    """

    numbers = []
    for port in self.ports:
        if abs(port.voltage) > 1E-6:
            # skip zero voltage ports for excitation
            # append as list, we need that for create_palace() function
            numbers.append([port.portnumber])
    return numbers
  
       
  '''
    openEMS dump types:

    * 0  : for E-field time-domain dump (default)
    * 1  : for H-field time-domain dump
    * 2  : for electric current time-domain dump
    * 3  : for total current density (rot(H)) time-domain dump

    * 10 : for E-field frequency-domain dump
    * 11 : for H-field frequency-domain dump
    * 12 : for electric current frequency-domain dump
    * 13 : for total current density (rot(H)) frequency-domain dump

    * 20 : local SAR frequency-domain dump
    * 21 :  1g averaging SAR frequency-domain dump
    * 22 : 10g averaging SAR frequency-domain dump

    * 29 : raw data needed for SAR calculations (electric field FD, cell volume, conductivity and density)

    openEMS dump modes:

    * 0 : no-interpolation
    * 1 : node-interpolation (default, see warning below)
    * 2 : cell-interpolation (see warning below)

    openEMS file types:

    * 0 : vtk-file  (default)
    * 1 : hdf5-file (easier to read by python, using h5py)
'''



class dump():
  def __init__ (self, name, file_type, dump_type, source_layernum, from_layername, to_layername, offset_top, offset_bottom, sub_sampling):
      self.name = name

      # allow string names for filetype also
      if file_type == 'vtk': 
          file_type=0
      elif file_type == 'hdf5': 
          file_type=1

      if file_type not in [0,1]:
        print('Invalid dump filetype specified for ', name)
        exit(1)

      self.file_type = file_type
      self.source_layernum = source_layernum
      self.from_layername=from_layername
      self.to_layername=to_layername
      self.offset_top = offset_top
      self.offset_bottom = offset_bottom
      self.subsampling = sub_sampling


class time_dump(dump):
  def __init__ (self, name, file_type, dump_type, source_layernum, from_layername, to_layername, offset_top, offset_bottom, sub_sampling):
      super().__init__(name, file_type, dump_type, source_layernum, from_layername, to_layername, offset_top, offset_bottom, sub_sampling)

      # allow string names for dumptype also
      if dump_type == 'E' or dump_type == 'Et': 
          dump_type=0
      elif dump_type == 'H' or dump_type == 'Ht': 
          dump_type=1
      elif dump_type == 'J' or dump_type == 'Jt': 
          dump_type=2
      elif dump_type == 'rotH' or dump_type == 'rotHt': 
          dump_type=3

      self.dump_type = dump_type

      if dump_type not in [0,1,2,3]:
        print('Invalid dumptype specified for time domain dump ', name)
        exit(1)


class frequency_dump(dump):
  def __init__ (self, name, frequency, file_type, dump_type, source_layernum, from_layername='', to_layername='', offset_top=0, offset_bottom=0, sub_sampling=[1,1,1]):
      super().__init__(name, file_type, dump_type, source_layernum, from_layername, to_layername, offset_top, offset_bottom, sub_sampling)
      self.frequency = frequency

      # allow string names for dumptype also
      if dump_type == 'E' or dump_type == 'Ef': 
          dump_type=10
      elif dump_type == 'H' or dump_type == 'Hf': 
          dump_type=11
      elif dump_type == 'J' or dump_type == 'Jf': 
          dump_type=12
      elif dump_type == 'rotH' or dump_type == 'rotHf': 
          dump_type=13

      self.dump_type = dump_type

      if dump_type not in [10,11,12,13]:
        print('Invalid dumptype specified for frequency domain dump ', name)
        exit(1)




class all_field_dumps():
  def __init__ (self):
      self.field_dumps = []
      self.dumplayers  = []
      self.count = 0

  def add_dump (self, dump):
      self.field_dumps.append(dump)
      self.count = len(self.field_dumps)
      self.dumplayers.append(dump.source_layernum)

  def add_frequency_dump (self, name, frequency, file_type, dump_type, source_layernum, from_layername='', to_layername='', offset_top=0, offset_bottom=0, sub_sampling=[1,1,1]):
      self.field_dumps.append(frequency_dump(name=name, frequency=frequency, file_type=file_type, dump_type=dump_type, source_layernum=source_layernum, from_layername=from_layername, to_layername=to_layername, offset_top=offset_top, offset_bottom=offset_bottom, sub_sampling=sub_sampling))
      self.count = len(self.field_dumps)      
      self.dumplayers.append(source_layernum)

  def add_time_dump (self, name, file_type, dump_type, source_layernum, from_layername='', to_layername='', offset_top=0, offset_bottom=0, sub_sampling=[1,1,1]):
      self.field_dumps.append(time_dump(name=name, file_type=file_type, dump_type=dump_type, source_layernum=source_layernum, from_layername=from_layername, to_layername=to_layername, offset_top=offset_top, offset_bottom=offset_bottom, sub_sampling=sub_sampling))
      self.count = len(self.field_dumps)      
      self.dumplayers.append(source_layernum)



def addGeometry_to_CSX (CSX, excite_portnumbers,simulation_ports,FDTD, materials_list, dielectrics_list, metals_list, allpolygons):
# Add polygons   

    # hold CSX material definitions, but only for stackup materials that are actually used
    CSX_materials_list = {}

    # add geometries on metal and via layers
    for poly in allpolygons.polygons:
        # each poly knows its layer number
        # get material name for poly, by using metal information from stackup
        # special case MIM: we can have two different materials (metal and dielectric) coming from same source layer

        all_assigned = metals_list.getallbylayernumber (poly.layernum)
        if all_assigned != None:
            for metal in all_assigned:
                materialname = metal.material
                
                # check for stackup defintions that are not compatible with this workflow
                if not metal.is_sheet:
                    # check for openEMS CSX material object that belongs to this material name
                    if materialname in CSX_materials_list.keys():
                        # already in list, was used before
                        CSX_material = CSX_materials_list[materialname]
                    else:
                        # create CSX material, was not used before
                        material = materials_list.get_by_name(materialname)
                        CSX_material = CSX.AddMaterial(material.name, kappa=material.sigma, epsilon=material.eps)
                        CSX_materials_list.update({material.name: CSX_material})
                        # set color for IHP layers, if available, so that we see that color in AppCSXCAD 3D view
                        if material.color != "":
                            CSX_material.SetColor('#' + material.color, 255)  # transparency value 255 = solid

                    # add Polygon to CSX 
                    # remember value for MA meshing algorithm, which works on CSX polygons rather than our GDS polygons
                    p = CSX_material.AddLinPoly(priority=200, points=poly.pts, norm_dir ='z', elevation=metal.zmin, length=metal.thickness)
                    poly.CSXpoly = p

                else:
                    print('Sheet material assigned to layer', metal.name)
                    # create a unique material defintion for this layer

                    # get thickness of layer definition
                    thickness = metal.zmax - metal.zmin # should always be zero for sheet

                    # get material type
                    material = materials_list.get_by_name(materialname)

                    if material.type == 'RESISTOR' and material.Rs>0 :
                        # define conducting sheet with sigma calculated from material Rs value and thickness from layer 
                        if thickness==0:
                            # thickness not specified in stackup
                            thickness=1e-6 # assume 1 micron for loss calculation, we then calculate Sigma to obtain desired Rs
                        sigma = 1/(thickness*material.Rs)  
                        CSX_material = CSX.AddConductingSheet(metal.name + '_' + material.name, conductivity=sigma, thickness=thickness)
                        CSX_materials_list.update({material.name: CSX_material})
                    else:
                        print('WARNING: Invalid material assigned to layer ', metal.name)
                        print(str(material))    
                        print('=====> MATERIAL IS REPLACED BY PEC (PERFECT CONDUCTOR) <=====')
                        CSX_material = CSX.AddMaterial('PEC_' + material.name)
                        CSX_materials_list.update({material.name: CSX_material})

                    # add Polygon to CSX but no thickness
                    # remember value for MA meshing algorithm, which works on CSX polygons rather than our GDS polygons
                    p = CSX_material.AddLinPoly(priority=200, points=poly.pts, norm_dir ='z', elevation=metal.zmin, length=0)
                    poly.CSXpoly = p

                
    return CSX, CSX_materials_list                    


def addDielectrics_to_CSX (CSX, CSX_materials_list,  materials_list, dielectrics_list, allpolygons, margin, addPEC):
# Add dielectric layers (these extend through simulation area and have no polygons in GDSII)

    for dielectric in dielectrics_list.dielectrics:
        # get CSX material object for this dielectric layers material name
        materialname = dielectric.name
        material = materials_list.get_by_name(dielectric.material)
        if material is None:
            print('ERROR: Material ', materialname, 'for dielectric layer ', dielectric.name, ' is not defined in stackup file. ')
            exit(1)
        
        if materialname in CSX_materials_list.keys():
            # create new material per layer, so that we can enable/disable them in appCSXCAD when used more than once
            materialname = materialname + '_1'
            
        # create CSX material
        CSX_material = CSX.AddMaterial(materialname, kappa=material.sigma, epsilon=material.eps)
        CSX_materials_list.update({materialname: CSX_material})
        # set color for IHP layers, if available
        if material.color != "":
            CSX_material.SetColor('#' + material.color, 20)  # transparency value 20, very transparent

        # now that we have a CSX material, add the dielectric body (substrate, oxide etc)
            bbox_xmin, bbox_xmax, bbox_ymin, bbox_ymax = allpolygons.bounding_box.get_layer_bounding_box(dielectric.gdsboundary)
            CSX_material.AddBox(priority=10, start=[bbox_xmin - margin, bbox_ymin - margin, dielectric.zmin], stop=[bbox_xmax + margin, bbox_ymax + margin, dielectric.zmax])

    # Optional: add a layer of PEC with zero thickness below stackup
    # This is useful if we have air layer around for absorbing boundaries (antenna simulation)
    if addPEC:
        PEC = CSX.AddMetal( 'PEC_bottom' )
        PEC.SetColor("#ffffff", 50) 
        PEC.AddBox(priority=255, start=[bbox_xmin - margin, bbox_ymin - margin, 0], stop=[bbox_xmax + margin, bbox_ymax + margin, 0])

    return CSX, CSX_materials_list  


def addPorts_to_CSX (CSX, excite_portnumbers,simulation_ports,FDTD, materials_list, dielectrics_list, metals_list, allpolygons):
# Add polygons   

    # hold CSX material definitions, but only for stackup materials that are actually used
    CSX_materials_list = {}

    # add geometries on metal and via layers
    for poly in allpolygons.polygons:
        # each poly knows its layer number
        # get material name for poly, by using metal information from stackup
        metal = metals_list.getbylayernumber (poly.layernum)
        if metal == None: # this layer does not exist in XML stackup
            # found a layer that is not defined in stackup from XML, check if used for ports

            # find port definition for this GDSII source layer number
            port = simulation_ports.get_port_by_layernumber(poly.layernum)
            if port is not None:
                # mark polygon for special handling in meshing
                poly.is_port = True 

                portnum = port.portnumber
                port_direction = port.direction
                port_Z0 = port.port_Z0
                if portnum in excite_portnumbers: # list of excited ports, this can be more than one port number for GSG with composite ports
                    voltage = port.voltage        # only apply source voltage to ports that are excited in this simulation run
                else:
                    voltage = 0                   # passive port in this simulation run
                if port.reversed_direction:       # port direction changes polarity
                    xmin = poly.xmax
                    xmax = poly.xmin
                    ymin = poly.ymax
                    ymax = poly.ymin
                else:        
                    xmin = poly.xmin
                    xmax = poly.xmax
                    ymin = poly.ymin
                    ymax = poly.ymax
                
                # port z coordinates are different between in-plane ports and via ports
                if port.target_layername != None:
                    # in-plane port   
                    port_metal = metals_list.getbylayername(port.target_layername)
                    zmin = port_metal.zmin
                    zmax = port_metal.zmax
                else:
                    # via port 
                    if port.from_layername == 'GND': # special case bottom of simulation box
                        zmin_from = 0
                        zmax_from = 0
                    else:
                        from_metal = metals_list.getbylayername(port.from_layername)
                        if from_metal==None:
                            print('[ERROR] Invalid layer ' , port.from_layername, ' in port definition, not found in XML stackup file!')
                            sys.exit(1)                             
                        zmin_from  = from_metal.zmin
                        zmax_from  = from_metal.zmax
                    
                    if port.to_layername == 'GND': # special case bottom of simulation box
                        zmin_to = 0
                        zmax_to = 0
                    else:
                        to_metal   = metals_list.getbylayername(port.to_layername)
                        if to_metal==None:
                            print('[ERROR] Invalid layer ' , port.to_layername, ' in port definition, not found in XML stackup file!')
                            sys.exit(1)                             
                        zmin_to    = to_metal.zmin
                        zmax_to    = to_metal.zmax
                    
                    # if necessary, swap from and to position
                    if zmin_from < zmin_to:
                        # from layer is lower layer
                        zmin = zmax_from
                        zmax = zmin_to
                    else:    
                        # to layer is lower layer
                        zmin = zmax_to
                        zmax = zmin_from

                CSX_port = FDTD.AddLumpedPort(portnum, port_Z0, [xmin, ymin, zmin], [xmax, ymax, zmax], port_direction, voltage, priority=150)
                # store CSX_port in the port object, for evaluation later
                port.set_CSXport(CSX_port)
                    


    return CSX



def addMesh_to_CSX (CSX, allpolygons, dielectrics_list, metals_list, refined_cellsize, max_cellsize, margin, air_around, unit, z_mesh_function, xy_mesh_function):
# Add mesh using default method
    mesh = CSX.GetGrid()
    mesh.SetDeltaUnit(unit)

    # meshing of dielectrics and metals
    no_z_mesh_list = [] # exclude from meshing, specify stackup layer name here
    mesh = z_mesh_function (mesh, dielectrics_list, metals_list, refined_cellsize, max_cellsize, air_around, no_z_mesh_list)
    mesh = xy_mesh_function (mesh, allpolygons, margin, air_around, refined_cellsize, max_cellsize)

    return mesh


def addFielddumps_to_CSX (FDTD, CSX, all_field_dumps, allpolygons, metals_list):
# Add field dumps for time and frequency domain and nf2ff, if any
    if all_field_dumps.count > 0:
        for field_dump in all_field_dumps.field_dumps:
            if isinstance(field_dump, time_dump):
                Dump = CSX.AddDump(field_dump.name, 
                                     file_type=field_dump.file_type, 
                                     dump_type=field_dump.dump_type, 
                                     sub_sampling=field_dump.subsampling)

            elif isinstance(field_dump, frequency_dump):
                Dump = CSX.AddDump(field_dump.name, 
                                     file_type=field_dump.file_type, 
                                     dump_type=field_dump.dump_type, 
                                     frequency=field_dump.frequency, 
                                     sub_sampling=field_dump.subsampling)

            # add dump box
            xmin, xmax, ymin, ymax  = allpolygons.get_layer_bounding_box(field_dump.source_layernum)
            zmin = metals_list.getbylayername(field_dump.from_layername).zmin + field_dump.offset_bottom
            zmax = metals_list.getbylayername(field_dump.to_layername).zmax + field_dump.offset_top
            Dump.AddBox([xmin,ymin,zmin], [xmax,ymax,zmax])
    

def setupSimulation (excite_portnumbers=None,
                     simulation_ports=None, 
                     FDTD=None, 
                     materials_list=None, 
                     dielectrics_list=None, 
                     metals_list=None, 
                     allpolygons=None, 
                     max_cellsize=None, 
                     refined_cellsize=None, 
                     margin=None, 
                     unit=None, 
                     z_mesh_function=util_meshlines.create_z_mesh, 
                     xy_mesh_function=util_meshlines.create_standard_xy_mesh, 
                     air_around=0, 
                     field_dumps=False,
                     settings=None):

    # This is the unction for model creation because we need to create and run separate CSX
    # for each excitation. For S11,S21 we only need to excite port 1, but for S22,S12
    # we need to excite port 2. This requires separate CSX with different port settings.

    # This function can be called in two ways: 
    # 1) by all those positional parameters or 
    # 2) by passing just FDTD and settings dictionary, where everything is inside the settings dict

    if dielectrics_list is None:
        if settings is not None:
            print('Getting simulation settings from "settings" dictionary')
            # This is option 2, everything is inside the settings dict and we need to get it from there
            excite_portnumbers = settings['excite_portnumbers']
            simulation_ports   = settings['simulation_ports']
            materials_list     = settings['materials_list']
            dielectrics_list   = settings['dielectrics_list']
            metals_list        = settings['metals_list']
            allpolygons        = settings['allpolygons']
            refined_cellsize   = settings['refined_cellsize']
            margin             = settings['margin']
            unit               = settings['unit']
            z_mesh_function    = settings.get('z_mesh_function',util_meshlines.create_z_mesh) 
            xy_mesh_function   = settings.get('xy_mesh_function', util_meshlines.create_xy_mesh_from_polygons)
            air_around         = settings.get('air_around', 0)
            field_dumps        = settings.get('field_dumps', False)

            # calculate maximum cellsize from wavelength in dielectric
            fstop = settings.get('fstop',None)
            unit  = settings.get('unit',None)
            cpw   = settings.get('cells_per_wavelength',None)
            if (fstop is not None) and (unit is not None) and (cpw is not None):
                wavelength_air = 3e8/fstop / unit
                max_cellsize = (wavelength_air)/(np.sqrt(materials_list.eps_max)*cpw) 
            else:
                max_cellsize       = settings.get('max_cellsize',None)
                if max_cellsize is None:
                    print('If fstop, units and cells_per_wavelength are not included in settings, you must specify max_cellsize value')
                    exit(1)                    

        else:
            print('If positional parameters are not defined in setupSimulation, you must provide valid "settings" dictionary instead')                
            exit(1)

        if FDTD is None:
            print('FDTD must be passed to setupSimulation as named parameter, i.e. "FDTD=FDTD" in parameters')                
            exit(1)



    CSX = ContinuousStructure()
    FDTD.SetCSX(CSX)

    # add geometries and return list of used materials
    CSX, CSX_materials_list = addGeometry_to_CSX (CSX, excite_portnumbers,simulation_ports,FDTD, materials_list, dielectrics_list, metals_list, allpolygons)
    CSX, CSX_materials_list = addDielectrics_to_CSX (CSX, CSX_materials_list,  materials_list, dielectrics_list, allpolygons, margin, addPEC=False)

    # add ports
    CSX  = addPorts_to_CSX (CSX, excite_portnumbers,simulation_ports,FDTD, materials_list, dielectrics_list, metals_list, allpolygons)

    # check which layers are actually used, this information is required for meshing in z direction
    # mark if polygon is a via
    if metals_list != None: 
      for poly in allpolygons.polygons:
        layernum = poly.layernum
        metal = metals_list.getbylayernumber(layernum)

        if metal is not None:
            metal.is_used = True
            # set polygon via property, used later for meshing
            poly.is_via = metal.is_via

    # add mesh
    mesh = addMesh_to_CSX (CSX, allpolygons, dielectrics_list, metals_list, refined_cellsize, max_cellsize, margin, air_around, unit, z_mesh_function, xy_mesh_function )

    if field_dumps != False:
        addFielddumps_to_CSX (FDTD, CSX, field_dumps, allpolygons, metals_list)

    # display mesh information (line count and smallest mesh cells)
    meshinfo = util_meshlines.get_mesh_information(mesh)
    print(meshinfo)

    return FDTD


def runSimulation (excite_portnumbers=None, 
                   FDTD=None, 
                   sim_path=None, 
                   model_basename=None, 
                   preview_only=None, 
                   postprocess_only=None, 
                   force_simulation=False,
                   no_gui = False,
                   settings=None):
    
    # This function runs the actual simulation in openEMS

    # This function can be called in two ways: 
    # 1) by all those positional parameters or 
    # 2) by passing just FDTD and settings dictionary, where everything is inside the settings dict

    if excite_portnumbers is None:
        if settings is not None:
            print('Getting simulation settings from "settings" dictionary')
            # This is option 2, everything is inside the settings dict and we need to get it from there
            excite_portnumbers = settings['excite_portnumbers']
            sim_path           = settings['sim_path']
            model_basename     = settings['model_basename']
            preview_only       = settings.get('preview_only',False)
            postprocess_only   = settings.get('postprocess_only','')
            force_simulation   = settings.get('force_simulation', False)
            no_gui             = settings.get('no_gui', False)
        else:
            print('If positional parameters are not defined in setupSimulation, you must provide valid "settings" dictionary instead')                
            exit(1)

        if FDTD is None:
            print('FDTD must be passed to setupSimulation as named parameter, i.e. "FDTD=FDTD" in parameters')                
            exit(1)

    # If no_gui is enabled, always start simulation even if preview_only is True
    # and force re-simulation, even if results already exist
    if no_gui:
        preview_only = False
        postprocess_only = False


    excitation_path = utilities.get_excitation_path (sim_path, excite_portnumbers)
    
    if not postprocess_only:
        # write CSX file 
        CSX_file = os.path.join(excitation_path, model_basename + '.xml')
        CSX = FDTD.GetCSX()
        CSX.Write2XML(CSX_file)

        # preview model
        if 1 in excite_portnumbers and not no_gui:  # only for first port excitation
            print('Starting AppCSXCAD 3D viewer with file: \n', CSX_file)
            print('Close AppCSXCAD to continue or press <Ctrl>-C to abort')

            # for Linux, send warningas and errors to nowhere, so that we don't trash console with vtk warnings
            if os.name == 'posix':
                suffix = ' 2>/dev/null'
            else:
                suffix = ''    

            ret = os.system(AppCSXCAD_BIN + ' "{}"'.format(CSX_file) + suffix)
            if ret != 0:
                print('[ERROR] AppCSXCAD failed to launch. Exit code: ', ret)
                sys.exit(1)

    if not (preview_only or postprocess_only):  # start simulation 
        # Check if we can read a hash file from the result folder
        existing_data_hash = get_hash_from_data_folder(excitation_path)

        # Create hash of newly created CSX file, we will store that to result folder when simulation is finished.
        # This will enable checking for pre-existing data of the exact same model.
        XML_hash = calculate_sha256_of_file(CSX_file)

        if (existing_data_hash != XML_hash) or force_simulation:
            # Hash is different or not found, or simulation is forced
            print('Starting FDTD simulation for excitation ', str(excite_portnumbers))
            try:

                FDTD.Run(excitation_path)  # DO NOT SPECIFY COMMAND LINE OPTIONS HERE! That will fail for repeated runs with multiple excitations.
                print('FDTD simulation completed successfully for excitation ', str(excite_portnumbers))
                # Now that simulation created output data, write the hash of the underlying XML model. This will help to identify existing data for this model.
                write_hash_to_data_folder(excitation_path, XML_hash)
            except AssertionError as e:
                print('[ERROR] AssertionError during FDTD simulation: ', e)
                sys.exit(1)
        else:
            print('Data for this model already exists, skipping simulation!')
            print('To force re-simulation, add parameter "force_simulation=True" to the runSimulation() call.')

    return excitation_path 


def runOpenEMS (excite_ports, settings):
    # This is the all-in-one simulation function that creates openEMS model and runs all ports, on eafter another

    # get settings from simulation model
    preview_only = settings.get('preview_only', False)
    postprocess_only = settings.get('postprocess_only', False)


    if not postprocess_only:
        unit    = settings.get('unit', 1e-6) # unit defaults to micron
        margin  = settings['margin']   # oversize of dielectric layers relative to drawing

        fstart  = settings['fstart']
        fstop   = settings['fstop']
        numfreq = settings.get('numfreq', 401)

        
        energy_limit = settings['energy_limit']
        refined_cellsize = settings['refined_cellsize']
        cells_per_wavelength = settings['cells_per_wavelength']
        Boundaries = settings['Boundaries']

        simulation_ports = settings['simulation_ports'] 
        materials_list = settings['materials_list']
        dielectrics_list = settings['dielectrics_list'] 
        metals_list = settings['metals_list'] 
        allpolygons = settings['allpolygons'] 

        sim_path = settings['sim_path'] 
        model_basename = settings['model_basename'] 

        # calculate wavelength and max_cellsize in project units
        wavelength_air = 3e8/fstop / unit
        max_cellsize = (wavelength_air)/(np.sqrt(materials_list.eps_max)*cells_per_wavelength) 

        # define excitation and stop criteria and boundaries
        FDTD = openEMS(EndCriteria=np.exp(energy_limit/10 * np.log(10)))
        FDTD.SetGaussExcite( (fstart+fstop)/2, (fstop-fstart)/2 )
        FDTD.SetBoundaryCond( Boundaries )

        for port in simulation_ports.ports:
            setupSimulation   ([port.portnumber], 
                                simulation_ports, 
                                FDTD, 
                                materials_list, 
                                dielectrics_list, 
                                metals_list, 
                                allpolygons, 
                                max_cellsize, 
                                refined_cellsize, 
                                margin, 
                                unit, 
                                xy_mesh_function=util_meshlines.create_xy_mesh_from_polygons)
            
            runSimulation  ([port.portnumber], 
                                FDTD, 
                                sim_path, 
                                model_basename, 
                                preview_only, 
                                False)        
    

        # Initialize an empty matrix for S-parameters
        num_ports = simulation_ports.portcount
        s_params = np.empty((num_ports, num_ports, numfreq), dtype=object)

        # Define frequency resolution. Due to FFT from Empire time domain results, 
        # this is postprocessing and we can change it again at any time.
        f = np.linspace(fstart, fstop, numfreq)

        # Populate the S-parameter matrix with simulation results
        for i in range(1, num_ports + 1):
            for j in range(1, num_ports + 1):
                s_params[i-1, j-1] = utilities.calculate_Sij(i, j, f, sim_path, simulation_ports)

        # Write to Touchstone *.snp file
        snp_name = os.path.join(sim_path, model_basename + '.s' + str(num_ports) + 'p')
        utilities.write_snp(s_params, f, snp_name)

        print('Created S-parameter output file at ', snp_name)




# Utility functions for hash file.
# By creating and storing a hash of CSX file to the result folder when simulation is finished,
# we can identify pre-existing data of the exact same model. In this case, we can skip simulation.

def calculate_sha256_of_file(filename):
    import hashlib
    sha256_hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()

def write_hash_to_data_folder (excitation_path, hash_value):
    filename = os.path.join(excitation_path, 'simulation_model.hash')
    hashfile = open(filename, 'w')
    hashfile.write(str(hash_value))
    hashfile.close() 

def get_hash_from_data_folder (excitation_path):
    filename = os.path.join(excitation_path, 'simulation_model.hash')
    hashvalue = ''
    if os.path.isfile(filename):
        hashfile = open(filename, "r")
        hashvalue = hashfile.read()
        hashfile.close()
    return hashvalue

