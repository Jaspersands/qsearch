"""Headline-20 referee: independent check of the five l-level {0}-contraction tables against
fragment-v2 def:ell-contraction.  (iii) is checked by contracting C on every axis with a basis
of W = {x : sum_m z_m x_m = 0} pivoted at the LAST index, u_m = e_m - (z_m/z_{k-1}) e_{k-1}
(m < k-1); the author's checks pivot at 0.  Second, independent test: <C, w_1 (x) ... (x) w_l> = 0
for 300 random w_r in W (rank-one tensors span W^{(x)l}).  (i),(ii): x in P iff x^{(p-1)/k} = 1."""
import json, random, itertools, sys
from verify_tl6 import lpr
SRC = "../2026-11-13-rees-k9-below-21/"
TABLES = [("B4_19.json", 19, 9, 4), ("B4_37.json", 37, 9, 4), ("B4_73.json", 73, 9, 4),
          ("B3_13_4.json", 13, 4, 3), ("B3_13_6.json", 13, 6, 3)]
def load(fn, k, l, p=None, xi=None, raw=False):
    """The artifact stores B(y) = C_y / z^y (normal form of k9-below-21.md Sec. 2, NOT stated in
    fragment-v2); C_y = z^y B(y) with z^y = prod_r xi^{y_r}.  raw=True returns B itself."""
    d = json.load(open(SRC + fn))
    C = {}
    for key, v in d.items():
        y = tuple(int(ch) for ch in key); assert len(y) == l and all(0 <= t < k for t in y), key
        C[y] = v if raw else v * pow(xi, sum(y), p) % p
    assert len(C) == k ** l
    return C
def contract_axis(T, p, k, l, axis, vecs):
    """T: dict y->val over shape with axis of length k; returns dict with that axis replaced by
    index into vecs (list of length-k vectors)."""
    out = {}
    for y, v in T.items():
        if v == 0: continue
        for n, u in enumerate(vecs):
            c = u[y[axis]]
            if c:
                yy = y[:axis] + (n,) + y[axis + 1:]
                out[yy] = (out.get(yy, 0) + v * c) % p
    return out
def check(C, p, k, l, xi):
    z = [pow(xi, m, p) for m in range(k)]
    inv_last = pow(z[k - 1], p - 2, p)
    basis = []
    for m in range(k - 1):
        u = [0] * k; u[m] = 1; u[k - 1] = (-z[m] * inv_last) % p
        assert sum(z[t] * u[t] for t in range(k)) % p == 0
        basis.append(u)
    T = dict(C)
    for ax in range(l): T = contract_axis(T, p, k, l, ax, basis)
    ann_bad = sum(1 for v in T.values() if v % p)
    e = (p - 1) // k
    cls_bad = sum(1 for v in C.values() if v % p and pow(v, e, p) != 1)
    c0 = C[(0,) * l] % p
    ok0 = c0 != 0 and pow(c0, e, p) == 1
    # random rank-one test
    rnd = random.Random(p * 100 + k)
    rbad = 0
    for _ in range(300):
        ws = []
        for _r in range(l):
            w = [rnd.randrange(p) for _ in range(k)]
            # fix w_0 so that sum z_m w_m = 0
            w[0] = (-sum(z[m] * w[m] for m in range(1, k))) % p
            ws.append(w)
        s = 0
        for y, v in C.items():
            if v:
                t = v
                for r in range(l): t = t * ws[r][y[r]] % p
                s += t
        rbad += (s % p) != 0
    nz = sum(1 for v in C.values() if v % p)
    return ann_bad, cls_bad, ok0, rbad, nz
allok = True
for fn, p, k, l in TABLES:
    xi = lpr(p); C = load(fn, k, l, p, xi)
    a, c, o, r, nz = check(C, p, k, l, xi)
    ok = a == 0 and c == 0 and o and r == 0
    allok &= ok
    print(f"{fn}: p={p} k={k} l={l} xi={xi} nonzero={nz}/{k**l} (iii)-violations={a} random-rank1-fail={r}/300 non-P entries={c} C0 in P={o} -> {'VERIFIED' if ok else 'FAILED'}")
print("ALL VERIFIED" if allok else "SOME FAILED")
print("negative controls:")
for fn, p, k, l in TABLES:
    C = load(fn, k, l, p, lpr(p)); rnd = random.Random(1)
    nzk = [y for y, v in C.items() if v % p and y != (0,) * l]
    y = rnd.choice(nzk); C2 = dict(C)
    e = (p - 1) // k; P = [x for x in range(1, p) if pow(x, e, p) == 1]
    C2[y] = rnd.choice([x for x in P if x != C[y] % p])   # stays in P: only (iii) can catch it
    a, c, o, r, nz = check(C2, p, k, l, lpr(p))
    print(f"  {fn} one entry changed within P: (iii)-viol={a} rank1-fail={r}/300 -> {'FAILED (good)' if a or r else 'PASSED (BAD)'}")
    # wrong generator: any other generator xi' of F_p^x
    xi = lpr(p); others = [g for g in range(2, p) if g != xi and all(pow(g, (p - 1) // qq, p) != 1 for qq in {2, 3, 5, 7, 11, 13, 17, 19} if (p - 1) % qq == 0)]
    res = []
    for g in others:
        Cg = load(fn, k, l, p, g)       # table re-read with the other generator throughout
        a, c, o, r, nz = check(Cg, p, k, l, g)
        res.append((g, a == 0 and r == 0 and c == 0))
    passing = [g for g, ok in res if ok]
    # predicted invariance: C is a table for xi' = xi*pi (pi in P) iff C_y*pi^{-sum y} is one for xi.
    print(f"  {fn} other primitive roots passing (iii): {passing} of {len(others)}")

print("raw-B read (C := stored values) must FAIL:")
for fn, p, k, l in TABLES:
    a, c, o, r, nz = check(load(fn, k, l, raw=True), p, k, l, lpr(p))
    print(f"  {fn}: (iii)-viol={a} non-P={c} -> {'FAILED (good)' if a or c else 'PASSED'}")
