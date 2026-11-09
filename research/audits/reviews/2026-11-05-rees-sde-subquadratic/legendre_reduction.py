"""Theorem 2: power-residue PRF key recovery from an SDE solver at arity a + n (n = 2 main case).

Oracle: O_K(c) = chi(K + c) in Z_kappa (None if K + c = 0), chi = kappa-th power class.
Reduction (n >= 2):
  1. draw c_1..c_k i.i.d. uniform in F_p, query eps_i = O_K(c_i); if some eps_i is None return -c_i.
  2. u_i := uniform element of class -eps_i;  kernel basis  b_j = (u_i c_i^j)_i,  j = 0..n-1.
  3. Lambda := random (k-n) x k matrix with kernel exactly span(b_0..b_{n-1})   (a = k - n, M = k).
  4. give Lambda to the solver; write its x as x_i = u_i f(c_i) with deg f < n; output -root of f.
The planted solution is f(z) = z + K.  Here the "solver" is exhaustive enumeration of the
projective kernel (all p^{n-1} + ... + 1 points), so we can count EVERY solution and check that each
one reveals K (event G).  For tiny p, the kernel enumeration is cross-checked against exhaustive
search over Sq^M.

Usage:  python legendre_reduction.py sweep      -> failure rates vs. the Theorem 2 bound
        python legendre_reduction.py crosscheck -> exhaustive Sq^M check on tiny p
        python legendre_reduction.py countlemma -> exact count lemma for chi((t+c)/(K+c))
"""
import itertools
import math
import random
import sys

import numpy as np

from common import F, annihilator_matrix, kernel, rank, brute_force_solutions, check_witness


def class_table(Fd):
    p = Fd.p
    tab = np.full(p, -1, dtype=np.int64)
    for y in range(1, p):
        tab[y] = Fd.cls(y)
    return tab


def build_instance(Fd, K, k, n, rng, consecutive=False):
    """Returns (cols, u, c) or ('key', K') if a query hit zero."""
    p = Fd.p
    while True:
        c = list(range(k)) if consecutive else [rng.randrange(p) for _ in range(k)]
        if len(set(c)) >= n:
            break
    eps = []
    for ci in c:
        e = Fd.chi(K + ci)
        if e is None:
            return ('key', (-ci) % p)
        eps.append(e)
    u = [(Fd.rep(-e) * rng.choice(Fd.P)) % p for e in eps]
    basis = [[(u[i] * pow(c[i], j, p)) % p for i in range(k)] for j in range(n)]
    cols = annihilator_matrix(basis, k, p, rng)
    return cols, u, c


def all_solutions_projective(Fd, cols, tab):
    """All solution rays: projective points y of ker(cols) that are monochromatic (then a
    scalar multiple lies in Sq^M).  Returns list of representative x in Sq^M."""
    p, k = Fd.p, Fd.k
    B = kernel(cols, p)
    n = len(B)
    B = np.array(B, dtype=np.int64)
    sols = []
    # projective points: coefficient vectors with first nonzero entry 1
    for lead in range(n):
        free = n - 1 - lead
        for tail in itertools.product(range(p), repeat=max(free - 1, 0)):
            if free == 0:
                Y = B[lead][None, :] % p
            else:
                s = np.arange(p, dtype=np.int64)[:, None]
                base = B[lead].copy()
                for j, tv in enumerate(tail):
                    base = base + tv * B[lead + 2 + j]
                Y = (base[None, :] + s * B[lead + 1][None, :]) % p
            C = tab[Y]
            Cm = np.where(C < 0, 10 ** 6, C)
            mn = Cm.min(axis=1)
            Cx = np.where(C < 0, -10 ** 6, C)
            mx = Cx.max(axis=1)
            nz = (C >= 0).any(axis=1)
            mono = nz & (mn == mx)
            for r in np.nonzero(mono)[0]:
                y = Y[r]
                cl = int(mn[r])
                scale = Fd.rep(-cl)
                x = [(int(v) * scale) % p for v in y]
                sols.append(x)
    return sols


def recover_f(Fd, x, u, c, n):
    """Interpolate f (deg < n) from x_i = u_i f(c_i); returns coefficient list or None."""
    p = Fd.p
    k = len(x)
    rows = []
    for i in range(k):
        iu = pow(u[i], p - 2, p)
        rows.append([pow(c[i], j, p) for j in range(n)] + [(x[i] * iu) % p])
    # solve rows * f = rhs (overdetermined, consistent)
    from common import rref
    R, piv = rref(rows, p)
    if n in piv:
        return None
    f = [0] * n
    for r, pc in zip(R, piv):
        f[pc] = r[n]
    return f


