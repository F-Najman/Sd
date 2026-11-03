// Diagnose the exact stage; this is not a classification certificate.
load "family_input.m";
p := StringToInteger(p);
t := Cputime();
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),source_genus-1),source_equations),GF(p));
F := AlgorithmicFunctionField(FunctionField(C));
assert Genus(F) eq source_genus;
printf "starting ClassGroup CPU=%o\n",Cputime(t);
SetVerbose("ClassGroup",1);
if assigned factor_bound then
    G,rep,cl := ClassGroup(F:DegreeBound:=StringToInteger(factor_bound),Proof:=true);
else
    G,rep,cl := ClassGroup(C);
end if;
printf "ClassGroup complete invariants=%o CPU=%o\n",Invariants(G),Cputime(t);
for d in [1..4] do
    places := Places(C,d);
    printf "places degree=%o count=%o CPU=%o\n",d,#places,Cputime(t);
end for;
print "SUCCESS class group and place enumeration timing";
quit;
