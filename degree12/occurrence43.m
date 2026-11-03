SetQuitOnError(true);SetColumns(0);R<t>:=PolynomialRing(Rationals());
f:=t^12-t^11-5*t^10+6*t^9+9*t^8-16*t^7-3*t^6+19*t^5-3*t^4-12*t^3+t^2+4*t+1;
g:=(35*t^11-65*t^10-107*t^9+314*t^8-34*t^7-580*t^6+601*t^5+156*t^4-552*t^3+219*t^2+136*t-81)/43;
assert IsIrreducible(f);K<a>:=NumberField(f);x:=a;y:=Evaluate(g,a);r:=(x^2*y-x*y+y-1)/(x^2*y-x);s:=(x*y-y+1)/(x*y);b:=r*s*(r-1);c:=s*(r-1);E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and 43*P eq E!0;assert Degree(MinimalPolynomial(jInvariant(E)))eq 4;
print "S12_OCCURRENCE_43_VERIFIED exact_field_degree12=true j_degree4=true exact_point_order43=true";quit;
