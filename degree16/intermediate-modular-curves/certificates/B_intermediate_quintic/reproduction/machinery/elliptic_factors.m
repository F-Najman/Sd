// Complete rational simple-factor census; inspect every dimension-one factor.
// EllipticCurve(A) returns an isogenous curve, not necessarily the optimal
// quotient. We use it only for isogeny-invariant conductor/rank information.
N := StringToInteger(N);
J := JZero(N);
factors := Decomposition(J);
assert &+[Dimension(A): A in factors] eq Dimension(J);
printf "N=%o genus=%o simple_dimensions=%o\n",N,Dimension(J),[Dimension(A):A in factors];
no_positive := true;
for A in factors do
    if Dimension(A) ne 1 then continue; end if;
    E := EllipticCurve(A);
    lo,hi := RankBounds(E);
    no_positive := no_positive and hi eq 0;
    printf "ELLIPTIC conductor=%o coefficients=%o rank_bounds=%o,%o root_number=%o central_zero=%o\n",
           Conductor(E),aInvariants(E),lo,hi,RootNumber(E),IsZeroAt(LSeries(A),1);
end for;
if no_positive then print "CERTIFIED: no positive-rank elliptic factors"; end if;
print "SUCCESS elliptic factor census";
quit;
