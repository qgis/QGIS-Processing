##ggplot=group
##showplots
##Layer=Vector
##X= Field Layer
##Y=Field Layer
##Z=Field Layer
##Grouping = boolean
##Group=Field Layer
library("ggplot2")
library("ggtern")
ggplot()+
geom_point(aes(Layer[[X]],Layer[[Y]], Layer[[Z]]))+
coord_tern() +
xlab(X)+
ylab(Y) +
zlab(Z) +
theme_showarrows()+
if (Grouping == 1) {
ggplot()+
geom_point(aes(Layer[[X]],Layer[[Y]], Layer[[Z]], color=as.factor(Layer[[Group]])))+
coord_tern() +
xlab(X)+
ylab(Y) +
zlab(Z) +
theme_showarrows()+
theme(legend.title=element_blank())
}
