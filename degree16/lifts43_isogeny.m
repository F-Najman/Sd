SetQuitOnError(true);SetColumns(0);tt:=Cputime();AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
R<t>:=PolynomialRing(Rationals());
f:=((-1)*t^0+(-4)*t^1+(1)*t^2+(13)*t^3+(-6)*t^4+(-12)*t^5+(33)*t^6+(-33)*t^7+(-59)*t^8+(99)*t^9+(28)*t^10+(-85)*t^11+(14)*t^12+(21)*t^13+(-9)*t^14+(1)*t^15);assert IsIrreducible(f);K<z>:=NumberField(f);assert Degree(K)eq 15;x:=z;y:=Evaluate(((2692776/356723)*t^0+(4252675/356723)*t^1+(-12279174/356723)*t^2+(-2664228/356723)*t^3+(24925492/356723)*t^4+(-35722009/356723)*t^5+(4631869/356723)*t^6+(83025032/356723)*t^7+(-75374686/356723)*t^8+(-55548319/356723)*t^9+(80258022/356723)*t^10+(-4006085/356723)*t^11+(-22219204/356723)*t^12+(8361953/356723)*t^13+(-882583/356723)*t^14),z)/Evaluate(((1)*t^0),z);r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);b:=r*ss*(r-1);c:=ss*(r-1);E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and 43*P eq E!0;
PF:=PolynomialRing(GF(2));FF<a>:=GF(2,15);roots:=Roots(PolynomialRing(FF)![GF(2)!c:c in Coefficients(f)]);assert #roots eq 15;aa:=roots[1][1];
function Red(z) return Evaluate(PolynomialRing(FF)![FF!GF(2)!c:c in Eltseq(K!z)],aa);end function;
function JR(EE)
 j:=Red(jInvariant(EE));return Eltseq(MinimalPolynomial(j,GF(2)));
end function;
printf "S16_KNOWN43_BASE jpoly=%o elapsed=%o\n",JR(E),Cputime(tt);
for q in[3,5,7]do
 pol:=DivisionPolynomial(E,q);fac:=Factorization(pol);print "S16_KNOWN43_DIVISION",q,[Degree(a[1]):a in fac];
 if q ne 3 then continue;end if;
 for h in fac do
  if Degree(h[1])ne 1 then continue;end if;
  EE,phi:=IsogenyFromKernel(E,h[1]);PP:=phi(P);assert PP ne EE!0 and 43*PP eq EE!0;
  printf "S16_KNOWN43_ISOGENOUS q=%o jpoly=%o elapsed=%o\n",q,JR(EE),Cputime(tt);
 end for;
end for;print "S16_KNOWN43_ISOGENOUS_LIFTS_COMPLETE";quit;
