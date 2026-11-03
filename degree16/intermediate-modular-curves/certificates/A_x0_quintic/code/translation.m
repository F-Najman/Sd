// Coordinate action of z -> z+1/n in the canonical LLL q-expansion basis.
function CanonicalQExpansionMatrix(N)
 M:=CuspidalSubspace(ModularForms(N,2)); prec:=Max(200,Ceiling(N*4*2/12));
 bs:=qExpansionBasis(M,prec); rows:=[];
 for b in bs do
  r:=[Coefficient(b,i):i in [1..prec-1]];
  den:=LCM([Denominator(a):a in r]); z:=[Integers()!(den*a):a in r]; d:=GCD(z);
  Append(~rows,[a div d:a in z]);
 end for;
 return LLL(Matrix(Integers(),rows));
end function;
function CanonicalTranslationMatrix(N,n)
 L:=CanonicalQExpansionMatrix(N); prec:=Ncols(L)+1; K<z>:=CyclotomicField(n);
 B:=ChangeRing(L,K); twisted:=B*DiagonalMatrix([z^i:i in [1..prec-1]]);
 S:=Solution(B,twisted); assert S*B eq twisted;
 return S;
end function;
