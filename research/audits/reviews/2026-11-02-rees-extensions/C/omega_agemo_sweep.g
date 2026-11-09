# Item C: for every group G of order p^n (p in {3,5}, n<=4, plus 3^5) with class < p and
# exponent p^e, e >= 2, compare Omega_1(G) = {g : g^p = 1} with
# agemo_{e-1}(G) = {g^(p^(e-1))}, which is Phi(Omega_1(F_{s,c})) for the free cover
# over Z/p^e (F is a free Z/p^e-module, so F[p] = p^(e-1) F).
# Run: printf 'Read("<this file>");\nQUIT;\n' | $E/gap -q
res := []; p := 0; e := 0;
for pn in [[3,3],[3,4],[3,5],[5,3],[5,4]] do
  p := pn[1]; n := pn[2];
  tot := 0; strict := 0; om_sub := 0; eq := 0;
  for G in AllSmallGroups(p^n) do
    if NilpotencyClassOfGroup(G) < p and Exponent(G) > p then
      tot := tot + 1;
      e := Length(FactorsInt(Exponent(G)));
      els := AsList(G);
      om := Filtered(els, g -> g^p = One(G));
      ag := Set(els, g -> g^(p^(e-1)));
      if Size(Group(om)) = Length(om) then om_sub := om_sub + 1; fi;
      if not IsSubset(om, ag) then Print("AGEMO NOT IN OMEGA ", IdGroup(G), "\n"); fi;
      if Length(ag) < Length(om) then strict := strict + 1; else eq := eq + 1; fi;
    fi;
  od;
  Add(res, [p, n, tot, strict, eq, om_sub]);
od;
Print("[p, n, #groups class<p exp>p, #agemo_{e-1} strictly smaller than Omega_1, #equal, #Omega_1 is a subgroup]\n");
for r in res do Print(r, "\n"); od;
# the metacyclic example
for p in [3,5,7] do
  F := FreeGroup("a","b"); a := F.1; b := F.2;
  G := F / [a^(p^2), b^p, b*a*b^-1*a^-(1+p)];
  G := Image(IsomorphismPcGroup(G));
  Print("p=", p, " metacyclic IdGroup ", IdGroup(G), " |Omega1| ",
        Length(Filtered(AsList(G), g -> g^p = One(G))),
        " |agemo1| ", Length(Set(AsList(G), g -> g^p)), " class ", NilpotencyClassOfGroup(G), "\n");
od;
