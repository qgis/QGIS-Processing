##Database=group
##Create vector layer from postgis table=name
##Host=string localhost
##Port=number 5432
##Database=string
##User=string
##Password=string
##Schema=string public
##Table=string
##Geometry_column=string geom
##Where_clause=string
##Unique_id_field_name=string id
##output=output vector

from qgis.core import *
from processing.tools.vector import VectorWriter

# Create uri from database connection options
uri = QgsDataSourceURI()
uri.setConnection(Host, str(Port), Database, User, Password)
uri.setDataSource(Schema, Table, Geometry_column, Where_clause, Unique_id_field_name)

# Create the vector layer
layer = QgsVectorLayer(uri.uri(), 'vlayer', 'postgres')

# Output the vector layer
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

else:
    progress.setText('<b>## The layer is invalid - Please check the connection parameters.</b>')

