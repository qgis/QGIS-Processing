##Raster processing=group
##Create raster attribute table=name
##Layer=raster
##Levels=string NULL
##Output=output raster

# Load necessary libraries ----
library(raster)
library(stringr)

# Turn raster layer into factor ----
Layer <- as.factor(Layer[[1]])

# Add raster attribute table ---
rat <- levels(Layer[[1]])[[1]]
if (Levels == "NULL") {
  rat$tmp <- rat$ID
} else {
  tmp <- c(stringr::str_split_fixed(string = Levels, pattern = " ", n = Inf))
  if (length(tmp) != length(rat$ID)) {
    stop (paste("'Levels' does not match the number of levels in Layer (", length(rat$ID), ")", sep = ""))
  }
  rat$tmp <- tmp
}
colnames(rat)[2] <- names(Layer)
levels(Layer)[[1]] <- rat

# Output ----
Output <- Layer
Output
