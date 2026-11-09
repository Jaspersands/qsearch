"""(M') extended: CoherentSDEKappa._less_into on ALL 2^(2b) pairs for b = 9..12 with an own
bit-sliced simulator. Referee script, AI-written, pending human review."""
import json, sys, time, types
import numpy as np
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from theorems.rees_coherent_sde_kappa import CoherentSDEKappa
from theorems.rees_circuit_arith import Anc, anc_size
from theorems.rees_coherent_sde import Prog

out = []
for b in (9, 10, 11, 12):
    t0 = time.time()
    x, y, f = list(range(b)), list(range(b, 2*b)), 2*b
    anc = Anc(list(range(2*b+1, 2*b+1+anc_size(b))), b)
    nw = 2*b+1+anc_size(b)
    P = Prog()
    CoherentSDEKappa._less_into(types.SimpleNamespace(anc=anc), P, x, y, f)
    N = 1 << (2*b)
    idx = np.arange(N, dtype=np.uint64)
    xv, yv = idx & np.uint64((1 << b)-1), idx >> np.uint64(b)
    S = np.zeros((nw, N), dtype=bool)
    for j in range(b):
        S[x[j]] = (xv >> np.uint64(j)) & np.uint64(1)
        S[y[j]] = (yv >> np.uint64(j)) & np.uint64(1)
    for name, q in P:
        if name == "x":
            S[q[0]] ^= True
        elif name == "cx":
            S[q[1]] ^= S[q[0]]
        elif name == "ccx":
            S[q[2]] ^= S[q[0]] & S[q[1]]
        else:
            raise ValueError(name)
    rd = lambda reg: sum(S[w].astype(np.uint64) << np.uint64(j) for j, w in enumerate(reg))
    r = {"b": b, "pairs": N, "gates": len(P),
         "flag_is_x_lt_y": bool(np.array_equal(S[f], xv < yv)),
         "x_restored": bool(np.array_equal(rd(x), xv)), "y_restored": bool(np.array_equal(rd(y), yv)),
         "ancillas_zero": not S[2*b+1:].any(), "seconds": round(time.time()-t0, 1)}
    r["passed"] = all(v for k, v in r.items() if isinstance(v, bool))
    print(json.dumps(r), flush=True)
    out.append(r)
    del S
json.dump(out, open("comparator_check.json", "w"), indent=1)
