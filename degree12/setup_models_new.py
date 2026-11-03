from pathlib import Path
import re,json
W=Path(__file__).resolve().parent;B=W.parents[1];L=Path('/home/fnajman/degree9_torsion/nonic-torsion')
template=(B/'work/degree11/P61_full/canonical_units/stage1.m').read_text();template=template[:template.index('F<a>:=GF(2^9);chosen:=false;')]
for N in[107,109]:
 g=(N-5)*(N-7)//24;m=(N-1)//2;prec=max(1300,(N*N-1)//6+200);H=W/f'full{N}';H.mkdir(exist_ok=True)
 text=''.join((L/f'mdmagma/models_X1_n/FFFc{N}.txt').read_text().replace('\\','').split());terms={}
 for term in re.findall(r'[+-]?[^+-]+',text):
  c=1;i=j=0
  for a in term.lstrip('+-').rstrip(';').split('*'):
   if a.startswith('x'):i=int(a.split('^')[1])if'^'in a else 1
   elif a.startswith('y'):j=int(a.split('^')[1])if'^'in a else 1
   else:c*=int(a)
  terms[i,j]=terms.get((i,j),0)^(c&1)
 terms={k:v for k,v in terms.items()if v};px=max(j for i,j in terms);py=max(i for i,j in terms)
 vals={61:N,126:g,252:2*g,1300:prec,1800:prec+600,30:m,311:(N*N-1)//12+1,301:2*g-2+max(px,py),299:2*g-2+px,51:max(px,py)}
 s=re.sub(r'\b(?:'+'|'.join(map(str,vals))+r')\b',lambda z:str(vals[int(z[0])]),template)
 s=s.replace('Nrows(RX)gt 0 and Nrows(RY)gt 0','Nrows(RX)gt 0 and Nrows(RY)gt 0')
 s=s.replace('MS:=CuspidalSubspace','DiamondRoot:=1;repeat DiamondRoot:=NextPrime(DiamondRoot);until Order(GF(N)!DiamondRoot)eq N-1;\nMS:=CuspidalSubspace',1)
 s=s.replace('chi:=(Coefficient(ff,2)^2-Coefficient(ff,4))/2','chi:=(Coefficient(ff,DiamondRoot)^2-Coefficient(ff,DiamondRoot^2))/DiamondRoot')
 s=s.replace('ux2,uy2:=TateUnits(2)','ux2,uy2:=TateUnits(DiamondRoot)').replace('QPrec-10','QPrec-20-DiamondRoot')
 s=s.replace('Q0:=[];D0:=[];','Q0:=[];D0:=[];A0:=[];')
 extra='''if N eq 43 then
  chi11:=(Coefficient(ff,11)^2-Coefficient(ff,121))/11;
  lam:=(chi-1)*(Coefficient(ff,11)-chi11-11);
  ac:=[Flat(KF!(lam*Coefficient(ff,n))):n in[0..QPrec-1]];
  for k in[1..#Flat(KF!1)]do Append(~A0,[a[k]:a in ac]);end for;
 end if;
'''
 s=s.replace(' printf "NONIC83_CANONICAL_UNIT_EIGENFORM',extra+' printf "NONIC83_CANONICAL_UNIT_EIGENFORM')
 s+='''
function CodePoly(z)return[Integers()!a:a in Eltseq(z)];end function;
out:=OUTFILE;
PrintFile(out,Sprintf("N:=%o;genus:=%o;precision:=%o;DiamondRoot:=%o;DiamondOrder:=%o;PoleBoundX:=%o;PoleBoundY:=%o;SturmWeight2:=%o;SturmWeight4:=%o;qcoeffs:=Matrix(GF(2),%o,%o,%o);DiamondMatrix:=Matrix(GF(2),%o,%o,%o);UnitXRelations:=Matrix(GF(2),%o,%o,%o);UnitYRelations:=Matrix(GF(2),%o,%o,%o);",N,g,QPrec,DiamondRoot,(N-1)div 2,PX,PY,(N*N-1)div 12,(N*N-1)div 6,g,QPrec,Eltseq(Q2),g,g,Eltseq(Md),Nrows(RX),2*g,Eltseq(RX),Nrows(RY),2*g,Eltseq(RY)):Overwrite:=true);
if N eq 43 then
 AFull:=TT*Matrix(Rationals(),A0);AM:=Solution(QMR,AFull);assert AM*QMR eq AFull and &and[IsOdd(Denominator(a)):a in Eltseq(AM)];
 PrintFile(out,Sprintf("AlphaA11Cotangent:=Matrix(GF(2),%o,%o,%o);",g,g,Eltseq(ChangeRing(AM,GF(2)))));
end if;
printf "AUDIT_FULL_MODEL_COMPLETE N=%o genus=%o primitive=%o precision=%o pole_bounds=%o elapsed=%o\\n",N,g,DiamondRoot,QPrec,[PX,PY],Cputime(tt);quit;
'''.replace('OUTFILE','"'+str(H/'units_data.m')+'"').replace('PX',str(px)).replace('PY',str(py))
 (H/'build.m').write_text(s)
 print(N,g,prec,px,py)
