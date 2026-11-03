SetColumns(0);SetQuitOnError(true);SetMemoryLimit(8*10^9);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");tt:=Cputime();X:=MDX1(41,GF(2));cs:=Cusps(X);ns:=[P:P in cs|Degree(P)eq 10];assert #ns eq 2;
assert not (GF(41)!3) in {s*(GF(41)!2)^i:s in [1,-1],i in[0..19]};
B:=2*(Divisor(ns[1])-Divisor(ns[2]));flag:=IsPrincipal(B);assert not flag;
printf "DECIC41_NONRATIONAL_CUSP A3_principal=%o elapsed=%o\n",flag,Cputime(tt);print "DECIC41_NONRATIONAL_CUSP_COMPLETE";quit;
