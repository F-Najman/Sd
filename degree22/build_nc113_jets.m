// Root-allocated elliptic Hecke/jet stage; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree22/full113/units_data.m";
g:=genus;
RXa:=Submatrix(UnitXRelations,1,1,Nrows(UnitXRelations),g);RXb:=Submatrix(UnitXRelations,1,g+1,Nrows(UnitXRelations),g);RYa:=Submatrix(UnitYRelations,1,1,Nrows(UnitYRelations),g);RYb:=Submatrix(UnitYRelations,1,g+1,Nrows(UnitYRelations),g);
function Code(z) if Type(z)eq RngUPolElt then return[Integers()!a:a in Eltseq(z)];end if;return [Integers()!a:a in Eltseq(z,GF(2))];end function;
function SimplifyPoint(E,P)
 F:=BaseRing(E);a1,a2,a3,a4,a6:=Explode(aInvariants(E));if a1 eq 0 then assert a3 ne 0;return E,P;end if;assert a1 eq 1 and a3 eq 0;EE:=EllipticCurve([F!1,a2,F!0,F!0,a6+a4^2]);PP:=EE![P[1],P[2]+a4];assert jInvariant(EE)eq jInvariant(E)and N*PP eq EE!0;assert TateNormalForm_xy(EE,PP)eq TateNormalForm_xy(E,P);return EE,PP;
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
function PsiGeneral(xx,aa)
 a1,a2,a3,a4,a6:=Explode(aa);PS:=Parent(xx);b2:=a1^2;b4:=a1*a3;b6:=a3^2;b8:=a1^2*a6+a1*a3*a4+a2*a3^2+a4^2;v:=a1*xx+a3;
 pp:=[PS!0,PS!1,v,xx^4+b2*xx^3+b4*xx^2+b6*xx+b8,v*(b2*xx^5+b4*xx^4+(b2*b8+b4*b6)*xx+(b4*b8+b6^2))];
 for n in[5..N]do m:=n div 2;if IsOdd(n)then pn:=pp[m+3]*pp[m+1]^3+pp[m]*pp[m+2]^3;else pn:=pp[m+1]/v*(pp[m+3]*pp[m]^2+pp[m-1]*pp[m+2]^2);end if;Append(~pp,pn);end for;return pp[N+1];
end function;
function CanonicalJets(E,P,z0,jprec,LL,uk,selected)
 F:=BaseRing(E);aa:=aInvariants(E);PS<u>:=PowerSeriesRing(F,jprec);xx:=PS!P[1];yy:=PS!P[2];ap:=[PS!a:a in aa];if aa[1]eq 0 then ap[1]+:=u;else ap[5]+:=u;end if;
 PX<X>:=PolynomialRing(F);assert PsiGeneral(X,[PX!a:a in aa])eq DivisionPolynomial(E,N);
 der:=Coefficient(PsiGeneral(xx+u,[PS!a:a in aa]),1);assert der ne 0 and aa[1]*P[1]+aa[3]ne 0;
 for n in[1..jprec-1]do xx+:=(Coefficient(PsiGeneral(xx,ap),n)/der)*u^n;assert Valuation(PsiGeneral(xx,ap))ge n+1;end for;
 for n in[1..jprec-1]do er:=Coefficient(yy^2+ap[1]*xx*yy+ap[3]*yy+xx^3+ap[2]*xx^2+ap[4]*xx+ap[5],n);yy+:=(er/(aa[1]*P[1]+aa[3]))*u^n;assert Valuation(yy^2+ap[1]*xx*yy+ap[3]*yy+xx^3+ap[2]*xx^2+ap[4]*xx+ap[5])ge n+1;end for;
 xy:=UnitValues(ap,xx,yy);RM:=[UnitMatrix(F,Coefficient(xy[1],0),Coefficient(xy[2],0))];
 for n in[1..jprec-1]do Append(~RM,VerticalJoin(Coefficient(xy[1],n)*ChangeRing(RXb,F),Coefficient(xy[2],n)*ChangeRing(RYb,F)));end for;
 ki:=Index([z ne 0:z in z0],true);assert z0[ki]eq 1 and uk eq[i:i in[1..g]|i ne ki];zv:=[Vector(F,z0)];
 for n in[1..jprec-1]do
  br:=Vector(F,[0:i in[1..Nrows(RM[1])]]);for j in[1..n]do br+:=zv[n-j+1]*Transpose(RM[j+1]);end for;ur:=Vector(F,[br[r]:r in selected])*Transpose(LL);zz:=Vector(F,[0:i in[1..g]]);for j in[1..g-1]do zz[uk[j]]:=ur[j];end for;Append(~zv,zz);
 end for;
 for n in[0..jprec-1]do er:=&+[zv[n-j+1]*Transpose(RM[j+1]):j in[0..n]];assert IsZero(er);end for;
 return <[Code(Coefficient(xx,n)):n in[0..jprec-1]],[Code(Coefficient(yy,n)):n in[0..jprec-1]],[[Code(zv[n+1][i]):n in[0..jprec-1]]:i in[1..g]]>;
