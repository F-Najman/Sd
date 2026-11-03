SetQuitOnError(true);SetColumns(0);SetMemoryLimit(16*10^9);tt:=Cputime();AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "work/degree22/full127/units_data.m";load "work/degree22/sources127.m";
g:=genus;D:=DiamondMatrix;I:=IdentityMatrix(GF(2),g);m:=63;log2:=Min([k:k in[0..62]|3^k mod 127 in[2,125]]);alpha:=(D^7-I)*(D^log2-I);AA:=[];
for q in[2,3,5]do
 cut:=Min((127^2-1)div 12,(precision-1)div q);C:=Submatrix(qcoeffs,1,1,g,cut+1);if Rank(C)lt g then continue;end if;
 log:=Min([k:k in[0..62]|3^k mod 127 in[q,127-q]]);DQ:=D^log*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select(GF(2)!q)*DQ[i,n div q+1]else 0):n in[0..cut]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;
 A:=alpha*(T-D^log-(GF(2)!q)*I);Append(~AA,A);printf "S22_REL127_OPERATOR q=%o prefix=%o\n",q,cut;
end for;assert #AA gt 0;
function UnitValues(aa,xx,yy)
 a1,a2,a3,a4,a6:=Explode(aa);aa3:=2*yy+a3+a1*xx;aa2:=3*xx+a2;aa4:=3*xx^2+2*xx*a2+a4-a1*yy;aaa1:=2*aa4/aa3+a1;aaa2:=aa2-(aa4/aa3)^2-a1*aa4/aa3;b:=-aaa2^3/aa3^2;c:=-(aaa1*aaa2-aa3)/aa3;r:=b/c;s:=c^2/(b-c);t:=r*s-2*r+1;return[(s-r)/t,t/(s^2-s-r+1)];
end function;
function CV(F,x,y)
 R:=VerticalJoin(Matrix(F,[[F!v[i]+x*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+y*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)]));printf "S22_REL127_CANONICAL_RANK field_degree=%o rank=%o\n",Degree(F),Rank(R);assert Rank(R)eq g-1;z:=Basis(Kernel(Transpose(R)))[1];return z/z[Min([k:k in[1..g]|z[k]ne 0])];
end function;
PF:=PolynomialRing(GF(2));r:=Rep([rr:rr in AuditSources|rr[1]eq 9 and rr[6]eq 7 and rr[7]]);assert r[1]eq 9 and r[6]eq 7 and r[7];F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];xy:=TateNormalForm_xy(E,P);zo:=CV(F,xy[1],xy[2]);
K<a>:=GF(2^7);assert Order(a)eq 127;xx:=a/(1+a)^2;yy:=a^2/(1+a)^3;uv:=UnitValues([K!1,K!0,K!0,K!0,K!0],xx,yy);zn:=CV(K,uv[1],uv[2]);
B:=ZeroMatrix(GF(2),0,16);
for A in AA do
 vo:=zo*Transpose(ChangeRing(A,F));vn:=zn*Transpose(ChangeRing(A,K));O:=Matrix(GF(2),[Eltseq(v,GF(2)):v in Eltseq(vo)]);NC:=Matrix(GF(2),[Eltseq(v,GF(2)):v in Eltseq(vn)]);B:=VerticalJoin(B,HorizontalJoin(O,NC));
end for;assert Rank(B)eq 14;print "S22_REL127_TWO_PULLBACK_TANGENT_RANK",Rank(B);
CJ:=[**];for k in[0..62]do
 C:=ZeroMatrix(GF(2),0,6);
 for A in AA do
  QJ:=Submatrix(qcoeffs,1,2,g,6);C:=VerticalJoin(C,A*D^k*QJ);
 end for;Append(~CJ,[Eltseq(v):v in Rows(C)]);
end for;
PrintFile("work/degree22/relative127_data.m",Sprintf("Relative127Base:=%o;Relative127CuspJets:=%o;",[Eltseq(v):v in Rows(B)],CJ):Overwrite:=true);
print "S22_RELATIVE127_EXPORT_COMPLETE family_dimension=2";quit;
