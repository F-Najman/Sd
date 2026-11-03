SetQuitOnError(true);SetColumns(0);
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/full61/units_data.m";oldQ:=qcoeffs;oldD:=DiamondMatrix;oldPrec:=precision;
load "/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/extended_model.m";assert precision eq 2200;
C:=Solution(Submatrix(qcoeffs,1,1,genus,oldPrec),oldQ);assert C*Submatrix(qcoeffs,1,1,genus,oldPrec)eq oldQ and Rank(C)eq genus and oldD*C eq C*DiamondMatrix;
QQ:=C*qcoeffs;PrintFile("/home/fnajman/Documents/Codex/2026-10-28/on-this-computer-there-are-a/work/degree15/ss61/extended_q.m",Sprintf("ExtendedQ:=Matrix(GF(2),%o,%o,%o);",genus,precision,Eltseq(QQ)):Overwrite:=true);print "S15_SS61_OLD_BASIS_EXTENDED_VERIFIED";quit;