end function;
function RecordPoint(E,P,GoodRows)
 E,P:=SimplifyPoint(E,P);F:=BaseRing(E);z,xy,LL,uk,selected:=CanonicalPointFast(E,P,GoodRows);d:=LCM([Degree(MinimalPolynomial(x,GF(2))):x in xy]);jprec:=12;assert jprec ge 1;if jprec eq 1 then jt:=<[Code(P[1])],[Code(P[2])],[[Code(a)]:a in z]>;else jt:=CanonicalJets(E,P,z,jprec,LL,uk,selected);end if;assert LCM([Degree(MinimalPolynomial(x,GF(2))):x in z])eq d;
 rec:=<[Integers()!c:c in Eltseq(DefiningPolynomial(F,GF(2)))],[Code(a):a in aInvariants(E)],[Code(P[i]):i in[1,2]],[Code(a):a in z],[Code(a):a in xy],jt>;return rec,d;
end function;

function CanonicalJetsNodal(aa,P,z0,jprec,LL,uk,selected)
 F:=Universe(aa);PS<u>:=PowerSeriesRing(F,jprec);xx:=PS!P[1];yy:=PS!P[2];ap:=[PS!a:a in aa];if aa[1]eq 0 then ap[1]+:=u;else ap[5]+:=u;end if;
 
 der:=Coefficient(PsiGeneral(xx+u,[PS!a:a in aa]),1);assert der ne 0 and aa[1]*P[1]+aa[3]ne 0;
 for n in[1..jprec-1]do xx+:=(Coefficient(PsiGeneral(xx,ap),n)/der)*u^n;assert Valuation(PsiGeneral(xx,ap))ge n+1;end for;
 for n in[1..jprec-1]do er:=Coefficient(yy^2+ap[1]*xx*yy+ap[3]*yy+xx^3+ap[2]*xx^2+ap[4]*xx+ap[5],n);yy+:=(er/(aa[1]*P[1]+aa[3]))*u^n;assert Valuation(yy^2+ap[1]*xx*yy+ap[3]*yy+xx^3+ap[2]*xx^2+ap[4]*xx+ap[5])ge n+1;end for;
 xy:=UnitValues(ap,xx,yy);RM:=[UnitMatrix(F,Coefficient(xy[1],0),Coefficient(xy[2],0))];
 for n in[1..jprec-1]do Append(~RM,VerticalJoin(Coefficient(xy[1],n)*ChangeRing(RXb,F),Coefficient(xy[2],n)*ChangeRing(RYb,F)));end for;
 ki:=Index([z ne 0:z in z0],true);assert z0[ki]eq 1 and uk eq[i:i in[1..g]|i ne ki];zv:=[Vector(F,z0)];
 for n in[1..jprec-1]do
  br:=Vector(F,[0:i in[1..Nrows(RM[1])]]);for j in[1..n]do br+:=zv[n-j+1]*Transpose(RM[j+1]);end for;ur:=Vector(F,[br[r]:r in selected])*Transpose(LL);zz:=Vector(F,[0:i in[1..g]]);for j in[1..g-1]do zz[uk[j]]:=ur[j];end for;Append(~zv,zz);
 end for;
 for n in[0..jprec-1]do er:=&+[zv[n-j+1]*Transpose(RM[j+1]):j in[0..n]];assert IsZero(er);end for;
 return <[Code(Coefficient(xx,n)):n in[0..jprec-1]],[Code(Coefficient(yy,n)):n in[0..jprec-1]],[[Code(zv[n+1][i]):n in[0..jprec-1]]:i in[1..g]]>;
end function;

load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree22/relative113_nc_data.m";
PF:=PolynomialRing(GF(2));F<a>:=ext<GF(2)|PF!Relative113NCField>;zeta:=F!PF!Relative113NCZeta;assert Order(zeta)eq 113;
aa:=[F!1,F!0,F!0,F!0,F!0];P:=[zeta/(1+zeta)^2,zeta^2/(1+zeta)^3];xy:=UnitValues(aa,P[1],P[2]);R0:=UnitMatrix(F,xy[1],xy[2]);assert Rank(R0)eq g-1;
z:=[F!PF!v:v in Relative113NCZ];assert IsZero(Vector(F,z)*Transpose(R0));ki:=Index([v ne 0:v in z],true);assert z[ki]eq 1;
EF0:=EchelonForm(Transpose(R0));assert IsZero(EF0[g]);selected:=[Min([j:j in[1..Ncols(EF0)]|EF0[i,j]ne 0]):i in[1..g-1]];uk:=[i:i in[1..g]|i ne ki];LL:=Submatrix(R0,selected,uk)^(-1);
jt:=CanonicalJetsNodal(aa,P,z,8,LL,uk,selected);
for row in jt[3]do for v in row do x:=F!PF!v;assert x^(2^14)eq x;end for;end for;
assert &or[(F!PF!row[2])ne 0:row in jt[3]];
rec:=<[Integers()!c:c in Eltseq(DefiningPolynomial(F,GF(2)))],[Code(v):v in aa],[Code(v):v in P],[Code(v):v in z],[Code(v):v in xy],jt>;
SourceMetadata:=[*<1,14,4,[0,1]>*];SourceRecords:=[*rec*];
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree22/nc113_jets.m",Sprintf("SourceMetadata:=%o;SourceRecords:=%o;",SourceMetadata,SourceRecords):Overwrite:=true);
printf "S22_NC113_CUSP_JETS_COMPLETE degree14 ambient28 jets8 elapsed=%o\n",Cputime(tt);quit;
