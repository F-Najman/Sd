SetQuitOnError(true);SetColumns(0);R<t>:=PolynomialRing(Rationals());assert IsIrreducible(t^19-2);K<a>:=NumberField(t^19-2);assert Degree(K)eq 19;
for dat in[<2,[0,0,0,-1,0]>,<3,[0,0,1,0,0]>,<5,[0,-1,-1,0,0]>,<7,[-1,-4,-4,0,0]>]do
 p,aa:=Explode(dat);E:=EllipticCurve([K!b:b in aa]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and p*P eq E!0;printf "S19_SMALL_OCCURRENCE_VERIFIED prime=%o exact_field_degree=19\n",p;
end for;
for p in[11,13,17,19]do g:=ExactQuotient((p-5)*(p-7),24);assert 18 gt 2*g-2;end for;
print "S19_SMALL_OCCURRENCES_AND_RIEMANN_ROCH_BOUND_VERIFIED";quit;
