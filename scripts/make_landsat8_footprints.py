##url=string http://landsat-pds.s3.amazonaws.com/scene_list.gz
##output_layer=output vector

from qgis.core import *
from PyQt4.QtCore import *
import os, sys
import urllib2
import gzip

shpname = os.path.basename(output_layer)[:-4]
folder = os.path.dirname(output_layer)

gzfilename = os.path.join(folder, os.path.basename(url))
filename = gzfilename.replace(".gz", "")

req = urllib2.urlopen(url)
with open(gzfilename, 'wb') as fp:
    fp.write(req.read())

inF = gzip.open(gzfilename, 'rb')
outF = open(filename, 'wb')
outF.write( inF.read() )
inF.close()
outF.close()

f = open(filename, "r")
header = f.readline()

fields = QgsFields()
fields.append(QgsField("ENTITY_ID", QVariant.String))
fields.append(QgsField("ACQ_DATE", QVariant.String))
fields.append(QgsField("CLOUDCOVER", QVariant.Double))
fields.append(QgsField("PROC_LEVEL", QVariant.String))
fields.append(QgsField("PATH", QVariant.Int))
fields.append(QgsField("ROW", QVariant.Int))
fields.append(QgsField("MIN_LAT", QVariant.Double))
fields.append(QgsField("MIN_LON", QVariant.Double))
fields.append(QgsField("MAX_LAT", QVariant.Double))
fields.append(QgsField("MAX_LON", QVariant.Double))
fields.append(QgsField("DATA_URL", QVariant.String))

crs = QgsCoordinateReferenceSystem()
crs.createFromString('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]')
writer = QgsVectorFileWriter(output_layer, "CP1250", fields, QGis.WKBPolygon, crs, "ESRI Shapefile")
for line in f:
    line = line.strip().split(",")
    min_lat = float(line[6])
    min_lon = float(line[7])
    max_lat = float(line[8])
    max_lon = float(line[9])

    if abs(max_lon - min_lon) > 180:
        min_lon = min_lon + 360

    feat = QgsFeature()    
    gPolygon = QgsGeometry.fromPolygon([[QgsPoint(min_lon,max_lat), QgsPoint(max_lon,max_lat), QgsPoint(max_lon,min_lat), QgsPoint(min_lon,min_lat)]])
    feat.setGeometry(gPolygon)
    
    feat.setAttributes([line[0], line[1], float(line[2]), line[3], int(line[4]), int(line[5]), min_lat, min_lon, max_lat, max_lon, line[10]])
    
    writer.addFeature(feat)
del writer
f.close()

# Remove
os.unlink(gzfilename)
os.unlink(filename)
