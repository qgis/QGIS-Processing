##Create equivalent numerical field=Name
##Vector=group
##layer=vector
##fieldname=field layer
##Equivalent_numerical_field_layer=output vector
##Equivalent_numerical_field_table=output table

# In addition to adding the Equivalent numerical field, this will create a reference table
# to relate the numbers with their original values.

from PyQt4.QtCore import QVariant
from qgis.core import (
    QgsFeatureRequest,
    QgsGeometry,
    QGis,
    QgsFeature,
    QgsField)
from processing.tools import vector
from processing.core.TableWriter import TableWriter
from processing.core.VectorWriter import VectorWriter
from processing.core.GeoAlgorithmExecutionException import *

vlayer = processing.getObject(layer)
vprovider = vlayer.dataProvider()
fieldindex = vlayer.fieldNameIndex(fieldname)
fields = vprovider.fields()
fields.append(QgsField('NUM_FIELD', QVariant.Int))

layer_writer = VectorWriter(Equivalent_numerical_field_layer, None, fields, vprovider.geometryType(), vlayer.crs())   
table_writer = TableWriter(Equivalent_numerical_field_table, None, [fieldname, 'num'])

outFeat = QgsFeature()
inGeom = QgsGeometry()
nElement = 0
classes = {}
features = vector.features(vlayer)
nFeat = len(features)
for feature in features:
  progress.setPercentage(int(100 * nElement / nFeat))
  nElement += 1
  inGeom = feature.geometry()
  outFeat.setGeometry(inGeom)
  atMap = feature.attributes()
  clazz = atMap[fieldindex]
  if clazz not in classes:
    classes[clazz] = len(classes.keys())
    table_writer.addRecord([clazz, classes[clazz]])
  atMap.append(classes[clazz])
  outFeat.setAttributes(atMap)
  layer_writer.addFeature(outFeat)
    
del layer_writer
del table_writer
