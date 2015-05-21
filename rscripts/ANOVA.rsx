##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##Field2=Field Layer
##Field3=Field Layer
##Field4=Field Layer
##Field5=Field Layer
test1<-lm(Layer[[Field1]]~Layer[[Field2]]+Layer[[Field3]]+Layer[[Field4]]+Layer[[Field5]] )
test2<-lm(Layer[[Field1]]~Layer[[Field2]]+Layer[[Field4]]+Layer[[Field5]]  )
anova(test1,test2)