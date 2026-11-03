SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
for N in[23,29,31]do
 X:=MDX1(N,Rationals());AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));x:=am(X`_coordinates_xy[1]);y:=am(X`_coordinates_xy[2]);found:=false;
 fs:=[x,y,1-x,1-y,x-y,1-x*y,x-y+1];ds:=[Divisor(f):f in fs];ps:=Setseq(&join[Seqset(Support(d)):d in ds]);vs:=[[Valuation(f,p):p in ps]:f in fs];degs:=[Degree(p):p in ps];
 candidates:=[];
 for ex in CartesianPower([-1,0,1],#fs)do
  orders:=[&+[ex[i]*vs[i][j]:i in[1..#fs]]:j in[1..#ps]];
  if &+[Max(0,-orders[j])*degs[j]:j in[1..#ps]]ne 12 then continue;end if;
  Append(~candidates,< &+[Abs(e):e in ex],ex>);
 end for;
 Sort(~candidates);assert #candidates gt 0;printf "S12_UNIT_CANDIDATES N=%o count=%o simplest=%o\n",N,#candidates,candidates[1..Min(6,#candidates)];
end for;quit;
