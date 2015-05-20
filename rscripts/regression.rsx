##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##Field2=Field Layer
##showplots
test<-lm(Layer[[Field1]] ~Layer[[Field2]] )
par(mfrow=c(2,2))
plot(test,which=1)
plot(test,which=2)
plot(test,which=3)
plot(test,which=4)
summary(test)
