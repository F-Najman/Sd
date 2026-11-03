// Root-allocated elliptic Hecke/jet stage; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/full61/units_data.m";
g:=genus;
function Code(z) if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return [Integers()!a:a in Eltseq(z,GF(2))];end function;
function SimplifyPoint(E,P)
 F:=BaseRing(E);xy:=TateNormalForm_xy(E,P);d:=LCM([Degree(MinimalPolynomial(v,GF(2))):v in xy]);if d lt Degree(F)then L:=sub<F|d>;else L:=F;end if;x:=L!xy[1];y:=L!xy[2];r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);b:=r*ss*(r-1);c:=ss*(r-1);EE:=EllipticCurve([1-c,-b,-b,L!0,L!0]);PP:=EE![0,0];assert N*PP eq EE!0 and PP ne EE!0 and TateNormalForm_xy(EE,PP)eq [x,y];return EE,PP;
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
function PsiN(xx,aa)
 PS:=Parent(xx);a1,a2,a3,a4,a6:=Explode(aa);b2:=a1^2;b4:=a1*a3;b6:=a3^2;b8:=a1^2*a6+a1*a3*a4+a2*a3^2+a4^2;psi2:=a1*xx+a3;
 pp:=[PS!0,PS!1,psi2,xx^4+b2*xx^3+b4*xx^2+b6*xx+b8,psi2*(b2*xx^5+b4*xx^4+(b2*b8+b4*b6)*xx+b4*b8+b6^2)];
 for n in[5..N]do m:=n div 2;if IsOdd(n)then pn:=pp[m+3]*pp[m+1]^3+pp[m]*pp[m+2]^3;else pn:=pp[m+1]/psi2*(pp[m+3]*pp[m]^2+pp[m-1]*pp[m+2]^2);end if;Append(~pp,pn);end for;return pp[N+1];
end function;
function CanonicalJets(E,P,z0)
 F:=BaseRing(E);aa0:=aInvariants(E);assert aa0[1]eq 0 and aa0[3]ne 0;PS<u>:=PowerSeriesRing(F,8);aa:=[PS!v:v in aa0];aa[1]+:=u;xx:=PS!P[1];yy:=PS!P[2];der:=Coefficient(PsiN(xx+u,[PS!v:v in aa0]),1);assert der ne 0;dy:=aa0[1]*P[1]+aa0[3];assert dy ne 0;
 for n in[1..7]do xx+:=(Coefficient(PsiN(xx,aa),n)/der)*u^n;assert Valuation(PsiN(xx,aa))ge n+1;end for;
 for n in[1..7]do er:=Coefficient(yy^2+aa[1]*xx*yy+aa[3]*yy+xx^3+aa[2]*xx^2+aa[4]*xx+aa[5],n);yy+:=(er/dy)*u^n;assert Valuation(yy^2+aa[1]*xx*yy+aa[3]*yy+xx^3+aa[2]*xx^2+aa[4]*xx+aa[5])ge n+1;end for;
 xy:=UnitValues(aa,xx,yy);RM:=[UnitMatrix(F,Coefficient(xy[1],0),Coefficient(xy[2],0))];
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

load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/sources61.m";assert AuditN eq N;
function XYKey(x,y)
 d:=LCM(Degree(MinimalPolynomial(x,GF(2))),Degree(MinimalPolynomial(y,GF(2))));found:=false;bb:=[1,0];
 for ab in[[1,0],[0,1],[1,1]]do z:=ab[1]*x+ab[2]*y;mp:=MinimalPolynomial(z,GF(2));if Degree(mp)eq d then bb:=ab;found:=true;break;end if;end for;assert found;
 B:=Matrix(GF(2),[Eltseq(z^i,GF(2)):i in[0..d-1]]);assert Rank(B)eq d;
 cs:=[Eltseq(Solution(B,Vector(GF(2),Eltseq(v,GF(2))))):v in[x,y]];
 return[d]cat bb cat Code(mp)cat[Integers()!c:c in &cat cs];
end function;
function Process(E,P,d)
 E,P:=SimplifyPoint(E,P);F:=BaseRing(E);sr,sd:=RecordPoint(E,P);assert sd eq d;
 fq:=DivisionPolynomial(E,3);fac:=Factorization(fq);assert Degree(fq)eq 4 and IsSquarefree(fq)and &+[Degree(a[1]):a in fac]eq 4;
 trs:=[**];for ff in fac do
  h:=ff[1];e:=Degree(h);if e eq 1 then L:=F;xx:=-Coefficient(h,0)/Coefficient(h,1);else L:=ext<F|h>;xx:=L.1;end if;
  EL:=EllipticCurve([L!a:a in aInvariants(E)]);PL:=EL![L!P[1],L!P[2]];PX<X>:=PolynomialRing(L);ET,phi:=IsogenyFromKernel(EL,X-xx);PT:=phi(PL);assert N*PT eq ET!0 and PT ne ET!0;
  tr,td:=RecordPoint(ET,PT);assert (d*e)mod td eq 0;Append(~trs,<e,td,d*e div td,tr>);
 end for;assert &+[r[2]*r[3]:r in trs]eq 4*d;
 return sr,trs;
