SetQuitOnError(true);SetColumns(0);PF<t>:=PolynomialRing(Rationals());
f:=((1)*t^0+(5)*t^1+(0)*t^2+(-23)*t^3+(-4)*t^4+(56)*t^5+(1)*t^6+(-80)*t^7+(24)*t^8+(61)*t^9+(-43)*t^10+(-11)*t^11+(21)*t^12+(-8)*t^13+(1)*t^14);
g:=((-36881/2813)*t^0+(-127126/2813)*t^1+(215600/2813)*t^2+(535187/2813)*t^3+(-739371/2813)*t^4+(-974129/2813)*t^5+(1568080/2813)*t^6+(560225/2813)*t^7+(-1851704/2813)*t^8+(625052/2813)*t^9+(662254/2813)*t^10+(-637367/2813)*t^11+(208418/2813)*t^12+(-24162/2813)*t^13);
assert IsIrreducible(f);K<a>:=NumberField(f);x:=a;y:=Evaluate(g,a);r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);b:=r*ss*(r-1);c:=ss*(r-1);E:=EllipticCurve([1-c,-b,-b,K!0,K!0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and 41*P eq E!0;print "S15_KNOWN41_CHARACTERISTIC_ZERO_LIFT_VERIFIED";quit;
