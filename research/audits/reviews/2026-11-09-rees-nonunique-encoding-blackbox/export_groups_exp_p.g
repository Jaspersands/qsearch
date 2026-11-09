# Export small p-groups of exponent p and class < p (plus C3^2 and C5^2) as permutation
# groups with a minimal generating set and all subgroups (conjugacy class representatives
# above order 625). Run: gap -q -c 'DIR:="<this folder>";' export_groups_exp_p.g
out := OutputTextFile(Concatenation(DIR, "/groups_exp_p.txt"), false);
SetPrintFormattingStatus(out, false);
emit := function(tag, G, p)
  local iso, P, gens, subs, deg, cl;
  iso := SmallerDegreePermutationRepresentation(Image(IsomorphismPermGroup(G)));
  P := Image(iso);
  deg := LargestMovedPoint(P);
  gens := MinimalGeneratingSet(P);
  if Size(P) <= 625 then subs := List(AllSubgroups(P), H -> GeneratorsOfGroup(H));
  else subs := List(ConjugacyClassesSubgroups(P), cc -> GeneratorsOfGroup(Representative(cc))); fi;
  cl := NilpotencyClassOfGroup(P);
  AppendTo(out, "GROUP ", tag, " ", p, " ", Size(P), " ", cl, " ", Exponent(P), " ", deg, "\n");
  AppendTo(out, "GENS ", List(gens, g -> ListPerm(g, deg)), "\n");
  for H in subs do AppendTo(out, "SUB ", List(H, g -> ListPerm(g, deg)), "\n"); od;
end;
emit("9_2", SmallGroup(9, 2), 3);
emit("25_2", SmallGroup(25, 2), 5);
for spec in [[27,3],[81,3],[243,3],[125,5],[625,5],[343,7],[2401,7]] do
  n := spec[1]; p := spec[2];
  for i in [1..NumberSmallGroups(n)] do
    G := SmallGroup(n, i);
    if Exponent(G) = p and NilpotencyClassOfGroup(G) < p and not IsAbelian(G)
       and Length(MinimalGeneratingSet(G)) <= 3 then
      emit(Concatenation(String(n), "_", String(i)), G, p);
    fi;
  od;
od;
CloseStream(out);
QUIT;
