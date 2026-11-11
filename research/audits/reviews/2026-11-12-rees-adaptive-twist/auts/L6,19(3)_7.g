LoadPackage("autpgrp");;
# L6,19(3) over F_7, dim 6, class 3, levels [1, 1, 1, 2, 2, 3]
F := FreeGroup(6);; g := GeneratorsOfGroup(F);;
coll := SingleCollector(F, ListWithIdenticalEntries(6, 7));;
SetConjugate(coll, 2, 1, g[2]^1*g[4]^6*g[6]^4);
SetConjugate(coll, 3, 1, g[3]^1*g[5]^6*g[6]^5);
SetConjugate(coll, 4, 2, g[4]^1*g[6]^6);
SetConjugate(coll, 5, 3, g[5]^1*g[6]^4);
G := GroupByRws(coll);;
LEVEL := [1, 1, 1, 2, 2, 3];; CLS := 3;; P := 7;; NAME := "L6,19(3)";;
pc := FamilyPcgs(G);; if not IsConfluent(G) then Print("NOTCONFLUENT\n"); fi;
A := AutomorphismGroup(G);;
PrintTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L6,19(3)_7.gout", "SIZE ", Size(A), "\n");
for a in GeneratorsOfGroup(A) do AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L6,19(3)_7.gout", "GEN ", List(pc, x -> ExponentsOfPcElement(pc, Image(a, x))), "\n"); od;
AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L6,19(3)_7.gout", "END\n");
QUIT;
