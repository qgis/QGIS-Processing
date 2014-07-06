##Vector=group
##Define multiple vector layers properties=name
##Vector_layers=multiple vector
##QML_file=file
##Coordinate_Reference_System=crs None
##Create_spatial_index=boolean False
##Calculate_extent=boolean False
##Save_layer_style_as_default=boolean False

from qgis.core import *
from qgis.utils import iface
import os

# rename inputs
qml = QML_file
crs = Coordinate_Reference_System
csi = Create_spatial_index
ce = Calculate_extent
ss = Save_layer_style_as_default

# Iterate over the chosen layers
layersUri = Vector_layers.split(';')
for i, uri in enumerate(layersUri):
    progress.setPercentage(int(100 * i / len(layersUri)))
    
    # Get layer from passed uri
    layer = processing.getObjectFromUri(uri)
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
        
    # Save style as default
    if ss:
        layer.saveDefaultStyle()