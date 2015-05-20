##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##showplots
library(cluster)
library(rpart)
arbre <- rpart(Layer[[Field1]]~.,Layer)
arbre
plot(arbre, main="Arbre", branch=1, compress=T, margin=0.1)
text(arbre,splits=T, fancy=T, use.n=F, pretty=0, all=T)
