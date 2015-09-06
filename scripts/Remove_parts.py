##Polygons=vector
##Max_Area=number 100000
##Delete_holes=boolean True
##Results=output vector

from qgis.core import *
from PyQt4.QtCore import *
from processing.tools.vector import VectorWriter
from shapely.geometry import Polygon, MultiPolygon
from shapely.wkb import loads
from shapely.wkt import dumps


polyLayer = processing.getObject(Polygons)
polyPrder = polyLayer.dataProvider()
n = polyLayer.featureCount()
l = 0

writer = VectorWriter(Results, None, polyPrder.fields(),
					  QGis.WKBMultiPolygon, polyPrder.crs())
					  

for feat in processing.features(polyLayer):
	progress.setPercentage(int(100*l/n))
	l+=1
	
	geom = loads(feat.geometry().asWkb())
	resgeom = []
	
	if geom.geom_type == 'Polygon': geom = [geom]
		
	for g in geom:
						
		if Polygon(g.exterior).area > Max_Area:			# polygon is large enough
						
			if not Delete_holes or len(g.interiors) == 0:
				resgeom.append(g)
			
			else:
				
				# only keep large enough holes
				
				h = [h for h in g.interiors if Polygon(h).area > Max_Area]
				resgeom.append(Polygon(g.exterior,h))
	
	if len(resgeom) > 0:
		feat.setGeometry(QgsGeometry.fromWkt(dumps(MultiPolygon(resgeom))))
		writer.addFeature(feat)		

del writer
