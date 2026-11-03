SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
for N in[23,29,31]do
 X:=MDX1(N,Rationals());AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));x:=am(X`_coordinates_xy[1]);y:=am(X`_coordinates_xy[2]);found:=false;
 fs:=[x,y,x/y,y/x,1/(x*y),x-y,x-y+1,x*y-1];
 for i in[-4..4]do for j in[-4..4]do if i ne 0 or j ne 0 then Append(~fs,x^i*y^j);end if;end for;end for;
 for h in fs do
  if Degree(h)ne 12 then continue;end if;
  printf "S12_DEGREE12_FUNCTION N=%o h=%o\n",N,h;
  for c in[2..20]do
   zs:=Zeros(h-c);if #zs ne 1 or Degree(zs[1])ne 12 then continue;end if;pl:=zs[1];K,ev:=ResidueClassField(pl);E:=EllipticCurve([Evaluate(am(a),pl):a in X`_E]);P:=E![0,0];if Discriminant(E)eq 0 then continue;end if;assert P ne E!0 and N*P eq E!0;
   printf "S12_OCCURRENCE_VERIFIED prime=%o field_degree=%o specialization=%o field_polynomial=%o aInvariants=%o\n",N,Degree(K),c,DefiningPolynomial(K),aInvariants(E);found:=true;break;
  end for;if found then break;end if;
 end for;
 printf "S12_SMALL_SEARCH N=%o found=%o\n",N,found;assert found;
end for;print "S12_OCCURRENCES_SMALL_COMPLETE";quit;
