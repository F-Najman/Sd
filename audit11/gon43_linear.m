SetQuitOnError(true);SetColumns(0);SetMemoryLimit(16*10^9);SetSeed(20261028);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
X:=MDX1(43,GF(2));AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));assert Genus(AF)eq 57;
rats:=Places(AF,1);assert #rats eq 21;C:=&+[Divisor(p):p in rats];P:=Divisor(rats[1]);Dstar:=5*C+8*P;
V,ev:=RiemannRochSpace(Dstar);assert Degree(Dstar)eq 113 and Dimension(V)eq 57;
fs:=[ev(v):v in Basis(V)];caps:=[13]cat[5:i in[2..21]];blocks:=[];
for i in[1..21]do
 p:=rats[i];u:=UniformizingElement(p);assert Valuation(u,p)eq 1;cap:=caps[i];rows:=[];
 for f in fs do
  h:=AF!RationalFunction(f*u^cap);aa:=[];
  for j in[0..cap]do
   assert Valuation(h,p)ge 0;a:=GF(2)!Evaluate(h,p);Append(~aa,a);h:=AF!RationalFunction((h-AF!a)/u);
  end for;Append(~rows,aa);
 end for;Append(~blocks,Matrix(GF(2),rows));
 printf "AUDIT_GON43_PRINCIPAL_PARTS point=%o cap=%o elapsed=%o\n",i,cap,Cputime(tt);
end for;
ALL:=HorizontalJoin(blocks);assert Rank(ALL)eq 57;
out:="/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/audit11/gon43_principal_parts.m";
PrintFile(out,Sprintf("Gonality43Genus:=57;Caps:=%o;PrincipalParts:=Matrix(GF(2),57,%o,%o);",caps,Ncols(ALL),Eltseq(ALL)):Overwrite:=true);
printf "AUDIT_GON43_GLOBAL_RR_PRINCIPAL_PARTS_COMPLETE dimension57=true elapsed=%o\n",Cputime(tt);quit;
