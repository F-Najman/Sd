SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);SetSeed(20261028);
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
Ns:=[41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113];
root:="/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree13/";tt:=Cputime();
function Code(z)
 if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return[Integers()!a:a in Eltseq(z,GF(2))];end function;
function XYKey(x,y)
 d:=LCM(Degree(MinimalPolynomial(x,GF(2))),Degree(MinimalPolynomial(y,GF(2))));found:=false;bb:=[1,0];
 for ab in[[1,0],[0,1],[1,1]]do z:=ab[1]*x+ab[2]*y;mp:=MinimalPolynomial(z,GF(2));if Degree(mp)eq d then bb:=ab;found:=true;break;end if;end for;assert found;
 B:=Matrix(GF(2),[Eltseq(z^i,GF(2)):i in[0..d-1]]);assert Rank(B)eq d;
 cs:=[Eltseq(Solution(B,Vector(GF(2),Eltseq(v,GF(2))))):v in[x,y]];
 return[d]cat bb cat Code(mp)cat[Integers()!c:c in &cat cs];
end function;
records:=AssociativeArray();seen:=AssociativeArray();
for N in Ns do records[N]:=[**];seen[N]:={};end for;
for d in[1..13]do
 F<z>:=GF(2^d);jseen:={};cnt:=AssociativeArray();reps:=AssociativeArray();jds:=AssociativeArray();
 for N in Ns do cnt[N]:=0;reps[N]:=0;jds[N]:=[];end for;
 for j in F do
  mp:=MinimalPolynomial(j,GF(2));if mp in jseen then continue;end if;Include(~jseen,mp);
  for E in Twists(EllipticCurveFromjInvariant(j))do
   ord:=#E;
   for N in Ns do
    if ord mod N ne 0 then continue;end if;assert ord mod N^2 ne 0;
    G,gp:=AbelianGroup(E);iv:=Invariants(G);P:=(iv[#iv]div N)*gp(G.#iv);assert P ne E!0 and N*P eq E!0;
    xy:=TateNormalForm_xy(E,P);sd:=LCM([Degree(MinimalPolynomial(v,GF(2))):v in xy]);if sd ne d then continue;end if;
    orb:={XYKey(vv[1],vv[2])where vv:=TateNormalForm_xy(E,k*P):k in[1..N-1]};key:=<d,Sort(Setseq(orb))[1]>;
    if key in seen[N]then continue;end if;ss:=seen[N];Include(~ss,key);seen[N]:=ss;
    rec:=<d,Code(DefiningPolynomial(F,GF(2))),[Code(a):a in aInvariants(E)],[Code(P[i]):i in[1,2]],Code(mp),#orb,aInvariants(E)[1]ne 0>;
    rs:=records[N];Append(~rs,rec);records[N]:=rs;cnt[N]+:=#orb;reps[N]+:=1;jj:=jds[N];Append(~jj,Degree(mp));jds[N]:=jj;
   end for;
  end for;
 end for;
 for N in Ns do
  PrintFile(root cat Sprintf("sources%o.m",N),Sprintf("AuditN:=%o;AuditSources:=%o;",N,records[N]):Overwrite:=true);
  printf "S12_CENSUS N=%o degree=%o closed_points=%o diamond_orbits=%o j_degrees=%o elapsed=%o\n",N,d,cnt[N],reps[N],jds[N],Cputime(tt);
 end for;
end for;
print "S12_ALL_FINITE_SOURCE_ORBITS_COMPLETE";quit;
