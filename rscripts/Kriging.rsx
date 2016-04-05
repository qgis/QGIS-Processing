##Basic statistics=group
##showplots
##Layer=vector
##Field=Field Layer
##by=number 0.1
##Output=output raster
library(automap)
library(raster)
Y<-as.factor(LayerField)
attribut<-as.data.frame(Y)
A<-as.numeric(Y)
for(j in (1:length(levels(Y))))
for(i in 1:dim(attribut)[1]){
if (attribut[i,1]==levels(Y)[j]){
A[i]=j
}
}
coords<-coordinates(Layer)
MinX<-min(coords[,1])
MinY<-min(coords[,2])
MaxX<-max(coords[,1])
MaxY<-max(coords[,2])
Seqx<-seq(MinX, MaxX, by=by)
Seqy<-seq(MinY, MaxY, by=by)
MSeqx<-rep(Seqx, length(Seqy))
MSeqy<-rep(Seqy, length(Seqx))
MSeqy <- sort(MSeqy, decreasing=F)
Grille <- data.frame(X=MSeqx, Y=MSeqy)
coordinates(Grille)=c("X","Y")
gridded(Grille)<-TRUE
Mesure<- data.frame(LON=coords[,1], LAT=coords[,2],A)
coordinates(Mesure)<-c("LON","LAT")
variogram = autofitVariogram(A~1, Mesure)
plot(variogram)
kriging_result = autoKrige(A~1, Mesure, Grille,model=c("Cir","Lin","Bes","Wav","Hol","Leg","Per","Pen","Mat","Exc","Spl","Ste"))
prediction = raster(kriging_result$krige_output)
Output<-prediction