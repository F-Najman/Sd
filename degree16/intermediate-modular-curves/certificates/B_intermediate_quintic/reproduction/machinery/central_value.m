// Exact endpoint central-value test. A zero value is NOT a rank determination.
N := StringToInteger(N);
J := JOne(N);
zero := IsZeroAt(LSeries(J),1);
printf "RESULT N=%o dimension=%o central_zero=%o\n",N,Dimension(J),zero;
print "SUCCESS central-value test";
quit;
