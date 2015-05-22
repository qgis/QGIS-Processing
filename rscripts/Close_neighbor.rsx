##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##distance= number 10
##Output= output vector
library(spdep)
library(sp)
coordi <- as.matrix(coordinates(Layer))
tram_nb <- dnearneigh(coordi, d1 = 0, d2 = distance, row.names=Layer[[Field1]])
tram_nb<-as.data.frame(card(tram_nb))
tram<-cbind(as.vector(Layer[[Field1]]), tram_nb)
Coord<-cbind()
n<-length(Layer[[Field1]])
for(i in 1:n){
if (tram[i,2]!=0 ){ Coord <-rbind(Coord,cbind(coordi[i,1], coordi[i,2],as.vector(Layer[[Field1]])[i]))
}
}
x<-as.numeric(Coord[,1])
y<-as.numeric(Coord[,2])
X<-cbind(x,y)
matrix<-as.matrix(X)
matrix<-SpatialPointsDataFrame(matrix, as.data.frame(Coord),proj4string=CRS("+init=epsg:2154"))
Output=matrix