SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
for N in[23,29,31]do
 X:=MDX1(N,Rationals());AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));x:=am(X`_coordinates_xy[1]);y:=am(X`_coordinates_xy[2]);found:=false;
 fs:=[x,y,1-x,1-y,x-y,1-x*y,x-y+1];ds:=[Divisor(f):f in fs];ps:=Setseq(&join[Seqset(Support(d)):d in ds]);vs:=[[Valuation(f,p):p in ps]:f in fs];degs:=[Degree(p):p in ps];
 for ex in CartesianPower([-1,0,1],#fs)do
  orders:=[&+[ex[i]*vs[i][j]:i in[1..#fs]]:j in[1..#ps]];
  if &+[Max(0,-orders[j])*degs[j]:j in[1..#ps]]ne 12 then continue;end if;
  h:=&*[AF|fs[i]^ex[i]:i in[1..#fs]];assert Degree(h)eq 12;
  printf "S12_DEGREE12_FUNCTION N=%o exponents=%o\n",N,ex;
  for c in[2..30]do
   zs:=Zeros(h-c);if #zs ne 1 or Degree(zs[1])ne 12 then continue;end if;pl:=zs[1];K,ev:=ResidueClassField(pl);aa:=[Evaluate(am(a),pl):a in X`_E];if Discriminant(EllipticCurve(aa))eq 0 then continue;end if;E:=EllipticCurve(aa);P:=E![0,0];assert P ne E!0 and N*P eq E!0;
   printf "S12_OCCURRENCE_VERIFIED prime=%o field_degree=%o specialization=%o exponents=%o field_polynomial=%o aInvariants=%o\n",N,Degree(K),c,ex,DefiningPolynomial(K),aa;found:=true;break;
  end for;if found then break;end if;
 end for;
 printf "S12_UNIT_SEARCH N=%o found=%o\n",N,found;assert found;
end for;print "S12_OCCURRENCES_UNITS_COMPLETE";quit;
