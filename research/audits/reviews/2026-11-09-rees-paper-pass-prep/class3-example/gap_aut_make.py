"""Write gap_aut_p{5,7}.g: G = (L, BCH) as a permutation group by right multiplication,
then GAP/autpgrp computes |Aut(G)| and the central scalars of Stab_Aut(G)(H) for
H = <exp(x1+x2+x3+x4)>, Z(G), and the joint stabilizer of all <exp(x1+x2+a x3+b x4)>."""
import itertools
import numpy as np
from verify_class3 import L_tensor, bch, enc, all_vectors, M

for p in (5, 7):
    TL = L_tensor(p)
    G = all_vectors(M, p)
    idx = enc(G, p)
    order = np.argsort(idx)
    G = G[order]                      # G[i] has enc i
    def perm(w):
        img = enc(bch(TL, G, np.broadcast_to(np.array(w) % p, G.shape), p), p)
        return "PermList([" + ",".join(str(int(i) + 1) for i in img) + "])"
    lines = [f"p := {p};", f"gx1 := {perm((1,0,0,0))};", f"gx2 := {perm((0,1,0,0))};",
             f"gz := {perm((0,0,0,1))};", f"gv := {perm((1,1,1,1))};"]
    fam = [perm((1, 1, a, b)) for a in range(p) for b in range(p)]
    lines.append("fam := [" + ",\n".join(fam) + "];")
    lines.append(r'''
LoadPackage("autpgrp");
onsub := function(U, a) return Image(a, U); end;;
G := Group(gx1, gx2);;
Print("|G| = ", Size(G), ", exponent ", Exponent(G), ", class ", NilpotencyClassOfGroup(G), "\n");
Print("centre = <gz>: ", Centre(G) = Group(gz), "\n");
iso := IsomorphismPcGroup(G);; P := Image(iso);;
A := AutomorphismGroup(P);;
Print("|Aut(G)| = ", Size(A), " = (p-1)^2 p^5: ", Size(A) = (p-1)^2*p^5, "\n");
z := Image(iso, gz);;
scal := function(S) local ks, a, k, img;
  ks := [];
  for a in GeneratorsOfGroup(S) do
    img := Image(a, z);
    k := First([1..p-1], k -> z^k = img);
    Add(ks, k);
  od;
  if ks = [] then return [1]; fi;
  return Set(Elements(Group(List(ks, k -> Z(p)^LogFFE(k*One(GF(p)), Z(p))))), x -> IntFFE(x));
end;;
Print("central scalars of Aut(G): ", scal(A), "\n");
H := Image(iso, Group(gv));;
SH := Stabilizer(A, H, onsub);;
Print("H = <exp(x1+x2+x3+x4)>: |Stab| = ", Size(SH), ", central scalars ", scal(SH), "\n");
SZ := Stabilizer(A, Image(iso, Group(gz)), onsub);;
Print("Z(G): |Stab| = ", Size(SZ), ", central scalars ", scal(SZ), "\n");
S := A;;
for f in fam do S := Stabilizer(S, Image(iso, Group(f)), onsub); od;
Print("joint stabilizer of all <exp(x1+x2+a x3+b x4)>: |S| = ", Size(S), ", central scalars ", scal(S), "\n");
QUIT;
''')
    open(f"gap_aut_p{p}.g", "w").write("\n".join(lines))
print("written")
