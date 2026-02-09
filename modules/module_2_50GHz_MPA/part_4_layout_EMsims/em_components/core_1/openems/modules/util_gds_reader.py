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

# Extract objects on IHP layers in GDSII file

import gdspy
import numpy as np
import os


# check that we have gdspy version 1.6.x or later
# gdspy 1.4.2 is known for issues with our geometries

version_str = gdspy.__version__
major, minor, patch = version_str.split('.')
if int(major) == 1:
  if int(minor) < 6:
    print('\nWARNING: Your gdspy module version ', version_str, ' is too old, this is known to cause problems.')
    print(' Please update to 1.6.13 or later!')
    print(' Consider using venv if you are not allowed to modify the global Python modules of your system.')
    print(' https://docs.python.org/3/library/venv.html \n')
    

# ============= technology specific stuff ===============


# ======================================

class layer_bounding_box:
  """
    bounding box class is used to store xmin,xmax,ymin,ymax for one layer
  """
  def __init__ (self, xmin, xmax, ymin, ymax):
    self.xmin = xmin
    self.xmax = xmax
    self.ymin = ymin
    self.ymax = ymax

  def update (self, xmin, xmax, ymin, ymax):
    self.xmin = min(xmin, self.xmin)
    self.xmax = max(xmax, self.xmax)
    self.ymin = min(ymin, self.ymin)
    self.ymax = max(ymax, self.ymax)



class all_bounding_box_list:
  """
    stores bounding box instances for multiple layers
    and global bounding box across all layers
  """
  def __init__ (self):
    self.bounding_boxes = {}
    # initialize values for bounding box calculation
    self.xmin=float('inf')
    self.ymin=float('inf')
    self.xmax=float('-inf')
    self.ymax=float('-inf')

  def update (self, layer, xmin, xmax, ymin, ymax):  
    if self.bounding_boxes.get(layer) is not None:
      self.bounding_boxes[layer].update(xmin, xmax, ymin, ymax)
    else:
      self.bounding_boxes[layer] = layer_bounding_box(xmin, xmax, ymin, ymax)
    # also update global values
    self.xmin = min(self.xmin, xmin)   
    self.xmax = max(self.xmax, xmax)   
    self.ymin = min(self.ymin, ymin)   
    self.ymax = max(self.ymax, ymax)   

  def get_layer_bounding_box (self, layer):
    # return bounding box of one specific layer 
    # if layer not found, return global bounding box
    xmin = self.xmin 
    xmax = self.xmax
    ymin = self.ymin
    ymax = self.ymax
    if layer is not None:
      if self.bounding_boxes.get(layer) is not None:
        bbox = self.bounding_boxes[int(layer)]
        xmin = bbox.xmin 
        xmax = bbox.xmax
        ymin = bbox.ymin
        ymax = bbox.ymax
    return xmin, xmax, ymin, ymax  
  
  def merge (self, another_bounding_box_list):
    # combine this bounding box with another bounding box from another GDSII import
    # combine the dictionaries with per-layer data
    self.bounding_boxes.update (another_bounding_box_list.bounding_boxes)
    # combine the overall total boundary
    self.xmin = min(self.xmin, another_bounding_box_list.xmin)
    self.xmax = max(self.xmax, another_bounding_box_list.xmax)
    self.ymin = min(self.ymin, another_bounding_box_list.ymin)
    self.ymax = max(self.ymax, another_bounding_box_list.ymax)


# ============= polygons ===============

class gds_polygon:
  """
    gds polygon object
  """
  
  def __init__ (self, layernum):
    self.pts_x = np.array([])
    self.pts_y = np.array([])
    self.pts   = np.array([])
    self.layernum = layernum
    self.is_port = False
    self.is_via = False
    self.CSXpoly = None
    
  def add_vertex (self, x,y):
    self.pts_x = np.append(self.pts_x, x)
    self.pts_y = np.append(self.pts_y, y)

  def process_pts (self):
    self.pts = [self.pts_x, self.pts_y]
    self.xmin = np.min(self.pts_x)
    self.xmax = np.max(self.pts_x)
    self.ymin = np.min(self.pts_y)
    self.ymax = np.max(self.pts_y)

  def __str__ (self):
    # string representation 
    mystr = 'Layer = ' + str(self.layernum) + ', Polygon = ' + str(self.pts) + ', Via = ' + str(self.is_via)
    return mystr


