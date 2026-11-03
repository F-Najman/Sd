SetQuitOnError(true);SetColumns(0);SetMemoryLimit(8*10^9);
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");

function VerifyDegree22(E,P,n)
 K:=BaseRing(E);assert Degree(K)eq 11;R<v>:=PolynomialRing(K);assert IsIrreducible(v^2-2);L<a>:=NumberField(v^2-2);assert AbsoluteDegree(L)eq 22;EE:=ChangeRing(E,L);PP:=EE![L!P[1],L!P[2]];assert Discriminant(EE)ne 0 and PP ne EE!0 and n*PP eq EE!0;printf "S22_EXTENSION_OCCURRENCE_VERIFIED prime=%o field_degree=22\n",n;return true;
end function;
for dat in[<11,-6,-5>,<13,-6,-1>,<19,-2,1>,<23,-1,1>,<29,-1,0>]do
 N,i,j:=Explode(dat);X:=MDX1(N,Rationals());AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));
 x:=am(X`_coordinates_xy[1]);y:=am(X`_coordinates_xy[2]);h:=x^i*y^j;assert Degree(h)eq 11;
 zs:=Zeros(h-2);assert #zs eq 1 and Degree(zs[1])eq 11;p:=zs[1];K,ev:=ResidueClassField(p);
 E:=EllipticCurve([Evaluate(am(a),p):a in X`_E]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and N*P eq E!0;assert VerifyDegree22(E,P,N);
 printf "S11_OCCURRENCE_VERIFIED prime=%o field_degree=%o function_exponents=%o specialization=2 field_polynomial=%o aInvariants=%o\n",N,Degree(K),[i,j],DefiningPolynomial(K),aInvariants(E);
end for;
N:=17;X:=MDX1(N,Rationals());AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));
EE:=EllipticCurve([am(a):a in X`_E]);cs:=[p:p in Poles(jInvariant(EE))|Degree(p)eq 1];assert #cs gt 0;
V,mp:=RiemannRochSpace(11*Divisor(cs[1]));hs:=[mp(v):v in Basis(V)|Degree(mp(v))eq 11];assert #hs gt 0;found:=false;
for h in hs do for c in[2..15]do
 zs:=Zeros(h-c);if #zs ne 1 or Degree(zs[1])ne 11 then continue;end if;p:=zs[1];K,ev:=ResidueClassField(p);
 E:=EllipticCurve([Evaluate(am(a),p):a in X`_E]);P:=E![0,0];if Discriminant(E)eq 0 then continue;end if;
 assert P ne E!0 and 17*P eq E!0;assert VerifyDegree22(E,P,17);
 printf "S11_OCCURRENCE_VERIFIED prime=17 field_degree=%o field_polynomial=%o aInvariants=%o\n",Degree(K),DefiningPolynomial(K),aInvariants(E);found:=true;break;
end for;if found then break;end if;end for;assert found;
R<t>:=PolynomialRing(Rationals());f:=t^11-t^10+2*t^8+t^6-7*t^5+t^4+4*t^3-t^2+2*t-1;
yp:=(1036*t^10-31*t^9-503*t^8+2108*t^7+1676*t^6+2654*t^5-5898*t^4-4556*t^3+2817*t^2+2307*t+3370)/2033;
assert IsIrreducible(f);K<a>:=NumberField(f);x:=a;y:=Evaluate(yp,a);
r:=(x^2*y-x*y+y-1)/(x^2*y-x);s:=(x*y-y+1)/(x*y);b:=r*s*(r-1);c:=s*(r-1);
E:=EllipticCurve([1-c,-b,-b,0,0]);P:=E![0,0];assert Discriminant(E)ne 0 and P ne E!0 and 31*P eq E!0;assert VerifyDegree22(E,P,31);
print "S11_OCCURRENCE_VERIFIED prime=31 field_degree=11";
print "S22_ALL_DEGREE11_TO22_EXTENSIONS_COMPLETE";quit;
