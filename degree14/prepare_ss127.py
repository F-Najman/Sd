from pathlib import Path
W=Path(__file__).resolve().parent;s=(W.parent/'degree13/full113/stage2.m').read_text();s=s.replace(str(W.parent/'degree13'),str(W)).replace('full113','full127').replace('sources113','sources127')
a=s.index('function SimplifyPoint');b=s.index('function UnitValues',a);s=s[:a]+'function SimplifyPoint(E,P)return E,P;end function;\n'+s[b:]
a=s.index('function PsiN');b=s.index('function CanonicalJets',a)
psi='''function PsiN(xx,aa)
 PS:=Parent(xx);a1,a2,a3,a4,a6:=Explode(aa);b2:=a1^2;b4:=a1*a3;b6:=a3^2;b8:=a1^2*a6+a1*a3*a4+a2*a3^2+a4^2;psi2:=a1*xx+a3;
 pp:=[PS!0,PS!1,psi2,xx^4+b2*xx^3+b4*xx^2+b6*xx+b8,psi2*(b2*xx^5+b4*xx^4+(b2*b8+b4*b6)*xx+b4*b8+b6^2)];
 for n in[5..N]do m:=n div 2;if IsOdd(n)then pn:=pp[m+3]*pp[m+1]^3+pp[m]*pp[m+2]^3;else pn:=pp[m+1]/psi2*(pp[m+3]*pp[m]^2+pp[m-1]*pp[m+2]^2);end if;Append(~pp,pn);end for;return pp[N+1];
end function;
'''
s=s[:a]+psi+s[b:];a=s.index(' F:=BaseRing(E);aa:=aInvariants(E);assert aa[1]eq 1',s.index('function CanonicalJets'));b=s.index(' xy:=UnitValues(',a)
new=''' F:=BaseRing(E);aa0:=aInvariants(E);assert aa0[1]eq 0 and aa0[3]ne 0;PS<u>:=PowerSeriesRing(F,8);aa:=[PS!v:v in aa0];aa[1]+:=u;xx:=PS!P[1];yy:=PS!P[2];der:=Coefficient(PsiN(xx+u,[PS!v:v in aa0]),1);assert der ne 0;dy:=aa0[1]*P[1]+aa0[3];assert dy ne 0;
 for n in[1..7]do xx+:=(Coefficient(PsiN(xx,aa),n)/der)*u^n;assert Valuation(PsiN(xx,aa))ge n+1;end for;
 for n in[1..7]do er:=Coefficient(yy^2+aa[1]*xx*yy+aa[3]*yy+xx^3+aa[2]*xx^2+aa[4]*xx+aa[5],n);yy+:=(er/dy)*u^n;assert Valuation(yy^2+aa[1]*xx*yy+aa[3]*yy+xx^3+aa[2]*xx^2+aa[4]*xx+aa[5])ge n+1;end for;
'''
s=s[:a]+new+s[b:];s=s.replace('xy:=UnitValues([PS!1,PS!a2,PS!0,PS!0,a6],xx,yy)','xy:=UnitValues(aa,xx,yy)');s=s.replace('if not rec[7]then continue;end if;','if rec[7]then continue;end if;')
(W/'full127/stage2.m').write_text(s)
