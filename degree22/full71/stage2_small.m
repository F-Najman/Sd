// Root-allocated elliptic Hecke/jet stage; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree22/full71/units_data.m";
g:=genus;
RXa:=Submatrix(UnitXRelations,1,1,Nrows(UnitXRelations),g);RXb:=Submatrix(UnitXRelations,1,g+1,Nrows(UnitXRelations),g);RYa:=Submatrix(UnitYRelations,1,1,Nrows(UnitYRelations),g);RYb:=Submatrix(UnitYRelations,1,g+1,Nrows(UnitYRelations),g);
function Code(z) if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return [Integers()!a:a in Eltseq(z,GF(2))];end function;
function SimplifyPoint(E,P)
 F:=BaseRing(E);a1,a2,a3,a4,a6:=Explode(aInvariants(E));assert a1 eq 1 and a3 eq 0;EE:=EllipticCurve([F!1,a2,F!0,F!0,a6+a4^2]);PP:=EE![P[1],P[2]+a4];assert jInvariant(EE)eq jInvariant(E)and N*PP eq EE!0;assert TateNormalForm_xy(EE,PP)eq TateNormalForm_xy(E,P);return EE,PP;
end function;
function UnitValues(aa,xx,yy)
 a1,a2,a3,a4,a6:=Explode(aa);aa3:=2*yy+a3+a1*xx;aa2:=3*xx+a2;aa4:=3*xx^2+2*xx*a2+a4-a1*yy;aaa1:=2*aa4/aa3+a1;aaa2:=aa2-(aa4/aa3)^2-a1*aa4/aa3;b:=-aaa2^3/aa3^2;c:=-(aaa1*aaa2-aa3)/aa3;r:=b/c;s:=c^2/(b-c);t:=r*s-2*r+1;return[(s-r)/t,t/(s^2-s-r+1)];
end function;
function UnitMatrix(F,x0,y0)
 return VerticalJoin(ChangeRing(RXa,F)+x0*ChangeRing(RXb,F),ChangeRing(RYa,F)+y0*ChangeRing(RYb,F));
end function;
function CanonicalPoint(E,P)
 F:=BaseRing(E);xy:=TateNormalForm_xy(E,P);RR:=UnitMatrix(F,xy[1],xy[2]);assert Rank(RR)eq g-1;zz:=Eltseq(Basis(Kernel(Transpose(RR)))[1]);ki:=Index([z ne 0:z in zz],true);return[z/zz[ki]:z in zz],xy;
end function;
function CanonicalPointFast(E,P,GoodRows)
 F:=BaseRing(E);xy:=TateNormalForm_xy(E,P);RR:=UnitMatrix(F,xy[1],xy[2]);uk:=[2..g];selected:=GoodRows;ok:=true;
 try LL:=Submatrix(RR,selected,uk)^(-1);catch err ok:=false;end try;
 if ok then
  br:=Vector(F,[RR[r,1]:r in selected]);ur:=br*Transpose(LL);z:=[F!1]cat Eltseq(ur);assert IsZero(Vector(F,z)*Transpose(RR));
 else
  assert Rank(RR)eq g-1;z:=Eltseq(Basis(Kernel(Transpose(RR)))[1]);ki:=Index([a ne 0:a in z],true);z:=[a/z[ki]:a in z];uk:=[i:i in[1..g]|i ne ki];selected:=[1..Nrows(RR)];M0:=Submatrix(RR,selected,uk);LL:=Solution(M0,IdentityMatrix(F,g-1));assert LL*M0 eq IdentityMatrix(F,g-1);
 end if;
 return z,xy,LL,uk,selected;
end function;
function PsiN(xx,aa6)
 PS:=Parent(xx);pp:=[PS!0,PS!1,xx,xx^4+xx^3+aa6,xx^6+aa6*xx^2];
 for n in[5..N]do m:=n div 2;if IsOdd(n)then pn:=pp[m+3]*pp[m+1]^3+pp[m]*pp[m+2]^3;else pn:=pp[m+1]/xx*(pp[m+3]*pp[m]^2+pp[m-1]*pp[m+2]^2);end if;Append(~pp,pn);end for;return pp[N+1];
