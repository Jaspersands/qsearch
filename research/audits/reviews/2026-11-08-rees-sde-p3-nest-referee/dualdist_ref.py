"""How often does the peeled pool F* still have proportional pairs (dual distance 2)?  And sigma vs bounds."""
import math, numpy as np
import adversarial_ref as A
from wnest_ref import WNEST, theorem_bound
print("family        n  pieces  pieces_with_size2_class  max#size2  max 9Var/(2N*)  (dual distance >=3 <=> ratio 1)")
for f in ["random", "dup_blocks", "chain5", "coloops", "series3", "series4", "weight2", "subspace"]:
    for n in (20, 30):
        m = math.ceil(theorem_bound(n)); P = W2 = 0; mx = 0; rat = 0
        for rep in range(4):
            v = A.fam(f, n, m); W = WNEST(v); W.run()
            for L in W.log:
                if "c2" in L:
                    P += 1; W2 += L["c2"] > 0; mx = max(mx, L["c2"]); rat = max(rat, L["var9"] / (2 * L["Ns"]))
        print(f"{f:12s} {n:3d}  {P:5d}   {W2:5d}                  {mx:4d}       {rat:.3f}")
