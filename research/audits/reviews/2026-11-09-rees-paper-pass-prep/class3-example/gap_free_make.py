"""Write gap_free_p5.g: G = exp of the free 2-generator class-3 Lie algebra over F_5, as a
permutation group (right BCH multiplication on its 3125 elements). GAP checks the Related Work
claims (no abelian subgroup of index p, not abelian-by-cyclic, <exp x>, <exp y> do not permute),
|Aut(G)| and the central action, and the stabilizers used in example_free.tex."""
import numpy as np
from verify_free import L_tensor, bch, enc, all_vectors, M

p = 5
TL = L_tensor(p)
G = all_vectors(M, p)
G = G[np.argsort(enc(G, p))]


def perm(w):
    img = enc(bch(TL, G, np.broadcast_to(np.array(w) % p, G.shape), p), p)
    return "PermList([" + ",".join(str(int(i) + 1) for i in img) + "])"


lines = [f"p := {p};", f"gx := {perm((1,0,0,0,0))};", f"gy := {perm((0,1,0,0,0))};",
         f"gu := {perm((0,0,0,1,0))};", f"gw := {perm((0,0,0,0,1))};",
         f"gv := {perm((1,0,1,1,0))};", f"gc := {perm((0,0,1,1,0))};"]
fam = [perm((1, 0, a, b, c)) for a in range(p) for b in range(p) for c in range(p)]
lines.append("famx := [" + ",\n".join(fam) + "];")
lines.append(r'''
LoadPackage("autpgrp");
onsub := function(U, a) return Image(a, U); end;;
G := Group(gx, gy);;
Print("|G| = ", Size(G), " exponent ", Exponent(G), " class ", NilpotencyClassOfGroup(G), "\n");
Print("Z(G) = <exp u, exp w>: ", Centre(G) = Group(gu, gw), "; |G'| = ", Size(DerivedSubgroup(G)), "\n");
max := MaximalSubgroups(G);;
Print("maximal subgroups: ", Length(max), ", all of index p: ", ForAll(max, U -> Index(G, U) = p),
      ", abelian ones: ", Number(max, IsAbelian), "\n");
idxp := Filtered(NormalSubgroups(G), N -> Index(G, N) = p);;
Print("subgroups of index p (all normal): ", Length(idxp), ", abelian: ", Number(idxp, IsAbelian), "\n");
ns := NormalSubgroups(G);;
abc := Filtered(ns, N -> IsAbelian(N) and IsCyclic(G/N));;
Print("normal subgroups: ", Length(ns), "; abelian N with G/N cyclic: ", Length(abc), " (abelian-by-cyclic: ", Length(abc) > 0, ")\n");
CX := Group(gx);; CY := Group(gy);;
prodset := Set(Flat(List(Elements(CX), a -> List(Elements(CY), b -> a*b))));;
Print("|<exp x><exp y>| = ", Length(prodset), ", |<exp x, exp y>| = ", Size(Group(gx, gy)),
      ": permute = ", Length(prodset) = Size(Group(gx, gy)), "\n");
iso := IsomorphismPcGroup(G);; P := Image(iso);;
A := AutomorphismGroup(P);;
Print("|Aut(G)| = ", Size(A), " = |GL_2(F_5)| 5^6: ", Size(A) = 480*5^6, "\n");
zu := Image(iso, gu);; zw := Image(iso, gw);;
scal := function(S) local out, a, iu, iw, k;
  out := [];
  for a in Elements(S) do
    iu := Image(a, zu); iw := Image(a, zw);
    k := First([1..p-1], k -> zu^k = iu and zw^k = iw);
    if k <> fail then AddSet(out, k); fi;
  od;
  return out;
end;;
SH := Stabilizer(A, Image(iso, Group(gv)), onsub);;
Print("H = <exp(x+z+u)>: |Stab| = ", Size(SH), ", central scalars ", scal(SH), "\n");
SC := Stabilizer(A, Image(iso, Group(gc)), onsub);;
Print("H' = <exp(z+u)>: |Stab| = ", Size(SC), ", central scalars ", scal(SC), "\n");
S := A;;
for f in famx do S := Stabilizer(S, Image(iso, Group(f)), onsub); od;
Print("joint stabilizer of all <exp(x + c)>, c in [L,L]: |S| = ", Size(S), ", central scalars ", scal(S),
      ", acts trivially on Z(G): ", ForAll(GeneratorsOfGroup(S), a -> Image(a, zu) = zu and Image(a, zw) = zw), "\n");
QUIT;
''')
open("gap_free_p5.g", "w").write("\n".join(lines))
print("written")
