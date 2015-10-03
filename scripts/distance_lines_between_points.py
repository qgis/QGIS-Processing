##Distance lines between points=name
##Vector=group
##pointLayer=vector
##outputLayer=output vector

from qgis.core import *
from PyQt4.QtCore import *
from processing.tools.vector import VectorWriter

inputLayer = processing.getObject(pointLayer)
# create new layer for output:
fields = [QgsField('distance', QVariant.Double)]
writer = VectorWriter(outputLayer, None, fields, QGis.WKBLineString, inputLayer.crs())
# loop all points:
iter1 = inputLayer.getFeatures()
for feature1 in iter1:
    p1 = feature1.geometry().asPoint()
    # loop all points again:
    iter2 = inputLayer.getFeatures()
    for feature2 in iter2:
        # check this to prevent creating double (reversed) lines:
        if feature1.id() < feature2.id():
            # create new line feature:
            p2 = feature2.geometry().asPoint()
            l = QgsGeometry.fromPolyline([p1,p2])
            feat = QgsFeature()
            feat.setGeometry(l)
            feat.setAttributes([l.length()])
            writer.addFeature(feat)
del writer
