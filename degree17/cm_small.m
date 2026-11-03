SetQuitOnError(true);SetColumns(0);
Data:=[<137,1728,4,3,0>,<113,1728,4,3,0>];
for dat in Data do
 p,j,w,q,tr:=Explode(dat);E:=EllipticCurveFromjInvariant(Rationals()!j);assert Valuation(Discriminant(MinimalModel(E)),q)eq 0;
 EF:=EllipticCurve([GF(q)!a:a in aInvariants(MinimalModel(E))]);assert q+1-#EF eq tr;
 F:=Matrix(GF(p),2,2,[0,1,-q,tr]);for k in[1..17]do assert Determinant(F^(w*k)-1)ne 0;end for;
 printf "S17_CM_EXCLUDED p=%o j=%o q=%o through_degree=17\n",p,j,q;
end for;print "S17_CM_FROBENIUS_COMPLETE";quit;
