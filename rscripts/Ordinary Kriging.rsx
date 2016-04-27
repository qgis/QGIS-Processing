##[R-Geostatistics]=group
##showplots
##layer=vector
##field=field layer
##Estimate_range_and_psill_initial_values_from_sample_variogram=boolean True
##nugget=number 0
##model=selection Exp;Sph;Gau;Mat
##range=number 0
##psill=number 0
##Local_kriging=boolean False
##Number_of_nearest_observations=number 25
##Show_Sum_of_Square_Errors=boolean False
##Extent=selection Convex Hull; Layer Extent
##Resolution=number 0
##kriging_variance= output raster
##kriging_prediction= output raster


library('gstat')
library('sp')
Models<-c("Exp","Sph","Gau","Mat")
model2<-Models[model+1]

create_new_data_ch <- function (layer)
{
  convex_hull = chull(coordinates(layer)[, 1], coordinates(layer)[,2])
  convex_hull = c(convex_hull, convex_hull[1])
  d = Polygon(layer[convex_hull, ])
  if(!is.projected(layer) | Resolution== 0){new_data = spsample(d, 5000, 
                                                              type = "regular")}
  if(is.projected(layer)  & Resolution!= 0){
    new_data = spsample(d, n= 1, cellsize=c(Resolution,Resolution),
                      type="regular")}
  gridded(new_data) = TRUE
  attr(new_data, "proj4string") <-layer@proj4string
  return(new_data)
}

create_new_data_ext <- function (layer){ 
  bottomright <- c(layer@bbox[1], layer@bbox[2])
  topleft <- c(layer@bbox[3], layer@bbox[4])
  d <- SpatialPolygons(
    list(Polygons(list(Polygon(coords = matrix(
      c(topleft[1],bottomright[1], bottomright[1],topleft[1],topleft[1],
        topleft[2], topleft[2], bottomright[2], 
        bottomright[2],topleft[2]), ncol=2, nrow= 5))), ID=1)))
  if(!is.projected(layer) | Resolution== 0){new_data = spsample(d, 5000, 
                                                              type = "regular")}
  if(is.projected(layer) & Resolution != 0){
    new_data = spsample(d, n= 1, cellsize=c(Resolution,Resolution),
                        type="regular")}
  gridded(new_data) = TRUE
  attr(new_data, "proj4string") <-layer@proj4string
  return(new_data)
}

if(Extent==0){mask<-create_new_data_ch(layer)}
if(Extent==1){mask<-create_new_data_ext(layer)}

field <- make.names(field)
names(layer)[names(layer)==field]="field"

layer$field <- as.numeric(as.character(layer$field))
str(layer)
layer <- remove.duplicates(layer)
layer <- layer[!is.na(layer$field),]

g = gstat(id = field, formula = field~1, data = layer)
vg = variogram(g)

if(Estimate_range_and_psill_initial_values_from_sample_variogram){range=NA}
if(Estimate_range_and_psill_initial_values_from_sample_variogram){psill=NA}

vgm = vgm(nugget=nugget, psill=psill, range=range, model=model2)
vgm = fit.variogram(vg, vgm)
>vgm
plot(vg, vgm, plot.numbers = TRUE)
if(Local_kriging==FALSE){prediction = krige(field~1, layer, newdata = mask, vgm)}
if(Local_kriging==TRUE){prediction = krige(field~1, layer, newdata = mask, vgm, nmax=Number_of_nearest_observations)}
>if(Show_Sum_of_Square_Errors==TRUE){paste("SSE:", attr(vgm, "SSErr"))}
#>if(!is.projected(layer)){warning(paste0("'layer' isn't projected.\n", "Resolution was not used. Interpolation was done over 5000 cells"))}
#>if(is.projected(layer) & Resolution == 0){warning("Resolution was set to 0. Final resolution estimated from data")}

kriging_prediction = raster(prediction)
kriging_variance = raster(prediction["var1.var"])
