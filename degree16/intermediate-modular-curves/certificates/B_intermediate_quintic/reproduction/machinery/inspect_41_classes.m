// Inspect all possible reductions of rational degree-five classes assuming
// the separate rank-zero input. This file records data, not that input.
load "model_41.m";
C := Curve(ProjectiveSpace(Rationals(),4),equations);
for p in [3,7,11] do
    Cp := ChangeRing(C,GF(p));
    assert IsNonsingular(Cp);
    P := Divisor(Place(Cp![1,0,0,0,0]));
    G,rep,cl := ClassGroup(Cp);
    iv := Invariants(G);
    H := sub<G|[(iv[i] div GCD(iv[i],40))*G.i:i in [1..#iv]|iv[i] ne 0]>;
    printf "p=%o candidate_torsion_group=%o\n",p,#H;
    for c in H do
        D := rep(G!c)+5*P;
        V,to_function := RiemannRochSpace(D);
        if Dimension(V) lt 2 then continue; end if;
        s := to_function(Basis(V)[1]);
        effective := D+Divisor(s);
        assert IsEffective(effective) and Degree(effective) eq 5;
        U,mp := RiemannRochSpace(effective);
        moving := 0*effective;
        for v in Basis(U) do
            f := mp(v);
            if f ne 0 then moving := LCM(moving,Denominator(Divisor(f))); end if;
        end for;
        printf "class=%o h0=%o moving_degree=%o\n",Eltseq(G!c),Dimension(V),Degree(moving);
    end for;
end for;
print "SUCCESS inspection only";
quit;
