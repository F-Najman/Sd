SetQuitOnError(true);SetColumns(0);tt:=Cputime();AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree13/full43/units_data.m";
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree13/full43/hecke_jets.m";
ix:=Index([v[1]:v in SourceMetadata],29);assert ix ne 0;rec:=SourceRecords[ix];PF<t>:=PolynomialRing(GF(2));F<a>:=ext<GF(2)|PF!rec[1]>;assert Degree(F)eq 12;
z:=Vector(F,[F!PF!c:c in rec[4]]);A:=AlphaA11Cotangent;assert Nrows(A)eq genus;D:=DiamondMatrix;
f:=t^12-t^11-5*t^10+6*t^9+9*t^8-16*t^7-3*t^6+19*t^5-3*t^4-12*t^3+t^2+4*t+1;
g:=(35*t^11-65*t^10-107*t^9+314*t^8-34*t^7-580*t^6+601*t^5+156*t^4-552*t^3+219*t^2+136*t-81)/43;
assert IsIrreducible(f);roots:=Roots(PolynomialRing(F)!f);assert #roots eq 12;x:=roots[1][1];y:=Evaluate(g,x);
r:=(x^2*y-x*y+y-1)/(x^2*y-x);ss:=(x*y-y+1)/(x*y);bb:=r*ss*(r-1);cc:=ss*(r-1);EE:=EllipticCurve([1-cc,-bb,-bb,F!0,F!0]);PP:=EE![0,0];assert Discriminant(EE)ne 0 and PP ne EE!0 and 43*PP eq EE!0;
sourcexy:=[F!PF!v:v in rec[5]];direct:=false;
for j in[1..42]do uv:=TateNormalForm_xy(EE,j*PP);for k in[0..11]do if uv eq [v^(2^k):v in sourcexy]then direct:=true;break;end if;end for;if direct then break;end if;end for;assert direct;
print "S13_KNOWN43_DIRECT_TATE_REDUCTION_MATCH_VERIFIED";
RR:=VerticalJoin(Matrix(F,[[F!v[i]+x*v[genus+i]:i in[1..genus]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+y*v[genus+i]:i in[1..genus]]:v in Rows(UnitYRelations)]));assert Rank(RR)eq genus-1;zz:=Eltseq(Basis(Kernel(Transpose(RR)))[1]);ki:=Index([v ne 0:v in zz],true);zz:=[v/zz[ki]:v in zz];
function Normalize(z)
 l:=Eltseq(z);k:=Index([v ne 0:v in l],true);return Vector([v/l[k]:v in l]);end function;
found:=false;foundj:=0;for j in[0..20]do for k in[0..11]do if Normalize(Vector(F,zz)*Transpose(ChangeRing(D^j,F)))eq Vector(F,[v^(2^k):v in Eltseq(z)])then found:=true;foundj:=j;break;end if;end for;if found then break;end if;end for;assert found;
// Irreducibility and prime order of this characteristic-zero point were checked in occurrence43.m.
q1:=Vector(GF(2),[qcoeffs[i,2]:i in[1..genus]]);v:=z*Transpose(ChangeRing(A,F));
mat:=Matrix(GF(2),[[GF(2)!c:c in Eltseq(v[i],GF(2))]:i in[1..genus]]);assert Rank(mat)eq 12;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree13/mixed43_tangents.m","TangentMatrices:=[**];":Overwrite:=true);
for k in[0..20]do
 c:=q1*Transpose(A*D^k);B:=HorizontalJoin(mat,Transpose(Matrix(c)));rk:=Rank(B);printf "S13_MIXED43_FI cusp=%o rank=%o\n",k,rk;assert rk eq 13;PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree13/mixed43_tangents.m",Sprintf("Append(~TangentMatrices,%o);",[Eltseq(v):v in Rows(B)]));
end for;
printf "S13_MIXED43_KNOWN_LIFT_AND_FI_COMPLETE orbit_shift=%o elapsed=%o\n",foundj,Cputime(tt);quit;
