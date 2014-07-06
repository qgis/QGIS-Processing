##Vector=group
##Define 1 vector layer properties=name
##Vector_layer=vector
##QML_file=file
##Coordinate_Reference_System=crs None
##Create_spatial_index=boolean False
##Calculate_extent=boolean False
##Layer_title=string
##Layer_abstract=longstring
##Save_layer_style_as_default=boolean False

from qgis.core import *
from qgis.utils import iface
import os

# rename inputs
qml = QML_file
crs = Coordinate_Reference_System
csi = Create_spatial_index
ce = Calculate_extent
lt = Layer_title
la = Layer_abstract
ss = Save_layer_style_as_default

# Get layer object
layer = processing.getObject(Vector_layer)
provider = layer.dataProvider()
    
# Set style from QML
if os.path.exists(qml):
    layer.loadNamedStyle(qml)
    iface.legendInterface().refreshLayerSymbology(layer)    

# Set CRS
if Coordinate_Reference_System:
    qcrs = QgsCoordinateReferenceSystem()
    qcrs.createFromOgcWmsCrs(crs)
    layer.setCrs(qcrs)
    
# Create spatial index
if csi and provider.capabilities() and QgsVectorDataProvider.CreateSpatialIndex:
    if not provider.createSpatialIndex():
        progress.setText(u'Cannot create spatial index for layer : %s' % layer.name())
    
# Calculate extent
if ce:
    layer.updateExtents()
    
# Set layer metadata 
if lt:
    layer.setTitle(lt)
if la:
    layer.setAbstract(la)

# Save style as default
if ss:
    layer.saveDefaultStyle()