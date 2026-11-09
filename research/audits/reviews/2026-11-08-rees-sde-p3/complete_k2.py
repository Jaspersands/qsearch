"""0/1-completeness of k-dim subspaces K of F_3^t: do the 2^t zero-one vectors hit all 3^(t-k)
cosets?  (k=2, t=4: the two-dimension-from-two-dependencies partition gadgets; k=2, t=5: would be
three dimensions from two dependencies.)  Also the partition lemma count (3/4)2^t."""
import itertools, numpy as np
from kow_p3 import rank3
def subspaces(t, k):
    seen = set()
    for rows in itertools.combinations([v for v in itertools.product(range(3), repeat=t) if any(v)], k):
        M = np.array(rows)
        if rank3(M) < k: continue
        # canonical form: set of all elements
        elems = frozenset(tuple((np.array(c) @ M) % 3) for c in itertools.product(range(3), repeat=k))
        if elems in seen: continue
        seen.add(elems); yield M, elems
def complete(M, elems, t, k):
    cosets = set()
    for z in itertools.product((0, 1), repeat=t):
        # canonical coset rep: min over elems of z + e
        rep = min(tuple((np.array(z) + np.array(e)) % 3) for e in elems)
        cosets.add(rep)
    return len(cosets) == 3 ** (t - k), len(cosets)
for (t, k) in ((4, 2), (5, 2), (3, 1), (2, 1)):
    n = 0; good = []
    for M, elems in subspaces(t, k):
        n += 1
        ok, c = complete(M, elems, t, k)
        if ok: good.append(M.tolist())
    print(f"t={t}, k={k}: {n} subspaces, {len(good)} are 0/1-complete (all {3**(t-k)} cosets hit by {2**t} zero-one vectors)")
    for g in good[:6]: print("   e.g. pattern matrix rows:", g)
