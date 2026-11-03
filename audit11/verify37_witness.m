SetColumns(0);SetQuitOnError(true);R<t>:=PolynomialRing(Rationals());
f:=t^10-5*t^8+3*t^7+10*t^6-8*t^5-7*t^4+9*t^3-3*t+1;
g:=2*t^9+t^8-10*t^7+t^6+23*t^5-6*t^4-22*t^3+11*t^2+9*t-5;
assert IsIrreducible(f);K<a>:=NumberField(f);x:=a;y:=Evaluate(g,a);
r:=(x^2*y-x*y+y-1)/(x^2*y-x);s:=(x*y-y+1)/(x*y);b:=r*s*(r-1);c:=s*(r-1);
E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and 37*P eq E!0;
printf "DECIC37_WITNESS_VERIFIED degree=%o j_degree=%o field_polynomial=%o y_polynomial=%o point_order=37\n",Degree(K),Degree(MinimalPolynomial(jInvariant(E))),f,g;
print "DECIC37_OCCURRENCE_COMPLETE";quit;
