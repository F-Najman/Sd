SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);SetSeed(20261028);tt:=Cputime();which:=StringToInteger(Which);
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
X:=MDX1(43,GF(2));AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));assert Genus(AF)eq 57;
rats:=Places(AF,1);assert #rats eq 21;for d in[2..6]do assert #Places(AF,d)eq 0;end for;
C:=&+[Divisor(p):p in rats];P:=Divisor(rats[1]);
if which le 6 then
 ps:=Places(AF,7);assert #ps eq 6;D:=C+P+Divisor(ps[which]);
else
 ps:=Places(AF,8);assert #ps eq 42;E:=EllipticCurve([am(a):a in X`_E]);jj:=jInvariant(E);reps:=[];keys:={};sizes:=AssociativeArray();
 for pl in ps do
  k:=MinimalPolynomial(Evaluate(jj,pl),GF(2));assert Degree(k)eq 8;
  if k notin keys then Include(~keys,k);Append(~reps,pl);sizes[k]:=0;end if;sizes[k]+:=1;
 end for;assert #reps eq 2 and &and[sizes[k]eq 21:k in keys];D:=C+Divisor(reps[which-6]);
end if;
V,ev:=RiemannRochSpace(D);assert Dimension(V)eq 1 and Degree(ev(V.1))eq 0;
printf "AUDIT_GON43_NONRATIONAL_COMPLETE case=%o RR_dimension=1 no_nonconstant_function=true elapsed=%o\n",which,Cputime(tt);quit;
