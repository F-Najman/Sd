SetQuitOnError(true);SetColumns(0);ss:=Split(Read(Raw),";");
q:=StringToInteger(ss[1][4..#ss[1]]);dimension:=StringToInteger(ss[2][12..#ss[2]]);sequence:=eval ss[3][11..#ss[3]];
F:=GF(q);assert #sequence eq 2*dimension;C,L:=BerlekampMassey([F!a:a in sequence]);assert L eq dimension;
PrintFile(Final,Sprintf("q:=%o;dimension:=%o;linear_complexity:=%o;sequence:=%o;recurrence:=%o;",q,dimension,L,sequence,[Integers()!a:a in Eltseq(C)]):Overwrite:=true);
printf "S12_CPP_LINEAR_COMPLEXITY_CERTIFIED dimension=%o q=%o\n",dimension,q;quit;
