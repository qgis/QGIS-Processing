##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##Field2=Field Layer
##Field3=Field Layer
##Field4=Field Layer
##Field5=Field Layer
##method= Selection ward;average;single;complete;ward
##showplots
library(cluster)
Data<-cbind(Layer[[Field1]],Layer[[Field2]],Layer[[Field3]],Layer[[Field4]],Layer[[Field5]])
methodes <-c("ward","average","single","complete","ward")
methode<-methodes[method+1]
methode
cahCSP <- agnes(Data, metric = "euclidean", method = methode)
sortedHeight <- sort(cahCSP$height, decreasing = TRUE)
par(mfrow=c(2,1))
plot(sortedHeight, type = "h", xlab = "Noeuds", ylab = "Niveau d'agregation")
dendroCSP <- as.dendrogram(cahCSP)
plot(dendroCSP, leaflab = "none")