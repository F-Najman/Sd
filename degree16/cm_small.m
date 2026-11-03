SetQuitOnError(true);SetColumns(0);Data:=[**];
for p in[97,113]do
 js:=p eq 97 select [0,1728]else[287496,1728,16581375,-3375,-32768,-262537412640768000,8000];
 for j in js do
 E:=MinimalModel(EllipticCurveFromjInvariant(Rationals()!j));w:=j eq 0 select 6 else (j eq 1728 select 4 else 2);found:=false;
 for q in PrimesInInterval(3,53)do
  if q eq p or Valuation(Discriminant(E),q)ne 0 then continue;end if;
  EE:=EllipticCurve([GF(q)!a:a in aInvariants(E)]);a:=q+1-#EE;F:=Matrix(GF(p),2,2,[0,-q,1,a]);
  if &and[Determinant(F^(w*k)-1)ne 0:k in[1..16]]then
   printf "S16_RATIONAL_J_EXCLUSION p=%o j=%o automorphisms=%o prime=%o trace=%o all_powers_through_degree16_invertible=true\n",p,j,w,q,a;Append(~Data,<p,j,w,q,a>);found:=true;break;
  end if;
 end for;assert found;
 end for;
end for;
PrintFile("work/degree16/cm_small_data.m",Sprintf("CMData:=%o;",Data):Overwrite:=true);print "S16_RATIONAL_CM_J_EXCLUSIONS_COMPLETE";quit;
