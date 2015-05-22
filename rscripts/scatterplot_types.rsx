##Vector processing=group
##showplots
##Layer=vector
##X=Field Layer
##Y=Field Layer
##type=selection point;lines;point&lines
if (type == 0) {
plot(Layer[[X]], Layer[[Y]], xlab=X, ylab=Y)
} else if (type == 1) {
plot(Layer[[X]], Layer[[Y]], xlab=X, ylab=Y, type="l")
} else if (type == 2) {
plot(Layer[[X]], Layer[[Y]], xlab=X, ylab=Y, type="b")
}
