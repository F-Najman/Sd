SetQuitOnError(true);SetColumns(0);tt:=Cputime();
prs:=[53,61,67,73,79,83,89,97,101,103];inds:=[13,15,11,12,39,41,11,8,5,17];
for k in [1..#prs]do
 p:=prs[k];ind:=inds[k];ns:=p in [61,67,73]select[2,3,5]else[p eq 97 select 5 else 2];h:=Integers()!((GF(p)!PrimitiveRoot(p))^ind);
 MS:=CuspidalSubspace(ModularSymbolsH(p,[h],2,0));e:=WindingElementProjection(MS);S:=ModularSymbolsH(p,[h],2,-1);
 S0:=CuspidalSubspace(ModularSymbols(p,2,1));g0:=Dimension(S0);e0:=WindingElementProjection(S0);T20:=Transpose(DualHeckeOperator(S0,2));ws:=[];v:=e0;for j in[0..g0-1]do Append(~ws,Eltseq(v));v:=v*T20;end for;W0:=Matrix(Rationals(),ws);r0:=Rank(W0);
 for n in ns do
  pol:=CharacteristicPolynomial(IntegralHeckeOperator(S,n));fac:=Factorization(pol);TnMS:=HeckeOperator(MS,n);
  flags:=[f[2] ge 2 or IsZero(e*Evaluate(ExactQuotient(pol,f[1]^f[2]),TnMS)):f in fac];killpol:=&*[Parent(pol)|fac[i][1]^fac[i][2]:i in[1..#fac]|flags[i]];
  Tn0:=Transpose(DualHeckeOperator(S0,n));U:=Evaluate(killpol,Tn0);rr:=Rank(VerticalJoin(W0,U));printf "S15_FI_FINITE_IMAGE p=%o index=%o n=%o killpol=%o gamma0_genus=%o winding_rank=%o image_union_rank=%o\n",p,ind,n,killpol,g0,r0,rr;assert rr eq r0;
 end for;
end for;
print "S15_ALL_SELECTED_FI_FINITE_IMAGE_CERTIFICATES_COMPLETE",Cputime(tt);quit;
