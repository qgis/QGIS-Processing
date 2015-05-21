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
cl1<-acp$li[,1]
cc1<-acp$co[,1]
cl2<-acp$li[,2]
cc2<-acp$co[,2]
plot(cc1,cc2,type="n", main="Les variables", xlim=c(-1,1), ylim=c(-1,1), asp=1, ylab= "",xlab= "")
abline(h=0,v=0)
text(cc1,cc2,row.names(acp$co))