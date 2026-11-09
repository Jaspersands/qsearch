"""Independent re-check of the 2026-11-05 subquadratic report (written from scratch, no imports
from the report's folder).  Exact arithmetic mod p throughout.

Usage: python indep_check.py thm1 | prop2 | mono | kernel2 | reduction | bound
"""
import itertools
import random
import sys

import numpy as np


def prim_root(p):
    fac = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, q))]
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g


class Fld:
    def __init__(self, p, k):
        assert (p - 1) % k == 0
        self.p, self.k = p, k
        g = prim_root(p)
        self.cos = [None] * p
        y = 1
        for e in range(p - 1):
            self.cos[y] = e % k
            y = y * g % p
        self.P = [y for y in range(1, p) if self.cos[y] == 0]
        self.Sq = [0] + self.P
        self.g = g

    def coset(self, nu):
        return [y for y in range(1, self.p) if self.cos[y] == nu % self.k]


def nullspace(M, p):
    """M: list of rows (m x n). Returns basis of {x : M x = 0}."""
    M = [list(r) for r in M]
    m, n = len(M), len(M[0])
    piv = []
    r = 0
    for c in range(n):
        pr = next((i for i in range(r, m) if M[i][c] % p), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [v * inv % p for v in M[r]]
        for i in range(m):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        x = [0] * n
        x[f] = 1
        for i, c in enumerate(piv):
            x[c] = (-M[i][f]) % p
        basis.append(x)
    return basis


def realizable(F, cols, q):
    """Boolean array over F_p^q (encoded base p) of R(S) = {sum x_i col_i : x in Sq^S}."""
    p = F.p
    Sq = np.array(F.Sq, dtype=np.int64)
    vals = np.zeros(1, dtype=np.int64)  # encoded vectors
    vecs = np.zeros((1, q), dtype=np.int64)
    for col in cols:
        col = np.array(col, dtype=np.int64)
        new = (vecs[:, None, :] + Sq[None, :, None] * col[None, None, :]) % p
        vecs = new.reshape(-1, q)
        enc = vecs @ (p ** np.arange(q))
        enc, idx = np.unique(enc, return_index=True)
        vecs = vecs[idx]
    R = np.zeros(p ** q, dtype=bool)
    R[vecs @ (p ** np.arange(q))] = True
    return R


def enc(v, p):
    return sum(int(x) * p ** i for i, x in enumerate(v))


def lines_in(F, R, q):
    p = F.p
    out = []
    seen = set()
    for v in itertools.product(range(p), repeat=q):
        if not any(v):
            continue
        lead = next(x for x in v if x)
        inv = pow(lead, p - 2, p)
        nv = tuple(x * inv % p for x in v)
        if nv in seen:
            continue
        seen.add(nv)
        if all(R[enc([c * x % p for x in nv], p)] for c in range(1, p)):
            out.append(nv)
    return out


def contains_plane(F, R, q, lines):
    p = F.p
    L = set(lines)
    for a_, b_ in itertools.combinations(lines, 2):
        ok = True
        for s in range(p):
            w = [(x + s * y) % p for x, y in zip(a_, b_)]
            lead = next(x for x in w if x)
            inv = pow(lead, p - 2, p)
            if tuple(x * inv % p for x in w) not in L:
                ok = False
                break
        if ok:
            return True
    return False


def random_circuit(F, rng, q, pattern=None):
    """q+1 columns in F_p^q, generic, with dependency delta having prescribed coset pattern."""
    p = F.p
    while True:
        base = [[rng.randrange(p) for _ in range(q)] for _ in range(q)]
        # independent?
        if len(nullspace([list(r) for r in zip(*base)], p)) == 0:
            break
    if pattern is None:
        delta = [rng.randrange(1, p) for _ in range(q + 1)]
    else:
        delta = [rng.choice(F.coset(c)) for c in pattern]
    # last column = -(sum delta_i b_i)/delta_q
    inv = pow(delta[q], p - 2, p)
    last = [(-sum(delta[i] * base[i][j] for i in range(q)) * inv) % p for j in range(q)]
    cols = base + [last]
    return cols, delta


def _masks(F):
    p, k = F.p, F.k
    # mask[m][a] = a in Q_{-m} u {0}
    return [np.array([a == 0 or F.cos[a] == (-m) % k for a in range(p)]) for m in range(k)]


def _adm(F, masks, beta, C, nu):
    """boolean array over alpha in F_p: alpha + beta_c in Q_{-(nu+c)} u {0} for all c in C."""
    p = F.p
    ok = np.ones(p, dtype=bool)
    for b, c in zip(beta, C):
        ok &= np.roll(masks[(nu + c) % F.k], -b)  # ok[a] = mask[(a+b) % p]
    return ok


def restricted_contraction_exists(F, C):
    """exists alpha: Z_k -> F_p, beta: C -> F_p nonconstant with alpha_nu + beta_c in Q_{-(nu+c)} u {0}.
    WLOG beta at min(C) is 0 (translate alpha by +t, beta by -t)."""
    p, k = F.p, F.k
    C = sorted(C)
    masks = _masks(F)
    for rest in itertools.product(range(p), repeat=len(C) - 1):
        beta = (0,) + rest
        if len(set(beta)) == 1:
            continue
        if all(_adm(F, masks, beta, C, nu).any() for nu in range(k)):
            return True
    return False


def universal_exists(F):
    """exists alpha, beta in F_p^k with alpha_j + beta_i in Q_{-(i+j)} u {0} and alpha_0 + beta_0 != 0;
    WLOG beta_0 = 0."""
    p, k = F.p, F.k
    masks = _masks(F)
    C = list(range(k))
    for rest in itertools.product(range(p), repeat=k - 1):
        beta = (0,) + rest
        a0 = _adm(F, masks, beta, C, 0)
        a0[0] = False
        if a0.any() and all(_adm(F, masks, beta, C, nu).any() for nu in range(1, k)):
            return True
    return False


def thm1():
    rng = random.Random(101)
    tot = viol = 0
    for p, k, q in [(13, 2, 2), (17, 2, 2), (29, 2, 2), (13, 3, 2), (19, 3, 2), (13, 4, 2), (17, 4, 2),
                    (11, 5, 2), (31, 5, 2), (13, 2, 3), (13, 3, 3), (13, 4, 3), (7, 3, 3), (7, 2, 3)]:
        F = Fld(p, k)
        pats = [None, None, [0] * q + [1], [i % k for i in range(q + 1)], [i % 2 for i in range(q + 1)]]
        for pat in pats:
            cols, delta = random_circuit(F, rng, q, pat)
            mono = len({F.cos[d] for d in delta}) == 1
            R = realizable(F, cols, q)
            L = lines_in(F, R, q)
            pl = contains_plane(F, R, q, L) if len(L) >= 2 else False
            tot += 1
            if not mono and pl:
                viol += 1
            print(f"p={p} k={k} q={q} pattern={[F.cos[d] for d in delta]} mono={mono} lines={len(L)} plane={pl}")
    print(f"THM1 TOTAL {tot} circuits, violations among non-monochromatic: {viol}")


def prop2():
    rng = random.Random(202)
    tot = bad = 0
    for p, k, q in [(13, 2, 2), (13, 3, 2), (7, 3, 2), (13, 4, 2), (17, 4, 2), (37, 4, 2), (29, 4, 2),
                    (41, 4, 2), (11, 5, 2), (31, 5, 2), (13, 4, 3), (17, 4, 3)]:
        F = Fld(p, k)
        for t in range(6):
            pat = [i % k for i in range(q + 1)] if t == 0 and q + 1 >= k else None
            cols, delta = random_circuit(F, rng, q, pat)
            C = {F.cos[d] for d in delta}
            if len(C) < 2:
                continue
            R = realizable(F, cols, q)
            has_line = bool(lines_in(F, R, q))
            rc = restricted_contraction_exists(F, C)
            tot += 1
            bad += has_line != rc
            print(f"p={p} k={k} q={q} C={sorted(C)} line={has_line} restricted_contraction={rc}")
    print(f"PROP2(i) TOTAL {tot}, mismatches {bad}")
    # (iii): C = Z_k restricted contraction <=> universal (p not in E_2)
    E2 = {4: {5, 13, 17, 29, 37, 53}, 5: {11, 31, 41, 61, 71, 101, 131, 151, 181}}
    mism = 0
    for k, ps in [(2, [5, 7, 11, 13]), (3, [7, 13, 19, 31]), (4, [5, 13, 17, 29, 37, 41, 53, 61]),
                  (5, [11])]:
        for p in ps:
            F = Fld(p, k)
            r = restricted_contraction_exists(F, set(range(k))) 
            u = universal_exists(F)
            inE2 = p in E2.get(k, set())
            if r is not None:
                mism += (r != u)
            mism += (u == inE2)
            print(f"(iii) k={k} p={p} restricted(C=Z_k)={r} universal={u} paper_E2={inE2}")
    print(f"PROP2(iii) mismatches {mism}")


def mono():
    """Necessity of 'not all in one coset': a monochromatic circuit whose R is all of F_p^2."""
    for p in [29, 53, 101]:
        F = Fld(p, 2)
        cols = [[1, 0], [0, 1], [p - 1, p - 1]]  # delta = (1,1,1), all in P
        R = realizable(F, cols, 2)
        print(f"mono circuit p={p} kappa=2: |R| = {R.sum()} of {p*p}; full = {R.all()}")


def kernel2():
    rng = random.Random(303)
    for p in [13, 29]:
        F = Fld(p, 2)
        res = []
        for _ in range(4):
            while True:
                cols = [[rng.randrange(p) for _ in range(3)] for _ in range(5)]
                rows = [list(r) for r in zip(*cols)]
                if len(nullspace(rows, p)) == 2:
                    break
            res.append(bool(realizable(F, cols, 3).all()))
        print(f"kernel-2, p={p} kappa=2 q=3, 5 columns: R = F_p^3 in {sum(res)}/4 samples")


def build(F, K, c, rng):
    p = F.p
    eps = [F.cos[(K + ci) % p] for ci in c]
    u = [rng.choice(F.coset(-e)) for e in eps]
    w = [ui * ci % p for ui, ci in zip(u, c)]
    # Lambda: rows spanning the annihilator of span(u, w)
    ann = nullspace([u, w], p)
    return ann, u, w, eps


def all_solutions_bruteforce(F, Lam):
    p = F.p
    k = len(Lam[0])
    sols = []
    for x in itertools.product(F.Sq, repeat=k):
        if any(x) and all(sum(a * b for a, b in zip(r, x)) % p == 0 for r in Lam):
            sols.append(x)
    return sols


def reduction():
    rng = random.Random(404)
    checked = struct_bad = event_mismatch = planted_missing = 0
    for p, k, kk in [(13, 2, 5), (13, 3, 5), (13, 4, 5), (17, 2, 5), (7, 3, 6), (13, 2, 6)]:
        F = Fld(p, k)
        for _ in range(6):
            K = rng.randrange(p)
            while True:
                c = [rng.randrange(p) for _ in range(kk)]
                if len(set(c)) > 1 and (-K) % p not in c:
                    break
            Lam, u, w, eps = build(F, K, c, rng)
            sols = all_solutions_bruteforce(F, Lam)
            planted = tuple(ui * (K + ci) % p for ui, ci in zip(u, c))
            planted_missing += planted not in set(sols)
            reveal_all = True
            for x in sols:
                # write x = alpha u + beta w: solve from two coordinates with distinct c
                i, j = next((i, j) for i in range(kk) for j in range(kk) if c[i] != c[j])
                # x_i/u_i = alpha + beta c_i
                yi, yj = x[i] * pow(u[i], p - 2, p) % p, x[j] * pow(u[j], p - 2, p) % p
                beta = (yi - yj) * pow((c[i] - c[j]) % p, p - 2, p) % p
                alpha = (yi - beta * c[i]) % p
                if any((alpha * u[l] + beta * w[l] - x[l]) % p for l in range(kk)):
                    struct_bad += 1
                if beta == 0 or alpha * pow(beta, p - 2, p) % p != K:
                    reveal_all = False
            # predicted failure event: all eps equal, or exists t != K, theta with E_{t,theta}
            fail = len(set(eps)) == 1
            for t in range(p):
                if t == K:
                    continue
                for th in range(k):
                    if all((t + ci) % p == 0 or (F.cos[(t + ci) % p] - F.cos[(K + ci) % p]) % k == th
                           for ci in c):
                        # E_{t,theta} gives an actual solution unless all c_i = -t (excluded)
                        fail = True
            event_mismatch += fail != (not reveal_all)
            checked += 1
    print(f"REDUCTION: {checked} instances; planted missing {planted_missing}; "
          f"solutions outside span(u,w) {struct_bad}; predicted-vs-actual failure mismatches {event_mismatch}")


def bound():
    """Monte Carlo of the exact failure event vs the stated bound (no solver needed, by reduction())."""
    import math
    rng = np.random.default_rng(505)
    for p, k, kk, trials in [(1009, 2, 14, 40000), (1009, 2, 16, 40000), (1009, 4, 9, 40000),
                             (1009, 3, 12, 40000)]:
        F = Fld(p, k)
        cosarr = np.array([-1] + [F.cos[y] for y in range(1, p)], dtype=np.int64)
        fails = 0
        for _ in range(trials):
            K = int(rng.integers(p))
            c = rng.integers(p, size=kk)
            if np.any((K + c) % p == 0):
                continue  # R outputs K
            if np.all(c == c[0]):
                fails += 1
                continue
            eps = cosarr[(K + c) % p]
            if np.all(eps == eps[0]):
                fails += 1
                continue
            t = np.arange(p)[:, None]
            tc = (t + c[None, :]) % p
            zero = tc == 0
            diff = (cosarr[tc] - eps[None, :]) % k
            diff[zero] = -1
            bad = False
            for th in range(k):
                ok = np.all(zero | (diff == th), axis=1)
                ok[K] = False
                if ok.any():
                    bad = True
                    break
            fails += bad
        stated = k ** (1 - kk) + k * p * k ** (-kk) * math.exp(k * kk / (p - 1)) + (p - 1) ** (1 - kk)
        exact_union = k ** (1 - kk) + (p - 1) * ((k - 1) * (1 / k + 1 / (p - 1)) ** kk + k ** (-kk)) \
            + (p - 1) ** (1 - kk)
        rate = fails / trials
        se = math.sqrt(rate * (1 - rate) / trials)
        print(f"p={p} kappa={k} k={kk}: failure {rate:.4f} (s.e. {se:.4f}) over {trials}; "
              f"refined union {exact_union:.4f}; stated bound {stated:.4f}")


if __name__ == '__main__':
    {'thm1': thm1, 'prop2': prop2, 'mono': mono, 'kernel2': kernel2, 'reduction': reduction,
     'bound': bound}[sys.argv[1]]()
