# Written by Alexander Muriy with the Google help :)
# (Institute Of Environmental Geoscience, Moscow, Russia)
# amuriy AT gmail DOT com

##Merge all lines in layer=name
##Input_lines=vector
##Merged_lines=output vector

from qgis.core import *
from PyQt4.QtCore import *
from processing.tools.vector import VectorWriter

inputLayer = processing.getObject(Input_lines)
writer = VectorWriter(Merged_lines, None, '', QGis.WKBLineString, inputLayer.crs())
geoms = QgsGeometry.fromWkt('GEOMETRYCOLLECTION EMPTY')
for feature in inputLayer.getFeatures():
    geoms = geoms.combine(feature.geometry())

fet = QgsFeature()
fet.setGeometry(geoms)
writer.addFeature(fet)

del writer
    