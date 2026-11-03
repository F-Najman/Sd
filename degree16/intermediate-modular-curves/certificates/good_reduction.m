// Good reduction of every canonical model that the paper reduces modulo a prime p (67 pairs).
// For each pair (model, p) we check the hypotheses of Lemma 2.3 of Adzaga, Keller, Michaud-Jacobs, Najman,
// Ozman, Vukorepa, "Computing quadratic points on modular curves X_0(N)", Math. Comp. 93 (2024): the reduction
// mod p of the (nonsingular, canonical) model is an integral curve of geometric genus g with a nonsingular
// F_p-point. The lemma then gives good reduction at p.
// The reduction is computed by reducing the primitive defining equations; the check that they have the Hilbert
// polynomial (2g-2)t+1-g of a canonical curve shows that they cut out exactly the special fibre of the closure
// over Z_(p) (which lies inside them and has the same Hilbert polynomial).
// Models: MD Sage models (Theorem C lower bounds), the LMFDB model of 43.132.9.a.2 (Proposition 4.1, with the
// non-Magma line "gamma := None;" of the LMFDB file removed), the quotient Y of X_1(48) (Theorem D), Magma's
// models of X_0(N) (Theorem A), and the models on which the twelve special certificates of Theorem B run.
// The plane models of X_1(N) in Theorem D are checked separately (D_x1_gonality/model_checks.m).
// Run from this directory:  magma -b good_reduction.m        (about 30 seconds)
SetQuitOnError(true); SetColumns(0);
// Reduce primitive defining equations directly. Reduction(X,p) instead
// saturates an integral polynomial ideal at p, which can be very expensive.
// The canonical Hilbert polynomial checked below proves that these naive
// equations already give the special fibre of the flat closure.
procedure CheckEquations(label, equations, p, g, coordinates)
    t0 := Realtime();
    n := Rank(Parent(equations[1]));
    Pp := ProjectiveSpace(GF(p), n-1); Rp := CoordinateRing(Pp);
    eqp := [];
    for f in equations do
        den := LCM([Denominator(c) : c in Coefficients(f)]);
        ints := [Integers()!(den*c) : c in Coefficients(f)];
        content := GCD(ints);
        Append(~eqp, Rp!(f*den/content));
    end for;
    printf "START_CHECK %o p=%o\n",label,p;
    Cp := Curve(Pp,eqp);
    h := HilbertPolynomial(Ideal(Cp));
    assert h eq (2*g-2)*Parent(h).1+1-g;
    printf "HILBERT_OK seconds=%.3o\n", Realtime(t0);
    assert IsIrreducible(Cp) and IsReduced(Cp);
    printf "INTEGRAL_OK seconds=%.3o\n", Realtime(t0);
    assert Genus(Cp) eq g;
    printf "GENUS_OK seconds=%.3o\n", Realtime(t0);
    if coordinates ne [] then
        pt := Cp![GF(p)!c : c in coordinates];
    else
        pt := RepresentativePoint(Places(Cp,1)[1]);
    end if;
    assert IsNonsingular(Cp,pt);
    printf "GOOD_REDUCTION %o p=%o g=%o point=%o seconds=%.3o\n", label,p,g,Eltseq(pt),Realtime(t0);
end procedure;

// Same q-expansion basis and LLL convention as ModularCurveQuotient(N,[]).
// The first q-coefficients give the rational cusp at infinity.
function CanonicalCusp(N)
    M := CuspidalSubspace(ModularForms(N,2));
    prec := Max(200,Ceiling(N*4*2/12));
    B := qExpansionBasis(M,prec);
    rows := [];
    for b in B do
        coeffs := [Rationals()!Coefficient(b,j) : j in [1..prec-1]];
        den := LCM([Denominator(c) : c in coeffs]);
        ints := [Integers()!(den*c) : c in coeffs];
        content := GCD(ints);
        Append(~rows,[c div content : c in ints]);
    end for;
    L := LLL(Matrix(Integers(),rows));
    coords := [L[i,1] : i in [1..Nrows(L)]];
    divisor := GCD(coords);
    return [c div divisor : c in coords];
end function;

