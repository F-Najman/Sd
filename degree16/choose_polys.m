SetQuitOnError(true);SetColumns(0);R<x>:=PolynomialRing(Rationals());
for p in[43,193]do
 S:=CuspidalSubspace(ModularSymbols(p,2,1));g:=Dimension(S);T:=Transpose(DualHeckeOperator(S,2));e:=WindingElementProjection(S);rows:=[];v:=e;
 for k in[0..g-1]do Append(~rows,Eltseq(v));v:=v*T;end for;W:=Matrix(Rationals(),rows);r:=Rank(W);pol:=CharacteristicPolynomial(T);
 for f in Factorization(pol)do for k in[1..f[2]]do z:=ExactQuotient(pol,f[1]);if Rank(VerticalJoin(W,Evaluate(z,T)))eq r then pol:=z;else break;end if;end for;end for;
 assert Rank(VerticalJoin(W,Evaluate(pol,T)))eq r;
 printf "S16_FINITE_POLYNOMIAL N=%o genus=%o winding_rank=%o polynomial=%o\n",p,g,r,pol;
 if p eq 43 then assert pol eq x+2;end if;
end for;print "S16_SMALL_FINITE_POLYS_COMPLETE";quit;
