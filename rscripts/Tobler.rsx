##Basic statistics=group
##Layer=raster
##x_depart= number 0.1
##y_depart= number 0.1
##x_arrivee= number 0.1
##y_arrivee= number 1
##Output= output vector
library(gdistance)
library(rgdal)
datas<-raster(Layer)

heightDiff <-function(x)(x[2] - x[1])
hd <- transition(datas,heightDiff,8)#packages gdistance
slope <- geoCorrection(hd, scl=FALSE)#packages gdistance
adj <- adjacent(x = datas, cells = 1:ncell(datas),pairs=TRUE ,directions=8) #packages raster
speed <- slope
speed[adj] <- exp(-3.5 * abs(slope[adj])+0.05)
speed<-geoCorrection(speed) #packages gdistance

Ax=x_depart
Ay=y_depart
Bx=x_arrivee
By=y_arrivee

c1<-c(Ax, Ay)
c2<-c(Bx, By)

sPath1 <-shortestPath(speed, c1, c2,output="SpatialLines")
Output=SpatialLinesDataFrame(sPath1, data=as.data.frame(c(1:length(sPath1))), match.ID = F)
