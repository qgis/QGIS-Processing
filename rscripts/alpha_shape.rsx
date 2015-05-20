##Basic statistics=group
##Layer=vector
##alpha=number 10
##Output= output vector
library(rgdal)
library(alphahull)
library(maptools)
alpha_points = ashape(coordinates(Layer),alpha=alpha)
l <- list()
for (i in 1:nrow(alpha_points$edges)) {
l[[i]] <-  Line(rbind(alpha_points$edges[i, 3:4], alpha_points$edges[i, 5:6]))
}
l <- list(Lines(l, as.character("1")))
sldf <- SpatialLinesDataFrame(SpatialLines(l), data.frame(name ="ashape"), match.ID = FALSE)
Output=sldf