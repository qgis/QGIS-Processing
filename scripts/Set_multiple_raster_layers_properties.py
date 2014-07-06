##Raster=group
##Set multiple raster layers properties=name
##Raster_layers=multiple raster
##QML_file=file
##Coordinate_Reference_System=crs None
##Refresh_contrast_enhancement=boolean True
##Save_layer_style_as_default=boolean False

from qgis.core import *
from qgis.utils import iface
import os

# rename inputs
crs = Coordinate_Reference_System
qml = QML_file
rce = Refresh_contrast_enhancement
ss = Save_layer_style_as_default

# Iterate over the chosen layers
layersUri = Raster_layers.split(';')
for i, uri in enumerate(layersUri):
    progress.setPercentage(int(100 * i / len(layersUri)))
    
    # Get layer from passed uri
    layer = processing.getObjectFromUri(uri)
    
    # Set style from QML
    if os.path.exists(qml):
        layer.loadNamedStyle(qml)
        iface.legendInterface().refreshLayerSymbology(layer)    
    
    # Set CRS
    if crs:
        qcrs = QgsCoordinateReferenceSystem()
        qcrs.createFromOgcWmsCrs(crs)
        layer.setCrs(qcrs)    
        
    # Refresh default contrast enhancement
    if rce:
        layer.setDefaultContrastEnhancement()        
        
    # Save style as default
    if ss:
        layer.saveDefaultStyle()

