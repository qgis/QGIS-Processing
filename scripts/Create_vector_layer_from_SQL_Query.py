##Database=group
##Create vector layer from SQL Query=name
##Database_type=selection postgis;spatialite
##Connection_name=string
##Query=longstring
##Geometry_field_name=string geom
##Unique_id_field_name=string id
##Avoid_select_by_id=boolean True
##output=output vector

from qgis.core import *
from db_manager.db_plugins.plugin import DBPlugin, Schema, Table, BaseError
from db_manager.db_plugins import createDbPlugin
from db_manager.dlg_db_error import DlgDbError
from processing.tools.vector import VectorWriter

connectionName = unicode(Connection_name)
dbTypeMap = { 0: 'postgis', 1: 'spatialite' }
dbType = dbTypeMap[Database_type]

progress.setText('%s' % dbType)

# Get database connection via DbManager classes
connection = None
if connectionName:
    dbpluginclass = createDbPlugin( dbType, connectionName )
    if dbpluginclass:
        try:
            connection = dbpluginclass.connect()
        except BaseError as e:
            progress.setText(e.msg)
else:
    progress.setText('<b>## Please give a database connection name.</b>')

# Run the Query and create vector layer
layer = None
if connection:
    db = dbpluginclass.database()
    if db:

        # get a new layer name
        names = []
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            names.append( layer.name() )

        newLayerName = "vlayer"
        i = 0
        while newLayerName in names:
            i+=1
            newLayerName = u"%s_%d" % (layerName, i)
        
        # Create layer from query result
        layer = db.toSqlLayer(
            Query, 
            Geometry_field_name, 
            Unique_id_field_name, 
            newLayerName, 
            QgsMapLayer.VectorLayer, 
            Avoid_select_by_id
        )
        if layer.isValid():

            # Create writer
            writer = VectorWriter(
                output, 
                None, 
                layer.dataProvider().fields(),
                layer.dataProvider().geometryType(),
                layer.crs()
            )
                              
            # Export features
            features = layer.getFeatures()
            for feat in features:
                writer.addFeature(feat)

            del writer
            
            # Log number of features retrieves
            progress.setText('<b>|| The query returned %s features</b>' % layer.featureCount())
        
        else:
            progress.setText('<b>## The layer is invalid - Please check your query</b>')
    
    else:
        progress.setText('<b>## Database cannot be accessed</b>')
        
else:
    progress.setText('<b>## Cannot connect to the specified database connection name: "%s".</b>' % connectionName)
