##Basic statistics=group
##Layer=vector
##nombre=number 10
##Output= output vector
library(sp)
Coord<-Layer@lines[[nombre]]@Lines[[1]]@coords
x<-as.numeric(Coord[,1])
y<-as.numeric(Coord[,2])
X<-cbind(x,y)
matrix<-as.matrix(X)
matrix<-SpatialPointsDataFrame(matrix, as.data.frame(Coord),proj4string=CRS("+init=epsg:2154"))
Output=matrix
