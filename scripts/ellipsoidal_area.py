##Ellipsoidal Area=name
##Utils=group
##input=vector polygon
##ellipsoid=string WGS84
##new_field=string Area
##units=selection sq_km;sq_m;sq_miles;sq_ft;sq_nm;sq_degrees
##output=output vector

from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.tools.vector import VectorWriter
from PyQt4.QtCore import *
from qgis.core import *


measure_units_dict = {0: 'sq_km', 1: 'sq_m', 2: 'sq_miles', 3: 'sq_ft',
        4: 'sq_nm', 5:'sq_degrees'}
units_selection = measure_units_dict[units]
input_layer = processing.getObject(input)

if not input_layer.crs().geographicFlag():
  raise GeoAlgorithmExecutionException(
      'Your layer has a Projected CRS. '
      'This script works only on layers with Geographic CRS.')

fields = QgsFields()
for field in input_layer.pendingFields():
  if field.name().lower() == new_field.lower():
    raise GeoAlgorithmExecutionException(
        'The input layer already has a field named %s.'
        'Please choose a different name for the Area field.' % new_field)

  fields.append(field)
fields.append(QgsField(new_field, QVariant.Double))

writer = VectorWriter(output, None, fields,
                      QGis.WKBMultiPolygon, input_layer.crs())
# Initialize QgsDistanceArea object
area = QgsDistanceArea()
area.setEllipsoid(ellipsoid)
area.setEllipsoidalMode(True)
area.computeAreaInit()

out_f = QgsFeature()

# Get feature count for progress bar
features = processing.features(input_layer)
num_features = len(features)

for i, feat in enumerate(features):
  progress.setPercentage(int(100 *i / num_features))
  geom = feat.geometry()
  polygon_area = 0
  if geom.isMultipart():
    polygons = geom.asMultiPolygon()
    for polygon in polygons:
      polygon_area += area.measurePolygon(polygon[0])
  else:
    polygon = geom.asPolygon()
    polygon_area = area.measurePolygon(polygon[0])

  # calculated area is in sq. metres
  if units_selection == 'sq_km':
    final_area = polygon_area / 1e6
  elif units_selection == 'sq_ft':
    final_area = area.convertMeasurement(
        polygon_area, QGis.Meters, QGis.Feet, True)[0]
  elif units_selection == 'sq_miles':
    final_area = area.convertMeasurement(
        polygon_area, QGis.Meters, QGis.Feet, True)[0] / (5280.0 * 5280.0)
  elif units_selection == 'sq_nm':
    final_area = area.convertMeasurement(
        polygon_area, QGis.Meters, QGis.NauticalMiles, True)[0]
  elif units_selection == 'sq_degrees':
    final_area = area.convertMeasurement(
        polygon_area, QGis.Meters, QGis.Degrees, True)[0]
  else:
    final_area = polygon_area

  attrs = feat.attributes()
  attrs.append(final_area)
  out_f.setGeometry(geom)
  out_f.setAttributes(attrs)
  writer.addFeature(out_f)

progress.setPercentage(100)
del writer
