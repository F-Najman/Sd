// No positive-dimensional translate survives at these three levels.
// Example: magma -b N:=92 empty_cosets.m
load "common.m";
N := StringToInteger(N);
cases := [<85,7,2,17,34>, <88,9,1,7,7>, <92,10,1,7,7>];
matches := [row:row in cases|row[1] eq N];
assert #matches eq 1;
_,g,dimension,ell,aorder := Explode(matches[1]);
p := 3;
factors,positive := PositiveFactors(N);
assert #positive eq 1 and Dimension(positive[1][1]) eq dimension;
assert #positive[1][2] eq 1 and PointCount(positive[1][1],p) eq aorder;
complement := &*[PointCount(t[1],p)^#t[2]:t in factors
                 |not IsZeroAt(LSeries(t[1]),1)];
assert GCD(ell,complement) eq 1;
C,F := GoodModel(N,p,g);
G,representative,class_map := ClassGroup(F);
H := PrimarySubgroup(G,ell);
assert #H eq ell;
base := Divisor(Places(F,1)[1]);
W,reps,total,W1 := DegreeFiveClasses(F,class_map,base);
assert #WholeCosets(W,H,G) eq 0;
if N eq 92 then
    M := CanonicalALMatrix(92,23);
    w := CoordinateInvolution(ModularCurveQuotient(92,[]),M);
    assert Rank(IdentityMatrix(Rationals(),g)+M) eq 1;
    assert g gt 2*1+4;
end if;
printf "RESULT N=%o p=3 divisors=%o W0=%o subgroup_order=%o whole_cosets=0\n",
       N,total,#W,ell;
printf "SUCCESS empty N=%o\n",N;
quit;
