##Basic statistics=group
##Layer=vector
##distance=number 100
##Output1= output vector
##Output2= output vector
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
p<-length(Layer@polygons)
FRONT<-c()
front<-c()
for (w in (1:(p-1))){
Layer1<-SpatialPolygonsDataFrame(SpatialPolygons(list(Layer@polygons[[w]])),
data=as.data.frame(c(1:length(SpatialPolygons(list(Layer@polygons[[w]]))))),match.ID = F)
for(W in((w+1):p)){
Layer0<-SpatialPolygonsDataFrame(SpatialPolygons(list(Layer@polygons[[W]])),
data=as.data.frame(c(1:length(SpatialPolygons(list(Layer@polygons[[W]]))))),match.ID = F)
A<-gIntersection(Layer1, Layer0, byid=FALSE, id=NULL)
if (class(A)!='NULL'){
A<-gLineMerge(A, byid=FALSE, id = NULL)
front<-c(front,A)
}
}
if (class(front)!='NULL'){
for (t in(1:length(front))){
FRONT<-c(FRONT, Line(front[[t]]@lines[[1]]@Lines[[1]]@coords))
}
}
front<-c()
}
FRONT<-Lines(FRONT,ID='lin')
FRONT<-SpatialLines(list(FRONT))
Output1=SpatialLinesDataFrame(FRONT, data=as.data.frame(c(1:length(FRONT))), match.ID = F)

x<-length(Output1@lines[[1]]@Lines)
ligne<-c()
i=0
for (z in (1:x)){
Resultats<-c()
points<-Output1@lines[[1]]@Lines[[z]]@coords
result<-DouglasPeucker(PointList=points, epsilon=distance)
if (class(result)=='matrix'){
Resultats<-Resultats
} else{
Results<-rep(list(0),length(result))
Result<-rep(list(0),length(result))
for (k in (1:(length(result)))){
Result[[k]]<-Line(result[[k]])
i=i+1
Results[[k]]<-Lines(list(Result[[k]]),ID=paste("lignes",i))
}
Resultats<-c(Resultats,Results)
}
ligne<-c(ligne,Resultats)
}
Ligne<-SpatialLines(ligne)
Output1=SpatialLinesDataFrame(Ligne, data=as.data.frame(c(1:length(Ligne))), match.ID = F)

i=0
a<-c()
X<-gSymdifference(Layer, Ligne, byid=FALSE, id=NULL)

for (t in (1:length(X@polygons[[1]]@Polygons))){
a<-c(a,Lines(Line(X@polygons[[1]]@Polygons[[t]]@coords), ID=paste('lin',i)))
i=i+1
}
a<-SpatialLines(a)
a<-SpatialLinesDataFrame(a, data=as.data.frame(c(1:length(a))), match.ID = F)
ligne2<-c()
x<-length(a@lines)
for (z in (1:x)){
Resultats<-c()
points<-a@lines[[z]]@Lines[[1]]@coords
result<-DouglasPeucker(PointList=points, epsilon=distance)
if (class(result)=='matrix'){
Resultats<-Resultats
} else{
Results<-rep(list(0),length(result))
Result<-rep(list(0),length(result))
for (k in (1:(length(result)))){
Result[[k]]<-Line(result[[k]])
i=i+1
Results[[k]]<-Lines(list(Result[[k]]),ID=paste("lignes",i))
}
Resultats<-c(Resultats,Results)
}
ligne2<-c(ligne2,Resultats)
}
Ligne_2<-SpatialLines(ligne2)
Output2=SpatialLinesDataFrame(Ligne_2, data=as.data.frame(c(1:length(Ligne_2))), match.ID = F)