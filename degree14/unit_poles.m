SetQuitOnError(true);SetColumns(0);tt:=Cputime();
Ns:=[127];bounds:=[[0,0]];
for ii in[1..#Ns]do
 N:=Ns[ii];prec:=3200;LS<q>:=LaurentSeriesRing(GF(2),prec);s1:=LS!0;a6:=LS!0;
 for n in[1..prec div N+1]do if N*n lt prec then z:=q^(N*n);s1+:=(GF(2)!n)*z/(1+z);a6+:=(GF(2)!((5*n^3+7*n^5)div 12))*z/(1+z);end if;end for;
 vals:=[];
 for k in[1..(N-1)div 2]do
  xx:=q^k/(1+q^k)^2;yy:=q^(2*k)/(1+q^k)^3+s1;
  for n in[1..prec div N+1]do
   if N*n+k lt prec then z:=q^(N*n+k);xx+:=z/(1+z)^2;yy+:=z^2/(1+z)^3;end if;
   if N*n-k lt prec then z:=q^(N*n-k);xx+:=z/(1+z)^2;yy+:=z/(1+z)^3;end if;
  end for;
  assert Valuation(yy^2+xx*yy+xx^3+s1*xx+a6)ge prec;
  aa4:=xx^2+s1+yy;aa2:=xx+(aa4/xx)^2+aa4/xx;b:=aa2^3/xx^2;c:=(aa2+xx)/xx;r:=b/c;s:=c^2/(b+c);t:=r*s+1;xu:=(s+r)/t;yu:=t/(s^2+s+r+1);
  assert Min(AbsolutePrecision(xu),AbsolutePrecision(yu))gt 2*N+20 and xu ne 0 and yu ne 0;Append(~vals,[Valuation(xu),Valuation(yu)]);
 end for;
 dx:=&+[Max(0,-v[1]):v in vals];dy:=&+[Max(0,-v[2]):v in vals];
 e:=Order(Integers(N)!2);F:=GF(2^e);repeat zeta:=Random(F)^((#F-1)div N);until zeta ne 1 and zeta ne 0;assert zeta^N eq 1;
 for k in[1..(N-1)div 2]do
  z:=zeta^k;xx:=z/(1+z)^2;yy:=z^2/(1+z)^3;assert yy^2+xx*yy+xx^3 eq 0;
  aa4:=xx^2+yy;aa2:=xx+(aa4/xx)^2+aa4/xx;assert aa2 ne 0;b:=aa2^3/xx^2;c:=(aa2+xx)/xx;assert c ne 0 and b+c ne 0;r:=b/c;s:=c^2/(b+c);t:=r*s+1;assert t ne 0 and s^2+s+r+1 ne 0 and s+r ne 0;
 end for;
 printf "AUDIT_UNIT_POLES_COMPLETE N=%o degree_x=%o degree_y=%o rational_cusp_orders=%o nonrational_cusps_all_units=true elapsed=%o\n",N,dx,dy,vals,Cputime(tt);
end for;
print "AUDIT_ALL_UNIT_POLE_BOUNDS_COMPLETE";quit;
