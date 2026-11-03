// Rank-zero quotient sieve for all nine prime levels.
// Example: magma -b N:=131 quotient_sieve.m
load "common.m";
N := StringToInteger(N);
// N, good prime, genus, quotient genus, quotient torsion bound, #A(F_p).
cases := [
 <79,3,6,1,13,5>, <83,7,7,1,41,11>, <89,3,7,1,22,5>,
 <101,5,8,1,25,7>, <103,5,8,2,17,55>, <107,3,9,2,53,29>,
 <131,3,11,1,65,5>, <167,3,14,2,83,19>, <191,2,16,2,95,11>
];
matches := [row:row in cases|row[1] eq N];
assert #matches eq 1;
_,p,g,qgenus,m,aorder := Explode(matches[1]);
factors,positive := PositiveFactors(N);
assert #positive eq 1;
assert Dimension(positive[1][1]) eq qgenus and #positive[1][2] eq 1;
assert PointCount(positive[1][1],p) eq aorder;
other_orders := [&*[PointCount(t[1],q)^#t[2]:t in factors
                         |not IsZeroAt(LSeries(t[1]),1)]
                 :q in [3,5,7,11,13,17,19]];
assert GCD(other_orders) eq m;

CQ := ModularCurveQuotient(N,[]);
M,infinity := CanonicalALMatrix(N,N);
IQ := IdentityMatrix(Rationals(),g);
assert M^2 eq IQ and Rank(IQ+M) eq qgenus;
wQ := CoordinateInvolution(CQ,M);
PQ := CQ!infinity;
QQ := wQ(PQ);
assert PQ ne QQ and wQ(QQ) eq PQ;

// Identify A with the pullback of the Fricke quotient Jacobian.
// Only at 89 is there a competing elliptic constituent of equal dimension.
if N eq 89 then
    Y := ModularCurveQuotient(N,[N]);
    assert Genus(Y) eq 1 and IsNonsingular(ChangeRing(Y,GF(p)));
    assert ClassNumber(ChangeRing(Y,GF(p))) eq aorder;
    assert &and[Dimension(t[1]) gt 1 or PointCount(t[1],p) ne aorder
                :t in factors|not IsZeroAt(LSeries(t[1]),1)];
else
    assert &and[Dimension(t[1]) gt qgenus
                :t in factors|not IsZeroAt(LSeries(t[1]),1)];
end if;
if N notin [79,103] then assert g gt 2*qgenus+4; end if;

C,F := GoodModel(N,p,g);
Mp := ChangeRing(M,GF(p));
assert Rank(IdentityMatrix(GF(p),g)+Mp) eq qgenus;
w := CoordinateInvolution(C,Mp);
cache,points,quadratic,K2 := LowDegreePlaceCache(C);
function PointDivisor(P)
    return cache[Eltseq(C(K2)![K2!a:a in Eltseq(P)])];
end function;
P := PointDivisor(C!ReducePoint(PQ,p));
Q := PointDivisor(C!ReducePoint(QQ,p));
G,representative,class_map := ClassGroup(F);
t := class_map(Q-P);
assert Order(t) eq m;
complement := &*[PointCount(t[1],p)^#t[2]:t in factors
                 |not IsZeroAt(LSeries(t[1]),1)];
if GCD(aorder,complement) eq 1 then
    H := TorsionKilledBy(G,aorder);
else
    // At 131 the complement also has 5-torsion. Norms distinguish the
    // actual elliptic subgroup from the full 5-primary subgroup.
    assert N eq 131;
    H := sub<G|>;
    for R in points cat quadratic do
        D := PointDivisor(R);
        norm := D+PointDivisor(w(R))-Degree(D)*(P+Q);
        H := sub<G|[G!h:h in Generators(H)] cat [class_map(norm)]>;
    end for;
end if;
assert #H eq aorder;

// This proves order(image(t))=m in the reduced quotient J/A, including
// the shared-prime case 131 and characteristic-two case 191.
// Together with the odd-prime Frobenius gcd, it gives (J/A)(Q)=<image(t)>.
assert #sub<G|[t] cat [G!h:h in Generators(H)]> eq m*aorder;
printf "N=%o p=%o genus=%o quotient_genus=%o m=%o Aorder=%o J=%o\n",
       N,p,g,qgenus,m,aorder,Invariants(G);

W,reps,total,W1 := DegreeFiveClasses(F,class_map,P : Sections := N in [79,103]);
full := {};
special := {};
for i in [0..m-1] do
    coset := {i*t+G!h:h in H};
    if coset subset W then Include(~full,i); end if;
    if #(coset meet W1) gt 0 then Include(~special,i); end if;
end for;
expected := qgenus eq 1 select {1,2,3,4} else {2,3};
if N eq 83 then Include(~expected,23); end if;
assert full eq expected;
if N in [79,103] then assert special eq {2,3}; end if;
printf "RESULT N=%o divisors=%o W0=%o full_indices=%o special_indices=%o\n",
       N,total,#W,full,special;
printf "SUCCESS quotient N=%o\n",N;
quit;
