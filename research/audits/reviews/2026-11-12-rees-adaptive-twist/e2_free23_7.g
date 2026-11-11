# free23 over F_7, dim 5, class 3, levels [1, 1, 2, 3, 3]
F := FreeGroup(5);; g := GeneratorsOfGroup(F);;
coll := SingleCollector(F, ListWithIdenticalEntries(5, 7));;
SetConjugate(coll, 2, 1, g[2]^1*g[3]^6*g[4]^4*g[5]^4);
SetConjugate(coll, 3, 1, g[3]^1*g[4]^6);
SetConjugate(coll, 3, 2, g[3]^1*g[5]^6);
G := GroupByRws(coll);;
LEVEL := [1, 1, 2, 3, 3];; CLS := 3;; P := 7;; NAME := "free23";;
pc := FamilyPcgs(G);; T := CharacterTable(G);; irr := Irr(T);;
PrintTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/e2_free23_7.gout", "");
for w in [[1, 6, 2, 0, 3], [1, 0, 0, 1, 2], [3, 4, 3, 0, 5], [1, 5, 2, 3, 6]] do
  h := PcElementByExponents(pc, w);; H := Subgroup(G, [h]);; M := ClosureGroup(H, DerivedSubgroup(G));;
  TM := CharacterTable(M);; lin := LinearCharacters(M);;
  tot := 0;; eig := 0;; eig_nonlin := 0;;
  for chi in irr do
    pr := chi[1] / Size(G) * Sum(List(Elements(H), x -> x^chi));;
    tot := tot + pr;;
    r := RestrictedClassFunction(chi, M);;
    if ForAny(lin, psi -> ScalarProduct(r, psi) > 0) then eig := eig + pr;; if chi[1] > 1 then eig_nonlin := eig_nonlin + pr;; fi; fi;
  od;
  AppendTo("research/audits/reviews/2026-11-12-rees-adaptive-twist/e2_free23_7.gout", w, " total ", tot, " eigen_possible ", eig, " from_deg_p ", eig_nonlin, "\n");
od;
QUIT;
