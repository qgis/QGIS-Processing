##Vector processing=group
##showplots
##Layer=vector
##X=Field Layer
##Y=Field Layer
##type=selection No logarithm;logarithm X;logarithmY;logarithm X and Y
if (type == 0) {
plot(Layer[[X]], Layer[[Y]], xlab=X, ylab=Y)
}
if (type == 1) {
plot(log(Layer[[X]]), Layer[[Y]], xlab=X, ylab=Y)
} else if (type == 2) {
plot(Layer[[X]], log(Layer[[Y]]), xlab=X, ylab=Y)
} else if (type == 3) {
plot(log(Layer[[X]]), log(Layer[[Y]]), xlab=X, ylab=Y)
}
