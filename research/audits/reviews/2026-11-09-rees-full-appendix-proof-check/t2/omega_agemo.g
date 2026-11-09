# t2 check 3: Prop black-box(iii) / appendix 1246-1249: "strict inclusion mho_{e-1}(G) < Omega_1(G)
# in 49 of the 58 groups of order 3^3 to 3^5 and 5^3 to 5^4 with class below p and exponent above p".
tot := 0;; strict := 0;; bad := 0;;
for pr in [[3,3],[3,4],[3,5],[5,3],[5,4]] do
  p := pr[1];; n := pr[2];; cnt := 0;; scnt := 0;;
  for i in [1..NumberSmallGroups(p^n)] do
    G := SmallGroup(p^n, i);;
    if NilpotencyClassOfGroup(G) < p and Exponent(G) > p then
      e := Length(Factors(Exponent(G)));;
      A := Agemo(G, p, e-1);; O := Omega(G, p, 1);;
      if not IsSubgroup(O, A) then bad := bad + 1; fi;
      # regular p-group: Omega_1 = set of elements of order dividing p
      if Size(O) <> Number(Elements(G), g -> g^p = One(G)) then bad := bad + 1; fi;
      cnt := cnt + 1;;
      if Size(A) < Size(O) then scnt := scnt + 1; fi;
    fi;
  od;
  Print("order ", p, "^", n, ": ", cnt, " groups, strict in ", scnt, "\n");
  tot := tot + cnt;; strict := strict + scnt;;
od;
Print("TOTAL ", tot, " groups, strict inclusion in ", strict, ", inconsistencies ", bad, "\n");
# metacyclic C_{p^2} : C_p, p = 3,5,7: |Omega_1| = p^2, |mho_1| = p
for p in [3,5,7] do
  F := FreeGroup("a","b");; a := F.1;; b := F.2;;
  G := F / [a^(p^2), b^p, b*a*b^-1*a^-(1+p)];;
  G := Image(IsomorphismPcGroup(G));;
  Print("metacyclic p=", p, ": |G|=", Size(G), " class ", NilpotencyClassOfGroup(G),
        " |Omega_1|=", Size(Omega(G,p,1)), " |mho_1|=", Size(Agemo(G,p,1)), "\n");
od;
QUIT;
