LoadPackage("autpgrp");;
# fil4 over F_7, dim 4, class 3, levels [1, 1, 2, 3]
F := FreeGroup(4);; g := GeneratorsOfGroup(F);;
coll := SingleCollector(F, ListWithIdenticalEntries(4, 7));;
SetConjugate(coll, 2, 1, g[2]^1*g[3]^6*g[4]^4);
SetConjugate(coll, 3, 1, g[3]^1*g[4]^6);
G := GroupByRws(coll);;
LEVEL := [1, 1, 2, 3];; CLS := 3;; P := 7;; NAME := "fil4";;
pc := FamilyPcgs(G);; if not IsConfluent(G) then Print("NOTCONFLUENT\n"); fi;
A := AutomorphismGroup(G);;
PrintTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/fil4_7.gout", "SIZE ", Size(A), "\n");
for a in GeneratorsOfGroup(A) do AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/fil4_7.gout", "GEN ", List(pc, x -> ExponentsOfPcElement(pc, Image(a, x))), "\n"); od;
AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/auts/fil4_7.gout", "END\n");
QUIT;
