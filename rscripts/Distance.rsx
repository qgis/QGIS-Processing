##Basic statistics=group
##Layer1=vector
##Layer2=vector
##Field=Field Layer1
##output= output vector
library(geosphere)
library(rgeos)
line<-gLineMerge(Layer2, byid=FALSE, id = NULL)
x<-coordinates(Layer1)
X<-dist2Line(x, line, distfun=distHaversine)
matrix<-as.matrix(X[,2:3])
X<-cbind(X, as.data.frame(Layer1[[Field]]))
result<-SpatialPointsDataFrame(matrix, as.data.frame(X, row.names=NULL))
proj4string(Layer1)->crs
proj4string(result)<-crs
output<-result