##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##Field2=Field Layer
##Field3=Field Layer
##Field4=Field Layer
##Field5=Field Layer
##Field6=Field Layer
##Field7=Field Layer
library(ade4)
test<-lm(Layer[[Field1]]~Layer[[Field2]]+Layer[[Field3]]+Layer[[Field4]]+Layer[[Field5]]+Layer[[Field6]]+Layer[[Field7]])
summary(test)
