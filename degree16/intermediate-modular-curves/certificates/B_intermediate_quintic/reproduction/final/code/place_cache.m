// Match degree-one and degree-two function-field places to projective points.
// Avoid the expensive point -> curve place -> function-field divisor path.
function LowDegreePlaceCache(C)
 k:=BaseRing(C); p:=#k; K:=GF(p^2);
 FC:=FunctionField(C); F,toF:=AlgorithmicFunctionField(FC);
 R:=CoordinateRing(Ambient(C)); n:=Rank(R);
 fs:=[toF(FC!(R.i/R.n)):i in [1..n]];
 cache:=AssociativeArray(); rational:={C|}; quadratic:={C(K)|};
 counts:=[];
 for d in [1,2] do
  ps:=Places(F,d); Append(~counts,#ps);
  for T in ps do
   vals:=[Valuation(f,T):f in fs]; j:=Index(vals,Min(vals));
   values:=[Evaluate(f/fs[j],T):f in fs];
   if Universe(values) cmpne K then Embed(Universe(values),K); end if;
   v:=[K!a:a in values];
   P:=C(K)!v;
   for a in [0..d-1] do
    Q:=C(K)![x^(p^a):x in Eltseq(P)]; key:=Eltseq(Q);
    assert not IsDefined(cache,key);
    cache[key]:=Divisor(T); Include(~quadratic,Q);
   end for;
   if d eq 1 then Include(~rational,C![k!x:x in Eltseq(P)]); end if;
  end for;
 end for;
 assert #rational eq counts[1] and #quadratic eq counts[1]+2*counts[2];
 return cache,Setseq(rational),Setseq(quadratic),K;
end function;
