SetQuitOnError(true);SetColumns(0);out:=[**];
for d in[17..21]do
 F:=GF(2^d);curves:=[* *];cs:=[];
 for E in Twists(EllipticCurveFromjInvariant(F!0))do
  N:=Integers()!#E;Append(~cs,N);Append(~curves,<[[Integers()!c:c in Eltseq(a)]:a in aInvariants(E)],N>);
 end for;
 expected:=IsOdd(d)select{2^d+1-2^((d+1)div 2),2^d+1,2^d+1+2^((d+1)div 2)}else{2^d+1+j*2^(d div 2):j in[-2..2]};assert Seqset(cs)eq expected and #cs eq(IsOdd(d)select 3 else 7);
 Append(~out,<d,[Integers()!c:c in Eltseq(DefiningPolynomial(F))],curves>);print "S21_BOUND_TWISTS_CERTIFIED",d,Sort(cs);
end for;
PrintFile("work/degree21/bound_ss_data.m",Sprintf("BoundTwistData:=%o;",out):Overwrite:=true);print "S21_BOUND_TWISTS_CERTIFIED_COMPLETE";quit;
