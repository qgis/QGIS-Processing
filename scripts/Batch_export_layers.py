##Vector=group
##Batch export layers=name
##Vector_layers=multiple vector
##Format=selection ESRI Shapefile;GeoPackage;GeoJSON;CSV;ODS
##Use_table_name_instead_of_layer_name_for_database_layers=boolean True
##Output_folder=folder

from qgis.core import QgsDataSourceURI, QgsCoordinateReferenceSystem, QgsVectorFileWriter
import os

ogr_extensions = {
    0: 'shp',
    1: 'gpkg',
    2: 'geojson',
    3: 'csv',
    4: 'ods'
}
ogr_format = {
    0: 'ESRI Shapefile',
    1: 'GPKG',
    2: 'GeoJSON',
    3: 'CSV',
    4: 'ODS'
}

layers = Vector_layers.split(';')

# Writer options
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = ogr_format[Format]
options.fileEncoding = 'UTF-8'
options.onlySelectedFeatures = False
# options.ct = QgsCoordinateTransform instance
    
if ogr_format[Format] == 'GPKG':
    # Add option to create the file if not exists
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile

i = 0
for l in layers:
    
    layer = processing.getObject(l)
    lname = layer.name()
    progress.setInfo('%s' % lname)

    # Create filename for this layer
    output_name = layer.name()
    if layer.providerType() in ('postgres', 'spatialite') and Use_table_name_instead_of_layer_name_for_database_layers:
        output_name = QgsDataSourceURI(layer.dataProvider().dataSourceUri()).table()
    output_filename = os.path.join(Output_folder, output_name + '.' + ogr_extensions[Format])

    # CRS
    lcrs = layer.crs()
    #progress.setInfo('Source CRS = %s' % lcrs.authid())
    
    # Writer options
    options.layerName = output_name
    
    # For Geopackage
    if ogr_format[Format] == 'GPKG':
        
        # Change output file name
        output_filename = os.path.join(Output_folder, 'exported_layers.gpkg')
        
        # Change override method for Geopackage after first layer
        if i > 0:
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

    # Export layer
    writer = QgsVectorFileWriter.writeAsVectorFormat(
        layer,
        output_filename,
        options
    )
    if writer == 0:
        progress.setInfo('    Success')
    else:
        progress.setInfo('    Error')
        
    i = i + 1
    progress.setInfo('----------')
    progress.setInfo('')
    
