// Actual Jacobian group from the newly identified curve, not from JH lattices.
load "canonical_input.m";
p := StringToInteger(p);
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations),GF(p));
assert Dimension(C) eq 1 and Degree(C) eq 2*expected_genus-2;
assert IsIrreducible(C) and IsReduced(C) and ArithmeticGenus(C) eq expected_genus;
F := AlgorithmicFunctionField(FunctionField(C));
assert Genus(F) eq expected_genus and #Places(F,1) gt 0;
G,rep,cl := ClassGroup(F);
invariants := Invariants(G);
order := &*[d:d in invariants|d ne 0];
printf "ACTUAL_CURVE_JACOBIAN p=%o invariants=%o order=%o\n",p,invariants,order;
print "SUCCESS actual reduction group";
quit;
