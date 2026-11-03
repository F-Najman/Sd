from pathlib import Path
W=Path(__file__).resolve().parent
for n in[109,113]:
 p=W/f'full{n}/stage2.m';s=p.read_text()
 s=s.replace('function CanonicalJets(E,P,z0)','function CanonicalJets(E,P,z0,jprec)')
 a=s.index('function CanonicalJets');b=s.index('end function;',a);ss=s[a:b];ss=ss.replace('PowerSeriesRing(F,8)','PowerSeriesRing(F,jprec)').replace('[1..7]','[1..jprec-1]').replace('[0..7]','[0..jprec-1]');s=s[:a]+ss+s[b:]
 s=s.replace('jt:=CanonicalJets(E,P,z);d:=LCM([Degree(MinimalPolynomial(x,GF(2))):x in xy]);', 'd:=LCM([Degree(MinimalPolynomial(x,GF(2))):x in xy]);jprec:=Min(8,128 div d);assert jprec ge 2;jt:=CanonicalJets(E,P,z,jprec);')
 t=p.with_suffix('.new');t.write_text(s);t.replace(p)
# The universal positive-degree bound is 4*15*2=128 at both these levels.
# Every support multiplicity c satisfies c*closed_degree<=128.
