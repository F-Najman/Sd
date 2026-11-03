// Root-allocated elliptic Hecke/jet stage; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/full61/units_data.m";
g:=genus;
function Code(z) if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return [Integers()!a:a in Eltseq(z,GF(2))];end function;
function SimplifyPoint(E,P)
 F:=BaseRing(E);xy:=TateNormalForm_xy(E,P);d:=LCM([Degree(MinimalPolynomial(v,GF(2))):v in xy]);if d lt Degree(F)then L:=sub<F|d>;else L:=F;end if;x:=L!xy[1];y:=L!xy[2];r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);b:=r*ss*(r-1);c:=ss*(r-1);EE:=EllipticCurve([1-c,-b,-b,L!0,L!0]);PP:=EE![0,0];assert N*PP eq EE!0 and PP ne EE!0 and TateNormalForm_xy(EE,PP)eq [x,y];return EE,PP;
end function;
function XYKey(x,y)
 d:=LCM(Degree(MinimalPolynomial(x,GF(2))),Degree(MinimalPolynomial(y,GF(2))));found:=false;bb:=[1,0];
 for ab in[[1,0],[0,1],[1,1]]do z:=ab[1]*x+ab[2]*y;mp:=MinimalPolynomial(z,GF(2));if Degree(mp)eq d then bb:=ab;found:=true;break;end if;end for;assert found;
 B:=Matrix(GF(2),[Eltseq(z^i,GF(2)):i in[0..d-1]]);assert Rank(B)eq d;
 cs:=[Eltseq(Solution(B,Vector(GF(2),Eltseq(v,GF(2))))):v in[x,y]];
 return[d]cat bb cat Code(mp)cat[Integers()!c:c in &cat cs];
end function;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/hecke_jets.m";
PF:=PolynomialRing(GF(2));closedkeys:=[];
for rr in SourceRecords do FF:=ext<GF(2)|PF!rr[1]>;uv:=[FF!PF!v:v in rr[5]];Append(~closedkeys,XYKey(uv[1],uv[2]));end for;assert #Seqset(closedkeys)eq 4;
OutRecords:=[**];
for ell in[7,11,13]do
 ff:=ell eq 11 select 180 else 60;F:=GF(2^ff);rr:=SourceRecords[1];z:=Roots(PolynomialRing(F)!PF!rr[1])[1][1];E:=EllipticCurve([Evaluate(PF!v,z):v in rr[2]]);P:=E![Evaluate(PF!v,z):v in rr[3]];
 RX<X>:=PolynomialRing(F);fl:=DivisionPolynomial(E,ell);roots:={v[1]:v in Roots(fl)};assert #roots eq (ell^2-1)div 2;f3:=DivisionPolynomial(E,3);aa:=aInvariants(E);ks:={RX|};
 for xx in roots do cyc:={F|};v:=xx;repeat Include(~cyc,v);v+:=Evaluate(f3,v)/(aa[1]*v+aa[3])^2;until v eq xx;assert #cyc eq (ell-1)div 2;Include(~ks,&*[X-v:v in cyc]);end for;assert #ks eq ell+1;
 seen:={RX|};records:=[**];
 for h in ks do if h in seen then continue;end if;ee:=Min([k:k in[1..ff div 15]|RX![a^(2^(15*k)):a in Eltseq(h)]eq h]);orb:={RX![a^(2^(15*k)):a in Eltseq(h)]:k in[0..ee-1]};assert #orb eq ee;seen join:=orb;
  ET,phi:=IsogenyFromKernel(E,h);PT:=phi(P);ET,PT:=SimplifyPoint(ET,PT);uv:=TateNormalForm_xy(ET,PT);dd:=Degree(BaseRing(ET));ix:=Index(closedkeys,XYKey(uv[1],uv[2]));assert ix gt 0 and (15*ee)mod dd eq 0;Append(~records,<ix,15*ee div dd>);
 end for;assert #seen eq ell+1 and &+[SourceMetadata[r[1]][2]*r[2]:r in records]eq 15*(ell+1);Append(~OutRecords,<ell,records>);printf "S15_SS61_FURTHER_HECKE q=%o records=%o elapsed=%o\n",ell,records,Cputime(tt);
end for;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/further_hecke_data.m",Sprintf("FurtherHecke:=%o;",OutRecords):Overwrite:=true);print "S15_FURTHER_SS_HECKE_COMPLETE";quit;
