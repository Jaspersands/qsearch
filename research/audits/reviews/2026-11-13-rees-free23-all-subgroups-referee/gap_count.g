# Referee 2026-11-13: count all subgroups of free23 = F/(gamma_4(F) F^p), F free of rank 2, by invariants.
# Invariants per subgroup H: [log|H|, log|H cap G2|, log|H cap G3|, IsSubset(H,[H,G2]) ].
CountFree23 := function(p)
  local F, P, N, Q, G, G2, G3, cls, res, c, H, k, key, i, total;
  F := FreeGroup(2);
  # <a,b | a^p, b^p>, largest quotient of lower exponent-p class <= 3.  Class 3 < p and generators of order p
  # make it regular, hence of exponent p, so it is free23 (order p^5 is checked below).
  Q := F / [F.1^p, F.2^p];
  G := Image(EpimorphismPGroup(Q, p, 3));
  Print("p=", p, " |G|=p^", LogInt(Size(G), p), " class=", NilpotencyClassOfGroup(G),
        " exponent=", Exponent(G), "\n");
  G2 := DerivedSubgroup(G);
  G3 := CommutatorSubgroup(G2, G);
  Print("  |G2|=p^", LogInt(Size(G2),p), " |G3|=p^", LogInt(Size(G3),p), "\n");
  cls := ConjugacyClassesSubgroups(G);
  res := rec(); total := 0;
  for c in cls do
    H := Representative(c); k := Size(c); total := total + k;
    key := String([LogInt(Size(H),p), LogInt(Size(Intersection(H,G2)),p),
                   LogInt(Size(Intersection(H,G3)),p),
                   IsSubset(H, CommutatorSubgroup(H, G2))]);
    if IsBound(res.(key)) then res.(key) := res.(key) + k; else res.(key) := k; fi;
  od;
  Print("  total subgroups = ", total, "\n");
  for i in RecNames(res) do Print("  ", i, " : ", res.(i), "\n"); od;
end;
CountFree23(5);
CountFree23(7);
QUIT;
