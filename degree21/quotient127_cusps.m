SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);tt:=Cputime();
load "work/degree21/full127/units_data.m";
g:=genus;D:=DiamondMatrix;I:=IdentityMatrix(GF(2),g);m:=63;V:=BasisMatrix(Kernel(D^9-I));assert Nrows(V)eq 88;assert V*D^9 eq V;
AA:=[* *];Qs:=[];
for q in[2,3,5]do
 cut:=Min((127^2-1)div 12,(precision-1)div q);C:=Submatrix(qcoeffs,1,1,g,cut+1);if Rank(C)lt g then continue;end if;
 k:=Min([k:k in[0..62]|DiamondRoot^k mod 127 in[q,127-q]]);DQ:=D^k*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select(GF(2)!q)*DQ[i,n div q+1]else 0):n in[0..cut]]:i in[1..g]]);T:=Solution(C,TQ);assert T*C eq TQ;
 // Both Eisenstein factors kill all cusps. The first also annihilates
 // rational torsion. In characteristic2 the odd-q factors coincide.
 A:=(D-I)*(T-D^k-(GF(2)!q)*I)*(T-I-(GF(2)!q)*D^k);assert A*D eq D*A;
 B:=V*A;assert B*D^9 eq B;Append(~AA,B);Append(~Qs,q);
end for;assert #AA ge 2;
function UnitValues(aa,xx,yy)
 a1,a2,a3,a4,a6:=Explode(aa);aa3:=2*yy+a3+a1*xx;aa2:=3*xx+a2;aa4:=3*xx^2+2*xx*a2+a4-a1*yy;aaa1:=2*aa4/aa3+a1;aaa2:=aa2-(aa4/aa3)^2-a1*aa4/aa3;b:=-aaa2^3/aa3^2;c:=-(aaa1*aaa2-aa3)/aa3;r:=b/c;s:=c^2/(b-c);t:=r*s-2*r+1;return[(s-r)/t,t/(s^2-s-r+1)];
end function;
K<a>:=GF(2^7);assert Order(a)eq 127;PS<u>:=PowerSeriesRing(K,3);xx:=PS!(a/(1+a)^2);yy:=PS!(a^2/(1+a)^3);s1:=PS!0;a6:=PS!0;
for n in[1..2]do
 z:=u^n*a;w:=u^n/a;xx+:=z/(1+z)^2+w/(1+w)^2;yy+:=z^2/(1+z)^3+w/(1+w)^3;
 s1+:=(K!n)*u^n/(1+u^n);a6+:=(K!((5*n^3+7*n^5)div 12))*u^n/(1+u^n);
end for;yy+:=s1;assert Valuation(yy^2+xx*yy+xx^3+s1*xx+a6)ge 3;
uv:=UnitValues([PS!1,PS!0,PS!0,s1,a6],xx,yy);
RXa:=ChangeRing(Submatrix(UnitXRelations,1,1,Nrows(UnitXRelations),g),K);RXb:=ChangeRing(Submatrix(UnitXRelations,1,g+1,Nrows(UnitXRelations),g),K);RYa:=ChangeRing(Submatrix(UnitYRelations,1,1,Nrows(UnitYRelations),g),K);RYb:=ChangeRing(Submatrix(UnitYRelations,1,g+1,Nrows(UnitYRelations),g),K);
R0:=VerticalJoin(RXa+Coefficient(uv[1],0)*RXb,RYa+Coefficient(uv[2],0)*RYb);assert Rank(R0)eq g-1;
z0:=Basis(Kernel(Transpose(R0)))[1];ki:=Min([i:i in[1..g]|z0[i]ne 0]);z0/:=z0[ki];uk:=[i:i in[1..g]|i ne ki];EF:=EchelonForm(Transpose(R0));sel:=[Min([j:j in[1..Ncols(EF)]|EF[i,j]ne 0]):i in[1..g-1]];L:=Submatrix(R0,sel,uk)^(-1);
RM:=[R0]cat[VerticalJoin(Coefficient(uv[1],n)*RXb,Coefficient(uv[2],n)*RYb):n in[1..2]];Z:=[Vector(K,Eltseq(z0))];
for n in[1..2]do
 br:=&+[Z[n-j+1]*Transpose(RM[j+1]):j in[1..n]];ur:=Vector(K,[br[r]:r in sel])*Transpose(L);zz:=Vector(K,[0:i in[1..g]]);for j in[1..g-1]do zz[uk[j]]:=ur[j];end for;Append(~Z,zz);
end for;
for n in[0..2]do assert IsZero(&+[Z[n-j+1]*Transpose(RM[j+1]):j in[0..n]]);end for;
zseries:=[PS![Z[n+1][i]:n in[0..2]]:i in[1..g]];NC:=[* *];RC:=[* *];
for k in[0..8]do
 zk:=Vector(PS,zseries)*Transpose(ChangeRing(D^k,PS));vk:=zk*Transpose(ChangeRing(V,PS));ii:=Min([i:i in[1..#Eltseq(vk)]|Valuation(vk[i])eq 0]);den:=vk[ii];
 J:=ZeroMatrix(GF(2),0,3);
 for B in AA do
  v:=zk*Transpose(ChangeRing(B,PS));J:=VerticalJoin(J,Matrix(GF(2),[[GF(2)!Coefficient(v[i]/den,n):n in[0..2]]:i in[1..Nrows(B)]]));
 end for;Append(~NC,[Eltseq(r):r in Rows(J)]);
 QJ:=ZeroMatrix(GF(2),0,3);for B in AA do QJ:=VerticalJoin(QJ,B*D^k*Submatrix(qcoeffs,1,2,g,3));end for;Append(~RC,[Eltseq(r):r in Rows(QJ)]);
end for;
PrintFile("work/degree21/quotient127_cusps_data.m",Sprintf("Q127Genus:=%o;Q127HeckePrimes:=%o;Q127InvariantBasis:=%o;Q127RC:=%o;Q127NC:=%o;Q127NCPolynomial:=%o;Q127Zeta:=%o;Q127NCJets:=%o;",88,Qs,[Eltseq(r):r in Rows(V)],RC,NC,[Integers()!c:c in Eltseq(DefiningPolynomial(K))],[Integers()!c:c in Eltseq(a)],[[[Integers()!c:c in Eltseq(Z[n+1][i])]:n in[0..2]]:i in[1..g]]):Overwrite:=true);
print "S21_QUOTIENT127_ALL_CUSP_JETS_EXPORTED",Cputime(tt);quit;
