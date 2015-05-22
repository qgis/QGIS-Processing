##Basic statistics=group
##Layer0=raster
##xA=number 7
##yA=number 85
##xB=number 17
##yB=number 90
##direction=number 4
##hauteur= number 800
##Output=output raster
n0_distance =0
n0_somme_cout= 0
PP=0
estimate= function(x0,y0,x1,y1){
d = sqrt((x0-x1)^2+(y0-y1)^2)
}

nextMove= function(dirs,d,m0_distance){
if (dirs == 8 | round(d/2)!=d/2){
m0_distance = m0_distance + 14
}else{
m0_distance = m0_distance + 10
}
}

node=function(noeud,x_position,y_position,distance,somme_cout){
noeud_x_posisiton=x_position
noeud_y_posisiton=y_position
noeud_distance=distance
noeud_somme_cout=somme_cout
result<-c(noeud_x_posisiton,noeud_y_posisiton,noeud_distance,noeud_somme_cout)
return(result)
}
a_star=function (the_map, n, m, dirs, dx, dy, xA, yA, xB, yB){
closed_nodes_map <- c()
open_nodes_map  <- c()
dir_map  <- c()
for( i in (1:m)){ # create 2d arrays
closed_nodes_map=array(0,c(m,n))
open_nodes_map=array(0,c(m,n))
dir_map=array(0,c(m,n))}
priority_file = list(0,0)
index= 1
n0 = node(n0,xA, yA,0,0)
n0_somme_cout=estimate(n0[[1]],n0[[2]],xB,yB)+n0[[3]]
n0[[4]]<-n0_somme_cout
priority_file[index]<-list(n0)
open_nodes_map[yA,xA] <- n0_somme_cout
path <-c()
n1 <- priority_file[index]
x_position<-unlist(n1)[1]
y_position<-unlist(n1)[2]
n0_distance<-unlist(n1)[3]
noeud_somme_cout<-unlist(n1)[4]
open_nodes_map[y_position,x_position] <- 0
closed_nodes_map[y_position,x_position] <- 1
memoire_dir<-c()
memoire_point<-c()
while (length(priority_file[index]) > 0 & PP<2000000000& length(path)==0 ){
PP=PP+1
cout_precedent=100000000000000000
if (x_position== xB & y_position == yB){
while (x_position != xA | y_position != yA ){
j = dir_map[y_position,x_position]
c = (j + dirs / 2) %% dirs
path<-c(path,c)
x_position = x_position+ dx[j+1]
y_position =y_position+ dy[j+1]
}
}
for (t in (0:(length(dx)-1))){
xdx = x_position + dx[t+1]
ydy = y_position + dy[t+1]
if (xdx > 0 & xdx <=(n) & ydy > 0 & ydy <= (m)){
if(the_map[ydy,xdx] != 1 & closed_nodes_map[ydy,xdx]!= 1& the_map[ydy,xdx] != 10){
m0_x_position<-xdx
m0_y_position<-ydy
m0_distance<-nextMove(dirs, t,n0_distance)
m0_somme_cout<-estimate(m0_x_position,m0_y_position,xB,yB)+m0_distance
m0<-c(m0_x_position,m0_y_position,m0_distance,m0_somme_cout)
if (open_nodes_map[ydy,xdx] == 0){
open_nodes_map[ydy,xdx] <- m0_somme_cout
if(cout_precedent>=m0_somme_cout){
priority_file[index]<-list(m0)
indice<-t
cout_precedent=m0_somme_cout
}
}
if (open_nodes_map[ydy,xdx] > m0_somme_cout){
open_nodes_map[ydy,xdx]<-m0_somme_cout
indice<-t
priority_file[index]<-list(m0)
}
}
}
}

n1 <- priority_file[index]
if (x_position==unlist(n1)[1] & y_position==unlist(n1)[2]){
the_map[y_position,x_position]=10
n0_distance<-0
L=length(memoire_dir)
Y=1
while (memoire_dir[L]==memoire_dir[L-1] & Y==1){
if ((L-1)<length(memoire_dir)-1){
L=L-1
} else {
Y=2
}
}
p<-dim(memoire_point)[1]
x_position<-memoire_point[p-L-1,1]
y_position<-memoire_point[p-L-1,1]
} else {
dir_map[unlist(n1)[2],unlist(n1)[1]] = (indice + dirs / 2) %% dirs
memoire_dir<-c(memoire_dir,(indice + dirs / 2) %% dirs)
memoire_point<-rbind(memoire_point,cbind(unlist(n1)[1],unlist(n1)[2]))
open_nodes_map[y_position,x_position] <- 0
closed_nodes_map[y_position,x_position] <- 1
x_position<-unlist(n1)[1]
y_position<-unlist(n1)[2]
n0_distance<-unlist(n1)[3]
}
}
result<-c(path)
return (result)
}


library(gdistance)
N=100
M=101
the_map<-c()
for( s in (1:M)){
the_map<-array(0,c(M,N))
}
Layer = readGDAL("C:/Users/Jeandenans Laura/Documents/R/decoupe.tif")
P<-Layer@data
for (i in (1:length(P[,1]))){
if (P[i,1]>hauteur){
the_map[i]=1
} else{the_map[i]=0}
}
dirs = directions
if (dirs == 4){
dx = c(1, 0, -1, 0)
dy = c(0, 1, 0, -1)
}
if (dirs == 8){
dx<- c(1, 1, 0, -1, -1, -1, 0, 1)
dy<-c(0, 1, 1, 1, 0, -1, -1, -1)
}


route<- a_star(the_map, N, M, dirs, dx, dy, xA, yA, xB, yB)

if (length(route) > 0){
x = xA
y = yA
the_map[y,x] = 2

for (i in ((length(route)-1):0)){
j <- route[i+1]
x = x+dx[j+1]
y = y+dy[j+1]
the_map[y,x] = 3
}
}
the_map[yA,xA] = 2
the_map[yB,xB] = 4
X<-raster(the_map,template=Layer)
proj4string(Layer0)->crs
proj4string(X)<-crs
Output=X
