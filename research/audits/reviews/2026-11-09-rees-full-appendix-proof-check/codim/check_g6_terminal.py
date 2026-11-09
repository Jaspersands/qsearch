# Targeted check (codim checker): g6 over F_7 and F_11, subalgebras h of codimension <= 3, k = 3.
# Claim (appendix-codimension.tex line 133): every such h gives at k = 3, p > 5 a terminal of class 5.
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from liealg import *
from check_examples_defs import g6

rng = random.Random(7)
out = []
for p in [7, 11]:
    L = g6(p)
    found = 0; ok = True; ad_max = 0; codims = set()
    tries = 0
    while found < 40 and tries < 4000:
        tries += 1
        gens = [rand_vec_in(L.basis(), p, rng) for _ in range(rng.choice([1, 2, 3]))]
        h = subalgebra_generated(L, gens)
        if 6 - len(h) > 3:
            continue
        found += 1; codims.add(6 - len(h))
        xs, ext = ideal_construction(L, rng)
        b = len(span(xs, p))
        # level 0: k=3>0, nonabelian, b=3<=3 -> terminal is g6 itself
        term = (b <= 3)
        g = lcs(L)
        ad = [len(g[d - 1]) - len(intersect(h, g[d - 1], 6, p)) for d in range(2, 6)]
        ad_max = max(ad_max, max(ad))
        if not (term and nil_class(L) == 5 and max(ad) <= 6 - len(h) <= 3):
            ok = False
    out.append(f"p={p}: subalgebras tested={found} codims={sorted(codims)} terminal at level 0 with (dim,class)=(6,{nil_class(L)}) for all: {ok}; max a_d={ad_max}")
print("\n".join(out))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_g6_terminal.out"), "w") as fh:
    fh.write("\n".join(out) + "\n")
