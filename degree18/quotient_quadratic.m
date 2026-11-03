SetQuitOnError(true);SetColumns(0);
// Complete j lists: Box, section 4.7; Adzaga et al., Table 16.
// A point on X1(p)/H9 defined over a quadratic field has a torsion
// generator orbit stable under Aut(E) times the order-nine subgroup.
Data:=[<73,-19,Rationals()!-884736,0>,<73,-1,287496,0>,<73,-1,1728,0>,<73,-2,8000,0>,<73,-3,0,0>,<73,-3,54000,0>,<73,-3,-12288000,0>,<73,-1,-12288000,0>,<73,-67,-147197952000,0>,
<73,-31,-75276530483988147885303471/18889465931478580854784,-218623729131479023842537441/18889465931478580854784>,<73,-31,1809/4,-6561/4>,<73,-127,81450017206599109708140525/18889465931478580854784,14758692270140155157349165/18889465931478580854784>,
<127,-67,-147197952000,0>,<127,-3,54000,0>,<127,-3,-12288000,0>,<127,-7,16581375,0>,<127,-7,-3375,0>,<127,-3,0,0>,<127,-43,-884736000,0>];
for dat in Data do
 p,D,a,b:=Explode(dat);w:=a eq 0 and b eq 0 select 6 else(a eq 1728 and b eq 0 select 4 else 2);exponent:=LCM(18,w);found:=false;
 for q in PrimesUpTo(1000)do
  if q le 3 or q eq p or Denominator(a)mod q eq 0 or Denominator(b)mod q eq 0 or D mod q eq 0 then continue;end if;
  R<x>:=PolynomialRing(GF(q));rr:=Roots(x^2-D);if #rr eq 0 then continue;end if;
  j:=GF(q)!a+(GF(q)!b)*rr[1][1];if j in[GF(q)!0,GF(q)!1728]and w eq 2 then continue;end if;
  if b eq 0 then
   E:=MinimalModel(EllipticCurveFromjInvariant(Rationals()!a));if Valuation(Discriminant(E),q)ne 0 then continue;end if;EF:=EllipticCurve([GF(q)!c:c in aInvariants(E)]);
  else EF:=EllipticCurveFromjInvariant(j);end if;
  tr:=q+1-#EF;T:=Matrix(GF(p),2,2,[0,1,-q,tr]);det:=Determinant(T^exponent-1);
  if det ne 0 then found:=true;printf "S18_QUADRATIC_QUOTIENT_EXCLUDED p=%o D=%o j=[%o,%o] split_prime=%o theta=%o trace=%o exponent=%o determinant=%o\n",p,D,a,b,q,rr[1][1],tr,exponent,det;break;end if;
 end for;assert found;
end for;
for pj in[<73,0>,<97,1728>,<109,0>,<109,1728>,<113,1728>,<127,0>]do
 p,j:=Explode(pj);w:=j eq 0 select 6 else 4;E:=MinimalModel(EllipticCurveFromjInvariant(Rationals()!j));found:=false;
 for q in PrimesUpTo(1000)do
  if q eq p or Valuation(Discriminant(E),q)ne 0 then continue;end if;
  EF:=EllipticCurve([GF(q)!c:c in aInvariants(E)]);tr:=q+1-#EF;T:=Matrix(GF(p),2,2,[0,1,-q,tr]);det:=Determinant(T^(w*18)-1);
  if det ne 0 then found:=true;printf "S18_CM_DEGREE18_EXCLUDED p=%o j=%o q=%o trace=%o exponent=%o determinant=%o\n",p,j,q,tr,w*18,det;break;end if;
 end for;assert found;
end for;
print "S18_ALL_QUADRATIC_QUOTIENT_AND_BRANCH_CM_EXCLUSIONS_COMPLETE";quit;
