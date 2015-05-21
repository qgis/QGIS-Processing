##Basic statistics=group
##Layer=vector
##Field1 = Field Layer
##Field2 = Field Layer
##Field3 = Field Layer
##Field4 = Field Layer
##Field5 = Field Layer
##Field6 = Field Layer
##showplots
library(FactoMineR)
library(ade4)
Layer<-as.data.frame(Layer)
donne<-cbind(Layer[[Field1]],Layer[[Field2]],Layer[[Field3]],Layer[[Field4]],Layer[[Field5]],Layer[[Field6]])
colnames(donne)<-c(Field1, Field2, Field3,Field4,Field5,Field6)
X<-FAMD (donne, ncp = 5, graph =FALSE, sup.var = NULL,
ind.sup = NULL, axes = c(1,2), row.w = NULL, tab.comp = NULL)
s.corcircle(X$var$coord[,1:2])
