// Root-allocated elliptic Hecke/jet stage; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree14/full127/units_data.m";
g:=genus;
function Code(z) if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return [Integers()!a:a in Eltseq(z,GF(2))];end function;
function SimplifyPoint(E,P)return E,P;end function;
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

load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree14/sources127.m";assert AuditN eq N;
SourceRecords:=[**];SourceHeckeRecords:=[**];SourceMetadata:=[**];
for si in[1..#AuditSources]do
 rec:=AuditSources[si];if rec[7]then continue;end if;
 PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rec[2]>;E:=EllipticCurve([F!PF!a:a in rec[3]]);P:=E![F!PF!a:a in rec[4]];assert N*P eq E!0 and P ne E!0;
 E,P:=SimplifyPoint(E,P);sr,sd:=RecordPoint(E,P);d:=rec[1];assert sd eq d;Append(~SourceRecords,sr);Append(~SourceMetadata,<si,d,rec[6],rec[5]>);
 fq:=DivisionPolynomial(E,3);fac:=Factorization(fq);assert Degree(fq)eq 4 and IsSquarefree(fq)and &+[Degree(a[1]):a in fac]eq 4;
 trs:=[**];for ff in fac do
  h:=ff[1];e:=Degree(h);if e eq 1 then L:=F;xx:=-Coefficient(h,0)/Coefficient(h,1);else L:=ext<F|h>;xx:=L.1;end if;
  EL:=EllipticCurve([L!a:a in aInvariants(E)]);PL:=EL![L!P[1],L!P[2]];PX<X>:=PolynomialRing(L);ET,phi:=IsogenyFromKernel(EL,X-xx);PT:=phi(PL);assert N*PT eq ET!0 and PT ne ET!0;
  tr,td:=RecordPoint(ET,PT);assert (d*e)mod td eq 0;Append(~trs,<e,td,d*e div td,tr>);
 end for;assert &+[r[2]*r[3]:r in trs]eq 4*d;Append(~SourceHeckeRecords,trs);
 printf "AUDIT_ACTUAL_HECKE_JETS_SOURCE N=%o source=%o degree=%o orbit=%o target_degrees=%o weights=%o elapsed=%o\n",N,si,d,rec[6],[r[2]:r in trs],[r[3]:r in trs],Cputime(tt);
end for;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree14/full127/hecke_jets.m",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;SourceHeckeRecords:=%o;",SourceMetadata,SourceRecords,SourceHeckeRecords):Overwrite:=true);
printf "AUDIT_ACTUAL_HECKE_JETS_COMPLETE N=%o sources=%o elapsed=%o\n",N,#SourceRecords,Cputime(tt);quit;
