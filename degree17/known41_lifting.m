SetQuitOnError(true);SetColumns(0);tt:=Cputime();AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree17/full41/units_data.m";
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree17/full41/hecke_jets.m";
ix:=Index([v[1]:v in SourceMetadata],79);assert ix ne 0;rec:=SourceRecords[ix];PF<t>:=PolynomialRing(GF(2));F<a>:=ext<GF(2)|PF!rec[1]>;assert Degree(F)eq 14;
z:=Vector(F,[F!PF!c:c in rec[4]]);D:=DiamondMatrix;cut:=(41^2-1)div 12;C:=Submatrix(qcoeffs,1,1,genus,cut+1);assert Rank(C)eq genus;AA:=[];
for q in[3,5,7]do
 log:=Min([k:k in[0..19]|DiamondRoot^k mod 41 in[q,41-q]]);DQ:=D^log*qcoeffs;
 TQ:=Matrix(GF(2),[[qcoeffs[i,q*n+1]+(n mod q eq 0 select DQ[i,n div q+1]else 0):n in[0..cut]]:i in[1..genus]]);T:=Solution(C,TQ);assert T*C eq TQ;A:=T-D^log-IdentityMatrix(GF(2),genus);assert A*D eq D*A;Append(~AA,A);
end for;
f:=((1)*t^0+(5)*t^1+(0)*t^2+(-23)*t^3+(-4)*t^4+(56)*t^5+(1)*t^6+(-80)*t^7+(24)*t^8+(61)*t^9+(-43)*t^10+(-11)*t^11+(21)*t^12+(-8)*t^13+(1)*t^14);
g:=((-36881/2813)*t^0+(-127126/2813)*t^1+(215600/2813)*t^2+(535187/2813)*t^3+(-739371/2813)*t^4+(-974129/2813)*t^5+(1568080/2813)*t^6+(560225/2813)*t^7+(-1851704/2813)*t^8+(625052/2813)*t^9+(662254/2813)*t^10+(-637367/2813)*t^11+(208418/2813)*t^12+(-24162/2813)*t^13);
assert IsIrreducible(f);roots:=Roots(PolynomialRing(F)!f);assert #roots eq 14;x:=roots[1][1];y:=Evaluate(g,x);
r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);bb:=r*ss*(r-1);cc:=ss*(r-1);EE:=EllipticCurve([1-cc,-bb,-bb,F!0,F!0]);PP:=EE![0,0];assert Discriminant(EE)ne 0 and PP ne EE!0 and 41*PP eq EE!0;
sourcexy:=[F!PF!v:v in rec[5]];direct:=false;
for j in[1..40]do uv:=TateNormalForm_xy(EE,j*PP);for k in[0..13]do if uv eq [v^(2^k):v in sourcexy]then direct:=true;break;end if;end for;if direct then break;end if;end for;assert direct;
print "S17_KNOWN41_DIRECT_TATE_REDUCTION_MATCH_VERIFIED";
RR:=VerticalJoin(Matrix(F,[[F!v[i]+x*v[genus+i]:i in[1..genus]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+y*v[genus+i]:i in[1..genus]]:v in Rows(UnitYRelations)]));assert Rank(RR)eq genus-1;zz:=Eltseq(Basis(Kernel(Transpose(RR)))[1]);ki:=Index([v ne 0:v in zz],true);zz:=[v/zz[ki]:v in zz];
function Normalize(z)
 l:=Eltseq(z);k:=Index([v ne 0:v in l],true);return Vector([v/l[k]:v in l]);end function;
found:=false;foundj:=0;for j in[0..19]do for k in[0..13]do if Normalize(Vector(F,zz)*Transpose(ChangeRing(D^j,F)))eq Vector(F,[v^(2^k):v in Eltseq(z)])then found:=true;foundj:=j;break;end if;end for;if found then break;end if;end for;assert found;
// Irreducibility and prime order of this characteristic-zero point were checked in occurrence43.m.
q1:=Vector(GF(2),[qcoeffs[i,2]:i in[1..genus]]);q2:=Vector(GF(2),[qcoeffs[i,3]:i in[1..genus]]);
out:="work/degree17/known41_tangents.m";PrintFile(out,"TangentMatrices:=[**];":Overwrite:=true);cnt:=0;
q3:=Vector(GF(2),[qcoeffs[i,4]:i in[1..genus]]);
for k in[0..19]do for l in[k..19]do for mm in[l..19]do
 B:=ZeroMatrix(GF(2),0,17);
 for A in AA do
  v:=z*Transpose(ChangeRing(A,F));mat:=Matrix(GF(2),[[GF(2)!c:c in Eltseq(v[i],GF(2))]:i in[1..genus]]);
  c1:=q1*Transpose(A*D^k);c2:=(k eq l select q2 else q1)*Transpose(A*D^l);c3:=(k eq mm select q3 else(l eq mm select q2 else q1))*Transpose(A*D^mm);
  B:=VerticalJoin(B,HorizontalJoin(HorizontalJoin(HorizontalJoin(mat,Transpose(Matrix(c1))),Transpose(Matrix(c2))),Transpose(Matrix(c3))));
 end for;assert Rank(B)eq 17;cnt+:=1;PrintFile(out,Sprintf("Append(~TangentMatrices,%o);",[Eltseq(v):v in Rows(B)]));
end for;end for;end for;assert cnt eq 1540;printf "S17_KNOWN41_LIFT_AND_FI_COMPLETE cusp_configurations=%o elapsed=%o\n",cnt,Cputime(tt);quit;
