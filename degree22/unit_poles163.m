SetQuitOnError(true);SetColumns(0);tt:=Cputime();N:=163;QPrec:=1000;TatePrec:=1800;
LS<q>:=LaurentSeriesRing(GF(2),TatePrec);xp:=q/(1+q)^2;yp:=q^2/(1+q)^3;s1:=LS!0;a6:=LS!0;
for n in[1..TatePrec div N+1]do
 if N*n+1 lt TatePrec then z:=q^(N*n+1);xp+:=z/(1+z)^2;yp+:=z^2/(1+z)^3;end if;
 if N*n-1 lt TatePrec then w:=q^(N*n-1);xp+:=w/(1+w)^2;yp+:=w/(1+w)^3;end if;
 if N*n lt TatePrec then z:=q^(N*n);s1+:=(GF(2)!n)*z/(1+z);a6+:=(GF(2)!((5*n^3+7*n^5)div 12))*z/(1+z);end if;
end for;
yp+:=s1;a4:=s1;assert Valuation(yp^2+xp*yp+xp^3+a4*xp+a6)ge TatePrec;
// The universal Tate point u=q on E(q^61) has exact order83.
aa4:=xp^2+a4+yp;aaa2:=xp+(aa4/xp)^2+aa4/xp;b:=aaa2^3/xp^2;c:=(aaa2+xp)/xp;r:=b/c;s:=c^2/(b+c);t:=r*s+1;xu:=(s+r)/t;yu:=t/(s^2+s+r+1);
assert AbsolutePrecision(xu)ge QPrec and AbsolutePrecision(yu)ge QPrec and Valuation(xu)ge -95 and Valuation(yu)ge -95;
printf "NONIC83_TATE_UNIT_SERIES valuation_x=%o valuation_y=%o absolute_precision_x=%o absolute_precision_y=%o time=%o\n",Valuation(xu),Valuation(yu),AbsolutePrecision(xu),AbsolutePrecision(yu),Cputime(tt);
function TateUnits(k)
 xx:=q^k/(1+q^k)^2;yy:=q^(2*k)/(1+q^k)^3+s1;
 for n in[1..TatePrec div N+1]do
  if N*n+k lt TatePrec then z:=q^(N*n+k);xx+:=z/(1+z)^2;yy+:=z^2/(1+z)^3;end if;
  if N*n-k lt TatePrec then z:=q^(N*n-k);xx+:=z/(1+z)^2;yy+:=z/(1+z)^3;end if;
 end for;
 assert Valuation(yy^2+xx*yy+xx^3+s1*xx+a6)ge TatePrec;
 aa4:=xx^2+s1+yy;aaa2:=xx+(aa4/xx)^2+aa4/xx;b:=aaa2^3/xx^2;c:=(aaa2+xx)/xx;r:=b/c;s:=c^2/(b+c);t:=r*s+1;
 return(s+r)/t,t/(s^2+s+r+1);
end function;

rows:=[**];PX:=0;PY:=0;
for k in[1..81]do x,y:=TateUnits(k);vx:=Valuation(x);vy:=Valuation(y);assert AbsolutePrecision(x)-vx gt 100 and AbsolutePrecision(y)-vy gt 100;PX+:=Max(0,-vx);PY+:=Max(0,-vy);Append(~rows,<k,vx,vy>);end for;
assert &+[r[2]:r in rows]eq 0 and &+[r[3]:r in rows]eq 0;
d:=Order(GF(N)!2);F<z>:=GF(2^d);zeta:=z^ExactQuotient(#F-1,N);assert Order(zeta)eq N;
for k in[1..N-1]do v:=zeta^k;xx:=v/(1+v)^2;yy:=v^2/(1+v)^3;assert yy^2+xx*yy eq xx^3;
 aa4:=xx^2+yy;aaa2:=xx+(aa4/xx)^2+aa4/xx;b:=aaa2^3/xx^2;c:=(aaa2+xx)/xx;r:=b/c;s:=c^2/(b+c);t:=r*s+1;ux:=(s+r)/t;uy:=t/(s^2+s+r+1);assert ux ne 0 and uy ne 0;end for;
PrintFile("work/degree22/unit_poles163_data.m",Sprintf("PoleBoundX:=%o;PoleBoundY:=%o;RationalCuspValuations:=%o;AllNonrationalCuspValuesUnits:=true;",PX,PY,rows):Overwrite:=true);
printf "S22_ALL_UNIT_POLES163_CERTIFIED PX=%o PY=%o\n",PX,PY;quit;