class all_polygons_list:
  """
    list of gds polygon objects
  """

  def __init__ (self):
    self.polygons = []
    self.bounding_box = all_bounding_box_list() # manages bounding box per layer and global

  def append (self, poly):
    # before we append, combine points in polygon from pts_x and pts_y into pts
    poly.process_pts()
    # add polygon to list
    self.polygons.append (poly)

  def add_rectangle (self, x1,y1,x2,y2, layernum, is_port=False, is_via=False):
    # append simple rectangle to list, this can also be done later, after reading GDSII file
    poly = gds_polygon(layernum)
    poly.add_vertex(x1,y1)
    poly.add_vertex(x1,y2)
    poly.add_vertex(x2,y2)
    poly.add_vertex(x2,y1)
    poly.is_port = is_port
    poly.is_via = is_via
    self.append(poly)

    # need to update min and max here, for gds data that is done after reading file
    self.bounding_box.update (layernum, min(x1,x2), max(x1,x2),min(y1,y2),max(y1,y2))


  def add_polygon (self, xy, layernum, is_port=False, is_via=False):
    # append polygon array to list, this can also be done later, after reading GDSII file
    # polygon data structure must be [[x1,y1],[x2,y2],...[xn,yn]]
    xmin=float('inf')
    ymin=float('inf')
    xmax=float('-inf')
    ymax=float('-inf')

    poly = gds_polygon(layernum)
    numpts = len(xy)
    for pt in range(0, numpts):
      pt = xy[pt]
      x = pt[0]
      y = pt[1]
      poly.add_vertex(x,y)
      # need to update min and max here, for gds data that is done after reading file
      xmin = min(xmin, x)
      xmax = max(xmax, x)
      ymin = min(ymin, y)
      ymax = max(ymax, y)      
    # need to update min and max here, for gds data that is done after reading file
    self.bounding_box.update (layernum, xmin, xmax, ymin, ymax)
    self.append(poly)        


  def set_bounding_box (self, xmin,xmax,ymin,ymax):
    # global bounding box, over all evaluated layers
    self.bounding_box.xmin = xmin
    self.bounding_box.xmax = xmax
    self.bounding_box.ymin = ymin
    self.bounding_box.ymax = ymax

  def get_layer_bounding_box (self, layer):
    # return bounding box for specific layer, returns global if layer not found
    return self.bounding_box.get_layer_bounding_box (layer)

  def get_bounding_box (self):
    # return global bounding box
    return self.bounding_box.xmin, self.bounding_box.xmax, self.bounding_box.ymin, self.bounding_box.ymax 
 
  def get_xmin (self):
    # return global bounding box
    return self.bounding_box.xmin

  def get_xmax (self):
    # return global bounding box
    return self.bounding_box.xmax

  def get_ymin (self):
    # return global bounding box
    return self.bounding_box.ymin

  def get_ymax (self):
    # return global bounding box
    return self.bounding_box.ymax
  
  def merge (self, another_polygons_list):
    # merge with another polygon list from another GDSII import
    for polygon in another_polygons_list.polygons:
      self.polygons.append(polygon)
    # also merge boundary information  
    self.bounding_box.merge(another_polygons_list.bounding_box)          


# ---------------------- via merging option --------------------