end function;
function CanonicalJets(E,P,z0,jprec,LL,uk,selected)
 F:=BaseRing(E);aa:=aInvariants(E);assert aa[1]eq 1 and aa[3]eq 0 and aa[4]eq 0;PS<u>:=PowerSeriesRing(F,jprec);xx:=PS!P[1];yy:=PS!P[2];a2:=aa[2];a6:=PS!aa[5]+u;der:=Coefficient(PsiN(xx+u,PS!aa[5]),1);assert der ne 0 and P[1]ne 0;
 for n in[1..jprec-1]do xx+:=(Coefficient(PsiN(xx,a6),n)/der)*u^n;assert Valuation(PsiN(xx,a6))ge n+1;end for;
 for n in[1..jprec-1]do er:=Coefficient(yy^2+xx*yy+xx^3+a2*xx^2+a6,n);yy+:=(er/P[1])*u^n;assert Valuation(yy^2+xx*yy+xx^3+a2*xx^2+a6)ge n+1;end for;
 xy:=UnitValues([PS!1,PS!a2,PS!0,PS!0,a6],xx,yy);RM:=[UnitMatrix(F,Coefficient(xy[1],0),Coefficient(xy[2],0))];
 for n in[1..jprec-1]do Append(~RM,VerticalJoin(Coefficient(xy[1],n)*ChangeRing(RXb,F),Coefficient(xy[2],n)*ChangeRing(RYb,F)));end for;
 ki:=Index([z ne 0:z in z0],true);assert z0[ki]eq 1 and uk eq[i:i in[1..g]|i ne ki];zv:=[Vector(F,z0)];
 for n in[1..jprec-1]do
  br:=Vector(F,[0:i in[1..Nrows(RM[1])]]);for j in[1..n]do br+:=zv[n-j+1]*Transpose(RM[j+1]);end for;ur:=Vector(F,[br[r]:r in selected])*Transpose(LL);zz:=Vector(F,[0:i in[1..g]]);for j in[1..g-1]do zz[uk[j]]:=ur[j];end for;Append(~zv,zz);
 end for;
 for n in[0..jprec-1]do er:=&+[zv[n-j+1]*Transpose(RM[j+1]):j in[0..n]];assert IsZero(er);end for;
 return <[Code(Coefficient(xx,n)):n in[0..jprec-1]],[Code(Coefficient(yy,n)):n in[0..jprec-1]],[[Code(zv[n+1][i]):n in[0..jprec-1]]:i in[1..g]]>;
end function;
function RecordPoint(E,P,GoodRows)
 E,P:=SimplifyPoint(E,P);F:=BaseRing(E);z,xy,LL,uk,selected:=CanonicalPointFast(E,P,GoodRows);d:=LCM([Degree(MinimalPolynomial(x,GF(2))):x in xy]);jprec:=Min(N in[59,61,71,73,97,101]select 16 else 8,672 div d);assert jprec ge 1;if jprec eq 1 then jt:=<[Code(P[1])],[Code(P[2])],[[Code(a)]:a in z]>;else jt:=CanonicalJets(E,P,z,jprec,LL,uk,selected);end if;assert LCM([Degree(MinimalPolynomial(x,GF(2))):x in z])eq d;
 rec:=<[Integers()!c:c in Eltseq(DefiningPolynomial(F,GF(2)))],[Code(a):a in aInvariants(E)],[Code(P[i]):i in[1,2]],[Code(a):a in z],[Code(a):a in xy],jt>;return rec,d;
end function;

load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree22/sources71.m";assert AuditN eq N;
rr0:=AuditSources[StringToInteger(Start)];PF0:=PolynomialRing(GF(2));F0:=ext<GF(2)|PF0!rr0[2]>;E0:=EllipticCurve([F0!PF0!a:a in rr0[3]]);P0:=E0![F0!PF0!a:a in rr0[4]];xy0:=TateNormalForm_xy(E0,P0);R0:=UnitMatrix(F0,xy0[1],xy0[2]);EF0:=EchelonForm(Transpose(R0));assert IsZero(EF0[g]);GoodRows:=[Min([j:j in[1..Ncols(EF0)]|EF0[i,j]ne 0]):i in[1..g-1]];assert #Seqset(GoodRows)eq g-1;
SourceRecords:=[**];SourceHeckeRecords:=[**];SourceMetadata:=[**];
for si in[StringToInteger(Start)..Min(StringToInteger(End),#AuditSources)]do
 rec:=AuditSources[si];if not rec[7]or si notin [16, 17, 18, 19, 20, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138] then continue;end if;
 PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];assert N*P eq E!0 and P ne E!0;
 E,P:=SimplifyPoint(E,P);sr,sd:=RecordPoint(E,P,GoodRows);d:=rec[1];assert sd eq d;Append(~SourceRecords,sr);Append(~SourceMetadata,<si,d,rec[6],rec[5]>);
 fq:=DivisionPolynomial(E,3);fac:=Factorization(fq);assert Degree(fq)eq 4 and IsSquarefree(fq)and &+[Degree(a[1]):a in fac]eq 4;
 trs:=[**];for ff in fac do
  h:=ff[1];e:=Degree(h);if e eq 1 then L:=F;xx:=-Coefficient(h,0)/Coefficient(h,1);else L:=ext<F|h>;xx:=L.1;end if;
  EL:=EllipticCurve([L!a:a in aInvariants(E)]);PL:=EL![L!P[1],L!P[2]];PX<X>:=PolynomialRing(L);ET,phi:=IsogenyFromKernel(EL,X-xx);PT:=phi(PL);assert N*PT eq ET!0 and PT ne ET!0;
  tr,td:=RecordPoint(ET,PT,GoodRows);assert (d*e)mod td eq 0;Append(~trs,<e,td,d*e div td,tr>);
 end for;assert &+[r[2]*r[3]:r in trs]eq 4*d;Append(~SourceHeckeRecords,trs);
 printf "AUDIT_ACTUAL_HECKE_JETS_SOURCE N=%o source=%o degree=%o orbit=%o target_degrees=%o weights=%o elapsed=%o\n",N,si,d,rec[6],[r[2]:r in trs],[r[3]:r in trs],Cputime(tt);
end for;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree22/full71/small_jets_" cat Start cat ".m",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",SourceMetadata,SourceRecords,SourceHeckeRecords):Overwrite:=true);
printf "AUDIT_ACTUAL_HECKE_JETS_COMPLETE N=%o sources=%o elapsed=%o\n",N,#SourceRecords,Cputime(tt);quit;
