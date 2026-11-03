// Root-allocated elliptic Hecke/jet stage; no function-field normalization.
SetColumns(0);SetQuitOnError(true);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree16/full43/units_data.m";
g:=genus;
Attach("/home/fnajman/degree9_torsion/nonic-torsion/common/fast_hecke.m");
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

RF:=recformat<P:PtEll>;X:=MDX1(43,GF(2));load "work/degree16/sources43.m";
SS:=[**];for rr in AuditSources do
 if rr[7]then continue;end if;PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!rr[2]>;E:=EllipticCurve([F!PF!a:a in rr[3]]);P:=E![F!PF!a:a in rr[4]];pp:=ModuliPoint(X,E,rec<RF|P:=P>);assert Degree(pp)eq rr[1];Append(~SS,pp);
end for;print "S16_NATIVE43_SS_RECONSTRUCTED",[Degree(P):P in SS];
C:=[P:P in Cusps(X)|Degree(P)eq 7];assert #C eq 3;
function B(P)return HeckeOperatorFast(X,3,P)-Divisor(P)-3*Divisor(DiamondOperator(X,3,P));end function;
Ds:=[Divisor(P):P in SS];p:=SS[1];assert Degree(p)eq 7;q:=DiamondOperator(X,3,p);assert q ne p;
inputs:=[*<"SS7",B(p)>,<"2SS7",2*B(p)>,<"SS7pair",B(p)+B(q)>*];
for p in SS do if Degree(p)eq 14 then Append(~inputs,<"SS14",B(p)>);end if;end for;
for ij in[[1,0,0],[2,0,0],[1,1,0]]do
 dc:=&+[ij[k]*Divisor(C[k]):k in[1..3]];
 for shift in[1,2]do bc:=2*(dc-&+[ij[k]*Divisor(C[(k-1+shift)mod 3+1]):k in[1..3]]);Append(~inputs,<"NC7",bc>);end for;
end for;
for k in[1..3]do for l in[1..3]do if k ne l then bc:=2*(Divisor(C[k])-Divisor(C[l]));Append(~inputs,<"SS7NC7",B(SS[1])+bc>);end if;end for;end for;
for dat in inputs do flag:=IsPrincipal(5*dat[2]);printf "S16_NATIVE43_CASE label=%o principal=%o elapsed=%o\n",dat[1],flag,Cputime(tt);end for;print "S16_NATIVE43_COMPLETE";quit;
