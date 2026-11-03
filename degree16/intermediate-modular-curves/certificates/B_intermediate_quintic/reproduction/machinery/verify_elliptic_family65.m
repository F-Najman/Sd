// Exact fibers use canonical linear systems and local place valuations.
// Identify the known degree-four elliptic fibers inside W5 over a good field.
// This is exploratory until all translates and their lifting tangents pass.
load "family_input.m";
load "../../quotient_rational_fibers.m";
load "../../linear_scheme_divisor.m";
load "../../canonical_elliptic_fibers.m";
p := StringToInteger(p);
expected_order := StringToInteger(expected_order);
M := CuspidalSubspace(ModularForms(N,2));
Qbasis := Matrix(Rationals(),[[Coefficient(qExpansion(f,precision),i):i in [1..precision-1]]:f in Basis(M)]);
U := Matrix(Rationals(),[Eltseq(Solution(Qbasis,v)):v in Rows(target_basis)]);
assert U*Qbasis eq target_basis;
W := U*AtkinLehnerOperator(M,N)*U^-1;
assert W^2 eq IdentityMatrix(Rationals(),target_genus);
assert Rank(W+IdentityMatrix(Rationals(),target_genus)) eq 1;
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),source_genus-1),source_equations),GF(p));
Y := ChangeRing(Curve(ProjectiveSpace(Rationals(),target_genus-1),target_equations),GF(p));
for Z in [C,Y] do
    assert IsIrreducible(Z) and IsReduced(Z);
    assert ArithmeticGenus(Z) eq Genus(AlgorithmicFunctionField(FunctionField(Z)));
end for;
assert ArithmeticGenus(C) eq source_genus and ArithmeticGenus(Y) eq target_genus;
RC := CoordinateRing(Ambient(C));
RY := CoordinateRing(Ambient(Y));
Lp := ChangeRing(L,GF(p));
Wp := ChangeRing(W,GF(p));
phi := map<C->Y|[&+[Lp[i,j]*RC.j:j in [1..source_genus]]:i in [1..target_genus]]>;
// Degree will be certified from pullbacks of rational places below.
assert Rank(Lp) eq target_genus;
forms := [&+[Wp[i,j]*RY.j:j in [1..target_genus]]:i in [1..target_genus]];
w := iso<Y->Y|forms,forms>;
print "forgetting linear system and involution constructed over finite field";
G,rep,cl := ClassGroup(C);
ypoints := Setseq(Points(Y));
assert #ypoints gt 0;
fibers := CanonicalEllipticFibers(C,Y,Lp,Wp,p,expected_order);
assert &and[Degree(D) eq 2*cover_degree:D in fibers];
assert 2*cover_degree eq 4;
F4 := fibers[1];
B := sub<G|[cl(D-F4):D in fibers]>;
printf "elliptic_fiber_subgroup=%o expected=%o base_points=%o\n",#B,expected_order,#ypoints;
assert #B eq expected_order;
places := [Places(C,d):d in [1..5]];
assert #places[1] gt 0;
base := Divisor(places[1][1]);
classes := [[cl(Divisor(P)-d*base):P in places[d]]:d in [1..5]];
W5 := {G|};
representatives := AssociativeArray();
for partition in Partitions(5) do
    choices := CartesianProduct([Multisets({1..#places[d]},Multiplicity(Multiset(partition),d)):d in [1..5]]);
    for choice in choices do
        c := &+[e*classes[d][i]:i->e in s,d->s in choice];
        Include(~W5,c);
        if not IsDefined(representatives,c) then
            representatives[c] := &+[e*Divisor(places[d][i]):i->e in s,d->s in choice];
        end if;
    end for;
end for;
known := {cl(F4+Divisor(P)-5*base)+G!b:P in places[1],b in B};
assert known subset W5;
coset_union := {G|};
complete_cosets := [];
for c in W5 do
    if c in coset_union then continue; end if;
    coset := {c+G!b:b in B};
    if coset subset W5 then
        coset_union join:= coset;
        Append(~complete_cosets,coset);
    end if;
end for;
printf "W5=%o known_B_plus_C=%o full_B_coset_union=%o extra_classes=%o\n",#W5,#known,#coset_union,#(coset_union diff known);
assert coset_union eq known;
// At a nonspecial effective divisor, the annihilator of the Abel-image
// tangent space is H^0(K-D). Intersect tangents over the entire B-orbit.
K := CanonicalDivisor(C);
VK,to_function := RiemannRochSpace(K);
for orbit in complete_cosets do
    rows := [];
    for c in orbit do
        D := representatives[c];
        if Dimension(D) eq 1 then
            V,inclusion := RiemannRochSpace(K-D);
            rows cat:= [Eltseq(inclusion(v)@@to_function):v in Basis(V)];
        end if;
    end for;
    tangent_dimension := source_genus-Rank(Matrix(GF(p),#rows,source_genus,&cat rows));
    printf "orbit_size=%o intersection_tangent_dimension=%o\n",#orbit,tangent_dimension;
    assert tangent_dimension eq 2;
end for;
print "SUCCESS elliptic-family metadata; no Q-classification asserted";
quit;
