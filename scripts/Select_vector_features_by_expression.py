##[3liz - Vector]=group
##Select vector features by expression=name
##Input_vector_layer=vector
##Expression=longstring
##selected_features_count=output number

from qgis.core import *

# Get vector layer
layer = processing.getObject(Input_vector_layer)

# Script state
ok = True
nb = 0

# Build QGIS request with expression
qExp = QgsExpression(Expression)
if not qExp.hasParserError():
    qReq = QgsFeatureRequest(qExp)
else:
    progress.setText('An error occured while parsing the given expression: %s' % qExp.parserErrorString() )
    raise Expection(exp.parserErrorString())
    ok = False

# Set selection 
if ok:
    # Get features corresponding to the expression
    features = layer.getFeatures( qReq )
    # Set the selection
    layer.setSelectedFeatures( [ f.id() for f in features ] )
    nb = layer.selectedFeatureCount()

selected_feature_count = nb

progress.setText('<b>%s features have been selected in the vector layer</b>' % nb)