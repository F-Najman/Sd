SetQuitOnError(true);SetColumns(0);out:=[**];
for p in[59,71]do
 S:=CuspidalSubspace(ModularSymbolsH(p,[1],2,1));g:=Dimension(S);assert g eq ExactQuotient((p-5)*(p-7),24);e:=WindingElementProjection(S);T:=Transpose(DualHeckeOperator(S,2));v:=e;rr:=[];
 for j in[0..g-1]do Append(~rr,Eltseq(v));v:=v*T;end for;W:=Matrix(Rationals(),rr);assert Rank(W)eq g;
 Append(~out,<p,g,[<Numerator(z),Denominator(z)>:z in Eltseq(W)]>);printf "S20_FULL_JACOBIAN_WINDING_RANK_ZERO p=%o genus=%o winding_rank=%o verified=true\n",p,g,g;
end for;
PrintFile("work/degree20/rankzero_data.m",Sprintf("RankzeroData:=%o;",out):Overwrite:=true);print "S20_RANK_ZERO_COMPLETE";quit;
