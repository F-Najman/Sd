from pathlib import Path
from unit_arithmetic import lit
W=Path(__file__).resolve().parent;H=W/'full97';S=W/'ss97';S.mkdir(exist_ok=True)
s=(H/'stage2_chunk.m').read_text()
s=s.replace('assert a1 eq 1 and a3 eq 0;','if a1 eq 0 then assert a3 ne 0;return E,P;end if;assert a1 eq 1 and a3 eq 0;')
a=s.index('function PsiN(');b=s.index('function CanonicalJets',a)
psi='''function PsiGeneral(xx,aa)
 a1,a2,a3,a4,a6:=Explode(aa);PS:=Parent(xx);b2:=a1^2;b4:=a1*a3;b6:=a3^2;b8:=a1^2*a6+a1*a3*a4+a2*a3^2+a4^2;v:=a1*xx+a3;
 pp:=[PS!0,PS!1,v,xx^4+b2*xx^3+b4*xx^2+b6*xx+b8,v*(b2*xx^5+b4*xx^4+(b2*b8+b4*b6)*xx+(b4*b8+b6^2))];
 for n in[5..N]do m:=n div 2;if IsOdd(n)then pn:=pp[m+3]*pp[m+1]^3+pp[m]*pp[m+2]^3;else pn:=pp[m+1]/v*(pp[m+3]*pp[m]^2+pp[m-1]*pp[m+2]^2);end if;Append(~pp,pn);end for;return pp[N+1];
end function;
'''
s=s[:a]+psi+s[b:]
a=s.index(' F:=BaseRing(E);aa:=aInvariants(E);assert aa[1]',s.index('function CanonicalJets'));b=s.index('xy:=UnitValues(',a)
new=''' F:=BaseRing(E);aa:=aInvariants(E);PS<u>:=PowerSeriesRing(F,jprec);xx:=PS!P[1];yy:=PS!P[2];ap:=[PS!a:a in aa];if aa[1]eq 0 then ap[1]+:=u;else ap[5]+:=u;end if;
 PX<X>:=PolynomialRing(F);assert PsiGeneral(X,[PX!a:a in aa])eq DivisionPolynomial(E,N);
 der:=Coefficient(PsiGeneral(xx+u,[PS!a:a in aa]),1);assert der ne 0 and aa[1]*P[1]+aa[3]ne 0;
 for n in[1..jprec-1]do xx+:=(Coefficient(PsiGeneral(xx,ap),n)/der)*u^n;assert Valuation(PsiGeneral(xx,ap))ge n+1;end for;
 for n in[1..jprec-1]do er:=Coefficient(yy^2+ap[1]*xx*yy+ap[3]*yy+xx^3+ap[2]*xx^2+ap[4]*xx+ap[5],n);yy+:=(er/(aa[1]*P[1]+aa[3]))*u^n;assert Valuation(yy^2+ap[1]*xx*yy+ap[3]*yy+xx^3+ap[2]*xx^2+ap[4]*xx+ap[5])ge n+1;end for;
 '''
s=s[:a]+new+s[b:];s=s.replace('xy:=UnitValues([PS!1,PS!a2,PS!0,PS!0,a6],xx,yy);','xy:=UnitValues(ap,xx,yy);')
assert'jprec:=Min(N eq 101 select 4 else 3,160 div d)'in s
s=s.replace('jprec:=Min(N eq 101 select 4 else 3,160 div d)','jprec:=Min(24,480 div d)').replace('if not rec[7]or rec[1]ne 20 then','if rec[7]or rec[1]ne 16 then').replace('/hecke_jets_','/ss_jets_')
(H/'stage2_ss.m').write_text(s)
(S/'units_data.m').write_bytes((H/'units_data.m').read_bytes())
t=(W/'full_sieve.py').read_text().replace("H=W/f'full{N}'","H=W/f'ss{N}'").replace('97:{7:1,6:-1,1:1,0:-1}','97:{5:1,4:-1,3:-1,2:1,1:1,0:-1}')
t=t.replace("z=[row[:(4 if N==101 else 3)]for row in z]if N!=131 else z;",'').replace("1<=len(z[0])<=8","1<=len(z[0])<=24").replace('1<=k<=8','1<=k<=24')
(W/'ss_sieve.py').write_text(t)
rs=lit((W/'sources97.m').read_text().replace('true','True').replace('false','False'),'AuditSources');ids=[i+1 for i,z in enumerate(rs)if not z[6]and z[0]==16];assert len(ids)==1
import subprocess
si=ids[0]
with(H/'ss_export.log').open('w')as f:r=subprocess.run(['magma','-b',f'Start:={si}',f'End:={si}',str(H/'stage2_ss.m')],stdout=f,stderr=subprocess.STDOUT)
st=(H/'ss_export.log').read_text();assert r.returncode==0 and'AUDIT_ACTUAL_HECKE_JETS_COMPLETE'in st and'Runtime error'not in st
(S/'hecke_jets.m').write_bytes((H/f'ss_jets_{si}.m').read_bytes())
with(S/'sieve.log').open('w')as f:r=subprocess.run(['python3',str(W/'ss_sieve.py'),'97'],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
print('S20_SS97_OBSTRUCTION_CALCULATION_COMPLETE',flush=True)
