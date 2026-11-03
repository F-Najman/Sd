SetColumns(0);SetQuitOnError(true);SetMemoryLimit(4*10^9);
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
R<t>:=PolynomialRing(Rationals());
function FromXY(xx,yy)
 r:=(xx^2*yy-xx*yy+yy-1)/(xx^2*yy-xx);
 s:=(xx*yy-yy+1)/(xx*yy);b:=r*s*(r-1);c:=s*(r-1);
 return EllipticCurve([1-c,-b,-b,0,0]);
end function;
for N in [29,31] do
 if N eq 29 then
  f:=t^10-3*t^9+8*t^7-5*t^6-6*t^5+5*t^4-2*t^2+1;
  yp:=(2*t^9+t^8-11*t^7-8*t^6+49*t^5-77*t^3+35*t^2+46*t-13)/29;
 else
  f:=t^10-4*t^9+3*t^8+6*t^7-2*t^6-8*t^5-8*t^4+11*t^3+6*t^2-5*t+1;
  yp:=(109*t^9-266*t^8-207*t^7+801*t^6+606*t^5-304*t^4-1470*t^3-410*t^2+1000*t+71)/215;
 end if;
 assert IsIrreducible(f);K<a>:=NumberField(f);E:=FromXY(a,Evaluate(yp,a));P:=E![0,0];
 assert Discriminant(E) ne 0 and N*P eq E!0 and P ne E!0;
 if N eq 31 then assert jInvariant(E) eq 0;end if;
 printf "DECIC_WITNESS N=%o field_polynomial=%o y_polynomial=%o j_degree=%o exact_order_verified=true\n",N,f,yp,Degree(MinimalPolynomial(jInvariant(E)));
end for;
X:=MDX1(23,Rationals());F:=FunctionField(Curve(X));xx:=X`_coordinates_xy[1];yy:=X`_coordinates_xy[2];
found:=false;
for i in [-4..4] do
 for j in [-4..4] do
  if i eq 0 and j eq 0 then continue;end if;
  f:=xx^i*yy^j;
  if Degree(f) ne 10 then continue;end if;
  printf "DECIC_23_FUNCTION exponents=%o degree=%o\n",[i,j],Degree(f);
  for c in [2..20] do
   zz:=Zeros(f-c);
   if #zz ne 1 or Degree(zz[1]) ne 10 then continue;end if;
   L,ev:=ResidueClassField(zz[1]);E:=EllipticCurve([Evaluate(a,zz[1]):a in X`_E]);P:=E![0,0];
   if Discriminant(E) eq 0 then continue;end if;
   assert 23*P eq E!0 and P ne E!0;
   printf "DECIC_WITNESS N=23 function_exponents=%o specialization=%o field_degree=%o field_polynomial=%o aInvariants=%o exact_order_verified=true\n",[i,j],c,Degree(L),DefiningPolynomial(L),aInvariants(E);
   found:=true;break;
  end for;
  if found then break;end if;
 end for;
 if found then break;end if;
end for;
assert found;print "DECIC_WITNESSES_COMPLETE";quit;
