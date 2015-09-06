##Vector_layer=group
##Save features filtered by expression=name
##Vector_layer=vector
##Expression=longstring
##output=output vector

from qgis.core import *
from processing.tools.vector import VectorWriter

# Get vector layer object
layer = processing.getObject(Vector_layer)
provider = layer.dataProvider()

# Filter features
# Build QGIS request with expression
qExp = QgsExpression(Expression)
if not qExp.hasParserError():
    qReq = QgsFeatureRequest(qExp)
    ok = True
else:
    progress.setText('An error occured while parsing the given expression: %s' % qExp.parserErrorString() )
    raise Expection(exp.parserErrorString())
    ok = False 

# Get features
if ok:
    # Get features corresponding to the expression
    features = layer.getFeatures( qReq )
else:
    # Get all features
    features = layer.getFeatures()
    
# Create writer
writer = VectorWriter(output, None, provider.fields(),
                      provider.geometryType(), layer.crs())
                      
# Export features
for feat in features:
    writer.addFeature(feat)
    
del writer
