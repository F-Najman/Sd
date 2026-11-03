// Complete simple-factor profile, retaining every central-vanishing factor
// as potentially positive rank. Vanishing is NOT a proof of positive rank.
N := StringToInteger(N);
g := StringToInteger(g);
delta := [StringToInteger(s):s in Split(delta,",")];
J := JH(N,delta);
assert Dimension(J) eq g;
factors := Factorization(J);
assert &+[Dimension(t[1])*#t[2]:t in factors] eq g;
for t in factors do
    A := t[1];
    central_zero := IsZeroAt(LSeries(A),1);
    printf "FACTOR dimension=%o multiplicity=%o central_zero=%o\n",Dimension(A),#t[2],central_zero;
    if central_zero then
        for p in [2,3,5,7] do
            if N mod p eq 0 then continue; end if;
            f := FrobeniusPolynomial(A,p);
            printf "POTENTIAL_POSITIVE p=%o polynomial=%o order=%o\n",p,f,Evaluate(f,1);
        end for;
    end if;
end for;
print "SUCCESS full intermediate factor profile";
quit;
