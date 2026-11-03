// Formal W^1_5 test for 77,85,88.
// A Q-degree-four pencil exists by the published gonality theorem.
// The unique finite-field pencil class identifies its reduction.
load "common.m";
N := StringToInteger(N);
assert N in [77,85,88];
p := N eq 77 select 5 else (N eq 85 select 7 else 3);
g := N eq 88 select 9 else 7;
C,F := GoodModel(N,p,g);
places := [Places(F,d):d in [1..5]];
K := CanonicalDivisor(F);
poles := {};
total := 0;
special := 0;
for partition in Partitions(5) do
    choices := CartesianProduct([
        Multisets({1..#places[d]},Multiplicity(Multiset(partition),d))
        :d in [1..5]
    ]);
    for choice in choices do
        D := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        total +:= 1;
        V,to_function := RiemannRochSpace(D);
        assert Dimension(V) le 2;
        if Dimension(V) lt 2 then continue; end if;
        special +:= 1;
        moving := 0*D;
        for v in Basis(V) do
            f := to_function(v);
            if f ne 0 then moving := LCM(moving,Denominator(Divisor(f))); end if;
        end for;
        assert Degree(moving) eq 4;
        // Basepoint-free pencil trick: dimension of T_[D] W^1_5.
        assert 8-g+Dimension(K-D-moving) eq 1;
        Include(~poles,moving);
    end for;
end for;
assert #poles eq p+1;
moving := Rep(poles);
assert &and[Dimension(moving-other) eq 1:other in poles];
assert special eq #places[1]*(p+1);
printf "RESULT N=%o p=%o divisors=%o special_divisors=%o pencil_classes=1 tangent=1\n",
       N,p,total,special;
printf "SUCCESS local N=%o\n",N;
quit;
