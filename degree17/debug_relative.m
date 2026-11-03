SetQuitOnError(true);SetColumns(0);print [10*i+j:i in[1..2],j in[1..3]];
load "work/degree17/full73/units_data.m";D:=DiamondMatrix;g:=genus;h:=Min([k:k in[0..35]|5^k mod 73 in[2,71]]);print "LOG",h;assert D^36 eq IdentityMatrix(GF(2),g);Nm:=&+[D^(4*k):k in[0..8]];assert Nm*(D^h-IdentityMatrix(GF(2),g))eq 0;print "NORM_ZERO";quit;
