SetQuitOnError(true);SetColumns(0);SetMemoryLimit(160*10^9);SetSeed(20261029);SequenceOut:=SequenceOutput;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree12/large_orders/strange_primes_export.magma";
p:=StringToInteger(P);n:=StringToInteger(OrderToTest);assert IsPrime(p)and((p-1)div 2)mod n eq 0;
SetVerbose("User1",1);SetVerbose("User2",1);tt:=Cputime();q:=aux_prime(p);Fq:=GF(q);G:=DirichletGroup(p,Fq);chi:=G.1^ExactQuotient(#G,n);
assert Order(chi)eq n and IsEven(chi);
printf "S12_SELECTED_CHARACTER_START p=%o order=%o auxiliary_prime=%o\n",p,n,q;
result:=screen_character_lean(chi);assert result[1]eq 0;
printf "S12_SELECTED_CHARACTER_NONSTRANGE p=%o order=%o auxiliary_prime=%o rigorously_verified=true elapsed=%o\n",p,n,q,Cputime(tt);quit;
