// Nonzero central L-value of J1(N) proves rank zero of J1(N), and hence
// of every rational quotient Jacobian J_Delta(N). No BSD assumption.
for N in [35,41] do
    J := JOne(N);
    nonzero := not IsZeroAt(LSeries(J),1);
    printf "N=%o dimension=%o central_L_nonzero=%o\n",N,Dimension(J),nonzero;
    assert nonzero;
end for;
print "SUCCESS rank-zero endpoint certificates";
quit;
