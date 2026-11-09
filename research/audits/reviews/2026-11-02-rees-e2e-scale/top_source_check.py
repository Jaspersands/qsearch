"""Exact check that the level_set lifted source equals rho of exp(sum_k t^k (h cap gamma_k))
for every class-four (G, H) in the catalogue (added after the review; the long runs predate it)."""
import time
from theorems import rees_end_to_end_ext as X, rees_end_to_end_sim as base

for key in ("n5_7", "q5_7", "n5_11"):
    build, hs, mode, lazy = X.catalogue()[key]
    alg = build()
    cover = base.make_cover(alg)
    for name, gens in hs:
        t = time.time()
        inst = X.hidden(name, alg, gens, lazy=lazy)
        b = X.SparseExactBackend(cover)
        st, info = X.prepare_source(cover, inst, b, mode, 1)
        ok = b.equals_coset_state(st, base.expected_stage_indices(cover, inst.log_h, cover.c))
        print(inst.name, "|S| =", info["lifted_order"], info["subgroup_check"], info["coset_check"],
              "equals rho_(H_c):", ok, f"{time.time()-t:.1f}s", flush=True)
