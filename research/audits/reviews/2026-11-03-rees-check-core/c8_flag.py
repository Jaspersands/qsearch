"""C8b: every derivation of the Dixmier-Lister table moves the flag
L > [L,L] > span(e7,e8) > 0 down one step (exact, mod p), so D^3 = 0 for EVERY
derivation by linearity, not only for a basis. Run after check_core.py."""
import json
import numpy as np
from check_core import dixmier_lister, nullspace, in_span

out = {}
for p in (5, 7, 11, 13, 17, 19, 23):
    L = dixmier_lister(p)
    m = 8
    rows = []
    for i in range(m):
        for j in range(m):
            for k in range(m):
                r = [0]*(m*m)
                for l in range(m):
                    if L.T[i, j, l]:
                        r[k*m+l] += int(L.T[i, j, l])
                    if L.T[l, j, k]:
                        r[l*m+i] -= int(L.T[l, j, k])
                    if L.T[i, l, k]:
                        r[l*m+j] -= int(L.T[i, l, k])
                rows.append([v % p for v in r])
    D = [np.array(v, dtype=np.int64).reshape(m, m) for v in nullspace(rows, m*m, p)]
    F1 = L.lcs()[1]                         # [L,L] = span(e5..e8)
    F2 = [tuple(int(i == j) for j in range(m)) for i in (6, 7)]   # span(e7, e8)
    ok = True
    for Dm in D:
        for i in range(m):
            col = tuple(int(x) for x in Dm[:, i] % p)
            ok &= in_span(F1, col, p)
        for v in F1:
            ok &= in_span(F2, tuple(int(x) for x in (Dm @ np.array(v)) % p), p)
        for v in F2:
            ok &= not ((Dm @ np.array(v)) % p).any()
    out[p] = {"derivation_dim": len(D), "flag_shift_all_basis_derivations": bool(ok),
              "gamma3_is_span_e7_e8": sorted(L.lcs()[2]) == sorted(F2)}
print(json.dumps(out, indent=1))
