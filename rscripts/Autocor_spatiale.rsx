##Basic statistics=group
##Layer=vector
##Field=Field Layer
##nb_simul=number 100
##nb_vois=number 10
##showplots
library(spdep)
coords<-coordinates(Layer)
Y<-knearneigh(coords, k=nb_vois,longlat = T)
Y<-knn2nb(Y)
X<-nb2listw(Y, style="B", zero.policy=T)
if (class(Layer[[Field]])=="factor"){
Layer[[Field]]<-as.numeric(Layer[[Field]])
}
if(class(Layer[[Field]])=="character"){
Layer[[Field]]<-as.factor(as.numeric(Layer[[Field]]))
}
moran.test(x = Layer[[Field]], listw = X)
test<-moran.mc(x = Layer[[Field]], listw = X,nsim=nb_simul)
test
hist(test$res, freq=TRUE, breaks=20, xlab="Simulatec Moran's I")
abline(v=0,col="red")