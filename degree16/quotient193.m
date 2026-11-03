SetQuitOnError(true);SetColumns(0);tt:=Cputime();R<x>:=PolynomialRing(Rationals());p:=193;ind:=12;h:=Integers()!((GF(p)!PrimitiveRoot(p))^ind);
S:=CuspidalSubspace(ModularSymbolsH(p,[h],2,1));g:=Dimension(S);T:=Transpose(DualHeckeOperator(S,2));e:=WindingElementProjection(S);rows:=[];v:=e;
for k in[0..g-1]do Append(~rows,Eltseq(v));v:=v*T;end for;W:=Matrix(Rationals(),rows);r:=Rank(W);V:=VectorSpace(Rationals(),g);WS:=sub<V|Rows(W)>;VV,quo:=quo<V|WS>;
TT:=Matrix(Rationals(),[Eltseq(quo((v@@quo)*T)):v in Basis(VV)]);pol:=MinimalPolynomial(TT);assert Rank(VerticalJoin(W,Evaluate(pol,T)))eq r;
printf "S16_QUOTIENT193_FINITE genus=%o winding_rank=%o polynomial=%o elapsed=%o\n",g,r,pol,Cputime(tt);
PrintFile("work/degree16/finite193.m",Sprintf("Finite193Polynomial:=PolynomialRing(Rationals())!%o;",Eltseq(pol)):Overwrite:=true);
print "S16_QUOTIENT193_FINITE_COMPLETE";quit;
