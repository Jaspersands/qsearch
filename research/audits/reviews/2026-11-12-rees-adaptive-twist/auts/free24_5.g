LoadPackage("autpgrp");;
# free24 over F_5, dim 8, class 4, levels [1, 1, 2, 3, 3, 4, 4, 4]
F := FreeGroup(8);; g := GeneratorsOfGroup(F);;
coll := SingleCollector(F, ListWithIdenticalEntries(8, 5));;
SetConjugate(coll, 2, 1, g[2]^1*g[3]^4*g[4]^3*g[5]^3*g[6]^4*g[7]^1*g[8]^4);
SetConjugate(coll, 3, 1, g[3]^1*g[4]^4*g[6]^3);
SetConjugate(coll, 4, 1, g[4]^1*g[6]^4);
SetConjugate(coll, 5, 1, g[5]^1*g[7]^4);
SetConjugate(coll, 3, 2, g[3]^1*g[5]^4*g[8]^3);
SetConjugate(coll, 4, 2, g[4]^1*g[7]^4);
SetConjugate(coll, 5, 2, g[5]^1*g[8]^4);
G := GroupByRws(coll);;
LEVEL := [1, 1, 2, 3, 3, 4, 4, 4];; CLS := 4;; P := 5;; NAME := "free24";;
pc := FamilyPcgs(G);; if not IsConfluent(G) then Print("NOTCONFLUENT\n"); fi;
A := AutomorphismGroup(G);;
PrintTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/free24_5.gout", "SIZE ", Size(A), "\n");
for a in GeneratorsOfGroup(A) do AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/free24_5.gout", "GEN ", List(pc, x -> ExponentsOfPcElement(pc, Image(a, x))), "\n"); od;
AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/free24_5.gout", "END\n");
QUIT;
