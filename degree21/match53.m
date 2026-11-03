SetQuitOnError(true);SetColumns(0);SetMemoryLimit(8*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
function Code(z)return[Integers()!a:a in Eltseq(z)];end function;
function XYKey(x,y)
 d:=LCM(Degree(MinimalPolynomial(x,GF(2))),Degree(MinimalPolynomial(y,GF(2))));found:=false;
 for ab in[[1,0],[0,1],[1,1]]do z:=ab[1]*x+ab[2]*y;mp:=MinimalPolynomial(z,GF(2));if Degree(mp)eq d then bb:=ab;found:=true;break;end if;end for;assert found;
 B:=Matrix(GF(2),[Eltseq(z^i,GF(2)):i in[0..d-1]]);assert Rank(B)eq d;
 cs:=[Eltseq(Solution(B,Vector(GF(2),Eltseq(v,GF(2))))):v in[x,y]];
 return[d]cat bb cat Code(mp)cat[Integers()!c:c in &cat cs];
end function;
function MakePoint(r)
 PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];return E,P;
end function;
p:=StringToInteger(P);
load "work/degree20/sources53.m";Old:=AuditSources;OldKeys:=[**];
for r in Old do
 if not r[7]then Append(~OldKeys,[]);continue;end if;
 E,PT:=MakePoint(r);xy:=TateNormalForm_xy(E,PT);Append(~OldKeys,XYKey(xy[1],xy[2]));
end for;
load "work/degree21/sources53.m";Matches:=[**];used:={Integers()|};
for si in[1..#AuditSources]do
 r:=AuditSources[si];if not r[7]or r[1]eq 21 then continue;end if;
 candidates:=[i:i in[1..#Old]|Old[i][7]and Old[i][1]eq r[1]and Old[i][5]eq r[5]and Old[i][6]eq r[6]];assert #candidates gt 0;
 E,PT:=MakePoint(r);assert p*PT eq E!0;found:=[];selected:=0;
 for k in[1..(p-1)div 2]do
  xy:=TateNormalForm_xy(E,k*PT);key:=XYKey(xy[1],xy[2]);ids:=[i:i in candidates|OldKeys[i]eq key];if #ids gt 0 then found:=ids;selected:=k;break;end if;
 end for;
 assert #found eq 1 and found[1]notin used;Include(~used,found[1]);Append(~Matches,<si,found[1],r[1],r[6],selected>);
end for;
assert #used eq #[r:r in Old|r[7]];
PrintFile(Sprintf("work/degree21/inherited%o.m",p),Sprintf("InheritedOrbitMatches:=%o;",Matches):Overwrite:=true);
printf "S21_INHERITED_ORBITS_MATCHED p=%o ordinary_orbits=%o elapsed=%o\n",p,#Matches,Cputime(tt);quit;
