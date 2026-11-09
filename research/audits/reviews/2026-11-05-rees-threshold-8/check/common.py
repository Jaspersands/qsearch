# Referee scratch code (independent of the report's scripts).
from sympy import isprime, primitive_root
import math

def setup(p, k, gen=None):
    """ind[x] = log_xi(x) mod k for x in 1..p-1, with xi = gen (a coset generator) or a primitive root."""
    g = primitive_root(p)
    lg = [None]*p
    x = 1
    for e in range(p-1):
        lg[x] = e
        x = x*g % p
    if gen is None:
        gen = g
    # xi = g^u * q ; index of x w.r.t. xi: ind_xi(x) = u^{-1} * (log_g x) mod k (cosets labelled Q_m = xi^m Q_0)
    u = lg[gen] % k
    assert math.gcd(u, k) == 1, "not a coset generator"
    uinv = pow(u, -1, k)
    ind = [None] + [(lg[x] * uinv) % k for x in range(1, p)]
    return ind, gen

def eps_of(p, k, ind):
    return ind[p-1]
