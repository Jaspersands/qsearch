"""Exact checks for the bounded-excess barrier (report Section 3, Theorem 3.1 and Lemma 3.2).

1. e2   : re-derive E_2(kappa) on a small range by the criterion of Lemma 3.2(a):
          p notin E_2(kappa)  <=>  some nonconstant alpha (alpha_0 = 0) has n_i(alpha) >= 1 for all i,
          n_i(alpha) = #{beta : alpha_nu + beta in Q_{-nu-i} u {0} for all nu}.
2. zs   : the bound |Z_S| <= 1 + (p^r - 1)(kappa-1)/kappa at p in E_2(kappa)
          (r = 1: every alpha; r = 2: random S), and its failure at p notin E_2(kappa).
3. lines: for random Lambda in F_p^{m x (m+h)} compute the realizable set R(Lambda) (weights in
          P u {0}, P = kappa-th powers) exactly and decide whether it contains a line F_p w.
Interpreter: /opt/anaconda3/bin/python.
"""
import sys, random, itertools
import numpy as np

def primroot(p):
    n, fs, d = p-1, [], 2
    while d*d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fs.append(n)
    return next(g for g in range(2, p) if all(pow(g, (p-1)//q, p) != 1 for q in fs))

def cls_table(p, kappa):
    g = primroot(p); c = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p-1):
        c[x] = e % kappa; x = x*g % p
    return g, c

def row_index(p, kappa, cl, alpha):
    """for every beta: the i in Z_kappa it serves (all nonzero cells agree on i = -nu - cls), kappa = 'all', -1 = none"""
    beta = np.arange(p)
    val = np.full(p, kappa, dtype=np.int64)        # kappa means every i (all cells zero so far)
    for nu, a in enumerate(alpha):
        y = (a + beta) % p
        c = cl[y]
        inu = np.where(c >= 0, (-nu - c) % kappa, kappa)
        both = (val == kappa)
        val = np.where(both, inu, np.where((inu == kappa) | (inu == val), val, -1))
    return val

def served(p, kappa, cl, alpha):
    v = row_index(p, kappa, cl, alpha)
    if (v == kappa).any(): return set(range(kappa))
    return set(int(x) for x in np.unique(v[v >= 0]))

def in_E2(p, kappa, cl):
    for rest in itertools.product(range(p), repeat=kappa-1):
        alpha = (0,) + rest
        if len(set(alpha)) == 1: continue
        if len(served(p, kappa, cl, alpha)) == kappa: return False, alpha
    return True, None

def primes_1mod(k, lo, hi):
    out = []
    for n in range(max(lo, 3), hi+1):
        if n % k == 1 and all(n % d for d in range(2, int(n**0.5)+1)): out.append(n)
    return out

def zs_r1(p, kappa, cl):
    """max over nonconstant alpha (alpha_0 = 0) of |Z_alpha|, Z_alpha = {d : exists u, u + alpha_nu d in Q_{-nu} u 0}"""
    best = 0
    for rest in itertools.product(range(p), repeat=kappa-1):
        alpha = (0,) + rest
        if len(set(alpha)) == 1: continue
        s = served(p, kappa, cl, alpha)           # d = t: class of t must be served (u = t*beta)
        # Z = {0} u {t != 0 : cls(t) in s}
        z = 1 + (p-1)//kappa*len(s)
        best = max(best, z)
    return best

def zs_r2(p, kappa, cl, samples, rng):
    """random S in F_p^{kappa x 2}, row 0 zero, rank 2: |Z_S| by brute force over D in F_p^2 and u in F_p"""
    worst = 0
    us = np.arange(p)
    for _ in range(samples):
        while True:
            S = [(0, 0)] + [(rng.randrange(p), rng.randrange(p)) for _ in range(kappa-1)]
            if any((S[a][0]*S[b][1] - S[a][1]*S[b][0]) % p for a in range(kappa) for b in range(kappa)): break
        z = 0
        for d1 in range(p):
            for d2 in range(p):
                ok = np.ones(p, dtype=bool)
                for nu in range(kappa):
                    y = (us + S[nu][0]*d1 + S[nu][1]*d2) % p
                    c = cl[y]
                    ok &= (c < 0) | (c == (-nu) % kappa)
                    if not ok.any(): break
                if ok.any(): z += 1
        worst = max(worst, z)
    return worst

def realizable(p, kappa, cl, Lam):
    """boolean array over F_p^m (base-p encoding) of the values sum_b x_b lambda_b, x in (P u 0)^n"""
    m, n = Lam.shape
    Sq = np.array([0] + [x for x in range(1, p) if cl[x] == 0], dtype=np.int64)
    enc = p**np.arange(m)
    # value vectors of each column for each weight: shape (n, |Sq|, m)
    acc = np.zeros((1, m), dtype=np.int64)
    for b in range(n):
        contrib = (Sq[:, None] * Lam[:, b][None, :]) % p           # |Sq| x m
        acc = ((acc[:, None, :] + contrib[None, :, :]) % p).reshape(-1, m)
        acc = np.unique(acc, axis=0)                                 # values only (set)
    R = np.zeros(p**m, dtype=bool)
    R[(acc*enc).sum(axis=1)] = True
    return R

def has_line(p, kappa, g, R, m):
    allw = np.array(list(itertools.product(range(p), repeat=m)), dtype=np.int64)[:, ::-1]  # matches enc order
    enc = p**np.arange(m)
    good = R[(allw*enc).sum(axis=1)].copy()
    good[0] = False
    t = 1
    for nu in range(1, kappa):
        t = t*g % p
        good &= R[((allw*t % p)*enc).sum(axis=1)]
    return bool(good.any())

if __name__ == "__main__":
    mode = sys.argv[1]
    rng = random.Random(7)
    if mode == "e2":
        for kappa, hi in [(3, 80), (4, 61), (5, 31)]:
            ex = []
            for p in primes_1mod(kappa, 3, hi):
                g, cl = cls_table(p, kappa)
                e, wit = in_E2(p, kappa, cl)
                if e: ex.append(p)
            print("kappa=%d: primes p = 1 mod kappa, p <= %d, in E_2 by Lemma 3.2(a) criterion: %s" % (kappa, hi, ex), flush=True)
    if mode == "zs":
        for kappa, p in [(4, 17), (4, 37), (4, 53), (4, 41), (4, 61), (5, 11)]:
            g, cl = cls_table(p, kappa)
            z1 = zs_r1(p, kappa, cl)
            bound1 = 1 + (p-1)*(kappa-1)//kappa
            line = "kappa=%d p=%d: r=1 max|Z_alpha| = %d, bound 1+(p-1)(kappa-1)/kappa = %d, p = %d" % (kappa, p, z1, bound1, p)
            if kappa == 4 and p <= 41:
                z2 = zs_r2(p, kappa, cl, 30, rng)
                line += "; r=2 (30 random S) max|Z_S| = %d, bound = %d, p^2 = %d" % (z2, 1 + (p*p-1)*(kappa-1)//kappa, p*p)
            print(line, flush=True)
    if mode == "lines":
        configs = [(4, 17, [(2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2), (5, 2), (2, 3), (3, 3), (4, 3)]),
                   (4, 37, [(2, 1), (3, 1), (2, 2), (3, 2), (4, 2), (2, 3)]),
                   (4, 41, [(2, 1), (3, 1), (2, 2), (3, 2), (4, 2), (2, 3)]),
                   (5, 31, [(2, 1), (3, 1), (2, 2), (3, 2)])]
        samples = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        for kappa, p, mh in configs:
            g, cl = cls_table(p, kappa)
            for (m, h) in mh:
                n = m + h
                if ((p-1)//kappa + 1)**n > 3e6 or p**m > 4e6: continue
                cnt = 0
                for _ in range(samples):
                    Lam = np.array([[rng.randrange(p) for _ in range(n)] for _ in range(m)], dtype=np.int64)
                    R = realizable(p, kappa, cl, Lam)
                    cnt += has_line(p, kappa, g, R, m)
                print("kappa=%d p=%d m=%d h=%d (n=%d columns in F_p^%d): %d/%d random objects have a flexible line" % (
                    kappa, p, m, h, n, m, cnt, samples), flush=True)

if __name__ == "__main__" and mode == "circuits":
    # Prop 2(iii) of the subquadratic report / h = 1 case of Theorem 3.1: at p in E_2(kappa), a circuit whose
    # dependency meets every coset has no flexible line; at p notin E_2 it always has one.
    rng2 = random.Random(3)
    for kappa, p, m in [(4, 17, 3), (4, 17, 4), (4, 37, 3), (4, 53, 3), (4, 41, 3), (4, 61, 3), (5, 31, 4)]:
        g, cl = cls_table(p, kappa)
        tested = withline = 0
        while tested < 8:
            Lam = np.array([[rng2.randrange(p) for _ in range(m+1)] for _ in range(m)], dtype=np.int64)
            # dependency delta of the m+1 columns (generic: one-dimensional kernel)
            A = [[int(x) % p for x in row] for row in Lam.tolist()]
            from adaptive_chain import nullvec
            d = nullvec([[A[i][b] for i in range(m)] for b in range(m+1)], p)
            if any(x == 0 for x in d): continue
            if len(set(int(cl[x]) for x in d)) < kappa: continue
            R = realizable(p, kappa, cl, Lam)
            tested += 1; withline += has_line(p, kappa, g, R, m)
        print("kappa=%d p=%d m=%d: %d of %d circuits whose dependency meets all %d cosets have a flexible line" % (
            kappa, p, m, withline, tested, kappa), flush=True)
