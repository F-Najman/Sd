// Exact degree-four fibers via the canonical forgetting linear system.
// Requires QuotientRationalFibers and LinearSchemeDivisor already loaded.
function CanonicalEllipticFibers(C,Y,Lp,Wp,p,expected_order)
    g := ArithmeticGenus(C);
    h := ArithmeticGenus(Y);
    RC := CoordinateRing(Ambient(C));
    RY := CoordinateRing(Ambient(Y));
    k := BaseRing(C);
    assert Rank(Lp) eq h;
    forms := [&+[Lp[i,j]*RC.j:j in [1..g]]:i in [1..h]];
    phi := map<C->Y|forms>;
    places := &cat[Places(C,d):d in [1..4]];
    source_coordinates := [* Eltseq(RepresentativePoint(P)):P in places *];
    fixed := LinearSchemeDivisor(C,forms,places,source_coordinates);
    assert Degree(fixed) eq 2*g-2-2*(2*h-2);
    // Removing this fixed divisor identifies phi^*K_Y with K_C-fixed;
    // the degree identity certifies that the nonconstant map has degree two.
    quotient_fibers := QuotientRationalFibers(Y,Wp,p);
    assert #quotient_fibers eq expected_order;
    fibers := [];
    for D in quotient_fibers do
        decomposition := Decomposition(D);
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
        linear := [&+[v[j]*RY.j:j in [1..h]]:v in Basis(nullspace)];
        Z := Scheme(Y,linear);
        assert Dimension(Z) eq 0 and Degree(Z) eq 2;
        // Containment of the two reduced geometric points and equal lengths
        // identify Z with D, including nonsplit degree-two fibers.
        pulled := LinearSchemeDivisor(C,[Evaluate(f,forms):f in linear],
                                     places,source_coordinates)-fixed;
        assert IsEffective(pulled) and Degree(pulled) eq 4;
        Append(~fibers,pulled);
    end for;
    printf "complete canonical elliptic fibers=%o fixed_divisor_degree=%o\n",#fibers,Degree(fixed);
    return fibers;
end function;
