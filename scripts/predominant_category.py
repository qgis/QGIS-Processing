##Assing predominant category=name
##Polygons=group
##layera=vector polygon
##layerb=vector polygon
##category=field layera
##output=output vector

providera = layera.dataProvider()
fieldsa = providera.fields()
providerb = layerb.dataProvider()
fieldsb = providerb.fields()
fieldIdx = layerb.fieldNameIndex(category)
fields =[]
fields.extend(fieldsa)
fields.append(QgsField(category, fieldsb.field(category).type()))
writer = VectorWriter(output, None, fields, QGis.WKBMultiPolygon, layera.crs())
outFeat = QgsFeature()
index = vector.spatialindex(layerb)
featuresa = vector.features(layera)
nfeat = len(features)
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
                    category = attrs[fieldIdx]
        outFeat.setGeometry(geom)        
        attrs.append(cat)        
        outFeat.setAttributes(attrs)
        writer.addFeature(outFeat)

except exception, e:
    raise GeoAlgorithmExecutionException(e.args[0])

writer.close()