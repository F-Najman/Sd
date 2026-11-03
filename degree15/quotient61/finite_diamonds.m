SetQuitOnError(true);SetColumns(0);tt:=Cputime();Out:=[**];
for ind in[30,2]do
 h:=ind eq 30 select 1 else 4;S:=CuspidalSubspace(ModularSymbolsH(61,[h],2,1));g:=Dimension(S);assert g eq (ind eq 30 select 126 else 8);
 e:=WindingElementProjection(S);T2:=Transpose(DualHeckeOperator(S,2));T4:=Transpose(DualHeckeOperator(S,4));A:=AmbientSpace(S);phi:=RationalMapping(S);PM:=Matrix(Rationals(),[Eltseq(phi(b)):b in Basis(A)]);assert HeckeOperator(A,2)*PM eq PM*T2;assert HeckeOperator(A,4)*PM eq PM*T4;
 D2:=(T2^2-T4)/2;assert D2^ind eq IdentityMatrix(Rationals(),g);
 rows:=[];v:=e;for k in[0..g-1]do Append(~rows,Eltseq(v));v:=v*T2;end for;W:=Matrix(Rationals(),rows);U:=D2^(ind eq 30 select 6 else 1)-1;r:=Rank(W);assert r eq (ind eq 30 select 123 else 7);assert Rank(VerticalJoin(W,U))eq r;
 // W consists of Hecke translates of the winding element in period coordinates.
 // Thus image(U) is supported entirely on the analytic rank-zero factors.
 pairs:=func<M|[<Numerator(a),Denominator(a)>:a in Eltseq(M)]>;
 Append(~Out,<ind,g,r,pairs(W),pairs(U)>);
 printf "S15_DIAMOND_FINITE_IMAGE index=%o genus=%o winding_rank=%o operator_rank=%o verified=true elapsed=%o\n",ind,g,r,Rank(U),Cputime(tt);
end for;
PrintFile("work/degree15/quotient61/finite_diamonds_data.m",Sprintf("FiniteDiamondData:=%o;",Out):Overwrite:=true);print "S15_DIAMOND_FINITE_IMAGES_COMPLETE";quit;
