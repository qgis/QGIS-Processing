##[R-Geostatistics]=group
##showplots
##layer=vector
##field=field layer
##Estimate_range_and_psill_initial_values_from_sample_variogram=boolean True
##nugget=number 0
##model=selection Exp;Sph;Gau;Mat
##range=number 0
##psill=number 0
##Show_Sum_of_Square_Errors=boolean False

library('sp')
library('gstat')
print(model)
Models<-c("Exp","Sph","Gau","Mat")
model2<-Models[model+1]
# adjust variogram
names(layer)[names(layer)==field]="field"
layer$field <- as.numeric(as.character(layer$field))
str(layer)
layer <- remove.duplicates(layer)
layer <- layer[!is.na(layer$field),]

g <- gstat(id = field, formula = field~1, data = layer)
vg <- variogram(g)

if(Estimate_range_and_psill_initial_values_from_sample_variogram){range=NA} 
if(Estimate_range_and_psill_initial_values_from_sample_variogram){psill=NA}

vgm <- vgm(nugget=nugget, range=range, psill=psill, model=model2)
vgm = fit.variogram(vg, vgm)
>vgm
>if(Show_Sum_of_Square_Errors==TRUE){paste("SSE:", attr(vgm, "SSErr"))}
plot(vg, vgm, main = title , plot.numbers = TRUE)
