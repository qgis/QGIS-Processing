##Basic statistics=group
##Layer=vector
##Field1=Field Layer
##Field2=Field Layer
##Field3=Field Layer
##Field4=Field Layer
##showplots
library(ade4)
library(rpanel)
library(spatstat)
donne<-cbind(Layer[[Field1]], Layer[[Field2]], Layer[[Field3]], Layer[[Field4]])
donne<-na.exclude(donne)
donne<-as.data.frame(donne)
names(donne)<- c(Field1, Field2, Field3, Field4)
afc <- dudi.coa(donne, scannf = FALSE, nf = 2)
summary_afc <- data.frame(
EIG = afc$eig,
PCTVAR = 100 * afc$eig / sum(afc$eig),
CUMPCTVAR = cumsum(100 * afc$eig / sum(afc$eig))
)
par(mfrow=c(1,3))
barplot(summary_afc$PCTVAR,
xlab = "Composantes",
ylab = "Pourcentage de la variance (inertie)",
names = paste("C", seq(1, nrow(summary_afc), 1)),
col = "black",
border = "white")

plot(afc$li, pch = 20, col = "grey40")
abline(h=0, v=0)
points(afc$co, type = "o", pch = 18, col = "black")
text(afc$co,
labels = row.names(afc$co),
cex = 0.8,
pos = c(rep(4, times = 3), 1, rep(4, times = 4), 3))
contrib_afc<- inertia.dudi(afc,
row.inertia = TRUE,
col.inertia = TRUE)
tab<-cbind(afc$li[,1],afc$li[,2])
contrib_afc$col.abs
s.corcircle(afc$co)
