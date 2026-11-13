#!/opt/anaconda3/bin/python
"""Common code for l-level contractions (2026-11-13-rees-k9-below-21).  Interpreter: /opt/anaconda3/bin/python.

Shares no code with sat3.py, rc.py, rcdfs.c, exponents_hcd.py or chain_exec.py.

An l-level K-contraction at (p, kappa) is a table B: Z_kappa^l -> F_p such that
  (S) B lies in the span of functions that do not depend on one of the l coordinates; equivalently the
      l-fold mixed difference  sum_{S subset [l]} (-1)^{|S|} B(x with x_r := 0 for r in S)  vanishes for every x;
  (C) every nonzero B(x) has class cl(B(x)) in K - |x|   (|x| = sum of coordinates mod kappa);
  (N) B(0) != 0.
Classes: g = least primitive root mod p, cl(y) = dlog_g(y) mod kappa (computed here by exponentiation only).
"""
import itertools, random


def primitive_root(p):
    n, fs, d = p - 1, set(), 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d); n //= d
        d += 1
    if n > 1: fs.add(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            return g
    raise ValueError(p)


def cls(y, p, g, k):
    """class of y != 0 mod k by the power-character test y^((p-1)/k) = zeta^c, zeta = g^((p-1)/k)."""
    z, t, yy = pow(g, (p - 1) // k, p), 1, pow(y, (p - 1) // k, p)
    for c in range(k):
        if t == yy:
            return c
        t = t * z % p
    raise ValueError


def mixed_difference_zero(B, k, l, p):
    for x in itertools.product(range(k), repeat=l):
        s = 0
        for S in range(1 << l):
            y = tuple(0 if (S >> r) & 1 else x[r] for r in range(l))
            s += (-1) ** bin(S).count('1') * B[y]
        if s % p:
            return False, x
    return True, None


def annihilation_sample(B, k, l, p, g, n=200, seed=1):
    """C(x) = g^{sum x} B(x) paired with random product tensors w1 x .. x wl, wr in W = {w : sum z_m w_m = 0}."""
    rnd = random.Random(seed)
    z = [pow(g, m, p) for m in range(k)]
    zi0 = pow(z[0], p - 2, p)
    bad = 0
    for _ in range(n):
        ws = []
        for r in range(l):
            w = [rnd.randrange(p) for _ in range(k)]
            w[0] = (-sum(z[m] * w[m] for m in range(1, k)) * zi0) % p
            ws.append(w)
        s = 0
        for x, b in B.items():
            if b:
                t = b * pow(g, sum(x), p)
                for r in range(l):
                    t = t * ws[r][x[r]] % p
                s += t
        bad += s % p != 0
    return bad


def verify(B, p, k, K, l, sample=100):
    g = primitive_root(p)
    K = {m % k for m in K}
    okS, where = mixed_difference_zero(B, k, l, p)
    viol = [x for x, b in B.items() if b % p and (cls(b % p, p, g, k) + sum(x)) % k not in K]
    okN = B[(0,) * l] % p != 0
    ann = annihilation_sample(B, k, l, p, g, n=sample) if sample else 0
    nz = sum(1 for b in B.values() if b % p)
    ok = okS and not viol and okN and ann == 0
    return ok, dict(span=okS, span_fail_at=where, class_violations=len(viol), B0=B[(0,) * l] % p,
                    annihilation_failures=ann, nonzero=nz, cells=k ** l)
