SetQuitOnError(true);SetColumns(0);tt:=Cputime();J:=JH(43,[2]);fs:=Decomposition(J);assert [Dimension(A):A in fs]eq[1,2,2,4];
lr:=[LRatio(A,1):A in fs];assert lr eq[Rationals()!0,Rationals()!2/7,Rationals()!3/16,Rationals()!1/361];
A:=fs[1];assert Conductor(A)eq 43;B,pi:=J/A;assert Dimension(B)eq 8;ns:=[];
for q in[3,5,23]do n:=Integers()!Evaluate(FrobeniusPolynomial(B,q),1);Append(~ns,n);printf "S16_TORSION43_UPPER q=%o count=%o\n",q,n;end for;
assert GCD(ns)eq 532 and Valuation(GCD(ns),2)eq 2;
E:=EllipticCurve([Rationals()|0,1,1,0,0]);T:=TorsionSubgroup(E);assert #T eq 1;iso,md:=IsogenousCurves(E);assert #iso eq 1 and md eq 1;
print "S16_TORSION43_Q_TWO_BOUND=4 COMPLETE",Cputime(tt);quit;
