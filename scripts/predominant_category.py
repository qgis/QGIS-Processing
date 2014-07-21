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
from processing.core.VectorWriter import VectorWriter
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
featuresa = vector.features(layera)
nfeat = len(featuresa)
try:
    for n, feat in enumerate(featuresa):
        progress.setPercentage(n/ float(nfeat) * 100)
        geom = QgsGeometry(feat.geometry())
        attrs = feat.attributes()
        intersects = index.intersects(geom.boundingBox())
        maxArea = -1
        cat = None
        for i in intersects:
            request = QgsFeatureRequest().setFilterFid(i)
            featb = layerb.getFeatures(request).next()
            tmpGeom = featb.geometry()
            if geom.intersects(tmpGeom):
                intGeom = QgsGeometry(geom.intersection(tmpGeom))
                area =intGeom.area()
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
