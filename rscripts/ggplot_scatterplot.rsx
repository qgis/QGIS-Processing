##Vector processing=group
##showplots
##Layer=vector
##X=Field Layer
##Y=Field Layer
##Group=Field Layer
require(ggplot2)
ggplot()+
geom_point(aes(x=Layer[[X]],y=Layer[[Y]],
color=as.factor(Layer[[Group]])))+
theme(legend.title = element_blank())+
xlab(X)+
ylab(Y)
