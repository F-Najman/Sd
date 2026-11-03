SetQuitOnError(true);SetColumns(0);
S:=ModularSymbols(193,2,-1);I:=IntegralHeckeOperator(S,1);print Dimension(S),Nrows(I);
print AtkinLehnerOperator(S,193);
quit;
