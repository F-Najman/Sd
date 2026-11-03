// Good reduction at 7 of the canonical model of Y = X_{+-1,+-23}(48) (genus 13) in data_48_23.m: the reduced
// quadrics have the Hilbert polynomial of the generic canonical curve, define an irreducible curve of geometric
// genus 13, and contain (1:0:...:0), the reduction of the cusp at infinity (Section 2.2 of the paper).
SetQuitOnError(true);
load "data_48_23.m"; p := 7;
P := ProjectiveSpace(GF(p), gY - 1); S := CoordinateRing(P);
Poly := func< terms | &+[S | t[2] * &*[S | S.(i + 1) : i in t[1]] : t in terms] >;
I := ideal<S | [Poly(r) : r in Rel]>;
h := HilbertPolynomial(I); t := Parent(h).1; assert h eq (2*gY-2)*t + 1 - gY;
C := Curve(P, [Poly(r) : r in Rel]); assert IsIrreducible(C); assert Genus(C) eq gY;
assert P ! ([1] cat [0 : i in [2..gY]]) in C;
print "GOOD_REDUCTION Y = X_{+-1,+-23}(48) at p=7"; quit;
