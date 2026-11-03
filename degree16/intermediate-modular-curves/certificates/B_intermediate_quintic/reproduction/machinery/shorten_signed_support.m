// Find shorter representatives of the same reduction classes. Rational
// equivalence follows only after the independent rank/torsion proof passes.
load "canonical_input.m";
load "signed_support_candidates.m";
p := StringToInteger(p);
k := GF(p);
CQ := Curve(ProjectiveSpace(Rationals(),expected_genus-1),equations);
qpoints := [CQ!v:v in support_points];
C := ChangeRing(CQ,k);
assert IsIrreducible(C) and IsReduced(C);
assert ArithmeticGenus(C) eq expected_genus;
assert Genus(AlgorithmicFunctionField(FunctionField(C))) eq expected_genus;
points := [];
for P in qpoints do
    v := Eltseq(P);
    v := [Integers()!(LCM([Denominator(c):c in v])*c):c in v];
    common := GCD(v);
    Append(~points,C![k!(c div common):c in v]);
end for;
G,rep,cl := ClassGroup(C);
base := Divisor(Place(points[1]));
generators := [cl(Divisor(Place(P))-base):P in points];
targets := [&+[v[j]*generators[j]:j in [1..#points]]:v in support_divisors];
assert #Seqset(targets) eq #targets;
short := support_divisors;
for tuple in CartesianPower({-2..4},#points-1) do
    v := [Integers()|x:x in tuple];
    Append(~v,5-&+v);
    if v[#v] notin {-2..4} then continue; end if;
    c := &+[v[j]*generators[j]:j in [1..#points]];
    i := Index(targets,c);
    if i gt 0 and &+[Abs(x):x in v] lt &+[Abs(x):x in short[i]] then
        short[i] := v;
    end if;
end for;
for i in [1..#targets] do
    assert &+short[i] eq 5;
    assert &+[short[i][j]*generators[j]:j in [1..#points]] eq targets[i];
    printf "class=%o shortened=%o\n",i,short[i];
end for;
PrintFile("short_signed_support.m",Sprintf("support_points := %o;",[Eltseq(P):P in qpoints]):Overwrite:=true);
PrintFile("short_signed_support.m",Sprintf("support_divisors := %o;",short));
print "SUCCESS shorter representatives with exactly the same reduction classes";
quit;
