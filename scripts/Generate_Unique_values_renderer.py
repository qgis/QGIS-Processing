##Raster=group
##Generate unique values style=name
##Raster_to_extract_unique_values=raster
##round_values_to_ndigits=number 0

from osgeo import gdal
from random import randint
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import iface

# Rename verbose input vars
input = Raster_to_extract_unique_values
rdig = round_values_to_ndigits

# Initialize unique values list
sort_values = []
# create set for unique values list
cell_values = set()

# load raster
gdalData =  gdal.Open(str(input))

# get width and heights of the raster
xsize = gdalData.RasterXSize
ysize = gdalData.RasterYSize

# get number of bands
bands = gdalData.RasterCount

# process the raster
for i in xrange(1, bands + 1):
    progress.setText("processing band " + str(i) + " of " + str(bands))
    band_i = gdalData.GetRasterBand(i)
    raster = band_i.ReadAsArray() # This loads the entire raster into memory!
    # count unique values for the given band
    for col in range( xsize ):
        if col % 10 == 0: progress.setPercentage(int(100*col/xsize))
        for row in range( ysize ):
            cell_value = raster[row, col]
            # check if cell_value is NaN - don't add if it is
            if not math.isnan(cell_value):
                # round floats if needed
                if rdig:
                    try:
                        cell_value = round(cell_value, int(rdig))
                    except:
                        cell_value = round(cell_value)
                # Add to the unique values set
                cell_values.add(cell_value)
 
del(gdalData)

# decide whether to sort by the count-column or the value-column
sort_values = sorted(cell_values)
      
# Now load the layer and apply styling
layer = processing.getObjectFromUri(input)

qCRS = QgsColorRampShader()

# Build the colour ramp using random colours
colList = ['#ff0000','#ffff00','#0000ff','#00ffff','#00ff00','#ff00ff']

lst = []
for i,val in enumerate(sort_values):
    lst.append(QgsColorRampShader.ColorRampItem(val,QColor(colList[i % 6])))

qCRS.setColorRampItemList(lst)
qCRS.setColorRampType(QgsColorRampShader.EXACT)

shader = QgsRasterShader()
shader.setRasterShaderFunction(qCRS)

renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), layer.type(), shader)
layer.setRenderer(renderer)
layer.triggerRepaint()