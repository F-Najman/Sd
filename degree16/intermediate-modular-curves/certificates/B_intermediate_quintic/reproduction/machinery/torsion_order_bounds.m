// Isogeny-invariant Frobenius orders, not a claim about JH integral lattices.
N := StringToInteger(N);
g := StringToInteger(g);
delta := [StringToInteger(s):s in Split(delta,",")];
J := JH(N,delta);
assert Dimension(J) eq g;
orders := [];
for p in [3,5,7,11,13,17,19,23,29,31] do
    if N mod p eq 0 then continue; end if;
    order := Integers()!Evaluate(FrobeniusPolynomial(J,p),1);
    Append(~orders,<p,order>);
    printf "FROBENIUS_ORDER p=%o order=%o\n",p,order;
end for;
assert #orders ge 2;
primes := &join[{t[1]:t in Factorization(order[2])}:order in orders];
bound := 1;
for ell in primes do
    // Only prime-to-residue-characteristic injectivity is used.
    v := Minimum([Valuation(order[2],ell):order in orders|order[1] ne ell]);
    bound *:= ell^v;
end for;
printf "CERTIFIED rational_torsion_order_divides=%o\n",bound;
print "SUCCESS prime-to-characteristic torsion-order bound";
quit;
