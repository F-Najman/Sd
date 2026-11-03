// Alternative exact pullback through canonical linear systems.
// A common fixed divisor is subtracted, including at ramification points.
load "family_input.m";
load "../../quotient_rational_fibers.m";
load "../../linear_scheme_divisor.m";
p := StringToInteger(p);
k := GF(p);
M := CuspidalSubspace(ModularForms(N,2));
Qbasis := Matrix(Rationals(),[[Coefficient(qExpansion(f,precision),i):i in [1..precision-1]]:f in Basis(M)]);
U := Matrix(Rationals(),[Eltseq(Solution(Qbasis,v)):v in Rows(target_basis)]);
assert U*Qbasis eq target_basis;
W := U*AtkinLehnerOperator(M,N)*U^-1;
Y := ChangeRing(Curve(ProjectiveSpace(Rationals(),target_genus-1),target_equations),k);
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),source_genus-1),source_equations),k);
fibers := QuotientRationalFibers(Y,ChangeRing(W,k),p);
assert #fibers eq 12;
RC := CoordinateRing(Ambient(C));
RY := CoordinateRing(Ambient(Y));
Lp := ChangeRing(L,k);
forms := [&+[Lp[i,j]*RC.j:j in [1..source_genus]]:i in [1..target_genus]];
places := &cat[Places(C,d):d in [1..4]];
print "small places enumerated",#places;
source_coordinates := [* Eltseq(RepresentativePoint(P)):P in places *];
print "projective representatives cached";
fixed_scheme := Scheme(C,forms);
assert Dimension(fixed_scheme) le 0;
fixed := LinearSchemeDivisor(C,forms,places,source_coordinates);
printf "fixed canonical subsystem divisor degree=%o\n",Degree(fixed);
assert Degree(fixed) eq 2*source_genus-2-2*(2*target_genus-2);
pullbacks := [];
for D in fibers do
    decomposition := Decomposition(D);
    // These particular quotient fibers are reduced. Obtain their projective
    // spans directly from points, avoiding a costly two-generator ideal.
    assert &and[pair[2] eq 1:pair in decomposition];
    rows := [];
    for pair in decomposition do
        coordinates := Eltseq(RepresentativePoint(pair[1]));
        if Degree(pair[1]) eq 1 then
            Append(~rows,[k!a:a in coordinates]);
        else
            assert Degree(pair[1]) eq 2;
            rows cat:= [[k!Eltseq(a)[j]:a in coordinates]:j in [1..2]];
        end if;
    end for;
    assert Rank(Matrix(k,rows)) eq 2;
    nullspace := Kernel(Transpose(Matrix(k,rows)));
    linear := [&+[v[j]*RY.j:j in [1..target_genus]]:v in Basis(nullspace)];
    Z := Scheme(Y,linear);
    assert Dimension(Z) eq 0 and Degree(Z) eq 2;
    // Both reduced support points lie on Z by construction; length two
    // proves equality without another expensive divisor conversion.
    printf "target fiber span verified %o\n",#pullbacks+1;
    preimage := Scheme(C,[Evaluate(f,forms):f in linear]);
    assert Dimension(preimage) eq 0;
    printf "source preimage scheme degree=%o\n",Degree(preimage);
    pulled := LinearSchemeDivisor(C,[Evaluate(f,forms):f in linear],places,source_coordinates)-fixed;
    assert IsEffective(pulled) and Degree(pulled) eq 4;
    Append(~pullbacks,pulled);
    printf "linear pullback %o degree=%o\n",#pullbacks,Degree(pulled);
end for;
print "starting source class group";
G,rep,cl := ClassGroup(C);
B := sub<G|[cl(D-pullbacks[1]):D in pullbacks]>;
printf "complete elliptic fiber subgroup order=%o\n",#B;
assert #B eq 12;
print "SUCCESS complete linear fiber pullbacks and subgroup";
quit;
