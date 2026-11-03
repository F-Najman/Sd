SetQuitOnError(true);SetColumns(0);Data:=[**];
for dat in[<151,0,6>,<113,1728,4>,<97,1728,4>]do
 p,j,w:=Explode(dat);E:=MinimalModel(EllipticCurveFromjInvariant(Rationals()!j));found:=false;
 for q in PrimesInInterval(3,97)do
  if q eq p or Valuation(Discriminant(E),q)ne 0 then continue;end if;
  EE:=EllipticCurve([GF(q)!a:a in aInvariants(E)]);a:=q+1-#EE;F:=Matrix(GF(p),2,2,[0,-q,1,a]);
  if &and[Determinant(F^(w*k)-1)ne 0:k in[1..20]]then
   Append(~Data,<p,j,w,q,a>);printf "S20_CM_EXCLUDED p=%o j=%o automorphisms=%o prime=%o trace=%o through_degree=20\n",p,j,w,q,a;found:=true;break;
  end if;
 end for;
 printf "S20_CM_BRANCH_SEARCH p=%o found=%o\n",p,found;
end for;
PrintFile("work/degree20/cm_branch_data.m",Sprintf("CMBranchData:=%o;",Data):Overwrite:=true);print "S20_CM_BRANCH_SEARCH_COMPLETE";quit;
