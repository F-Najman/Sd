SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);SetSeed(20261028);
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
Ns:=[59, 61, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139];
root:="/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree22/";tt:=Cputime();
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
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources59.m"; records[59]:=AuditSources;seen[59]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources61.m"; records[61]:=AuditSources;seen[61]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources71.m"; records[71]:=AuditSources;seen[71]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources73.m"; records[73]:=AuditSources;seen[73]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources79.m"; records[79]:=AuditSources;seen[79]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources83.m"; records[83]:=AuditSources;seen[83]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources89.m"; records[89]:=AuditSources;seen[89]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources97.m"; records[97]:=AuditSources;seen[97]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources101.m"; records[101]:=AuditSources;seen[101]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources103.m"; records[103]:=AuditSources;seen[103]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources107.m"; records[107]:=AuditSources;seen[107]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources109.m"; records[109]:=AuditSources;seen[109]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources113.m"; records[113]:=AuditSources;seen[113]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources127.m"; records[127]:=AuditSources;seen[127]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources131.m"; records[131]:=AuditSources;seen[131]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources137.m"; records[137]:=AuditSources;seen[137]:={};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree21/sources139.m"; records[139]:=AuditSources;seen[139]:={};
for d in[22]do
 F<z>:=GF(2^d);jseen:={};cnt:=AssociativeArray();reps:=AssociativeArray();jds:=AssociativeArray();
 for N in Ns do cnt[N]:=0;reps[N]:=0;jds[N]:=[];end for;
 for j in F do
  mp:=MinimalPolynomial(j,GF(2));if mp in jseen then continue;end if;Include(~jseen,mp);
  for E in Twists(EllipticCurveFromjInvariant(j))do
   ord:=#E;
   for N in Ns do
    if ord mod N ne 0 then continue;end if;
    G,gp:=AbelianGroup(E);iv:=Invariants(G);P0:=(iv[#iv]div N)*gp(G.#iv);Ps:=[P0];
    if #iv eq 2 and iv[1]mod N eq 0 then Q0:=(iv[1]div N)*gp(G.1);Ps:=[Q0]cat[P0+k*Q0:k in[0..N-1]];assert #Seqset(Ps)eq N+1;printf "S22_FULL_N_TORSION N=%o degree=%o cyclic_subgroups=%o\n",N,d,#Ps;end if;
    for P in Ps do assert P ne E!0 and N*P eq E!0;
    xy:=TateNormalForm_xy(E,P);sd:=LCM([Degree(MinimalPolynomial(v,GF(2))):v in xy]);if sd ne d then continue;end if;
    orb:={XYKey(vv[1],vv[2])where vv:=TateNormalForm_xy(E,k*P):k in[1..N-1]};key:=<d,Sort(Setseq(orb))[1]>;
    if key in seen[N]then continue;end if;ss:=seen[N];Include(~ss,key);seen[N]:=ss;
    rec:=<d,Code(DefiningPolynomial(F,GF(2))),[Code(a):a in aInvariants(E)],[Code(P[i]):i in[1,2]],Code(mp),#orb,aInvariants(E)[1]ne 0>;
    rs:=records[N];Append(~rs,rec);records[N]:=rs;cnt[N]+:=#orb;reps[N]+:=1;jj:=jds[N];Append(~jj,Degree(mp));jds[N]:=jj;
    end for;
   end for;
  end for;
 end for;
 for N in Ns do
  PrintFile(root cat Sprintf("sources%o.m",N),Sprintf("AuditN:=%o;AuditSources:=%o;",N,records[N]):Overwrite:=true);
  printf "S22_CENSUS N=%o degree=%o closed_points=%o diamond_orbits=%o j_degrees=%o elapsed=%o\n",N,d,cnt[N],reps[N],jds[N],Cputime(tt);
 end for;
end for;
print "S22_ALL_FINITE_SOURCE_ORBITS_COMPLETE";quit;
