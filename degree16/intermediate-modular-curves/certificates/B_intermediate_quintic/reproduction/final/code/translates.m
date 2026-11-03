// One certificate for all fifteen cases needing a family-lifting argument.
// Example: magma -b N:=145 translates.m
load "common.m";
load "translation.m";
N := StringToInteger(N);

// N, p, genus, quotient generators, dimension of B, #B(F_p),
// test type, subgroup orders, positive simple factors (dimension,multiplicity).
cases := [*
 <74, 3, 8, [74], 2, 21, "torsion", [7], [<1,2>]>,
 <77, 5, 7, [77], 2, 35, "torsion", [7], [<1,1>]>,
 <82, 3, 9, [2,41], 1, 6, "whole", [], [<1,1>]>,
 <86, 7, 10, [2,43], 1, 8, "cyclic", [8], [<1,2>]>,
 <99, 5, 9, [9,11], 1, 10, "whole", [], [<1,1>]>,
 <111, 2, 11, [111], 2, 15, "torsion", [5], [<1,2>]>,
 <118, 3, 14, [2,59], 1, 5, "torsion", [5], [<1,1>]>,
 <123, 2, 13, [3,41], 1, 3, "torsion", [3,5], [<1,1>,<1,1>]>,
 <128, 3, 9, [], 1, 6, "whole", [], [<1,1>]>,
 <141, 2, 15, [3,47], 1, 3, "torsion", [3,5], [<1,1>,<1,1>]>,
 <142, 3, 17, [71], 2, 15, "torsion", [5,7], [<1,1>,<1,1>]>,
 <143, 2, 13, [143], 2, 15, "torsion", [3], [<1,1>]>,
 <145, 3, 13, [5,29], 1, 4, "torsion", [2], [<1,1>,<2,1>]>,
 <155, 2, 15, [5,31], 1, 3, "torsion", [3,5], [<1,1>,<1,1>]>,
 <159, 5, 17, [3,53], 1, 6, "torsion", [3], [<1,2>]>
*];
matches := [* row : row in cases | row[1] eq N *];
assert #matches eq 1;
_, p, g, generators, bdim, border, mode, orders, expected := Explode(matches[1]);
factors, positive := PositiveFactors(N);
assert Sort([<Dimension(t[1]), #t[2]> : t in positive]) eq Sort(expected);
positive_orders := [PointCount(t[1],p) : t in positive];
if mode eq "torsion" then
    // Every nonzero possible direction contains a simple constituent;
    // that constituent has rational torsion of at least one tested order.
    assert &and[&or[a mod ell eq 0 : ell in orders] : a in positive_orders];
    assert &and[IsPrime(ell) and ell ne p : ell in orders];
end if;
printf "N=%o p=%o positive_factors=%o positive_orders=%o\n", N,p,expected,positive_orders;

// Verify the characteristic-zero quotient and its coordinate action.
CQ := ModularCurveQuotient(N,[]);
if N eq 128 then
    W := CanonicalALMatrix(N,N);
    S := ChangeRing(CanonicalTranslationMatrix(N,2),Rationals());
    matricesQ := [W, S*W*S^-1];
else
    matricesQ := [CanonicalALMatrix(N,d) : d in generators];
end if;
IQ := IdentityMatrix(Rationals(),g);
assert &and[M^2 eq IQ : M in matricesQ];
if #matricesQ eq 2 then
    assert matricesQ[1]*matricesQ[2] eq matricesQ[2]*matricesQ[1];
    assert #{IQ,matricesQ[1],matricesQ[2],matricesQ[1]*matricesQ[2]} eq 4;
end if;
assert Rank(&*[(IQ+M) : M in matricesQ]) eq bdim;
for M in matricesQ do w := CoordinateInvolution(CQ,M); end for;

// When using the whole finite elliptic group, identify its Q-direction
// with the unique positive factor. This permits arbitrary p-adic lifts,
// including for p-primary elements (82,99,128).
if mode eq "whole" then
    L := ChangeRing(CanonicalQExpansionMatrix(N),Rationals());
    f := qExpansion(Newform(positive[1][1]),Ncols(L)+1);
    v := Solution(L,Vector(Rationals(),[Coefficient(f,i):i in [1..Ncols(L)]]));
    assert &and[v*M eq v : M in matricesQ];
    assert positive_orders eq [border];
end if;

if N eq 86 then
    // All Q-elliptic curves isogenous to E43 have cyclic order-eight
    // reduction at 7: no rational 2-isogeny, and an odd-degree isogeny
    // preserves the 2-primary group. See the proof for this deduction.
    E := EllipticCurve([Rationals()|0,1,1,0,0]);
    assert Conductor(E) eq 43 and positive_orders eq [8];
    assert IsIrreducible(DivisionPolynomial(E,2));
    assert #Points(ChangeRing(E,GF(7))) eq 8;
    assert #Roots(ChangeRing(DivisionPolynomial(E,2),GF(7))) eq 1;
    assert IsIsogenous(E,ModularCurveQuotient(86,[2,43]));
end if;

// Independently determine the finite group order of the known quotient.
if bdim eq 2 then
    Y := ModularCurveQuotient(N,generators);
    assert Genus(Y) eq 2 and IsNonsingular(ChangeRing(Y,GF(p)));
    assert ClassNumber(ChangeRing(Y,GF(p))) eq border;
elif mode ne "whole" then
    MF := CuspidalSubspace(ModularForms(N,2));
    U := &*[(IQ+AtkinLehnerOperator(MF,d)):d in generators];
    T := HeckeOperator(MF,p);
    assert Rank(U) eq 1 and U^2 eq 4*U and U*T eq T*U;
    assert p+1-Trace(U*T)/4 eq border;
end if;

C,F := GoodModel(N,p,g);
G,representative,class_map := ClassGroup(F);
matrices := [ChangeRing(M,GF(p)):M in matricesQ];
involutions := [CoordinateInvolution(C,M):M in matrices];
cache,points,quadratic,K2 := LowDegreePlaceCache(C);
function PointDivisor(P)
    return cache[Eltseq(C(K2)![K2!a:a in Eltseq(P)])];
end function;
function NormDivisor(P)
    orbit := [P,involutions[1](P)];
    if #involutions eq 2 then orbit cat:= [involutions[2](T):T in orbit]; end if;
    return &+[PointDivisor(T):T in orbit];
end function;
base := PointDivisor(points[1]);
fiber := NormDivisor(points[1]);
F4 := bdim eq 1 select fiber else 2*fiber;
assert Degree(F4) eq 4;
B := sub<G|[class_map(NormDivisor(P)-fiber):P in points]>;
if #B lt border then
    for P in quadratic do
        D := PointDivisor(P);
        B := sub<G|[G!b:b in Generators(B)] cat [class_map(NormDivisor(P)-Degree(D)*fiber)]>;
    end for;
end if;
assert #B eq border;

// Differential of B x C -> Pic^5: the trace kernel annihilates T B.
I := IdentityMatrix(GF(p),g);
trace := &*[(I+M):M in matrices];
annihilator := Basis(Kernel(trace));
assert #annihilator eq g-bdim;
assert &and[&or[InnerProduct(v,Vector(Eltseq(P))) ne 0:v in annihilator]:P in points];

W,reps,total,W1 := DegreeFiveClasses(F,class_map,base);
if N in [86,99,128] then
    // Equality means every class has a unique effective representative,
    // so h^0=1 throughout W_5^0(F_p): no degree-five pencil can specialize.
    assert #W eq total;
end if;
known := {G|};
for P in points do
    known join:= {class_map(F4+PointDivisor(P)-5*base)+G!b:b in B};
end for;

if mode eq "whole" then
    tests := [* <#B,[B]> *];
else
    tests := [* *];
    for n in orders do
        H := TorsionKilledBy(G,n);
        // For a prime n these are all order-n subgroups. For n=8 we
        // deliberately test only cyclic subgroups, justified above.
        subgroups := Setseq({sub<H|h>:h in H|Order(h) eq n});
        Append(~tests,<n,subgroups>);
    end for;
end if;
for test in tests do
    n,subgroups := Explode(test);
    used := 0; count := 0;
    for subgroup in subgroups do
        cosets := WholeCosets(W,subgroup,G);
        if #cosets gt 0 then used +:= 1; end if;
        for coset in cosets do
            assert &and[G!s in B:s in subgroup];
            assert coset subset known;
            assert IntersectionTangent(F,reps,coset) eq bdim+1;
            count +:= 1;
        end for;
    end for;
    printf "RESULT N=%o p=%o divisors=%o W0=%o B=%o n=%o subgroups=%o used=%o cosets=%o tangent=%o\n",
        N,p,total,#W,#B,n,#subgroups,used,count,bdim+1;
end for;
printf "SUCCESS translates N=%o\n",N;
quit;
