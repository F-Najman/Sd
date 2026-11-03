// Two-prime sieve of the non-smooth or base-point-free W^1_5 classes.
load "common.m";
SetColumns(180); SetSeed(1);
coords:=[[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,1],[-1,-1,0,1,0,0,1,0]];

CQ := ModularCurveQuotient(74,[]);
_, infinity := CanonicalALMatrix(74,74);
orbit := {CQ!infinity};
for d in [2,37,74] do
    M := CanonicalALMatrix(74,d);
    Include(~orbit,CQ!Eltseq(M*Matrix(Rationals(),8,1,infinity)));
end for;
assert orbit eq {CQ!v:v in coords};
factors,positive := PositiveFactors(74);
assert #positive eq 1 and Dimension(positive[1][1]) eq 1 and #positive[1][2] eq 2;
assert PointCount(positive[1][1],3) eq 7;
assert PointCount(positive[1][1],5) eq 8;
bounds := [&*[PointCount(t[1],q)^#t[2]:t in factors |
              not IsZeroAt(LSeries(t[1]),1)] : q in [3,5,7,11,13,17,19,23,29,31]];
assert GCD(bounds) eq 513;
Z:=FreeAbelianGroup(3); labels:=[]; remaining:={};
for p in [3,5] do
 C:=ChangeRing(ModularCurveQuotient(74,[]),GF(p)); F:=AlgorithmicFunctionField(FunctionField(C)); g:=Genus(F);
 assert g eq 8 and IsIrreducible(C) and IsReduced(C) and ArithmeticGenus(C) eq g;
 G,rep,cl:=ClassGroup(C); iv:=Invariants(G);
 ds:=[Divisor(Place(C![GF(p)!a:a in v])):v in coords];
 cgens:=[cl(ds[i]-ds[1]):i in [2..4]]; cm:=hom<Z->G|cgens>; CG:=sub<G|cgens>;
 assert #CG eq 513;
 if #labels eq 0 then labels:=[(G!c)@@cm:c in CG]; end if;
 ell:=p eq 3 select 7 else 2;
 H:=sub<G|[(iv[i] div ell^Valuation(iv[i],ell))*G.i:i in [1..#iv]|iv[i] ne 0]>;
 assert #H eq (p eq 3 select 49 else 256);
 assert #(H meet CG) eq 1;
 eligible:=sub<G|cgens cat [G!h:h in Generators(H)]>;
 ps:=[Places(C,d):d in [1..5]]; K:=CanonicalDivisor(C); poles:={}; bad:={};
 for part in Partitions(5) do
  choices:=CartesianProduct([Multisets({1..#ps[d]},Multiplicity(Multiset(part),d)):d in [1..5]]);
  for choice in choices do
   D:=&+[e*Divisor(ps[d][i]):i->e in s,d->s in choice];
   V,mp:=RiemannRochSpace(D); assert Dimension(V) le 2;
   if Dimension(V) lt 2 then continue; end if;
   A:=0*D; for v in Basis(V) do f:=mp(v); if f ne 0 then A:=LCM(A,Denominator(Divisor(f))); end if; end for;
   assert Degree(A) in [4,5];
   if Degree(A) eq 4 then Include(~poles,A); end if;
   c:=cl(D-5*ds[1]);
   if c in eligible and (Degree(A) eq 5 or 8-g+Dimension(K-D-A) ne 1) then Include(~bad,c); end if;
  end for;
 end for;
 assert #poles eq p+1;
 A:=Rep(poles); assert &and[Dimension(A-B) eq 1:B in poles];
 candidates:={i:i->z in labels|&or[cm(z)+G!h in bad:h in H]};
 assert #candidates eq 2;
 printf "p=%o eligible_primary_group=%o bad_classes=%o cusp_labels=%o\n",p,#H,#bad,[Eltseq(labels[i]):i in Sort(Setseq(candidates))];
 if p eq 3 then remaining:=candidates; else remaining meet:=candidates; end if;
end for;
assert #remaining eq 0;
print "SUCCESS pencils74";
quit;
