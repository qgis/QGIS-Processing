##Basic statistics=group
##Layer=vector
##distance= number 200
##numero= number 11
##Output= output vector
library(rgdal)
library('maptools')
library(maptools)
library(rgeos)
library(geosphere)
library(stats)
distance_max = function(PointList){
dmax = 0
index = 0
n <- dim(PointList)[1]
for (i in (2 :(n - 1))){
p=PointList[i,]
line=rbind(PointList[1,], PointList[n,])
d = dist2Line(p, line, distfun=distHaversine)
if (d[1] > dmax){
index = i
dmax = d[1]
}
}
result<-c(index,dmax)
return (result)
}

DouglasPeucker= function(PointList, epsilon){
n <- dim(PointList)[1]
d<-distance_max(PointList)
if (d[2] < epsilon){
Result<-PointList
}
else if (d[2] >= epsilon){
X<- PointList[1:d[1],]
Y<- PointList[d[1]:n,]
ResultList<-list(X,Y)
k=1
while (k<length(ResultList)+1){
d<-distance_max(ResultList[[k]])
if (d[2] >= epsilon){
m<-dim(ResultList[[k]])[1]
X<- ResultList[[k]][1:d[1],]
Y<- ResultList[[k]][d[1]:m,]
ResultList[[k]]<-NULL
ResultList<-c(ResultList,list(X,Y))
k=k
} else {
m<-dim(ResultList[[k]])[1]
ResultList[[k]]<-rbind(ResultList[[k]][1,],ResultList[[k]][m,])
k=k+1
}
}
Result<-c(ResultList)
}
return (Result)
}
p<-length(Layer@polygons[[numero]]@Polygons)
Resultats<-c()
Coordi<-c()
for (w in (1:p)){
Coords<-c()
points<-Layer@polygons[[numero]]@Polygons[[w]]@coords
result<-DouglasPeucker(PointList=points, epsilon=distance)
if (class(result)=='matrix'){
Resultats<-Resultats
Coordi<-Coordi
} else{
Results<-rep(list(0),length(result))
Result<-rep(list(0),length(result))
for (t in (1:(length(result)))){
Coords<-rbind(Coords,result[[t]][1,])
}
for (k in (1:(length(result)))){
Result[[k]]<-Line(result[[k]])
Results[[k]]<-Lines(list(Result[[k]]),ID=paste("lignes",k,w))
}
Resultats<-c(Resultats,Results)
Coordi<-rbind(Coordi,Coords)
}
}
X<-SpatialLines(Resultats)
XX<-SpatialLinesDataFrame(X, data=as.data.frame(Coordi[1:length(X),]), match.ID = F)
Output=XX
