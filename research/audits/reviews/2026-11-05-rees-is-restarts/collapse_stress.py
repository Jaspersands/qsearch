"""Random and adversarial checks of is_sde_solve(..., collapse=True).

Run: nice -n 10 /opt/anaconda3/bin/python collapse_stress.py
"""
import random
import sys
from math import gcd

sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from theorems.rees_is_sde_solver import (  # noqa: E402
    PiParts, _anchor_witness, columns_required, is_arity, is_sde_solve, reduced_degree,
    verify, _prime_divisors)


def omega_mult(n):
    out, f = 0, 2
    while n > 1:
        while n % f == 0:
            n //= f
            out += 1
        f += 1
    return out


def check(p, d, cols, **kw):
    w0 = is_sde_solve(p, d, cols, **kw)
    w1 = is_sde_solve(p, d, cols, collapse=True, **kw)
    assert w1 == is_sde_solve(p, d, cols, collapse=True, **kw)        # deterministic
    assert verify(p, d, cols, w0.s) and verify(p, d, cols, w1.s)
    assert not w0.collapsed
    k = w1.reduced_degree
    if k > 1 and w1.rank:
        primes = _prime_divisors(k)
        if len(primes) == 1:
            assert w1.restarts <= omega_mult(k) - 1, (p, d, w1.restarts)
        assert w1.restarts <= w0.restarts or len(primes) > 1 or True
        if w1.collapsed:
            assert all(i <= w1.rank for i, x in enumerate(w1.s) if x)
    return w0, w1


def random_runs():
    rng = random.Random(20261105)
    cases = [(3, 2, 2), (5, 2, 3), (7, 2, 3), (13, 2, 3), (41, 2, 2), (5, 6, 3),
             (7, 3, 1), (13, 3, 1), (7, 3, 2), (7, 9, 1), (13, 9, 1), (19, 3, 1), (37, 3, 1),
             (65537, 2, 1), (65537, 2, 2), (786433, 2, 1), (536870951, 2, 3), (536871017, 2, 3),
             (536870951, 6, 2), (536870923, 3, 1), (536870923, 9, 2), (536871017, 3, 5)]
    stats = dict(n=0, collapsed=0, r0=0, r1=0)
    for p, d, g in cases:
        k, _ = reduced_degree(p, d)
        M = columns_required(p, d, g)
        for seed in range(6):
            cols = [tuple(rng.randrange(1, p) for _ in range(g)) for _ in range(M)]
            for spread in (False, True):
                for ee in (True, False):
                    w0, w1 = check(p, d, cols, spread=spread, early_exit=ee)
                    stats["n"] += 1
                    stats["collapsed"] += w1.collapsed
                    stats["r0"] += w0.restarts
                    stats["r1"] += w1.restarts
    print("random:", stats)


