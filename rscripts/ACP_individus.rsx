##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##Field2=Field Layer
##Field3=Field Layer
##Field4=Field Layer
##Individu1= number 10
##Individu2= number 10
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
Nom<-as.vector(Layer[[Field1]])
Nom_bis<-as.vector(Layer[[Field1]])
Nom_bis[Individu1]<-""
Nom_bis[Individu2]<-""
x<-dim(donne)[1]
if (Individu1>x | Individu2>x) {
rp.messagebox('error selection unavailable', title = 'oops!')
} else {
plot(cl1,cl2 ,type="n",main="Les individus",xlim=c(-7,7), ylim=c(-2,2))
abline(h=0,v=0)
text(acp$li[Individu1,1],acp$li[Individu1,2],Nom[Individu1],col="red",cex=1.2)
text(acp$li[Individu2,1],acp$li[Individu2,2],Nom[Individu2],col="orange",cex=1.2)
}
Nom_bis