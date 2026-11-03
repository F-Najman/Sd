// The geometric degree-five obstruction: a double cover of genus h
// and a degree-five function would force g <= 2h+4.
load "common.m";
cases := [
 <83,7,83,1>, <89,7,89,1>, <92,10,23,1>, <101,8,101,1>,
 <107,9,107,2>, <111,11,111,2>, <118,14,59,3>,
 <123,13,41,3>, <131,11,131,1>, <141,15,47,3>,
 <142,17,71,2>, <143,13,143,2>, <145,13,29,4>,
 <155,15,155,4>, <159,17,159,4>, <167,14,167,2>, <191,16,191,2>
];
for row in cases do
    N,g,d,h := Explode(row);
    C := ModularCurveQuotient(N,[]);
    // Holomorphic differentials are weight-two cusp forms. This exact
    // dimension avoids recomputing a large characteristic-zero normalization.
    assert Dimension(CuspidalSubspace(ModularForms(N,2))) eq g;
    M := CanonicalALMatrix(N,d);
    I := IdentityMatrix(Rationals(),g);
    assert M^2 eq I and Rank(I+M) eq h;
    w := CoordinateInvolution(C,M);
    assert M ne I and g gt 2*h+4;
    printf "N=%o genus=%o involution=w%o quotient_genus=%o\n",N,g,d,h;
end for;
print "SUCCESS arithmetic";
quit;
