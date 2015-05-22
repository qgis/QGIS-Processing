##My scripts=group
##showplots
##Layer=vector
##X=Field Layer
##Y=Field Layer
##Title=string
plot(Layer[[X]], Layer[[Y]], xlab=X, ylab=Y, main=Title)+
abline(lm(Layer[[Y]]~Layer[[X]]))


