SetQuitOnError(true);SetColumns(0);tt:=Cputime();
PrintFile("work/degree20/strange_eigenvalues_data.m","StrangeHeckeEigenvalues:=AssociativeArray();":Overwrite:=true);
for dat in[<97,12,5>,<101,10,2>]do
 p,n,r:=Explode(dat);K<z>:=CyclotomicField(n);G:=DirichletGroup(p,K);chi:=G.1^ExactQuotient(#G,n);j:=Rep([j:j in[1..n]|z^j eq chi(r)]);chi:=chi^Modinv(j,n);assert chi(r)eq z and Order(chi)eq n;
 S:=CuspidalSubspace(ModularSymbols(chi,2,1));dec:=NewformDecomposition(S);strange:=[A:A in dec|IsZero(WindingElementProjection(A))];assert #strange eq 1 and Dimension(strange[1])eq 1;A:=strange[1];
 for q in[2,3,5,7]do
  a:=HeckeOperator(A,q)[1,1];cc:=Eltseq(a);assert &and[IsIntegral(c):c in cc];cs:=[Integers()!c:c in cc];PrintFile("work/degree20/strange_eigenvalues_data.m",Sprintf("StrangeHeckeEigenvalues[<%o,%o>]:=%o;",p,q,cs));
  printf "S20_STRANGE_EIGENVALUE p=%o character_order=%o diamond=%o hecke_prime=%o coefficients=%o verified=true\n",p,n,r,q,cs;
 end for;
end for;print "S20_STRANGE_EIGENVALUES_COMPLETE",Cputime(tt);quit;
