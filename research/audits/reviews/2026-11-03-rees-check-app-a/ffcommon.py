"""Shared finite-field helpers for the Appendix A check (exact integer arithmetic)."""
from sympy import primitive_root, isprime, primerange


def coset_table(p, k, xi=None):
    """ind[x] in Z_k for x in F_p^x (ind[0] = None), labelled by coset generator xi.
    Default xi = a primitive root.  Labels Q_m = xi^m Q_0, m = 0..k-1."""
    h = (p - 1) // k
    if xi is None:
        xi = primitive_root(p)
    zeta = pow(xi, h, p)
    pw = {}
    z = 1
    for m in range(k):
        pw[z] = m
        z = z * zeta % p
    assert len(pw) == k, "xi is not a coset generator"
    ind = [None] * p
    for x in range(1, p):
        ind[x] = pw[pow(x, h, p)]
    return ind, xi


def masks(p, k, ind, with_zero):
    """bitmask of Q_m (or Q_m u {0}) for each m."""
    ms = [0] * k
    for x in range(1, p):
        ms[ind[x]] |= 1 << x
    if with_zero:
        ms = [m | 1 for m in ms]
    return ms


def rot(S, b, p, full):
    """{x : x + b in S} as a bitmask."""
    b %= p
    if b == 0:
        return S
    return ((S >> b) | (S << (p - b))) & full
