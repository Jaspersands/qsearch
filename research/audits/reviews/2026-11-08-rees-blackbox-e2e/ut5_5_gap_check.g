# Independent check (GAP 4.15) of the ut5_5 black-box group in theorems/rees_blackbox_end_to_end.py:
# g0 = I+E01+E23, g1 = I+E12+E24 (0-indexed) in UT_5(F_5); GAP is 1-indexed.
F:=GF(5);; one:=One(F);;
Eij:=function(i,j) local m; m:=NullMat(5,5,F); m[i][j]:=one; return m; end;;
I5:=IdentityMat(5,F);;
a:=I5+Eij(1,2)+Eij(3,4);; b:=I5+Eij(2,3)+Eij(3,5);;
G:=Group(a,b);;
Print("order ", Size(G), " class ", NilpotencyClassOfGroup(G), " exponent ", Exponent(G), "\n");
Print("IdGroup ", IdGroup(G), "\n");
Print("lower central series orders ", List(LowerCentralSeriesOfGroup(G), Size), "\n");
Print("rank (min generators) ", Length(MinimalGeneratingSet(G)), "\n");
