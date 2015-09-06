##Points=vector
##Value_field=field Points
##Levels=string 0;10;20
##Group_by_field=boolean True
##Group_Field=field Points
##Results=output vector

from shapely.geometry import MultiPolygon
from qgis.core import *
from PyQt4.QtCore import *
from processing.tools.vector import VectorWriter
import numpy as np
import matplotlib.pyplot as plt


levels = [float(x) for x in Levels.split(";")]

nodeLayer = processing.getObject(Points)
nodePrder = nodeLayer.dataProvider()
n = nodeLayer.featureCount()
l = 0

pts = {}


for feat in processing.features(nodeLayer):
	progress.setPercentage(int(100*l/n))
	l+=1

	if Group_by_field:
		k = feat[Group_Field]
	else:
		k = 'a'
	
	geom = feat.geometry().asPoint()

	pts.setdefault(k, {'x':[], 'y':[], 'v':[]})
		
	pts[k]['x'].append(geom.x())
	pts[k]['y'].append(geom.y())
	pts[k]['v'].append(feat[Value_field])


if Group_by_field:
	fields = [QgsField(Group_Field, QVariant.String),
			  QgsField('min', QVariant.Double),
			  QgsField('max', QVariant.Double)]
else:
	fields = [QgsField('min', QVariant.Double),
			  QgsField('max', QVariant.Double)]
	
writer = VectorWriter(Results, None, fields, QGis.WKBMultiPolygon, nodePrder.crs())

feat = QgsFeature()

n = len(pts)
l = 0

for k in pts.keys():
	progress.setPercentage(int(100*l/n))
	l+=1
	
	if Group_by_field:
		attrs = [k]
	else:
		attrs = []

	# convert each sublist in a numpy array

	x = np.array(pts[k]['x'])
	y = np.array(pts[k]['y'])
	v = np.array(pts[k]['v'])

	cs = plt.tricontourf(x, y, v, levels, extend='neither')

	for i, polygon in enumerate(cs.collections):
		
		mpoly = []
		
		for path in polygon.get_paths():
			path.should_simplify = False
			poly = path.to_polygons()
			exterior = []
			holes = []
			
			if len(poly) > 0:
				exterior = poly[0]
				if len(poly) > 1: # There's some holes
					holes = [h for h in poly[1:] if len(h) > 2]

			mpoly.append([exterior, holes])
		
		if len(mpoly) > 0:
			if Group_by_field:
				attrs = [k, levels[i], levels[i+1]]
			else:
				attrs = [levels[i], levels[i+1]]
			feat.setAttributes(attrs)
			feat.setGeometry(QgsGeometry.fromWkt(MultiPolygon(mpoly).to_wkt()))
			writer.addFeature(feat)

del writer
