// Root-allocated elliptic Hecke/jet stage; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree17/full89/units_data.m";
g:=genus;
function Code(z) if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return [Integers()!a:a in Eltseq(z,GF(2))];end function;
function SimplifyPoint(E,P)
 F:=BaseRing(E);a1,a2,a3,a4,a6:=Explode(aInvariants(E));assert a1 eq 1 and a3 eq 0;EE:=EllipticCurve([F!1,a2,F!0,F!0,a6+a4^2]);PP:=EE![P[1],P[2]+a4];assert jInvariant(EE)eq jInvariant(E)and N*PP eq EE!0;assert TateNormalForm_xy(EE,PP)eq TateNormalForm_xy(E,P);return EE,PP;
end function;
function UnitValues(aa,xx,yy)
 a1,a2,a3,a4,a6:=Explode(aa);aa3:=2*yy+a3+a1*xx;aa2:=3*xx+a2;aa4:=3*xx^2+2*xx*a2+a4-a1*yy;aaa1:=2*aa4/aa3+a1;aaa2:=aa2-(aa4/aa3)^2-a1*aa4/aa3;b:=-aaa2^3/aa3^2;c:=-(aaa1*aaa2-aa3)/aa3;r:=b/c;s:=c^2/(b-c);t:=r*s-2*r+1;return[(s-r)/t,t/(s^2-s-r+1)];
end function;
function UnitMatrix(F,x0,y0)
 return VerticalJoin(Matrix(F,[[F!v[i]+x0*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+y0*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)]));
end function;
function CanonicalPoint(E,P)
 F:=BaseRing(E);xy:=TateNormalForm_xy(E,P);RR:=UnitMatrix(F,xy[1],xy[2]);assert Rank(RR)eq g-1;zz:=Eltseq(Basis(Kernel(Transpose(RR)))[1]);ki:=Index([z ne 0:z in zz],true);return[z/zz[ki]:z in zz],xy;
end function;
function PsiN(xx,aa6)
 PS:=Parent(xx);pp:=[PS!0,PS!1,xx,xx^4+xx^3+aa6,xx^6+aa6*xx^2];
 for n in[5..N]do m:=n div 2;if IsOdd(n)then pn:=pp[m+3]*pp[m+1]^3+pp[m]*pp[m+2]^3;else pn:=pp[m+1]/xx*(pp[m+3]*pp[m]^2+pp[m-1]*pp[m+2]^2);end if;Append(~pp,pn);end for;return pp[N+1];