def merge_via_array (polygons, maxspacing):
  # Via array merging consists of 3 steps: oversize, merge, undersize
  # Value for oversize depends on via layer
  # Oversized vias touch if each via is oversized by half spacing
  
  offset = maxspacing/2 + 0.01
  
  offsetpolygonset=gdspy.offset(polygons, offset, join='miter', tolerance=2, precision=0.001, join_first=False, max_points=199)
  mergedpolygonset=gdspy.boolean(offsetpolygonset, None,"or", max_points=199)
  mergedpolygonset=gdspy.offset(mergedpolygonset, -offset, join='miter', tolerance=2, precision=0.001, join_first=False, max_points=199)
  
  # offset and boolean return PolygonSet, we only need the list of polygons from that
  return mergedpolygonset.polygons 



# ----------- read GDSII file, return openEMS polygon list object -----------

def read_gds(filename, layerlist, purposelist, metals_list, preprocess=False, merge_polygon_size=0, mirror=False, offset_x=0, offset_y=0, gds_boundary_layers=[], layernumber_offset=0, cellname=""):

  """
  Read GDSII file and return polygon list object
  input value: filename
  """
  if os.path.isfile(filename):
    print('Reading GDSII input file:', filename)
  
    input_library = gdspy.GdsLibrary(infile=filename)

    if preprocess: 
      print('Pre-processing GDSII to handle cutouts and self-intersecting polygons')
      # iterate over cells
      for cell in input_library:
        
        # iterate over polygons
        for poly in cell.polygons:
          
          # points of this polygon
          polypoints = poly.polygons[0]

          poly_layer = poly.layers[0]
          poly_purpose = poly.datatypes[0]

          if ((poly_layer in layerlist) and (poly_purpose in purposelist)):
          
            # get number of vertices
            numvertices = len(polypoints) 
            
            seen   = set()    # already seen vertex values
            dupefound = False

            # iterate over vertices to find duplicates
            for i_vertex in range(numvertices):
              
              # print('polypoints  = ' + str(polypoints))
              x = polypoints[i_vertex][0]
              y = polypoints[i_vertex][1]
              
              # create string representation so that we can check for duplicates
              vertex_string = str(x)+','+str(y)
              if vertex_string in seen:
                dupefound = True
                # print('      found duplicate at vertex ' + str(i_vertex) + ': ' + vertex_string)
              else:
                seen.add(vertex_string)  

            if dupefound:
                          
              # do the slicing
              
              # convert polygon to format required for slicing
              basepoly_points = []

              for i_vertex in range(numvertices):
                basepoly_points.append((polypoints[i_vertex,0], polypoints[i_vertex,1]))

              # create new polygon
              basepoly = gdspy.Polygon(basepoly_points, layer=poly_layer, datatype=poly_purpose)  
              fractured = basepoly.fracture(max_points=6)

              # add fractured polygon to cell
              cell.add(fractured)

              # invalidate original polygon
              poly.layers=[0]
              # remove original polygon
              cell.remove_polygons(lambda pts, layer, datatype:
                layer == 0)
    
    # end preprocessing

    # evaluate only first top level cell
    toplevel_cell_list = input_library.top_level()

    # try to get cell named cellname, otherwise top level cell
    cell = input_library.cells.get(cellname, toplevel_cell_list[0])
    
    all_polygons = all_polygons_list()

    # flatten hierarchy below this cell
    cell.flatten(single_layer=None, single_datatype=None, single_texttype=None)

    # optional mirror and translation of entire cell
    for poly in cell.polygons:
      if mirror:
        # optional mirror
        poly = poly.mirror(p1=[0,0],p2=[0,1])
      if (offset_x != 0) or (offset_y != 0):
        # optional translation after mirror
        poly = poly.translate(offset_x, offset_y)


    # iterate over XML technology metal layers and (optional) dielectric layer boundary spec
    extended_layer_list = layerlist
    extended_layer_list.extend(gds_boundary_layers)

    for layer_to_extract in extended_layer_list:
      
      # print ("Evaluating layer ", str(layer_to_extract))

      # get layers used in cell
      used_layers = cell.get_layers()

      # Note on layer numbers:
      # Used layer is the layer base number, layer_to_extract has the layer number offset from XML
      # For this file, the layernumber_offset applies ALWAYS

      # check if layer-to-extract is used in cell 
      layer_to_extract_gds = layer_to_extract - layernumber_offset
      if (layer_to_extract_gds in used_layers):  # use base layer number here to match GDSII
              
        # iterate over layer-purpose pairs (by_spec=true)
        # do not descend into cell references (depth=0)
        LPPpolylist = cell.get_polygons(by_spec=True, depth=0)
        for LPP in LPPpolylist:
          layer = LPP[0]   
          purpose = LPP[1]
          
          # now get polygons for this one layer-purpose-pair
          if (layer==layer_to_extract_gds) and (purpose in purposelist):
            layerpolygons = LPPpolylist[(layer, purpose)]

            # optional via array merging, only for via layers
            metal = metals_list.getbylayernumber(layer_to_extract) # this is the layer number with offset, to match XML stackup
            if metal != None:
              if (merge_polygon_size>0) and metal.is_via:
                layerpolygons = merge_via_array (layerpolygons, merge_polygon_size)

            # bounding box for this layer
            xmin=float('inf')
            ymin=float('inf')
            xmax=float('-inf')
            ymax=float('-inf')

            # iterate over layer polygons
            for polypoints in layerpolygons:

              numvertices = int(polypoints.size/polypoints.ndim)

              # new polygon, store layer number information
              new_poly = gds_polygon(layer + layernumber_offset)

              # get vertices
              for vertex in range(numvertices):
                x = polypoints[vertex,0]
                y = polypoints[vertex,1]

                new_poly.add_vertex(x,y)
                
                # update bounding box information
                xmin = min(x,xmin)
                xmax = max(x,xmax)
                ymin = min(y,ymin)
                ymax = max(y,ymax)
              
              # polygon is complete, process and add to list
              all_polygons.append(new_poly)

              # done with this layer, store bounding box for this layer    
              all_polygons.bounding_box.update(layer + layernumber_offset, xmin, xmax, ymin, ymax)

    '''
    # Re-evaluate bounding box if we have a bounding box specified in GDS file and evaluation is requested
    if gds_boundary is not None:
      spec = gds_boundary.split(":")
      boundary_layer = int(spec[0])
      if len(spec)>1:
        # user has specified purpose explicitely
        boundary_purpose_list = [int(spec[1])]
      else:  
        # use global purpose list
        boundary_purpose_list = purposelist

      # get layers used in cell
      used_layers = cell.get_layers()

      # check if layer-to-extract is used in cell 
      if (boundary_layer in used_layers):
        # reset previous bounding box and start all over again
        xmin=float('inf')
        ymin=float('inf')
        xmax=float('-inf')
        ymax=float('-inf')
              
        # iterate over layer-purpose pairs (by_spec=true)
        # do not descend into cell references (depth=0)
        LPPpolylist = cell.get_polygons(by_spec=True, depth=0)
        for LPP in LPPpolylist:
          layer = LPP[0]
          purpose = LPP[1]
          
          # now get polygons for this one layer-purpose-pair
          if (layer==boundary_layer) and (purpose in boundary_purpose_list):
            layerpolygons = LPPpolylist[(layer, purpose)]
           
            # iterate over layer polygons
            for polypoints in layerpolygons:
              numvertices = int(polypoints.size/polypoints.ndim)

              # get vertices
              for vertex in range(numvertices):
                x = polypoints[vertex,0]
                y = polypoints[vertex,1]
                
                # update bounding box information
                if x<xmin: xmin=x
                if x>xmax: xmax=x
                if y<ymin: ymin=y
                if y>ymax: ymax=y
    '''


    # all_polygons.set_bounding_box (xmin,xmax,ymin,ymax)
    
    # done!
    return all_polygons
  
  else:
    print('GDSII input file not found: ', filename)
    exit()
 



  
