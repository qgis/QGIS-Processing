##Basic statistics=group
##Layer=vector
##Field=Field Layer
##showplots
Densite <- density(Layer[[Field]])
plot(Densite$x, Densite$y, type="b")
abline(v = mean(Layer[[Field]]), col = "red")
abline(v = mean(Layer[[Field]])+2*sd(Layer[[Field]]), col = "green")
abline(v = mean(Layer[[Field]])-2*sd(Layer[[Field]]), col = "green")