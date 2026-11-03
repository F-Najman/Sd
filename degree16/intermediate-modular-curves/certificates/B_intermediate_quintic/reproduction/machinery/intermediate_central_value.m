// Construct the actual intermediate Jacobian from its full subgroup.
// Never use the subgroup index alone: distinct subgroups can share an index.
N := StringToInteger(N);
g := StringToInteger(g);
delta := [StringToInteger(s):s in Split(delta,",")];
J := JH(N,delta);
assert Dimension(J) eq g;
zero := IsZeroAt(LSeries(J),1);
printf "RESULT N=%o delta=%o dimension=%o central_zero=%o\n",N,delta,Dimension(J),zero;
print "SUCCESS intermediate central-value test";
quit;
