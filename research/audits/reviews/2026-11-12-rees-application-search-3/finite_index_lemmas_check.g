# Lemmas N1 (exponent of G/Core(H) divides [G:H]) and N2 ([G:H] divides prod e_ij)
# for random subgroups H of UT_4(Z/m), which is G/Gamma(m) for G = UT_4(Z).
# x_ij = I + E_ij in the Mal'cev order (by distance from diagonal, top grade last);
# e_ij = least e > 0 with x_ij^e in H. Finite check only (TRAPS 7).
UTgens := function(n, m)
  local R, gens, i, j, M;
  R := ZmodnZ(m); gens := [];
  for i in [1..n-1] do for j in [i+1..n] do
    M := IdentityMat(n, R); M[i][j] := One(R); Add(gens, M);
  od; od;
  return gens;
end;
Check := function(n, m, trials)
  local gens, G, t, H, N, es, e, x, P, core, expo, bad, k;
  gens := UTgens(n, m); G := Group(gens); bad := 0;
  Print("UT_", n, "(Z/", m, "), order ", Size(G), "\n");
  for t in [1..trials] do
    k := Random([1,2,3]);
    H := Group(List([1..k], i -> PseudoRandom(G)));
    N := Index(G, H);
    es := [];
    for x in gens do e := 1; while not x^e in H do e := e + 1; od; Add(es, e); od;
    core := Core(G, H); expo := Exponent(G / core);
    if (Product(es) mod N <> 0) or (N mod expo <> 0) then bad := bad + 1; fi;
    Print("  trial ", t, ": [G:H]=", N, " prod e=", Product(es),
          " N|prod e: ", Product(es) mod N = 0, "  exp(G/Core)=", expo,
          " exp|N: ", N mod expo = 0, " normal: ", IsNormal(G, H), "\n");
  od;
  Print("  failures: ", bad, "\n");
end;
Reset(GlobalMersenneTwister, 20261112);
Check(4, 12, 12);
Check(4, 10, 8);
Check(5, 6, 6);
QUIT;
