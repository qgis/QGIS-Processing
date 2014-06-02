##[3liz - Vector]=group
##input=vector
##cellsize=number 1000.0
##grid=output vector

input = processing.getObject(input)

centerx = (input.extent().xMinimum() + input.extent().xMaximum()) / 2
centery = (input.extent().yMinimum() + input.extent().yMaximum()) / 2
width = max((input.extent().xMaximum() - input.extent().xMinimum()), cellsize)
height = width

processing.runalg('qgis:creategrid', cellsize, cellsize, width, height,
                  centerx, centery, 1, input.crs().authid(), grid)