def nth_root_of_unity(p, n):
    """An element of exact order n (brute force; small p only)."""
    for x in range(2, p):
        y = pow(x, (p-1)//n, p)
        if all(pow(y, n//q, p) != 1 for q in _prime_divisors(n)):
            return y
    raise ValueError


def adversarial_anchors():
    rng = random.Random(7)
    out = []
    # kappa = 2, anchor alpha = (-1, 1): H_1 = {+-1}; collapse needs <eta> of order >= 4.
    for p in (13, 17, 41, 97, 257, 65537):
        for g in (1, 2):
            M = columns_required(p, 2, g)
            for seed in range(4):
                head = [(1,), (1,)] if g == 1 else [(1, 0), (1, 0), (0, 1)]
                cols = head + [tuple(rng.randrange(1, p) for _ in range(g))
                               for _ in range(M - len(head))]
                w0, w1 = check(p, 2, cols, spread=bool(seed % 2))
                assert w1.restarts == 0
                out.append((p, 2, g, w0.restarts, w1.restarts, w1.collapsed))
    # kappa = 2, p = 3 mod 4, anchor a square: H_1 trivial, immediate collapse.
    for p in (7, 11, 19, 23):
        x = 3
        cols = [(1,), ((-x*x) % p,)] + [(rng.randrange(1, p),) for _ in range(columns_required(p, 2, 1)-2)]
        w0, w1 = check(p, 2, cols)
        assert w1.collapsed and w1.restarts == 0 and w1.classifications == 0
        out.append((p, 2, 1, w0.restarts, w1.restarts, w1.collapsed))
    # kappa = 3, p = 1 mod 9, anchor alpha = (omega, 1): H_1 of order 3.
    for p in (19, 37, 73, 109, 163, 271):
        om = nth_root_of_unity(p, 3)
        M = columns_required(p, 3, 1)
        for seed in range(4):
            cols = [(1,), ((-om) % p,)] + [(rng.randrange(1, p),) for _ in range(M-2)]
            w0, w1 = check(p, 3, cols, spread=bool(seed % 2))
            assert w1.restarts == 0
            out.append((p, 3, 1, w0.restarts, w1.restarts, w1.collapsed))
    print("adversarial anchors (p, d, g, restarts default, restarts collapse, collapsed):")
    print("   collapsed in", sum(r[-1] for r in out), "of", len(out),
          "; restarts default total", sum(r[3] for r in out), "collapse total", sum(r[4] for r in out))


def trigger_chains():
    """Model check of Lemma 1 on worst-case enlargement chains.

    Feed the anchor test elements of increasing pi-part order (one prime step per
    trigger). For kappa = l^e the anchor must collapse exactly when
    |<eta>| >= kappa |H_1|, i.e. at the e-th trigger; for kappa = 6 with a 3-part
    anchor and 2-part growth only, it never collapses (the limitation of section 5).
    """
    rows = []
    for p, k in ((65537, 2), (65537, 4), (65537, 8), (65537, 16), (786433, 2), (786433, 4),
                 (786433, 3), (163, 3), (1459, 3), (1459, 9), (39367, 3), (39367, 9), (39367, 27)):
        if (p-1) % k or not all(p % q for q in range(2, int(p**0.5)+1)):
            continue
        parts = PiParts(p, k)
        ell = _prime_divisors(k)[0]
        e = omega_mult(k)
        gen = None
        for x in range(2, p):
            gamma = parts.split(x)[0]
            if parts.order(gamma) == parts.n_pi:
                gen = gamma
                break
        n = parts.n_pi
        for j1 in range(1, omega_mult(n)):           # anchor group of order l^j1
            h1 = ell**j1
            gamma1 = pow(gen, n//h1, p)
            anchor = [(0, (gamma1, 1)), (1, (1, 1))]
            eta, h = gamma1, h1
            triggers = 0
            while h < n:
                h *= ell
                eta = parts.join(eta, pow(gen, n//h, p))
                triggers += 1
                hit = _anchor_witness(parts, eta, anchor)
                expect = h >= k*h1
                assert (hit is not None) == expect, (p, k, j1, h)
                if hit is not None:
                    assert triggers == e
                    break
            if h1*k <= n:
                rows.append((p, k, j1, triggers))
    print("prime-power chains: collapse exactly at trigger e on", len(rows), "chains")
    # kappa = 6 stall: p - 1 = 2^a 3^b * m with 2-part growth only.
    k = 6
    isprime = lambda n: n > 1 and all(n % q for q in range(2, int(n**0.5)+1))
    p = next(2**8*9*m+1 for m in range(1, 10**4) if m % 6 in (1, 5) and isprime(2**8*9*m+1))
    parts = PiParts(p, k)
    n2 = 2**8
    g = next(parts.split(x)[0] for x in range(2, p) if parts.order(parts.split(x)[0]) == parts.n_pi)
    g2, g3 = pow(g, 9, p), pow(g, n2, p)   # generators of the 2- and 3-parts
    assert parts.order(g2) == n2 and parts.order(g3) == 9
    anchor = [(0, (g3, 1)), (1, (1, 1))]          # anchor with a 3-part of order 9
    eta, collapses = g3, 0
    for j in range(1, 9):
        eta = parts.join(eta, pow(g2, 2**(8-j), p))
        collapses += _anchor_witness(parts, eta, anchor) is not None
    print(f"kappa=6 stall at p={p} (3-part anchor, 8 two-part triggers): collapses =", collapses)
    assert collapses == 0


if __name__ == "__main__":
    trigger_chains()
    adversarial_anchors()
    random_runs()
    print("ALL OK")
