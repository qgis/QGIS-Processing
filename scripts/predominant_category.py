##Assing predominant category=name
##Polygons=group
##layera=vector polygon
##layerb=vector polygon
##category=field layerb
##output=output vector

from PyQt4.QtCore import QVariant
from qgis.core import (
    QgsFeatureRequest,
    QgsGeometry,
    QGis,
    QgsFeature,
    QgsField)
from processing.tools import vector
from processing.tools.vector import VectorWriter
from processing.core.GeoAlgorithmExecutionException import *

layera = processing.getObject(layera)
layerb = processing.getObject(layerb)

providera = layera.dataProvider()
fieldsa = providera.fields()
providerb = layerb.dataProvider()
fieldsb = providerb.fields()
fieldIdx = layerb.fieldNameIndex(category)
fields =[]
fields.extend(fieldsa)
fields.append(QgsField(vector.createUniqueFieldName('MAJ', fieldsa), fieldsb.field(category).type()))
writer = VectorWriter(output, None, fields, QGis.WKBMultiPolygon, layera.crs())
outFeat = QgsFeature()
index = vector.spatialindex(layerb)
featuresa = list(layera.getFeatures())
nfeat = len(featuresa)
nprogress = 1 / float(nfeat) * 100
try:
    for n, feat in enumerate(featuresa):
        geom = feat.geometry()
        attrs = feat.attributes()
        intersects = index.intersects(geom.boundingBox())
        maxArea = -1
        cat = None
        nintersects = len(intersects)
        for m, i in enumerate(intersects):
            progress.setPercentage((nprogress * n) + (nprogress * (m / float(nintersects))))
            request = QgsFeatureRequest().setFilterFid(i)
            featb = layerb.getFeatures(request).next()
            tmpGeom = featb.geometry()
            if geom.intersects(tmpGeom):
                intGeom = geom.intersection(tmpGeom)
                if not intGeom:
                    continue
                area = intGeom.area()
                if area > maxArea:
                    maxArea = area
                    cat = featb.attributes()[fieldIdx]
        outFeat.setGeometry(geom)
        attrs.append(cat)
        outFeat.setAttributes(attrs)
        writer.addFeature(outFeat)            

except Exception, e:
    raise GeoAlgorithmExecutionException(e.args[0])

del writer
