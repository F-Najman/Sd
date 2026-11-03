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
 A:=(D^3-I)*(T-D^k-(GF(2)!q)*I);assert A*D eq D*A;
 B:=V*A;assert B*D^9 eq B;Append(~AA,B);Append(~Qs,q);
end for;assert #AA ge 2;
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");load "work/degree21/sources127.m";r:=AuditSources[23];assert r[1]eq 14 and r[6]eq 3 and not r[7];PF:=PolynomialRing(GF(2));F:=ext<GF(2)|PF!r[2]>;E:=EllipticCurve([F!PF!a:a in r[3]]);P:=E![F!PF!a:a in r[4]];xy:=TateNormalForm_xy(E,P);
R:=VerticalJoin(Matrix(F,[[F!v[i]+xy[1]*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+xy[2]*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)]));assert Rank(R)eq g-1;z:=Basis(Kernel(Transpose(R)))[1];ki:=Min([i:i in[1..g]|z[i]ne 0]);z/:=z[ki];
w:=z*Transpose(ChangeRing(D^21,F));assert w/w[ki]eq z;bb:=PrimitiveElement(F)^ExactQuotient(#F-1,3);assert Order(bb)eq 3;SS:=[**];RC:=[**];
for k in[0..2]do
 zk:=z*Transpose(ChangeRing(D^k,F));vz:=zk*Transpose(ChangeRing(V,F));den:=Rep([a:a in Eltseq(vz)|a ne 0]);M:=ZeroMatrix(GF(2),0,2);
 for B in AA do
  vals:=[a/den:a in Eltseq(zk*Transpose(ChangeRing(B,F)))];assert &and[a^4 eq a:a in vals];cs:=[Index([F!0,F!1,bb,bb+1],a)-1:a in vals];assert &and[c ge 0:c in cs];M:=VerticalJoin(M,Matrix(GF(2),[[c mod 2,c div 2]:c in cs]));
 end for;assert Rank(M)eq 2;Append(~SS,[Eltseq(v):v in Rows(M)]);
end for;
for k in[0..8]do M:=ZeroMatrix(GF(2),0,1);for B in AA do M:=VerticalJoin(M,B*D^k*Submatrix(qcoeffs,1,2,g,1));end for;Append(~RC,[Eltseq(v):v in Rows(M)]);end for;
for M in SS do for N in RC do assert Rank(HorizontalJoin(Matrix(GF(2),M),Matrix(GF(2),N)))eq 3;end for;end for;
PrintFile("work/degree21/quotient127_ss_data.m",Sprintf("Q127SS:=%o;Q127SSCusps:=%o;Q127SSPrimes:=%o;Q127SSField:=%o;Q127SSZ:=%o;Q127SSOmega:=%o;",SS,RC,Qs,[Integers()!a:a in Eltseq(DefiningPolynomial(F))],[[Integers()!a:a in Eltseq(v)]:v in Eltseq(z)],[Integers()!a:a in Eltseq(bb)]):Overwrite:=true);
print "S21_QUOTIENT127_SS_RELATIVE_ALL27_RANK3_CERTIFIED";quit;
