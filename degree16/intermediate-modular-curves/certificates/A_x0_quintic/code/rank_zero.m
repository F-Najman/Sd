// Run: magma -b N:=96 verify.m (also N:=98 and N:=100).
// Exhaustive Riemann--Roch certificate for the specialization argument.
load "common.m";
SetColumns(180);
SetSeed(1);
N:=StringToInteger(N);
assert N in [96,98,100];
p:=N eq 96 select 7 else 3;
assert not IsZeroAt(LSeries(JZero(N)),1);
_,checkedF := GoodModel(N,p,N eq 96 select 9 else 7);
C:=ModularCurveQuotient(N,[]);
if N eq 96 then
 coords:=[[0,0,0,0,0,0,0,0,1],[1,0,0,1,-1,-1,0,-1,1],
 [3,3,1,1,3,3,3,0,3],[-1,0,0,1,1,1,0,-1,1],
 [-3,3,1,1,-3,-3,3,0,3],[0,-1,0,0,0,0,0,1,0],
 [0,0,-1,2,0,0,3,0,0],[0,0,1,1,0,0,0,0,0]];
elif N eq 98 then
 coords:=[[1,1,1,-1,-3,-3,2],[2,2,2,5,1,8,4],
 [0,0,0,-1,1,0,0],[0,0,0,0,0,0,1]];
else
 coords:=[[1,-2,1,0,-1,0,1],[2,1,2,-5,3,0,2],[2,1,2,5,3,0,2],
 [0,0,0,0,0,0,1],[0,0,1,0,0,1,0],[0,0,-1,0,0,1,0]];
end if;
pts:=[C!v:v in coords];
Cp:=ChangeRing(C,GF(p));
pp:=[Cp![GF(p)!a:a in v]:v in coords];
assert #Seqset(pp) eq #pp;
F:=AlgorithmicFunctionField(FunctionField(Cp));
assert Genus(F) eq (N eq 96 select 9 else 7);
ps:=[Places(Cp,d):d in [1..5]];
printf "N=%o p=%o genus=%o place_counts=%o rational_lifts=%o\n",N,p,Genus(F),[#s:s in ps],#pp;
if N ne 98 then assert #ps[1] eq #pp; end if;
qds:=[Divisor(Place(P)):P in pts];
pds:=[Divisor(Place(P)):P in pp];
G,rep,cl:=ClassGroup(Cp);
liftclasses:={};
for s in Multisets({1..#pts},4) do
 Dp:=&+[m*pds[i]:i->m in s];
 if Dimension(Dp) lt 2 then continue; end if;
 c:=cl(Dp); if c in liftclasses then continue; end if;
 D:=&+[m*qds[i]:i->m in s];
 assert Dimension(D) eq 2 and Dimension(Dp) eq 2;
 Include(~liftclasses,c);
 printf "lifted degree-4 pencil: %o\n",s;
end for;
assert #liftclasses eq (N eq 96 select 2 else (N eq 98 select 1 else 3));
tested:=0; special:=0; maxdim:=0; poles:={}; classes:={};
for part in Partitions(5) do
 choices:=CartesianProduct([Multisets({1..#ps[d]},Multiplicity(Multiset(part),d)):d in [1..5]]);
 for choice in choices do
  D:=&+[m*Divisor(ps[d][i]):i->m in s,d->s in choice];
  assert Degree(D) eq 5;
  tested+:=1;
  V,mp:=RiemannRochSpace(D); r:=Dimension(V); maxdim:=Max(maxdim,r);
  assert r le 2;
  if r lt 2 then continue; end if;
  special+:=1;
  // For a two-dimensional space containing constants, every nonconstant
  // element has the same pole divisor. Thus one basis element suffices.
  fs:=[mp(v):v in Basis(V)];
  fs:=[f:f in fs|Degree(f) gt 0];
  assert #fs gt 0;
  A:=Denominator(Divisor(fs[1]));
  assert Degree(A) eq 4;
  assert &and[Denominator(Divisor(f)) eq A:f in fs];
  assert cl(A) in liftclasses;
  Include(~poles,A); Include(~classes,cl(D));
 end for;
 printf "partition=%o tested=%o special=%o\n",part,tested,special;
end for;
printf "RESULT N=%o tested=%o special_divisors=%o max_h0=%o degree4_poles=%o W4_classes=%o W5_classes=%o\n",
 N,tested,special,maxdim,#poles,#liftclasses,#classes;
assert tested eq (N eq 96 select 46248 else (N eq 98 select 2088 else 2094));
assert special eq (N eq 96 select 128 else (N eq 98 select 24 else 72));
assert #poles eq (N eq 96 select 16 else (N eq 98 select 4 else 12));
if N ne 98 then
 print "All computational hypotheses of Proposition 5.5 verified.";
else
 print "Hypothesis (5) fails at p=3: four rational lifts, six finite-field points.";
end if;

if N eq 98 then
    // Identify the four supplied rational points as the complete AL cusp orbit.
    _, infinity := CanonicalALMatrix(98,98);
    orbit := {C!infinity};
    for d in [2,49,98] do
        M := CanonicalALMatrix(98,d);
        Include(~orbit,C!Eltseq(M*Matrix(Rationals(),7,1,infinity)));
    end for;
    assert orbit eq Seqset(pts);
    // The two remaining F_3 points cannot lift even as rational Pic^1
    // classes: push down along X_0(98) -> X_0(49), of degree three.
    E := ModularCurveQuotient(49,[]);
    lo,hi := RankBounds(E);
    T := TorsionSubgroup(E);
    assert lo eq 0 and hi eq 0 and #T eq 2;
    E3 := ChangeRing(E,GF(3));
    assert Sort([Order(P):P in Points(E3)]) eq [1,2,4,4];
    assert Order(GF(7)!3) eq 6; // non-rational cusps have residue degree six
end if;
printf "SUCCESS rank_zero N=%o\n",N;
quit;