end function;
function CanonicalJets(E,P,z0)
 F:=BaseRing(E);aa:=aInvariants(E);assert aa[1]eq 1 and aa[3]eq 0 and aa[4]eq 0;PS<u>:=PowerSeriesRing(F,8);xx:=PS!P[1];yy:=PS!P[2];a2:=aa[2];a6:=PS!aa[5]+u;der:=Coefficient(PsiN(xx+u,PS!aa[5]),1);assert der ne 0 and P[1]ne 0;
 for n in[1..7]do xx+:=(Coefficient(PsiN(xx,a6),n)/der)*u^n;assert Valuation(PsiN(xx,a6))ge n+1;end for;
 for n in[1..7]do er:=Coefficient(yy^2+xx*yy+xx^3+a2*xx^2+a6,n);yy+:=(er/P[1])*u^n;assert Valuation(yy^2+xx*yy+xx^3+a2*xx^2+a6)ge n+1;end for;
 xy:=UnitValues([PS!1,PS!a2,PS!0,PS!0,a6],xx,yy);RM:=[UnitMatrix(F,Coefficient(xy[1],0),Coefficient(xy[2],0))];
 for n in[1..7]do Append(~RM,VerticalJoin(Matrix(F,[[Coefficient(xy[1],n)*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[Coefficient(xy[2],n)*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)])));end for;
 ki:=Index([z ne 0:z in z0],true);assert z0[ki]eq 1;uk:=[i:i in[1..g]|i ne ki];M0:=Matrix(F,[[RM[1][r,c]:c in uk]:r in[1..Nrows(RM[1])]]);assert Rank(M0)eq g-1;LL:=Solution(M0,IdentityMatrix(F,g-1));assert LL*M0 eq IdentityMatrix(F,g-1);zv:=[Vector(F,z0)];
 for n in[1..7]do
  br:=Vector(F,[0:i in[1..Nrows(M0)]]);for j in[1..n]do br+:=Vector(F,[&+[RM[j+1][r,c]*zv[n-j+1][c]:c in[1..g]]:r in[1..Nrows(M0)]]);end for;ur:=br*Transpose(LL);zz:=Vector(F,[0:i in[1..g]]);for j in[1..g-1]do zz[uk[j]]:=ur[j];end for;Append(~zv,zz);
 end for;
 for n in[0..7]do for r in[1..Nrows(M0)]do assert &+[&+[RM[j+1][r,c]*zv[n-j+1][c]:c in[1..g]]:j in[0..n]]eq 0;end for;end for;
 return <[Code(Coefficient(xx,n)):n in[0..7]],[Code(Coefficient(yy,n)):n in[0..7]],[[Code(zv[n+1][i]):n in[0..7]]:i in[1..g]]>;
end function;
function RecordPoint(E,P)
 E,P:=SimplifyPoint(E,P);F:=BaseRing(E);z,xy:=CanonicalPoint(E,P);jt:=CanonicalJets(E,P,z);d:=LCM([Degree(MinimalPolynomial(x,GF(2))):x in xy]);assert LCM([Degree(MinimalPolynomial(x,GF(2))):x in z])eq d;
 rec:=<[Integers()!c:c in Eltseq(DefiningPolynomial(F,GF(2)))],[Code(a):a in aInvariants(E)],[Code(P[i]):i in[1,2]],[Code(a):a in z],[Code(a):a in xy],jt>;return rec,d;
end function;

function XYKey(x,y)
 d:=LCM(Degree(MinimalPolynomial(x,GF(2))),Degree(MinimalPolynomial(y,GF(2))));found:=false;bb:=[1,0];
 for ab in[[1,0],[0,1],[1,1]]do z:=ab[1]*x+ab[2]*y;mp:=MinimalPolynomial(z,GF(2));if Degree(mp)eq d then bb:=ab;found:=true;break;end if;end for;assert found;
 B:=Matrix(GF(2),[Eltseq(z^i,GF(2)):i in[0..d-1]]);assert Rank(B)eq d;
 cs:=[Eltseq(Solution(B,Vector(GF(2),Eltseq(v,GF(2))))):v in[x,y]];
 return[d]cat bb cat Code(mp)cat[Integers()!c:c in &cat cs];
end function;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree16/full89/hecke_jets.m";
OldMetadata:=SourceMetadata;OldRecords:=SourceRecords;OldHecke:=SourceHeckeRecords;used:={Integers()|};
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree17/sources89.m";assert AuditN eq N;
SourceRecords:=[**];SourceHeckeRecords:=[**];SourceMetadata:=[**];
for si in[1..#AuditSources]do
 rec:=AuditSources[si];if not rec[7]then continue;end if;
 PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];assert N*P eq E!0 and P ne E!0;
 if rec[1] le 16 then
  good:=[];
  for oi in[1..#OldRecords]do
   if OldMetadata[oi][2]ne rec[1]or OldMetadata[oi][3]ne rec[6]or OldMetadata[oi][4]ne rec[5]then continue;end if;
   os:=OldRecords[oi];OF:=ext<GF(2)|PF!os[1]>;oxy:=[OF!PF!v:v in os[5]];okey:=XYKey(oxy[1],oxy[2]);
   found:=false;for k in[1..N-1]do uv:=TateNormalForm_xy(E,k*P);if XYKey(uv[1],uv[2])eq okey then found:=true;break;end if;end for;
   if found then Append(~good,oi);end if;
  end for;assert #good eq 1;oi:=good[1];assert oi notin used;Include(~used,oi);
  Append(~SourceRecords,OldRecords[oi]);Append(~SourceHeckeRecords,OldHecke[oi]);Append(~SourceMetadata,<si,rec[1],rec[6],rec[5]>);
  printf "S17_OLD_ORBIT_REUSE_VERIFIED N=%o source=%o old_source=%o degree=%o\n",N,si,OldMetadata[oi][1],rec[1];continue;
 end if;
 E,P:=SimplifyPoint(E,P);sr,sd:=RecordPoint(E,P);d:=rec[1];assert sd eq d;Append(~SourceRecords,sr);Append(~SourceMetadata,<si,d,rec[6],rec[5]>);
 fq:=DivisionPolynomial(E,3);fac:=Factorization(fq);assert Degree(fq)eq 4 and IsSquarefree(fq)and &+[Degree(a[1]):a in fac]eq 4;
 trs:=[**];for ff in fac do
  h:=ff[1];e:=Degree(h);if e eq 1 then L:=F;xx:=-Coefficient(h,0)/Coefficient(h,1);else L:=ext<F|h>;xx:=L.1;end if;
  EL:=EllipticCurve([L!a:a in aInvariants(E)]);PL:=EL![L!P[1],L!P[2]];PX<X>:=PolynomialRing(L);ET,phi:=IsogenyFromKernel(EL,X-xx);PT:=phi(PL);assert N*PT eq ET!0 and PT ne ET!0;
  tr,td:=RecordPoint(ET,PT);assert (d*e)mod td eq 0;Append(~trs,<e,td,d*e div td,tr>);
 end for;assert &+[r[2]*r[3]:r in trs]eq 4*d;Append(~SourceHeckeRecords,trs);
 printf "AUDIT_ACTUAL_HECKE_JETS_SOURCE N=%o source=%o degree=%o orbit=%o target_degrees=%o weights=%o elapsed=%o\n",N,si,d,rec[6],[r[2]:r in trs],[r[3]:r in trs],Cputime(tt);
end for;
assert #used eq #OldRecords;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree17/full89/hecke_jets.m",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",SourceMetadata,SourceRecords,SourceHeckeRecords):Overwrite:=true);
printf "AUDIT_ACTUAL_HECKE_JETS_COMPLETE N=%o sources=%o elapsed=%o\n",N,#SourceRecords,Cputime(tt);quit;
