##Basic statistics=group
##Layer=vector
##Criteres= Selection cp;bic;r2;adjr2;tous
##Methode=Selectionexhaustive;backward;forward;seqrep
##nbr_var = number 10
##Field1 = Field Layer
##Field2 = Field Layer
library(leaps)
library(stats)
library(rpanel)
layer<-as.data.frame(Layer)
Z<-colnames(Layer@data)
z<-c()
X<-c()
for (j in (1:dim(layer)[2])){
X<-cbind(X,layer[,j])
z<-cbind(z,Z[j])
}
colnames(X)<-z
a<-which(colnames(X)==Field1)
X<-X[,-a]
b<-which(colnames(X)==Field2)
X<-X[,-b]
Y<-Layer[[Field1]]
method=c("exhaustive", "backward", "forward", "seqrep")
methode<-method[Methode + 1]
test1<-regsubsets(Y~X,data=Layer, really.big=T,nbest=1,nvmax=nbr_var, intercept=F,method=methode)
model<-summary(test1)$which
result1<-cbind()
result2<-cbind()
result3<-cbind()
result4<-cbind()
result<-cbind()
num_mod<-which.min(summary(test1)$cp)
beta<-model[num_mod,]
for(i in (1:length(beta))){
if (beta[i]==T) {
result<-c(result,beta[i])
}
}
critere<-c("cp","bic","r2","adjr2","tous")
critere<-critere[Criteres+1]
if (critere=="tous"){
num_mod2<-which.min(summary(test1)$bic)
num_mod1<-which.min(summary(test1)$cp)
num_mod4<-which.min(summary(test1)$adjr2)
num_mod3<-which.min(summary(test1)$rsq)
beta1<-model[num_mod1,]
beta2<-model[num_mod2,]
beta3<-model[num_mod3,]
beta4<-model[num_mod4,]
for(i in (1:length(beta1))){
if (beta1[i]==T) {
result1<-c(result1,beta1[i])
}
}
for(i in (1:length(beta2))){
if (beta2[i]==T) {
result2<-c(result2,beta2[i])
}
}
for(i in (1:length(beta3))){
if (beta3[i]==T) {
result3<-c(result3,beta3[i])
}
}
for(i in (1:length(beta4))){
if (beta4[i]==T) {
result4<-c(result4,beta4[i])
}
}
}
result
result1
result2
result3
result4