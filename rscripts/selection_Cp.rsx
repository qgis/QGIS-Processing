##Basic statistics=group
##Layer=vector
##Field1 = Field Layer
##Field2 = Field Layer
##Field3 = Field Layer
##Field4 = Field Layer
##Field5 = Field Layer
##Field6 = Field Layer
##Methode=Selectionexhaustive;backward;forward;seqrep
##Nombre_var = number 5
##showplots
library(leaps)
X<-cbind(Layer[[Field2]],Layer[[Field3]],Layer[[Field4]],Layer[[Field5]],Layer[[Field6]])
colnames(X)<-c(Field2, Field3, Field4, Field5, Field6)
method=c("exhaustive", "backward", "forward", "seqrep")
methode<-method[Methode + 1]
test1<-regsubsets(Layer[[Field1]]~X,data=Layer,really.big=T,nbest=1,nvmax=Nombre_var, intercept=F,method=methode)
plot(test1, scale="Cp")
summary(test1)
