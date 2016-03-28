n = 2497
CmatrixNum = 618
WindowSize = 3
k = 1000;
max = 0;
pos = NULL;
pos2 = NULL;
sortedEigenArray = array(0,dim = c(n,CmatrixNum))
for ( i in 1:CmatrixNum ){
  currentArray = eigenArray[,i]
  sortedArray = sort(currentArray,decreasing = TRUE)
  count = 0;
  nonzero = NULL;
  for ( j in 1:n ){
    if ( sortedArray[j]>0 ) {
      count=count+1
      nonzero = c(nonzero,sortedArray[j])
    }
    else break;
  }
  pos = c(pos,count)
  pos2 = c(pos2,count/(1+k*var(nonzero)))
}

