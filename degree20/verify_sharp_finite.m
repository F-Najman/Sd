SetQuitOnError(true);SetColumns(0);load "work/degree20/strange_eigenvalues_data.m";Records:=[**];
function Code(x)return[<Numerator(a),Denominator(a)>:a in Eltseq(x)];end function;
for dat in[<97,12,5>,<101,10,2>]do
 p,n,r:=Explode(dat);K<z>:=CyclotomicField(n);G:=DirichletGroup(p,K);chi:=G.1^ExactQuotient(#G,n);j:=Rep([j:j in[1..n]|z^j eq chi(r)]);chi:=chi^Modinv(j,n);assert chi(r)eq z;
 S:=CuspidalSubspace(ModularSymbols(chi,2,1));d:=Dimension(S);e:=WindingElementProjection(S);T2:=Transpose(DualHeckeOperator(S,2));rr:=[];v:=e;
 for j in[0..d-1]do Append(~rr,Eltseq(v));v:=v*T2;end for;W:=Matrix(K,rr);rank:=Rank(W);assert rank eq d-1;
 for q in[2,3,5,7]do
  a:=K!StrangeHeckeEigenvalues[<p,q>];U:=Transpose(DualHeckeOperator(S,q))-a*IdentityMatrix(K,d);assert Rank(VerticalJoin(W,U))eq rank;
  Append(~Records,<p,n,r,q,[Integers()!a:a in Eltseq(DefiningPolynomial(K))],d,[Code(a):a in Eltseq(W)],[Code(a):a in Eltseq(U)],rank>);
  printf "S20_SHARP_FINITE_WINDING_IMAGE p=%o n=%o q=%o dimension=%o winding_rank=%o verified=true\n",p,n,q,d,rank;
 end for;
end for;PrintFile("work/degree20/sharp_finite_data.m",Sprintf("SharpFiniteData:=%o;",Records):Overwrite:=true);print "S20_SHARP_FINITE_IMAGE_COMPLETE";quit;
