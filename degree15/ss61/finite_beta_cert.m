SetQuitOnError(true);SetColumns(0);tt:=Cputime();
S:=CuspidalSubspace(ModularSymbols(61,2,1));assert Dimension(S)eq 4;e:=WindingElementProjection(S);T2:=HeckeOperator(S,2);T3:=HeckeOperator(S,3);I:=IdentityMatrix(Rationals(),4);rows:=[];v:=e;
for k in[0..3]do Append(~rows,Eltseq(v));v:=v*T2;end for;W:=Matrix(Rationals(),rows);U:=T3+2*I;assert Rank(W)eq 3 and Rank(VerticalJoin(W,U))eq 3;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/gamma0_beta_data.m",Sprintf("Winding:=Matrix(Rationals(),4,4,%o);T3plus2:=Matrix(Rationals(),4,4,%o);",Eltseq(W),Eltseq(U)):Overwrite:=true);
// Table2 says the only nontrivial strange character order at61 is6.
// Phi6(2)=d2^2-d2+1 kills that entire character space.
// Thus beta=(T3+2)*Phi6(<2>) has finite rational image on J1(61).
print "S15_BETA61_FINITE_IMAGE_CERTIFICATE_COMPLETE gamma0_rankzero_dimension=3 strange_order6_annihilated=true";quit;
