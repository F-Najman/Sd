// All rational fibers of an involution quotient, including quadratic places.
// A rational quotient point has either split rational preimages, a rational
// ramified preimage, or one quadratic place on which w acts as Frobenius.
function QuotientRationalFibers(Y,W,p)
    RY := CoordinateRing(Ambient(Y));
    forms := [&+[W[i,j]*RY.j:j in [1..Ncols(W)]]:i in [1..Nrows(W)]];
    w := iso<Y->Y|forms,forms>;
    fibers := {DivisorGroup(Y)|};
    for P in Points(Y) do
        Include(~fibers,Divisor(Place(P))+Divisor(Place(w(P))));
    end for;
    for Q in Places(Y,2) do
        P := RepresentativePoint(Q);
        v := Eltseq(P);
        kv := Universe(v);
        image := [&+[kv!W[i,j]*v[j]:j in [1..#v]]:i in [1..#v]];
        conjugate := [a^p:a in v];
        // Projective equality without choosing an affine patch.
        conjugate_equal := &and[image[i]*conjugate[j] eq image[j]*conjugate[i]:i,j in [1..#v]];
        fixed := &and[image[i]*v[j] eq image[j]*v[i]:i,j in [1..#v]];
        if conjugate_equal and not fixed then Include(~fibers,Divisor(Q)); end if;
    end for;
    assert &and[Degree(D) eq 2:D in fibers];
    return Setseq(fibers);
end function;
