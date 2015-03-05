##Raster=group
##input=raster
##round_values_to_ndigits=number 3
##Sort_by_count=boolean False
##Highest_value_on_top=boolean True
##output_file=output html

from osgeo import gdal
import sys
import math
import operator

# load raster
gdalData = gdal.Open(str(input))

# get width and heights of the raster
xsize = gdalData.RasterXSize
ysize = gdalData.RasterYSize

# get number of bands
bands = gdalData.RasterCount

# start writing html output
f = open(output_file, 'a')
f.write('<TABLE>\n<TH>Band Number  </TH> <TH>Cell Value  </TH> <TH>Count</TH>\n')

# process the raster
for i in xrange(1, bands + 1):
  progress.setText("processing band " + str(i) + " of " + str(bands))
  band_i = gdalData.GetRasterBand(i)
  raster = band_i.ReadAsArray()

  # create dictionary for unique values count
  count = {}

  # count unique values for the given band
  for col in range( xsize ):
    if col % 10 == 0: progress.setPercentage(int(100*col/xsize))
    for row in range( ysize ):
      cell_value = raster[row, col]

      # check if cell_value is NaN
      if math.isnan(cell_value):
        cell_value = 'Null'

      # round floats if needed
      elif round_values_to_ndigits:
        try:
          cell_value = round(cell_value, int(round_values_to_ndigits))
        except:
          cell_value = round(cell_value)

      # add cell_value to dictionary
      try:
        count[cell_value] += 1
      except:
        count[cell_value] = 1
  
  # decide whether to sort by the count-column or the value-column
  if Sort_by_count:
    sortcount = sorted(count.items(), key=operator.itemgetter(1), reverse=Highest_value_on_top)
  else:
    sortcount = sorted(count.items(), key=operator.itemgetter(0), reverse=Highest_value_on_top)
  
  # print sorted results
  for j in range(len(sortcount)):
    line = "<TD>%s</TD> <TD>%s</TD> <TD>%s</TD>" %(i, sortcount[j][0], sortcount[j][1])
    f.write('<TR>'+ line + '</TR>' + '\n')

f.write('</TABLE>')
f.close

