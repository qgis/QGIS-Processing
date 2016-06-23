##ggplot=group
##showplots
##Layer=Vector
##X= Field Layer
##Y=Field Layer
##Z=Field Layer
##Group=optional Field Layer
library("ggplot2")
library("ggtern")
if (is.null(Group)){
ggplot()+
geom_point(aes(Layer[[X]],Layer[[Y]], Layer[[Z]]))+
coord_tern() +
xlab(X)+
ylab(Y) +
zlab(Z) +
theme_showarrows()
} else {
ggplot()+
geom_point(aes(Layer[[X]],Layer[[Y]], Layer[[Z]], color=as.factor(Layer[[Group]])))+
coord_tern() +
xlab(X)+
ylab(Y) +
zlab(Z) +
theme_showarrows()+
theme(legend.title=element_blank())
}
