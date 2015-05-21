##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##Field2=Field Layer
##Field3=Field Layer
##Field4=Field Layer
##showplots
library(ade4)
library(rpanel)
library(spatstat)
donne<-cbind(Layer[[Field1]], Layer[[Field2]], Layer[[Field3]], Layer[[Field4]])
donne<-na.exclude(donne)
donne<-as.data.frame(donne)
names(donne)<- c(Field1, Field2, Field3, Field4)
acp<- dudi.pca(donne, center = T, scale = T, scannf = F)
contribution<-inertia.dudi(acp,col.inertia = T)$col.abs
plot(contribution)
text(contribution ,row.names(contribution))
