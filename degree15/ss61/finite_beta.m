SetQuitOnError(true);SetColumns(0);tt:=Cputime();
S:=CuspidalSubspace(ModularSymbolsH(61,[1],2,1));assert Dimension(S)eq 126;e:=WindingElementProjection(S);T2:=HeckeOperator(S,2);T3:=HeckeOperator(S,3);D2:=(T2^2-HeckeOperator(S,4))/2;I:=IdentityMatrix(Rationals(),126);U:=(T3+2*I)*(D2^3+I);assert U*T2 eq T2*U;
v:=e;rows:=[];for k in[0..125]do Append(~rows,Eltseq(v));v:=v*T2;end for;W:=Matrix(Rationals(),rows);r:=Rank(W);rr:=Rank(VerticalJoin(W,U));printf "S15_BETA61_WINDING rank=%o image_union_rank=%o beta_rank=%o elapsed=%o\n",r,rr,Rank(U),Cputime(tt);assert rr eq r;
PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/finite_beta_data.m",Sprintf("WindingKrylov:=Matrix(Rationals(),%o,%o,%o);Beta:=Matrix(Rationals(),%o,%o,%o);",Nrows(W),Ncols(W),Eltseq(W),Nrows(U),Ncols(U),Eltseq(U)):Overwrite:=true);
// Record the J0(61) reduction order for an additional arithmetic check.
M:=CuspidalSubspace(ModularSymbols(61,2,1));TT:=HeckeOperator(M,2);printf "S15_JZERO61_F2_ORDER=%o\n",Determinant(3*IdentityMatrix(Rationals(),4)-TT);
print "S15_BETA61_FINITE_IMAGE_CERTIFIED";quit;
