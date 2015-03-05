##poly=vector
##output=output vector
from qgis.core import *
from qgis.core import *
from qgis.utils import *
from processing.core.VectorWriter import VectorWriter
from math import sqrt

inputLayer = processing.getObject(poly)
features = processing.features(inputLayer)
fields = inputLayer.pendingFields().toList()
outputLayer = VectorWriter(output, None, fields, QGis.WKBPoint,
                           inputLayer.crs())
outFeat = QgsFeature()
for inFeat in features:
    inGeom = inFeat.geometry()
    if inGeom.isMultipart():
        # find largest part in case of multipart
        maxarea = 0
        tmpGeom = QgsGeometry()
        for part in inGeom.asGeometryCollection():
            area = part.area()
            if area > maxarea:
                tmpGeom = part
                maxarea = area
        inGeom = tmpGeom
    atMap = inFeat.attributes()
    if QGis.QGIS_VERSION > '2.4':
        outGeom = inGeom.pointOnSurface()
    else:
        outGeom = inGeom.centroid()
    if not inGeom.contains(outGeom):
        # weight point outside the polygon
        # find intersection of horizontal line through the weight pont
        rect = inGeom.boundingBox()
        horiz = QgsGeometry.fromPolyline([QgsPoint(rect.xMinimum(), outGeom.asPoint()[1]), QgsPoint(rect.xMaximum(), outGeom.asPoint()[1])])
        line = horiz.intersection(inGeom)
        if line.isMultipart():
            # find longest intersection
            mline = line.asMultiPolyline()
            l = 0
            for i in range(len(mline)):
                d = sqrt((mline[i][0][0] - mline[i][1][0])**2 + (mline[i][0][1] - mline[i][1][1])**2)
                if d > l:
                    l = d
                    xMid = (mline[i][0][0] + mline[i][1][0]) / 2.0
                    yMid = (mline[i][0][1] + mline[i][1][1]) / 2.0
        else:
            xMid = (line.vertexAt(0).x() + line.vertexAt(1).x()) / 2.0
            yMid = (line.vertexAt(0).y() + line.vertexAt(1).y()) / 2.0
        outGeom = QgsGeometry.fromPoint(QgsPoint(xMid, yMid))
    outFeat.setAttributes(atMap)
    outFeat.setGeometry(outGeom)
    outputLayer.addFeature(outFeat)