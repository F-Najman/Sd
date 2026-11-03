SetQuitOnError(true);SetColumns(0);R<x>:=PolynomialRing(Rationals());S:=CuspidalSubspace(ModularSymbols(101,2,1));g:=Dimension(S);e:=WindingElementProjection(S);T2:=Transpose(DualHeckeOperator(S,2));rows:=[];v:=e;
for j in[0..g-1]do Append(~rows,Eltseq(v));v:=v*T2;end for;
W:=Matrix(Rationals(),rows);V:=VectorSpace(Rationals(),g);U:=sub<V|Rows(W)>;Q,pi:=quo<V|U>;assert Dimension(Q)gt 0;Records:=[**];
for n in[2,3,5,7]do
 T:=Transpose(DualHeckeOperator(S,n));assert &and[(V!u*T)in U:u in Basis(U)];B:=Matrix(Rationals(),[Eltseq(pi((b@@pi)*T)):b in Basis(Q)]);pol:=MinimalPolynomial(B);A:=Evaluate(pol,T);assert Rank(VerticalJoin(W,A))eq Rank(W);
 Append(~Records,<n,[<Numerator(a),Denominator(a)>:a in Eltseq(pol)],g,Nrows(W),[<Numerator(a),Denominator(a)>:a in Eltseq(W)],[<Numerator(a),Denominator(a)>:a in Eltseq(A)]>);
 PrintFile("work/degree20/finite_FI_polynomials.m",Sprintf("FiniteFIPolynomials[<101,%o>]:=%o;",n,Sprintf("(%o)",Coefficient(pol,0))cat &cat[Sprintf("+(%o)*zz^%o",Coefficient(pol,j),j):j in[1..Degree(pol)]]));printf "S20_FINITE101_POLYNOMIAL n=%o pol=%o winding_rank=%o quotient_dimension=%o verified=true\n",n,pol,Rank(W),Dimension(Q);
end for;
PrintFile("work/degree20/finite101_data.m",Sprintf("Finite101Data:=%o;",Records):Overwrite:=true);print "S20_FINITE101_CERTIFICATES_COMPLETE";quit;
