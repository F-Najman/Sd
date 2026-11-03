SetQuitOnError(true);SetColumns(0);SetMemoryLimit(16*10^9);tt:=Cputime();
AttachSpec("/home/fnajman/degree9_torsion/nonic-torsion/mdmagma/v2/mdmagma.spec");
load "/home/fnajman/degree9_torsion/nonic-torsion/common/dt_expansions_local.m";
X:=MDX1(43,GF(2));AF,am:=AlgorithmicFunctionField(FunctionField(Curve(X)));assert Genus(AF)eq 57;rats:=Places(AF,1);assert #rats eq 21;printf "AUDIT_GON43_MODEL_READY elapsed=%o\n",Cputime(tt);
Om,om:=SpaceOfHolomorphicDifferentials(AF);B:=[om(v):v in Basis(Om)];assert #B eq 57;printf "AUDIT_GON43_HOLOMORPHIC_BASIS_READY elapsed=%o\n",Cputime(tt);caps:=[13]cat[5:i in[2..21]];blocks:=[];
function ExactJets(B,p,cap)
 w0:=UniformizingDifferential(B,p);fs0:=[AF!RationalFunction(w/w0):w in B];found:=false;for f in fs0 do u:=f-AF!(GF(2)!Evaluate(f,p));if Valuation(u,p)eq 1 then found:=true;break;end if;end for;assert found;du:=Differential(u);assert Valuation(du,p)eq 0;
 fs:=[AF!RationalFunction(w/du):w in B];blocks:=[];
 for k in[1..cap]do
  aa:=[GF(2)!Evaluate(f,p):f in fs];Append(~blocks,Matrix(GF(2),57,1,aa));fs:=[AF!RationalFunction((fs[i]-AF!aa[i])/u):i in[1..57]];
 end for;return HorizontalJoin(blocks);
end function;
for i in[1..21]do
 AA:=ExactJets(B,rats[i],caps[i]);assert Nrows(AA)eq 57 and Ncols(AA)eq caps[i];Append(~blocks,AA);
 printf "AUDIT_GON43_DIFFERENTIAL_JETS point=%o cap=%o elapsed=%o\n",i,caps[i],Cputime(tt);
end for;
JJ:=HorizontalJoin(blocks);assert Ncols(JJ)eq 113 and Rank(JJ)eq 57;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/audit11/gon43_dual_data.m",Sprintf("Caps:=%o;HolomorphicJetMatrix:=Matrix(GF(2),57,113,%o);",caps,Eltseq(JJ)):Overwrite:=true);
printf "AUDIT_GON43_DUAL_PRINCIPAL_PARTS_COMPLETE rank57=true elapsed=%o\n",Cputime(tt);quit;
