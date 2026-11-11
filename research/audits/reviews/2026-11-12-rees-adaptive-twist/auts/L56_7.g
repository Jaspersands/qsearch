LoadPackage("autpgrp");;
# L56 over F_7, dim 5, class 4, levels [1, 1, 2, 3, 4]
F := FreeGroup(5);; g := GeneratorsOfGroup(F);;
coll := SingleCollector(F, ListWithIdenticalEntries(5, 7));;
SetConjugate(coll, 2, 1, g[2]^1*g[3]^6*g[4]^4*g[5]^5);
SetConjugate(coll, 3, 1, g[3]^1*g[4]^6*g[5]^4);
SetConjugate(coll, 4, 1, g[4]^1*g[5]^6);
SetConjugate(coll, 3, 2, g[3]^1*g[5]^6);
G := GroupByRws(coll);;
LEVEL := [1, 1, 2, 3, 4];; CLS := 4;; P := 7;; NAME := "L56";;
pc := FamilyPcgs(G);; if not IsConfluent(G) then Print("NOTCONFLUENT\n"); fi;
A := AutomorphismGroup(G);;
PrintTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L56_7.gout", "SIZE ", Size(A), "\n");
for a in GeneratorsOfGroup(A) do AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L56_7.gout", "GEN ", List(pc, x -> ExponentsOfPcElement(pc, Image(a, x))), "\n"); od;
AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/L56_7.gout", "END\n");
QUIT;
