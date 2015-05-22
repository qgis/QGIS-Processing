##Basic statistics=group
##Layer1=vector
##Layer2=vector
##methode=number 1
##Output= output raster
library(rgdal)
library(surveillance)
library(maptools)
library(ggplot2)
library(plyr)
library(ellipse)
library(fields)
library(ks)
library(maps)
library(rgeos)
library(snow)
library(sp)
library(ggmap)
library(reshape2)
sCircle <- function(n = 100, centre = c(0, 0), radius){
theta <- seq(0, 2*pi, length = n)
m <- cbind(cos(theta), sin(theta)) * radius
m[, 1] <- m[, 1] + centre[1]
m[, 2] <- m[, 2] + centre[2]
colnames(m) <- c("x", "y")
m
}
sWeights <- function(x, h, polygon) {
leCercle <- sCircle(centre = x, radius = 1.759*h)
POLcercle <- as(leCercle[-nrow(leCercle),], "gpc.poly")
return(area.poly(intersect(polygon, POLcercle)) / area.poly(POLcercle))
}
sKDE <- function(U, polygon, optimal = TRUE, h = .1, parallel = FALSE, n_clusters = 4){
if(!class(polygon) == "gpc.poly") polygon <- as(polygon, "gpc.poly")
if(class(U) == "data.frame") U <- as.matrix(U)
IND <- which(is.na(U[, 1]) == FALSE)
U <- U[IND,]
n <- nrow(U)
if(optimal){
H <- Hpi(U, binned = FALSE)
H <- matrix(c(sqrt(H[1, 1] * H[2, 2]), 0, 0, sqrt(H[1, 1] * H[2, 2])), 2, 2)
}
if(!optimal){
H <- matrix(c(h, 0, 0, h), 2, 2)
}
poidsU <- function(i, U, h, POL){
x <- as.numeric(U[i,])
sWeights(x, h, POL)
}
OMEGA <- NULL
for(i in 1:n){
OMEGA <- c(OMEGA, poidsU(i, U, h = sqrt(H[1, 1]), POL = polygon))
}
fhat <- kde(U, H, w = 1/OMEGA,
xmin = c(min(get.bbox(polygon)$x), min(get.bbox(polygon)$y)),
xmax = c(max(get.bbox(polygon)$x), max(get.bbox(polygon)$y)))
fhat$estimate <- fhat$estimate * sum(1/OMEGA) / n
vx <- unlist(fhat$eval.points[1])
vy <- unlist(fhat$eval.points[2])
VX <- cbind(rep(vx, each = length(vy)))
VY <- cbind(rep(vy, length(vx)))
VXY <- cbind(VX, VY)
Ind <- matrix(inside.gpc.poly(x = VX, y = VY, polyregion = polygon), length(vy), length(vx))
f0 <- fhat
f0$estimate[t(Ind) == 0] <- NA
list(
X = fhat$eval.points[[1]],
Y = fhat$eval.points[[2]],
Z = fhat$estimate,
ZNA = f0$estimate,
H = fhat$H,
W = fhat$w)
}
sKDE_without_c = function(U, polygon, optimal = TRUE, h = .1){
polygon <- as(polygon, "gpc.poly")
IND <- which(is.na(U[,1]) == FALSE)
U <- U[IND,]
n <- nrow(U)
if(optimal){
H <- Hpi(U,binned=FALSE)
H <- matrix(c(sqrt(H[1, 1] * H[2, 2]), 0, 0, sqrt(H[1, 1] * H[2, 2])), 2, 2)
}
if(!optimal){
H <- matrix(c(h, 0, 0, h), 2, 2)
}
fhat <- kde(U, H,
xmin = c(min(get.bbox(polygon)$x), min(get.bbox(polygon)$y)),
xmax = c(max(get.bbox(polygon)$x), max(get.bbox(polygon)$y)))

vx <- unlist(fhat$eval.points[1])
vy <- unlist(fhat$eval.points[2])
VX <- cbind(rep(vx, each = length(vy)))
VY <- cbind(rep(vy, length(vx)))
VXY <- cbind(VX,VY)
Ind <- matrix(inside.gpc.poly(x = VX, y = VY, polyregion = polygon), length(vy), length(vx))
f0 <- fhat
f0$estimate[t(Ind) == 0] <- NA
list(
X = fhat$eval.points[[1]],
Y = fhat$eval.points[[2]],
Z = fhat$estimate,
ZNA = f0$estimate,
H = fhat$H,
W = fhat$W)
}
points<-coordinates(Layer1)
polygon<-Layer2
if(methode==0){
estimate <- sKDE(U = points, polygon = polygon,
optimal=TRUE, parallel = FALSE)
}
if(methode==1){
estimate <- sKDE_without_c(U = points, polygon = polygon,
optimal=TRUE)
}
matrix<-cbind()
MinX<-min(estimate$X)
MinY<-min(estimate$Y)
MaxX<-max(estimate$X)
MaxY<-max(estimate$Y)
Seqx<-seq(MinX, MaxX, by=((MaxX - MinX)/(length(estimate$X) - 1)))
Seqy<-seq(MinY, MaxY, by=((MaxY - MinY)/(length(estimate$X) - 1)))
MSeqx<-rep(Seqx, length(Seqy))
MSeqy<-rep(Seqy, length(Seqx))
MSeqy <- sort(MSeqy, decreasing=F)
Grille <- data.frame(X=MSeqx, Y=MSeqy)
ZNA<-as.data.frame(estimate$ZNA)
for(i in 1:length(Seqy)){
for(j in 1:length(Seqx)){
matrix<-rbind(matrix,ZNA[j,i])
}
}
Grille<-cbind(Grille,as.numeric(matrix))
coordinates(Grille)=c("X","Y")
gridded(Grille)<-TRUE
library(raster)
result<-raster(Grille,layer=1, values=TRUE)
proj4string(Layer1)->crs
proj4string(result)<-crs
Output=result
