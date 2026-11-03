from pathlib import Path
W=Path(__file__).resolve().parent
for h in W.glob('full*'):
 p=h/'stage2_chunk.m'
 if not p.exists():continue
 s=p.read_text()
 s=s.replace('g:=genus;','g:=genus;\nRXa:=Submatrix(UnitXRelations,1,1,Nrows(UnitXRelations),g);RXb:=Submatrix(UnitXRelations,1,g+1,Nrows(UnitXRelations),g);RYa:=Submatrix(UnitYRelations,1,1,Nrows(UnitYRelations),g);RYb:=Submatrix(UnitYRelations,1,g+1,Nrows(UnitYRelations),g);')
 old='return VerticalJoin(Matrix(F,[[F!v[i]+x0*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[F!v[i]+y0*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)]));'
 new='return VerticalJoin(ChangeRing(RXa,F)+x0*ChangeRing(RXb,F),ChangeRing(RYa,F)+y0*ChangeRing(RYb,F));'
 assert old in s;s=s.replace(old,new)
 old='VerticalJoin(Matrix(F,[[Coefficient(xy[1],n)*v[g+i]:i in[1..g]]:v in Rows(UnitXRelations)]),Matrix(F,[[Coefficient(xy[2],n)*v[g+i]:i in[1..g]]:v in Rows(UnitYRelations)]))'
 new='VerticalJoin(Coefficient(xy[1],n)*ChangeRing(RXb,F),Coefficient(xy[2],n)*ChangeRing(RYb,F))';assert old in s;s=s.replace(old,new)
 old='br+:=Vector(F,[&+[RM[j+1][r,c]*zv[n-j+1][c]:c in[1..g]]:r in[1..Nrows(M0)]]);'
 new='br+:=zv[n-j+1]*Transpose(RM[j+1]);';assert old in s;s=s.replace(old,new)
 old='for n in[0..jprec-1]do for r in[1..Nrows(M0)]do assert &+[&+[RM[j+1][r,c]*zv[n-j+1][c]:c in[1..g]]:j in[0..n]]eq 0;end for;end for;'
 new='for n in[0..jprec-1]do er:=&+[zv[n-j+1]*Transpose(RM[j+1]):j in[0..n]];assert IsZero(er);end for;';assert old in s;s=s.replace(old,new)
 p.write_text(s)
# Retain one controlled replay alongside the old eight-term output.
p=W/'full127/stage2_chunk.m';s=p.read_text().replace('/full127/hecke_jets_','/full127/fast_test_');(W/'full127/fast_test.m').write_text(s)
