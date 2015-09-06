##Polygons=vector
##Key_Field=field Polygons
##Cutting_polygons=vector
##Cut_Key_Field=field Cutting_polygons
##Results=output vector

from qgis.core import *
from PyQt4.QtCore import *
from processing.tools.vector import VectorWriter
from shapely.geometry import Polygon, MultiPolygon
from shapely.wkt import loads, dumps

cutLayer = processing.getObject(Cutting_polygons)
cutPrder = cutLayer.dataProvider()
n = cutLayer.featureCount()
l = 0

# key: key field, value: list of wkb geoms
cutters = {}

for feat in processing.features(cutLayer):
	progress.setPercentage(int(100*l/n))
	l+=1
	
	k = feat[Cut_Key_Field]
	cutters.setdefault(k, [])
	
	cutters[k].append(feat.geometry().exportToWkt())


# Transform list of geometries in multigeometries as WKT

for k in cutters.keys():

	t = []

	for g in [loads(c) for c in cutters[k]]:
		
		if g.geom_type == 'Polygon':
			t.append(g)
		else:
			t.extend(g)
				
	cutters[k] = dumps(MultiPolygon(t))


polyLayer = processing.getObject(Polygons)
polyPrder = polyLayer.dataProvider()
n = polyLayer.featureCount()
l = 0

writer = VectorWriter(Results, None, polyPrder.fields(),
					  QGis.WKBMultiPolygon, polyPrder.crs())
					  

for feat in processing.features(polyLayer):
	progress.setPercentage(int(100*l/n))
	l+=1
	
	geom = feat.geometry()
	k = feat[Key_Field]
	
	if k not in cutters:
		progress.setText("No corresponding key: {0}".format(k))
	else:
		cutgeom = QgsGeometry.fromWkt(cutters[k])
		feat.setGeometry(geom.intersection(cutgeom))
	
	writer.addFeature(feat)		

del writer
