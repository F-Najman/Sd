SetQuitOnError(true);SetColumns(0);SetMemoryLimit(12*10^9);SetSeed(20261028);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
part:=StringToInteger(Part);parts:=StringToInteger(Parts);out:=Out;
X:=MDX1(43,GF(2));AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));assert Genus(AF)eq 57;
rats:=Places(AF,1);assert #rats eq 21;for d in[2..6]do assert #Places(AF,d)eq 0;end for;
p7:=Places(AF,7);p8:=Places(AF,8);assert #p7 eq 6 and #p8 eq 42;
C:=&+[Divisor(p):p in rats];P:=Divisor(rats[1]);tasks:=[3*C-4*P];labels:=[<0,0,0>];
for k in[1..#p8]do Append(~tasks,C+Divisor(p8[k]));Append(~labels,<1,k,0>);end for;
for k in[1..#p7]do Append(~tasks,C+P+Divisor(p7[k]));Append(~labels,<2,k,0>);end for;
for k in[1..21]do Append(~tasks,C+4*Divisor(rats[k])+8*P);Append(~labels,<3,k,0>);end for;
Append(~tasks,2*C+5*P);Append(~labels,<4,0,0>);
for k in[1..21]do Append(~tasks,2*C+4*P+2*Divisor(rats[k]));Append(~labels,<5,k,0>);end for;
for k in[2..21]do for j in[k+1..21]do Append(~tasks,2*C+3*P+2*Divisor(rats[k])+2*Divisor(rats[j]));Append(~labels,<6,k,j>);end for;end for;
assert #tasks eq 282;
PrintFile(out,"GonalityRecords:=[**];":Overwrite:=true);
for idx in[part..#tasks by parts]do
 D:=tasks[idx];V,ev:=RiemannRochSpace(D);assert Dimension(V)le 20;
 supports:=[p:p in Support(D)|Valuation(D,p)gt 0];degrees:=[];
 for v in V do
  f:=ev(v);if f in ConstantField(AF)then continue;end if;
  df:=&+[Max(0,-Valuation(f,p))*Degree(p):p in supports];assert df gt 15;Append(~degrees,df);
 end for;
 PrintFile(out,Sprintf("Append(~GonalityRecords,<%o,%o,%o,%o>);",idx,labels[idx],Dimension(V),Sort(degrees)));
 printf "AUDIT_GON43_CASE index=%o label=%o RR_dimension=%o nonconstants=%o min_degree=%o elapsed=%o\n",idx,labels[idx],Dimension(V),#degrees,IsEmpty(degrees)select 0 else Min(degrees),Cputime(tt);
end for;
printf "AUDIT_GON43_PART_COMPLETE part=%o parts=%o no_function_degree_at_most15=true elapsed=%o\n",part,parts,Cputime(tt);quit;
