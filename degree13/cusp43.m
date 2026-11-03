SetQuitOnError(true);SetColumns(0);SetMemoryLimit(8*10^9);tt:=Cputime();AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
X:=MDX1(43,GF(2));ns:=[P:P in Cusps(X)|Degree(P)eq 7];assert #ns eq 3;
B:=2*(2*Divisor(ns[1])-Divisor(ns[2])-Divisor(ns[3]));
f:=IsPrincipal(B);printf "S13_CUSP43_ALPHA_A3 principal=%o elapsed=%o\n",f,Cputime(tt);print "S13_CUSP43_TEST_COMPLETE";quit;