end function;
rr:=[r:r in AuditSources|not r[7]];assert #rr eq 1 and rr[1][1]eq 15;rec:=rr[1];PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];
sr,tr:=Process(E,P,15);printf "S15_SS61_FIRST_TARGET degrees=%o weights=%o\n",[v[2]:v in tr],[v[3]:v in tr];assert #tr eq 1;td:=tr[1][2];rr2:=tr[1][4];FF:=ext<GF(2)|PF!rr2[1]>;EE:=EllipticCurve([FF!PF!a:a in rr2[2]]);PP:=EE![FF!PF!a:a in rr2[3]];sr2,tr2:=Process(EE,PP,td);
SourceRecords:=[*sr,sr2*];SourceHeckeRecords:=[*tr,tr2*];SourceMetadata:=[*<1,15,1,[0,1]>,<2,td,1,[0,1]>*];
// Add all further closed target classes, and their T3 images.
function XYrec(rr)
 RF:=ext<GF(2)|PF!rr[1]>;return RF,[RF!PF!v:v in rr[5]];
end function;
function SameClosed(a,b)
 FA,xa:=XYrec(a);FB,xb:=XYrec(b);da:=LCM([Degree(MinimalPolynomial(v,GF(2))):v in xa]);db:=LCM([Degree(MinimalPolynomial(v,GF(2))):v in xb]);if da ne db then return false;end if;
 // Compare via canonical Frobenius-invariant Tate-coordinate keys.
 return XYKey(xa[1],xa[2])eq XYKey(xb[1],xb[2]);
end function;
for rr2 in [v[4]:v in tr2]do
 if &or[SameClosed(rr2,ss):ss in SourceRecords]then continue;end if;
 FF:=ext<GF(2)|PF!rr2[1]>;EE:=EllipticCurve([FF!PF!a:a in rr2[2]]);PP:=EE![FF!PF!a:a in rr2[3]];EE,PP:=SimplifyPoint(EE,PP);sd:=Degree(BaseRing(EE));newr,newt:=Process(EE,PP,sd);Append(~SourceRecords,newr);Append(~SourceHeckeRecords,newt);Append(~SourceMetadata,<#SourceRecords,sd,1,[0,1]>);
end for;assert #SourceRecords eq 4;
// T5(P15): all six cyclic kernels over F_(2^60), grouped over F_(2^15).
F60:=GF(2^60);fp:=PolynomialRing(F60)!PF!sr[1];r0:=Roots(fp)[1][1];E5:=EllipticCurve([Evaluate(PF!v,r0):v in sr[2]]);P5:=E5![Evaluate(PF!v,r0):v in sr[3]];assert 61*P5 eq E5!0;
RX<X>:=PolynomialRing(F60);f5:=DivisionPolynomial(E5,5);roots5:={v[1]:v in Roots(f5)};assert #roots5 eq 12;f3:=DivisionPolynomial(E5,3);aa:=aInvariants(E5);ks:={RX|};
for x5 in roots5 do x25:=x5+Evaluate(f3,x5)/(aa[1]*x5+aa[3])^2;assert x25 in roots5 and x25 ne x5;Include(~ks,(X-x5)*(X-x25));end for;assert #ks eq 6;
function Frobh(h,e)return Parent(h)![a^(2^e):a in Eltseq(h)];end function;
seen:={RX|};T5Records:=[**];
for h in ks do
 if h in seen then continue;end if;ee:=Min([k:k in[1..4]|Frobh(h,15*k)eq h]);orb:={Frobh(h,15*k):k in[0..ee-1]};assert #orb eq ee;seen join:=orb;
 ET,phi:=IsogenyFromKernel(E5,h);PT:=phi(P5);r5,t5:=RecordPoint(ET,PT);assert (15*ee)mod t5 eq 0;Append(~T5Records,<ee,t5,15*ee div t5,r5>);
end for;assert #seen eq 6 and &+[v[2]*v[3]:v in T5Records]eq 90;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/t5_data.m",Sprintf("T5Records:=%o;",T5Records):Overwrite:=true);
printf "S15_SS61_T5_SOURCE15 target_degrees=%o weights=%o\n",[v[2]:v in T5Records],[v[3]:v in T5Records];
printf "S15_SS61_ACTUAL_HECKE_JETS source_degrees=[15,20] target_degrees=%o weights=%o elapsed=%o\n",[[v[2]:v in vv]:vv in SourceHeckeRecords],[[v[3]:v in vv]:vv in SourceHeckeRecords],Cputime(tt);
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/hecke_jets.m",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",SourceMetadata,SourceRecords,SourceHeckeRecords):Overwrite:=true);
printf "S15_SS61_ACTUAL_HECKE_JETS_COMPLETE N=%o sources=%o elapsed=%o\n",N,#SourceRecords,Cputime(tt);quit;
