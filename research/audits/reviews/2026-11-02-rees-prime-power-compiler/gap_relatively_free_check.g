# Independent check of the mod-p^e word evaluation on a non-matrix target.
# Reads PP_* data (pp_data_p{p}_c{c}.g) written by prime_power_lazard_words.gap_data.
# G = largest class-c quotient of C_M * C_M (M=p^e), built by GAP's p-quotient algorithm.
# G is the relatively free class-c exponent-M group, so Lazard predicts |G| = M^d, d = rank F_{2,c}.
SizeScreen([4000, 24]);;
EvalProg := function(r, x, y)
  local v, ins;
  v := [One(x), x, y];
  for ins in r.prog do
    if ins[1] = 1 then Add(v, v[ins[2]]*v[ins[3]]); else Add(v, v[ins[2]]^ins[3]); fi;
  od;
  return v[r.out];
end;;
MakePhi := function(gens, add, br)
  local imgs, i, t;
  imgs := [];
  for i in PP_order do
    t := PP_tree[i];
    if t[2] = 0 then imgs[i] := gens[t[1]]; else imgs[i] := EvalProg(br, imgs[t[1]], imgs[t[2]]); fi;
  od;
  return function(u)
    local r, j;
    r := One(gens[1]);
    for j in [1..Length(u)] do
      if u[j] <> 0 then r := EvalProg(add, r, imgs[j]^u[j]); fi;
    od;
    return r;
  end;
end;;
HomOK := function(phi)
  return ForAll(PP_triples, t -> phi(t[1])*phi(t[2]) = phi(t[3]));
end;;
F := FreeGroup(2);; fx := F.1;; fy := F.2;;
ws := [[fx],[fy]];;
for k in [2..PP_c+1] do ws := Concatenation(List(ws, w -> List([fx,fy], g -> Concatenation(w,[g])))); od;;
Gfp := F/Concatenation([fx^PP_M, fy^PP_M], List(ws, LeftNormedComm));;
t0 := Runtime();;
pc := PP_c+PP_e-2;; prev := 0;;
repeat
  pc := pc+1; hom := EpimorphismPGroup(Gfp, PP_p, pc); Q := Image(hom);
  done := Size(Q) = prev; prev := Size(Q);
until done;
gens := [Image(hom, Gfp.1), Image(hom, Gfp.2)];;
phi := MakePhi(gens, PP_add, PP_bracket);;
phiold := MakePhi(gens, PP_add_modp, PP_bracket_modp);;
unit := List([1..PP_d], i -> 0);;
genok := ForAll([1,2], i -> phi(List([1..PP_d], j -> Number([PP_tree[j]], t -> t = [i,0]))) = gens[i]);;
# A non-free quotient: kill a random element of the second centre term chain.
N := NormalClosure(Q, [Comm(gens[1], Comm(gens[1], gens[2]))^PP_p * Comm(gens[2], Comm(gens[1], gens[2]))]);;
nat := NaturalHomomorphismByNormalSubgroup(Q, N);;
qgens := List(gens, g -> Image(nat, g));;
phiq := MakePhi(qgens, PP_add, PP_bracket);;
phiqold := MakePhi(qgens, PP_add_modp, PP_bracket_modp);;
Print("RESULT p=", PP_p, " e=", PP_e, " c=", PP_c, " d=", PP_d,
      " order_is_M^d=", Size(Q) = PP_M^PP_d, " class=", NilpotencyClassOfGroup(Q), " exponent=", Exponent(Q),
      " generators_ok=", genok, " hom_mod_p^e=", HomOK(phi), " hom_mod_p_control=", HomOK(phiold),
      " quotient_order=", Collected(Factors(Size(Image(nat)))), " quotient_hom_mod_p^e=", HomOK(phiq),
      " quotient_hom_mod_p_control=", HomOK(phiqold), " samples=", Length(PP_triples),
      " pclass=", pc-1, " seconds=", Int((Runtime()-t0)/1000), "\n");
QUIT;
