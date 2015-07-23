##Vector=group
##layer=multiple vector
##file_prj=file

from qgis.core import *
import shutil

my_list = layer.split(",")
progress.setInfo(theCrs)
for i in my_list:
    a=i.replace(".shp",".prj")
    shutil.copy2(file_prj,a)
    progress.setInfo(a)
