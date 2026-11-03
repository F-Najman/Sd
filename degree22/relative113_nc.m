SetQuitOnError(true);SetColumns(0);SetMemoryLimit(16*10^9);tt:=Cputime();AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "work/degree22/full113/units_data.m";load "work/degree22/sources113.m";
g:=genus;D:=DiamondMatrix;I:=IdentityMatrix(GF(2),g);m:=56;alpha:=D^7-I;AA:=[];
for q in[2,3,5]do
 cut:=Min((113^2-1)div 12,(precision-1)div q);C:=Submatrix(qcoeffs,1,1,g,cut+1);if Rank(C)lt g then continue;end if;
 log:=Min([k:k in[0..55]|DiamondRoot^k mod 113 in[q,113-q]]);DQ:=D^log*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select(GF(2)!q)*DQ[i,n div q+1]else 0):n in[0..cut]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;
 A:=alpha*(T-D^log-(GF(2)!q)*I)*(T-I-(GF(2)!q)*D^log);Append(~AA,A);printf "S22_REL113_NC_OPERATOR q=%o prefix=%o\n",q,cut;
end for;assert #AA gt 0;
function UnitValues(aa,xx,yy)
 a1,a2,a3,a4,a6:=Explode(aa);aa3:=2*yy+a3+a1*xx;aa2:=3*xx+a2;aa4:=3*xx^2+2*xx*a2+a4-a1*yy;aaa1:=2*aa4/aa3+a1;aaa2:=aa2-(aa4/aa3)^2-a1*aa4/aa3;b:=-aaa2^3/aa3^2;c:=-(aaa1*aaa2-aa3)/aa3;r:=b/c;s:=c^2/(b-c);t:=r*s-2*r+1;return[(s-r)/t,t/(s^2-s-r+1)];
end function;
function CV(F,x,y)
 R:=VerticalJoin(Matrix(F,[[F!v[i]+x*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+y*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)]));printf "S22_REL113_NC_CANONICAL_RANK field_degree=%o rank=%o\n",Degree(F),Rank(R);assert Rank(R)eq g-1;z:=Basis(Kernel(Transpose(R)))[1];return z/z[Min([k:k in[1..g]|z[k]ne 0])];
end function;
PF:=PolynomialRing(GF(2));r:=Rep([rr:rr in AuditSources|rr[1]eq 8 and rr[6]eq 7 and rr[7]]);F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];xy:=TateNormalForm_xy(E,P);zo:=CV(F,xy[1],xy[2]);
K<a>:=GF(2^28);a:=a^ExactQuotient(2^28-1,113);assert Order(a)eq 113;xx:=a/(1+a)^2;yy:=a^2/(1+a)^3;uv:=UnitValues([K!1,K!0,K!0,K!0,K!0],xx,yy);zn:=CV(K,uv[1],uv[2]);
L:=GF(2^14);Embed(L,K);assert &and[v^(2^14)eq v:v in Eltseq(zn)];B:=ZeroMatrix(GF(2),0,22);
for A in AA do
 vo:=zo*Transpose(ChangeRing(A,F));vn:=zn*Transpose(ChangeRing(A,K));O:=Matrix(GF(2),[Eltseq(v,GF(2)):v in Eltseq(vo)]);NC:=Matrix(GF(2),[Eltseq(L!v,GF(2)):v in Eltseq(vn)]);B:=VerticalJoin(B,HorizontalJoin(O,NC));
end for;
printf "S22_REL113_NC_BASE_RANK rank=%o expected21 operators=%o\n",Rank(B),#AA;
PrintFile("work/degree22/relative113_nc_data.m",Sprintf("Relative113NCBase:=%o;Relative113NCField:=%o;Relative113NCZeta:=%o;Relative113NCZ:=%o;Relative113NCOrdZ:=%o;",[Eltseq(v):v in Rows(B)],[Integers()!v:v in Eltseq(DefiningPolynomial(K))],[Integers()!v:v in Eltseq(a)],[[Integers()!a:a in Eltseq(v)]:v in Eltseq(zn)],[[Integers()!a:a in Eltseq(v)]:v in Eltseq(zo)]):Overwrite:=true);
PrintFile("work/degree22/relative113_nc_data.m",Sprintf("Relative113NCSmallField:=%o;Relative113NCSmallImage:=%o;",[Integers()!v:v in Eltseq(DefiningPolynomial(L))],[Integers()!v:v in Eltseq(K!L.1)]));assert Rank(B)eq 21;print "S22_REL113_NC_EXPORT_COMPLETE";quit;
