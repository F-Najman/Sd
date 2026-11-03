// Diagnose finite-field place-to-class conversions, without changing a proof.
load "family_input.m";
p := StringToInteger(p);
t := Cputime();
C := ChangeRing(Curve(ProjectiveSpace(Rationals(),source_genus-1),source_equations),GF(p));
F := AlgorithmicFunctionField(FunctionField(C));
assert Genus(F) eq source_genus;
if assigned factor_bound then
    _,_,_ := ClassGroup(F:DegreeBound:=StringToInteger(factor_bound),Proof:=true);
end if;
G,rep,cl := ClassGroup(C);
printf "class group ready CPU=%o\n",Cputime(t);
base := Divisor(Places(C,1)[1]);
for d in [1..5] do
    places := Places(C,d);
    printf "degree=%o places=%o CPU=%o\n",d,#places,Cputime(t);
    for i->P in places do
        c := cl(Divisor(P)-d*base);
        if i mod 100 eq 0 then printf "converted=%o CPU=%o\n",i,Cputime(t); end if;
    end for;
    printf "completed degree=%o CPU=%o\n",d,Cputime(t);
end for;
print "SUCCESS all place class maps profiled";
quit;
