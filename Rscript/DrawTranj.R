n = 2497
CmatrixNum = 618
WindowSize = 3

getPointTranj<-function(id){
  point = array(dim = c(CmatrixNum,2))
  for ( i in (WindowSize+1):CmatrixNum ){
    ut = eigenArray[id,i]
    rt = 0;
    for (j in (i-WindowSize):(i-1)){
      rt = rt + eigenArray[id,j]
    }
    rt = rt / WindowSize
    point[i,1] = rt
    point[i,2] = ut
  }
  return(point)
}

getTimeTranj<-function(time){
  point = array(dim = c(n,4))
  ut = eigenArray[,time]
  rt = 0;
  for (j in (time-WindowSize):(time-1)){
    rt = rt + eigenArray[,j]
  }
  rt = rt / WindowSize
  ut = ut/norm(as.matrix(ut),"f")
  rt = rt/norm(as.matrix(rt),"f")
  for (i in 1:n){
    point[i,3] = rt[i]
    point[i,4] = ut[i]
  }
  
  time = time-1
  ut = eigenArray[,time]
  rt = 0;
  for (j in (time-WindowSize):(time-1)){
    rt = rt + eigenArray[,j]
  }
  rt = rt / WindowSize
  ut = ut/norm(as.matrix(ut),"f")
  rt = rt/norm(as.matrix(rt),"f")
  for (i in 1:n){
    point[i,1] = rt[i]
    point[i,2] = ut[i]
  }
  return(point)
}

point = getPointTranj(127)
points = getTimeTranj(471)

plot(x=points[,1],y=points[,2],xlim=c(0,0.3),ylim = c(0,0.3))
for (i in 1:n ){
  x0 = points[i,1]
  y0 = points[i,2]
  x1 = points[i,3]
  y1 = points[i,4]
  points(x0,y0,col="red")
  points(x1,y1,col="blue")
  if ( x0 == 0 && y0 == 0 && x1 ==0 && y1 ==0 ) next;
  arrows(x0,y0,x1,y1,angle=30,code=2)
}

utup = NULL
utdown = NULL
for (index in (WindowSize+2):CmatrixNum){
  points = getTimeTranj(index)
  countup = 0;
  countdown = 0;
  for (i in 1:n ){
    x0 = points[i,1]
    y0 = points[i,2]
    x1 = points[i,3]
    y1 = points[i,4]
    if ( x0 == 0 && y0 == 0 && x1 == 0 && y1 == 0 ) next;
    if ( x0 < x1 ) countup = countup + 1
    if ( x0 > x1 ) countdown = countdown + 1
  }
  utup = c(utup,countup)
  utdown = c(utdown,countdown)
}
peak = NULL
for (index in 1:(CmatrixNum-WindowSize-1)){
  countup = utup[index];
  countdown = utdown[index+1];
  peak = c(peak,countup+countdown);
}