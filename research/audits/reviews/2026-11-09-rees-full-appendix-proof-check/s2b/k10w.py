"""s2b: witness search (node-limited) at the three primes Remark local-scope places outside E_2(10)."""
import sys, time
sys.path.insert(0, '.')
from rcsearch import Fld, two_level, Limit
out = []
for p in [3361, 3761, 5821]:
    t0 = time.time()
    try:
        w, n = two_level(Fld(p, 10), 10, node_limit=400_000)
        r = "contraction found (witness verified)" if w is not None else "exceptional"
    except Limit:
        r = "UNKNOWN (node limit)"
    s = "kappa=10 p=%d: %s [%.1fs]" % (p, r, time.time() - t0); print(s, flush=True); out.append(s)
open('k10w.out', 'w').write("\n".join(out) + "\n")