def reveals_key(Fd, f, K, n):
    """For n <= kappa + 1 the K-revealing solutions are exactly f = y (z + K)."""
    p = Fd.p
    if n == 2:
        a0, a1 = f
        return a1 % p != 0 and (a0 * pow(a1, p - 2, p)) % p == K % p
    # general: f(-K) == 0 and f / (z + K) is y * g^kappa; for n <= kappa + 1 that means deg f = 1
    deg = max(j for j in range(n) if f[j] % p)
    if deg != 1:
        return False
    return (f[0] * pow(f[1], p - 2, p)) % p == K % p


def bound(kappa, p, k):
    return kappa ** (1 - k) + kappa * p * kappa ** (-k) * math.exp(kappa * k / (p - 1)) + (p - 1) ** (1 - k)


def sweep():
    rng = random.Random(20261105)
    plan = [(2, 101, 2, range(4, 15, 2), 300), (2, 1009, 2, range(6, 21, 2), 200),
            (2, 10007, 2, [10, 14, 16, 18, 20, 22], 60), (3, 1009, 2, range(4, 13, 2), 200),
            (4, 1009, 2, range(3, 11, 1), 200), (5, 1021, 2, range(3, 9), 200),
            (2, 1009, 3, [12, 16, 20, 24, 26], 30), (3, 1009, 3, [10, 12, 14, 16], 30)]
    for kappa, p, n, ks, trials in plan:
        Fd = F(p, kappa)
        tab = class_table(Fd)
        for k in ks:
            if k <= n:
                continue
            fail = direct = nsol_tot = 0
            for _ in range(trials):
                K = rng.randrange(p)
                inst = build_instance(Fd, K, k, n, rng)
                if inst[0] == 'key':
                    direct += 1
                    assert inst[1] == K
                    continue
                cols, u, c = inst
                sols = all_solutions_projective(Fd, cols, tab)
                nsol_tot += len(sols)
                assert sols, "planted solution missing"
                for x in sols:
                    assert check_witness(Fd, cols, x)
                ok = all(reveals_key(Fd, recover_f(Fd, x, u, c, n), K, n) for x in sols)
                fail += not ok
            b = bound(kappa, p, k) if n == 2 else float('nan')
            print(f"kappa={kappa} p={p} n={n} M=k={k} a={k-n}: G fails {fail}/{trials} "
                  f"(rate {fail/trials:.3f}; Thm 2 bound {b:.3g}); direct key hits {direct}; "
                  f"mean #solution rays {nsol_tot/max(trials-direct,1):.2f}", flush=True)


def crosscheck():
    rng = random.Random(3)
    for kappa, p, n, k, trials in [(2, 13, 2, 5, 15), (2, 17, 2, 6, 8), (3, 13, 2, 6, 10),
                                   (4, 13, 2, 6, 10), (2, 11, 3, 6, 6), (2, 13, 2, 6, 5)]:
        Fd = F(p, kappa)
        tab = class_table(Fd)
        agree = 0
        for t in range(trials):
            K = rng.randrange(p)
            inst = build_instance(Fd, K, k, n, rng, consecutive=(t % 2 == 1))
            if inst[0] == 'key':
                agree += 1
                continue
            cols, u, c = inst
            rays = all_solutions_projective(Fd, cols, tab)
            bf = brute_force_solutions(Fd, cols)
            # compare as sets of projective rays: x ~ y if x = s y
            def ray(x):
                nz = next(v for v in x if v)
                iv = pow(nz, p - 2, p)
                return tuple((v * iv) % p for v in x)
            if {ray(x) for x in rays} == {ray(x) for x in bf}:
                agree += 1
            # planted solution present
            xK = [(u[i] * (K + c[i])) % p for i in range(k)]
            assert check_witness(Fd, cols, xK)
        print(f"kappa={kappa} p={p} n={n} M={k}: projective enumeration == exhaustive Sq^M search in {agree}/{trials}")


def countlemma():
    bad = 0
    for kappa, p in [(2, 11), (2, 13), (3, 13), (4, 13), (3, 31), (5, 31), (2, 101), (6, 37)]:
        Fd = F(p, kappa)
        for K in range(p):
            for t in range(p):
                if t == K:
                    continue
                cnt = [0] * kappa
                for c in range(p):
                    if c in ((-K) % p, (-t) % p):
                        continue
                    th = (Fd.cls(t + c) - Fd.cls(K + c)) % kappa
                    cnt[th] += 1
                exp = [(p - 1 - kappa * (th == 0)) // kappa for th in range(kappa)]
                if cnt != exp:
                    bad += 1
        print(f"kappa={kappa} p={p}: count lemma checked for all K != t; mismatches so far {bad}")


if __name__ == '__main__':
    {'sweep': sweep, 'crosscheck': crosscheck, 'countlemma': countlemma}[sys.argv[1]]()
