##cover_layer_name=vector 
##join_layer_name=vector
##result=output table

from qgis.core import *
import csv

cover_atrs=[];
join_atrs=[];
header_attr=[];

cover_layer = processing.getObject(cover_layer_name)
join_layer = processing.getObject(join_layer_name)

for (k, v) in cover_layer.dataProvider().fieldNameMap().iteritems():
    cover_atrs.append(k)
    header_attr.append('cover_' + k)
    
for (k, v) in join_layer.dataProvider().fieldNameMap().iteritems():
    join_atrs.append(k)
    header_attr.append('join_' + k)

writer = processing.TableWriter(result, None, header_attr)

for bb in cover_layer.getFeatures():
    request = QgsFeatureRequest()
    request.setFilterRect(bb.geometry().boundingBox())
    dp = join_layer.dataProvider()
    for r in dp.getFeatures(request):
        if bb.geometry().intersects(r.geometry()):
            row = []
            for ca in cover_atrs:
                row.append(bb[ca])
            
            for ja in join_atrs: 
                row.append(r[ja])
            
            writer.addRecord(row)