load "C_intermediate_gonality/models/41.168.11.b.1.m"; equations := DefiningEquations(X);
CheckEquations("41.168.11.b.1",equations,2,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/41.210.11.b.1.m"; equations := DefiningEquations(X);
CheckEquations("41.210.11.b.1",equations,5,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/41.420.21.d.1.m"; equations := DefiningEquations(X);
CheckEquations("41.420.21.d.1",equations,2,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/41.84.5.a.1.m"; equations := DefiningEquations(X);
CheckEquations("41.84.5.a.1",equations,3,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/42.192.9.c.2.m"; equations := DefiningEquations(X);
CheckEquations("42.192.9.c.2",equations,5,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/42.288.13.a.1.m"; equations := DefiningEquations(X);
CheckEquations("42.288.13.a.1",equations,5,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/43.308.15.b.1.m"; equations := DefiningEquations(X);
CheckEquations("43.308.15.b.1",equations,2,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/44.144.8.c.4.m"; equations := DefiningEquations(X);
CheckEquations("44.144.8.c.4",equations,3,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/44.360.16.e.1.m"; equations := DefiningEquations(X);
CheckEquations("44.360.16.e.1",equations,3,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/45.144.5.a.1.m"; equations := DefiningEquations(X);
CheckEquations("45.144.5.a.1",equations,2,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/45.216.11.d.2.m"; equations := DefiningEquations(X);
CheckEquations("45.216.11.d.2",equations,2,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/45.288.9.a.4.m"; equations := DefiningEquations(X);
CheckEquations("45.288.9.a.4",equations,2,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/45.432.21.g.2.m"; equations := DefiningEquations(X);
CheckEquations("45.432.21.g.2",equations,2,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/48.192.5.ky.2.m"; equations := DefiningEquations(X);
CheckEquations("48.192.5.ky.2",equations,5,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/48.192.7.hj.1.m"; equations := DefiningEquations(X);
CheckEquations("48.192.7.hj.1",equations,5,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/48.192.7.ho.1.m"; equations := DefiningEquations(X);
CheckEquations("48.192.7.ho.1",equations,5,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/48.384.13.nt.1.m"; equations := DefiningEquations(X);
CheckEquations("48.384.13.nt.1",equations,7,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/48.384.19.bc.1.m"; equations := DefiningEquations(X);
CheckEquations("48.384.19.bc.1",equations,7,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/48.384.19.bj.1.m"; equations := DefiningEquations(X);
CheckEquations("48.384.19.bj.1",equations,5,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/49.392.19.i.2.m"; equations := DefiningEquations(X);
CheckEquations("49.392.19.i.2",equations,2,g,[1] cat [0 : i in [2..g]]);

load "C_intermediate_gonality/models/50.450.22.f.1.m"; equations := DefiningEquations(X);
CheckEquations("50.450.22.f.1",equations,3,g,[1] cat [0 : i in [2..g]]);

load "good_reduction_lmfdb_43.132.9.a.2.m"; equations := model_0;
CheckEquations("43.132.9.a.2 (LMFDB model)",equations,3,9,[ 0, 0, 0, 0, 0, 1, 1, 0, 0 ]);

load "D_x1_gonality/double_cover_48/data_48_23.m";
RY := PolynomialRing(Rationals(),gY);
PolyQ := func< terms | &+[RY | t[2]* &*[RY | RY.(i+1) : i in t[1]] : t in terms] >;
equations := [PolyQ(r) : r in Rel];
CheckEquations("Y = X_{+-1,+-23}(48)",equations,7,gY,[1] cat [0 : i in [2..gY]]);

C := ModularCurveQuotient(74,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(74)",equations,3,Genus(Gamma0(74)),CanonicalCusp(74));

C := ModularCurveQuotient(74,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(74)",equations,5,Genus(Gamma0(74)),CanonicalCusp(74));

C := ModularCurveQuotient(77,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(77)",equations,5,Genus(Gamma0(77)),CanonicalCusp(77));

C := ModularCurveQuotient(79,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(79)",equations,3,Genus(Gamma0(79)),CanonicalCusp(79));

C := ModularCurveQuotient(82,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(82)",equations,3,Genus(Gamma0(82)),CanonicalCusp(82));

C := ModularCurveQuotient(83,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(83)",equations,7,Genus(Gamma0(83)),CanonicalCusp(83));

C := ModularCurveQuotient(85,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(85)",equations,3,Genus(Gamma0(85)),CanonicalCusp(85));

C := ModularCurveQuotient(85,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(85)",equations,7,Genus(Gamma0(85)),CanonicalCusp(85));

C := ModularCurveQuotient(86,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(86)",equations,7,Genus(Gamma0(86)),CanonicalCusp(86));

C := ModularCurveQuotient(88,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(88)",equations,3,Genus(Gamma0(88)),CanonicalCusp(88));

C := ModularCurveQuotient(89,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(89)",equations,3,Genus(Gamma0(89)),CanonicalCusp(89));

C := ModularCurveQuotient(92,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(92)",equations,3,Genus(Gamma0(92)),CanonicalCusp(92));

C := ModularCurveQuotient(96,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(96)",equations,7,Genus(Gamma0(96)),CanonicalCusp(96));

C := ModularCurveQuotient(98,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(98)",equations,3,Genus(Gamma0(98)),CanonicalCusp(98));

C := ModularCurveQuotient(99,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(99)",equations,5,Genus(Gamma0(99)),CanonicalCusp(99));

C := ModularCurveQuotient(100,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(100)",equations,3,Genus(Gamma0(100)),CanonicalCusp(100));

C := ModularCurveQuotient(101,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(101)",equations,5,Genus(Gamma0(101)),CanonicalCusp(101));

C := ModularCurveQuotient(103,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(103)",equations,5,Genus(Gamma0(103)),CanonicalCusp(103));

C := ModularCurveQuotient(107,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(107)",equations,3,Genus(Gamma0(107)),CanonicalCusp(107));

C := ModularCurveQuotient(111,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(111)",equations,2,Genus(Gamma0(111)),CanonicalCusp(111));

C := ModularCurveQuotient(118,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(118)",equations,3,Genus(Gamma0(118)),CanonicalCusp(118));

C := ModularCurveQuotient(123,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(123)",equations,2,Genus(Gamma0(123)),CanonicalCusp(123));

C := ModularCurveQuotient(128,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(128)",equations,3,Genus(Gamma0(128)),CanonicalCusp(128));

C := ModularCurveQuotient(131,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(131)",equations,3,Genus(Gamma0(131)),CanonicalCusp(131));

C := ModularCurveQuotient(141,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(141)",equations,2,Genus(Gamma0(141)),CanonicalCusp(141));

C := ModularCurveQuotient(142,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(142)",equations,3,Genus(Gamma0(142)),CanonicalCusp(142));

C := ModularCurveQuotient(143,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(143)",equations,2,Genus(Gamma0(143)),CanonicalCusp(143));

C := ModularCurveQuotient(145,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(145)",equations,3,Genus(Gamma0(145)),CanonicalCusp(145));

C := ModularCurveQuotient(155,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(155)",equations,2,Genus(Gamma0(155)),CanonicalCusp(155));

C := ModularCurveQuotient(159,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(159)",equations,5,Genus(Gamma0(159)),CanonicalCusp(159));

C := ModularCurveQuotient(167,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(167)",equations,3,Genus(Gamma0(167)),CanonicalCusp(167));

C := ModularCurveQuotient(191,[]);
equations := DefiningEquations(C);
CheckEquations("X_0(191)",equations,2,Genus(Gamma0(191)),CanonicalCusp(191));

load "B_intermediate_quintic/audit_runs/special/petri_1459e19c781c9c0f/evidence/hilbert_jobs/1459e19c781c9c0f/integral_model/canonical_input.m";
CheckEquations("petri 1459e19c781c9c0f",equations,5,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/petri_4517e2b49cc674e5/evidence/hilbert_jobs/4517e2b49cc674e5/integral_model/canonical_input.m";
CheckEquations("petri 4517e2b49cc674e5",equations,2,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/petri_577694554b43283f/evidence/hilbert_jobs/577694554b43283f/integral_model/canonical_input.m";
CheckEquations("petri 577694554b43283f",equations,2,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/family_4a0a750d72e5ecf2/evidence/family_jobs/4a0a750d72e5ecf2/family_input.m";
CheckEquations("family 4a0a750d72e5ecf2",equations,5,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/family_dc8a04ecdc10f967/evidence/family_jobs/dc8a04ecdc10f967/family_input.m";
CheckEquations("family dc8a04ecdc10f967",equations,5,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/family_ef93d63ca2b377a8/evidence/family_jobs/ef93d63ca2b377a8/family_input.m";
CheckEquations("family65 ef93d63ca2b377a8",equations,7,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/family3_5fa08fafc8523084/evidence/family3_jobs/5fa08fafc8523084/source/reduced_model/canonical_input.m";
CheckEquations("family3 5fa08fafc8523084",equations,3,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/family3_bd67dfd630eb6c1b/evidence/family3_jobs/bd67dfd630eb6c1b/source/reduced_model/canonical_input.m";
CheckEquations("family3 bd67dfd630eb6c1b",equations,3,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/torsion40/evidence/hilbert_jobs/82f731393c98cb7c/case40_final_replay/integral_model/reduced_model/canonical_input.m";
CheckEquations("torsion40 82f731393c98cb7c",equations,3,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/torsion48_2fea1fad025e6bab/evidence/hilbert_jobs/2fea1fad025e6bab/case48_replay/integral_model/canonical_input.m";
CheckEquations("torsion48 2fea1fad025e6bab",equations,5,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/torsion48_efd0600330b90e51/evidence/hilbert_jobs/efd0600330b90e51/case48_replay/integral_model/canonical_input.m";
CheckEquations("torsion48 efd0600330b90e51",equations,5,expected_genus,cusp_coordinates);

load "B_intermediate_quintic/audit_runs/special/translate43/evidence/hilbert_jobs/d0a49dd94f1144df/integral_model/canonical_input.m";
CheckEquations("translate43 d0a49dd94f1144df",equations,2,expected_genus,cusp_coordinates);
print "ALL_67_GOOD_REDUCTION_CHECKS_PASS";
quit;
