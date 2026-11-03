SetQuitOnError(true);SetColumns(0);R<x>:=PolynomialRing(Rationals());load "work/degree16/finite193.m";Records:=[**];
for dat in[<43,1,x+2>,<193,12,R!Finite193Polynomial>]do
 p,ind,pol:=Explode(dat);h:=Integers()!((GF(p)!PrimitiveRoot(p))^ind);S:=CuspidalSubspace(ModularSymbolsH(p,[h],2,1));g:=Dimension(S);T:=Transpose(DualHeckeOperator(S,2));A:=AmbientSpace(S);phi:=RationalMapping(S);PM:=Matrix(Rationals(),[Eltseq(phi(b)):b in Basis(A)]);assert HeckeOperator(A,2)*PM eq PM*T;
 e:=WindingElementProjection(S);rows:=[];v:=e;for k in[0..g-1]do Append(~rows,Eltseq(v));v:=v*T;end for;W:=Matrix(Rationals(),rows);U:=Evaluate(pol,T);assert Rank(VerticalJoin(W,U))eq Rank(W);
 pair:=func<M|[<Numerator(z),Denominator(z)>:z in Eltseq(M)]>;Append(~Records,<p,ind,g,Rank(W),pair(W),pair(U)>);printf "S16_NEW_FINITE_IMAGE p=%o index=%o genus=%o winding_rank=%o\n",p,ind,g,Rank(W);
end for;
PrintFile("work/degree16/new_finite_data.m",Sprintf("NewFiniteData:=%o;",Records):Overwrite:=true);print "S16_NEW_FINITE_IMAGE_CHECKS_COMPLETE";quit;
