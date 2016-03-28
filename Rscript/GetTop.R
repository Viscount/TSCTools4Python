n = 2497
CmatrixNum = 618
WindowSize = 3
num = 1
zArraywithPos = array(0,dim=c(CmatrixNum,2))
for ( i in 1:CmatrixNum){
  zArraywithPos[i,]=c(i,zArray[i])
}
zArraywithPos = zArraywithPos[order(zArraywithPos[,2]),]

start = 3;
utTotal = NULL
rtTotal = NULL
for ( i in 1:num ){
  pos = zArraywithPos[start+i,1]
  ut = eigenArray[,pos]
  rt = 0;
  for (j in (pos-WindowSize):(pos-1)){
    rt = rt + eigenArray[,j]
  }
  rt = rt / WindowSize
  ut = ut/norm(as.matrix(ut),"f")
  rt = rt/norm(as.matrix(rt),"f")
  utTotal = c(utTotal,ut)
  rtTotal = c(rtTotal,rt)
}
plot(x=rtTotal,y=utTotal,pch=16,cex=0.5)
