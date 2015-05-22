##Vector processing=group
##showplots
##Layer=vector
##Field=Field Layer
plot(ecdf(Layer[[Field]]), verticals=T, pch=46, main="Frequency plot", xlab=Field) +
abline(v=median(Layer[[Field]]), col="red") +
text(median(Layer[[Field]]), 0.2, "median", col="red", srt=90, adj=c(-0.1, -0.1)) +
abline(v=mean(Layer[[Field]]), col="green") +
text(mean(Layer[[Field]]), 0.2, "mean", col="green", srt=90, adj=c(2, -0.1))
