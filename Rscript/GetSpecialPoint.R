specialPoint = array(dim=c(n,3))
count = 0
for ( i in 1:n ){
  if ((ut[i]!=0)&&(rt[i]!=0)) {
    count = count+1
    specialPoint[count,1] = i;
    specialPoint[count,2] = rt[i];
    specialPoint[count,3] = ut[i];
    text(rt[i],ut[i],i)
  }
}