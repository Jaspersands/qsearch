# Theorem 1 tests: (a) enumerate all normalized contractions at small (k,p): zero-cell structure;
# (b) for each shift c != 0, brute-force (P_c) solvability vs transversal-clique existence;
# (c) Lemma 0 distinctness; (d) Lemma 5 restriction of witnesses for k=6.
import sys, itertools
from sympy import primerange
from common import setup
from c2_e2 import search, check

def zero_struct(p, k, ind, a, b):
    Z = [(i, j) for i in range(k) for j in range(k) if (a[j] + b[i]) % p == 0]
    rows = [i for i, _ in Z]; cols = [j for _, j in Z]
    assert len(set(rows)) == len(rows) and len(set(cols)) == len(cols), "row/col with 2 zeros"
    assert (0, 0) not in Z
    assert len(set(a)) == k and len(set(b)) == k, "Lemma 0 fails"
    if len(Z) == k:
        assert ind[p-1] == 0, "eps != 0 with k zeros"
        cs = {(i - j) % k for i, j in Z}
        assert len(cs) == 1 and 0 not in cs, ("pattern", Z)
        c = cs.pop()
        assert all((a[j] + b[(j + c) % k]) % p == 0 for j in range(k))
        return len(Z), c
    return len(Z), None

def clique_exists(p, k, ind):
    Q = [[x for x in range(1, p) if ind[x] == m] for m in range(k)]
    def rec(m, ys):
        if m == k: return True
        for y in Q[m]:
            if all(ind[(y - z) % p] == 0 and ind[(z - y) % p] == 0 for z in ys if (y - z) % p):
                if rec(m + 1, ys + [y]): return True
        return False
    # Q0-scaling: may fix y_1 to one representative
    return rec(2, [Q[1][0]]) if k > 2 else True

def Pc_exists(p, k, ind, c):
    # beta_c = 0; beta_i - beta_l in Q_{c-(i+l)} for all ordered i != l
    order = [c] + [i for i in range(k) if i != c]
    beta = {c: 0}
    def ok(i, x):
        for l, y in beta.items():
            d = (x - y) % p
            if d == 0 or ind[d] != (c - i - l) % k: return False
            d2 = (y - x) % p
            if ind[d2] != (c - i - l) % k: return False
        return True
    def rec(t):
        if t == k: return True
        i = order[t]
        for x in range(1, p):
            if ok(i, x):
                beta[i] = x
                if rec(t + 1): return True
                del beta[i]
        return False
    return rec(1)

mode = sys.argv[1]
if mode == "enum":
    for k, plist in [(3, [7, 13, 19, 31, 37, 43, 61, 67, 73]), (4, [41, 61, 73, 89, 97, 101, 109, 113]), (5, [191, 211, 241, 251, 271])]:
        for p in plist:
            ind, g = setup(p, k)
            sols = search(p, k, ind, all_=True)
            hist = {}; shifts = set()
            for a, b in sols:
                assert check(p, k, ind, a, b)
                n, c = zero_struct(p, k, ind, a, b)
                hist[n] = hist.get(n, 0) + 1
                if c is not None: shifts.add(c)
            kz = hist.get(k, 0) > 0
            cl = (ind[p-1] == 0) and clique_exists(p, k, ind)
            print(f"k={k} p={p} eps={ind[p-1]} #sols={len(sols)} zero-hist={dict(sorted(hist.items()))} shifts={sorted(shifts)} kzero={kz} clique={cl}" + ("" if kz == cl else "  MISMATCH"))
elif mode == "pc":
    for k, P in [(4, 400), (5, 400), (6, 400)]:
        for p in primerange(3, P):
            if (p - 1) % k: continue
            ind, g = setup(p, k)
            if ind[p-1] != 0:
                assert not any(Pc_exists(p, k, ind, c) for c in range(1, k)); continue
            cl = clique_exists(p, k, ind)
            pcs = [Pc_exists(p, k, ind, c) for c in range(1, k)]
            flag = "" if all(x == cl for x in pcs) else "  MISMATCH"
            print(f"k={k} p={p} clique={cl} Pc={pcs}{flag}")
elif mode == "lemma5":
    k = 6
    for p in [229, 233, 241, 251, 257, 263, 269, 277, 281, 283, 293, 307, 311, 313, 317]:
        if (p - 1) % k: continue
        ind, g = setup(p, k)
        s = search(p, k, ind)
        if not s: print(f"p={p} in E2(6)"); continue
        a, b = s[0]
        for D in (2, 3):
            m = k // D
            indD, _ = setup(p, D, pow(g, m, p))
            a2 = tuple(a[m*j] for j in range(D)); b2 = tuple(b[m*i] for i in range(D))
            print(f"p={p} D={D} restricted witness is a D-contraction: {check(p, D, indD, a2, b2)}")
