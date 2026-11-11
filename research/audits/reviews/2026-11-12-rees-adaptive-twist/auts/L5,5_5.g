LoadPackage("autpgrp");;
# L5,5 over F_5, dim 5, class 3, levels [1, 1, 1, 2, 3]
F := FreeGroup(5);; g := GeneratorsOfGroup(F);;
coll := SingleCollector(F, ListWithIdenticalEntries(5, 5));;
SetConjugate(coll, 2, 1, g[2]^1*g[4]^4*g[5]^3);
SetConjugate(coll, 4, 1, g[4]^1*g[5]^4);
SetConjugate(coll, 3, 2, g[3]^1*g[5]^4);
G := GroupByRws(coll);;
LEVEL := [1, 1, 1, 2, 3];; CLS := 3;; P := 5;; NAME := "L5,5";;
pc := FamilyPcgs(G);; if not IsConfluent(G) then Print("NOTCONFLUENT\n"); fi;
A := AutomorphismGroup(G);;
PrintTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L5,5_5.gout", "SIZE ", Size(A), "\n");
for a in GeneratorsOfGroup(A) do AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L5,5_5.gout", "GEN ", List(pc, x -> ExponentsOfPcElement(pc, Image(a, x))), "\n"); od;
AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L5,5_5.gout", "END\n");
QUIT;
