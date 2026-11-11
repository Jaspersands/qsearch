"""Unipotent symmetries of the extension-field Legendre function.

For q = p^r, the quadratic character of F_q is eta = chi_p o N, N the norm
F_q -> F_p. So x -> eta(x + k) on F_q = F_p^r is the multivariate Legendre
function chi_p(Q(x)) with Q(x) = N(x + k), a degree-r form over F_p.
This script lists the unipotent F_p-linear maps U (U - I nilpotent) of
F_p^r that preserve the function y -> N(y) on F_p-points, and, for each,
the nilpotency index of U - I. It also checks, for random k, that a
unipotent affine map x -> U x + b preserving x -> N(x + k) has
b = U k - k (so the hidden subgroup is a translate-conjugate of the
linear one). Finite check only: it can falsify, not prove (TRAPS 7).
Run: /opt/anaconda3/bin/python -I extfield_legendre_unipotent_check.py
"""
import itertools, random
import numpy as np

def irreducible(p, r):
    # monic irreducible of degree r over F_p (r <= 3 enough here; brute force)
    for tail in itertools.product(range(p), repeat=r):
        f = list(tail) + [1]  # coefficients low..high
        if f[0] == 0:
            continue
        # no roots and (for r<=3) irreducible iff no roots
        if r <= 3 and all(sum(c * pow(a, i, p) for i, c in enumerate(f)) % p for a in range(p)):
            return f
    raise ValueError

def mulmod(a, b, f, p):
    r = len(f) - 1
    prod = [0] * (2 * r - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                prod[i + j] = (prod[i + j] + x * y) % p
    for d in range(len(prod) - 1, r - 1, -1):
        c = prod[d]
        if c:
            for i in range(r + 1):
                prod[d - r + i] = (prod[d - r + i] - c * f[i]) % p
    return prod[:r]

def powmod(a, e, f, p):
    r = len(f) - 1
    res = [1] + [0] * (r - 1)
    base = a[:]
    while e:
        if e & 1:
            res = mulmod(res, base, f, p)
        base = mulmod(base, base, f, p)
        e >>= 1
    return res

def run(p, r, trials_k=3):
    f = irreducible(p, r)
    pts = list(itertools.product(range(p), repeat=r))
    idx = {v: i for i, v in enumerate(pts)}
    e = sum(p ** i for i in range(r))
    Ntab = np.array([powmod(list(v), e, f, p)[0] for v in pts], dtype=np.int64)
    P = np.array(pts, dtype=np.int64).T  # r x p^r
    found = []
    for entries in itertools.product(range(p), repeat=r * r):
        M = np.array(entries, dtype=np.int64).reshape(r, r)
        Mk = np.eye(r, dtype=np.int64)
        nil = None
        for k in range(1, r + 1):
            Mk = (Mk @ M) % p
            if not Mk.any():
                nil = k
                break
        if nil is None or not M.any():
            continue
        U = (np.eye(r, dtype=np.int64) + M) % p
        img = (U @ P) % p
        ids = [idx[tuple(c)] for c in img.T]
        if np.array_equal(Ntab[ids], Ntab):
            found.append((U, nil))
    print(f"p={p} r={r}: nontrivial unipotent U preserving N on F_p-points: {len(found)}")
    for U, nil in found:
        print("   U =", U.tolist(), " index of nilpotency of U-I:", nil)
    # affine check with random k
    rng = random.Random(p * 100 + r)
    for _ in range(trials_k):
        k = tuple(rng.randrange(p) for _ in range(r))
        Qtab = np.array([Ntab[idx[tuple((np.array(v) + k) % p)]] for v in pts])
        lin = [np.eye(r, dtype=np.int64)] + [U for U, _ in found]
        sols = []
        for U in lin:
            for b in itertools.product(range(p), repeat=r):
                img = ((U @ P) + np.array(b).reshape(r, 1)) % p
                ids = [idx[tuple(c)] for c in img.T]
                if np.array_equal(Qtab[ids], Qtab):
                    sols.append((U, b))
        ok = all(tuple(((U @ np.array(k)) - np.array(k)) % p) == tuple(b) for U, b in sols)
        print(f"   k={k}: affine unipotent stabilizer size {len(sols)}; all b = Uk - k: {ok}")

if __name__ == "__main__":
    run(3, 2)
    run(3, 3)
    run(5, 2)
    run(5, 3)
    run(7, 2)
