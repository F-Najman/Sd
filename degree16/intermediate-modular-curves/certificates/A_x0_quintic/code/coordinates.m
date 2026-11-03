// Coordinate action for the LLL basis used by ModularCurveQuotient(N,[]).
function CanonicalALMatrix(N,d)
 M:=CuspidalSubspace(ModularForms(N,2));
 prec:=Max(200,Ceiling(N*4*2/12));
 bs:=qExpansionBasis(M,prec);
 rows:=[]; scalars:=[];
 for b in bs do
  row:=[Coefficient(b,i):i in [1..prec-1]];
  den:=LCM([Denominator(a):a in row]);
  ints:=[Integers()!(den*a):a in row]; rowgcd:=GCD(ints);
  Append(~scalars,den/rowgcd); Append(~rows,[a div rowgcd:a in ints]);
 end for;
 L,T:=LLL(Matrix(Integers(),rows));
 U:=ChangeRing(T,Rationals())*DiagonalMatrix(scalars);
 return U*AtkinLehnerOperator(M,d)*U^-1, [L[i,1]:i in [1..Nrows(L)]];
end function;
