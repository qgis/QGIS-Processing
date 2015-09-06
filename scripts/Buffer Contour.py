##Points=vector point
##Value_field=field Points
##Levels=string 10;20
##Buffer_parameter=number 60
##Max_buffer_size=number 500
##Group_by_field=boolean True
##Group_Field=field Points
##Contour=output vector

from qgis.core import *
from PyQt4.QtCore import *
from processing.tools.vector import VectorWriter
from shapely.ops import cascaded_union
from shapely.wkb import loads
from shapely.wkt import dumps


levels = [float(x) for x in Levels.split(";")]
maxlevel = max(levels)
mbuf = Max_buffer_size

progress.setText("lvls {0}".format(levels))

nodeLayer = processing.getObject(Points)
nodePrder = nodeLayer.dataProvider()
n = nodeLayer.featureCount()
l = 0

pts = {}
bpr = Buffer_parameter

for feat in processing.features(nodeLayer):
	progress.setPercentage(int(100*l/n))
	l+=1

	if feat[Value_field] < maxlevel:
		if Group_by_field: k = feat[Group_Field]
		else: k = 'a'
		
		if k not in pts: pts[k] = []

		pts[k].append((feat.geometry().asPoint(), feat[Value_field]))


if Group_by_field:
	fields = [QgsField(Group_Field, QVariant.String), QgsField('level', QVariant.Double)]
else:
	fields = [QgsField('level', QVariant.Double)]
	
writer = VectorWriter(Contour, None, fields, QGis.WKBMultiPolygon, nodePrder.crs())

feat = QgsFeature()

n = len(pts)
l = 0

for k,v in pts.iteritems():
	progress.setPercentage(int(100*l/n))
	l+=1
	
	if Group_by_field: attrs = [k, 0]
	else: attrs = [0]

	for l in levels:
		
		if Group_by_field: attrs[1] = l
		else: attrs[0] = l
		feat.setAttributes(attrs)
			
		ptlist = [x for x in v if x[1] < l]
		polygons = [loads(QgsGeometry.fromPoint(p).buffer(min(mbuf, d * bpr), 10).asWkb())
					for p,d in ptlist]
		
		feat.setGeometry(QgsGeometry.fromWkt(dumps(cascaded_union(polygons))))
		writer.addFeature(feat)

del writer
