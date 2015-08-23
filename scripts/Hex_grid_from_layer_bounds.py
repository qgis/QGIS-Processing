##Polygons=group
##input=vector
##cellsize=number 1000.0
##grid=output vector

input = processing.getObject(input)

extent = input.extent()
extent = '%f,%f,%f,%f' %(input.extent().xMinimum()-cellsize/2, input.extent().xMaximum()+cellsize/2, input.extent().yMinimum()-cellsize/2, input.extent().yMaximum()+cellsize/2)

processing.runalg('qgis:creategrid', 3, extent, cellsize, cellsize, input.crs().authid(),grid)
