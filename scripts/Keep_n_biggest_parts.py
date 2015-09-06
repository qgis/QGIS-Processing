##Polygons=vector
##To_keep=number 1
##Results=output vector

from qgis.core import *
from PyQt4.QtCore import *
from processing.tools.vector import VectorWriter
from operator import itemgetter

To_keep = int(To_keep)
if To_keep < 1:
	progress.setText("At least 1 part to keep")
	To_keep = 1
	

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
	
	if geom.isMultipart():
	
		featres = feat
	
		geoms = geom.asGeometryCollection()
		geomlength = [(i, geoms[i].area()) for i in range(len(geoms))]
		
		geomlength.sort(key=itemgetter(1))
		
		if To_keep == 1:
			featres.setGeometry(geoms[geomlength[-1][0]])
		else: 
			geomres = [geoms[i].asPolygon() for i,a in geomlength[-1 * To_keep]]
			featres.setGeometry(QgsGeometry.fromMultiPolygon(geomres))
		
		writer.addFeature(featres)
		
	else:
		writer.addFeature(feat)

del writer
