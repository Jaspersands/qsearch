"""Referee C: brute-force existence of a normalised two-level contraction (alpha_0 = 1, beta_0 = 0,
alpha_j + beta_i in g^{-(i+j)} P u {0} for all i, j in Z_kappa) for kappa = 2 (odd p) and
kappa = 3 (p = 1 mod 3), p < PMAX.  Sanity check of the hypothesis p not in E_2(kappa) used by
Theorem C (the paper's E_2(2) = E_2(3) = empty).  Each found contraction is re-checked."""
import sys, itertools
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400


def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def prim(p):
    fac = [q for q in range(2, p) if (p - 1) % q == 0 and isprime(q)]
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fac))


def find(p, kappa):
    g = prim(p)
    h = (p - 1) // kappa
    cos = [None] * p
    for x in range(1, p):
        # cos(x) = nu with x in g^nu P  <=>  x^h = g^{nu h}
        xh = pow(x, h, p)
        cos[x] = next(nu for nu in range(kappa) if pow(g, nu * h, p) == xh)
    def ok(val, i, j):
        return val % p == 0 or cos[val % p] == (-(i + j)) % kappa
    for beta_rest in itertools.product(range(p), repeat=kappa - 1):
        beta = (0,) + beta_rest
        if not all(ok(1 + beta[i], i, 0) for i in range(kappa)):
            continue
        alpha = [1]
        for j in range(1, kappa):
            aj = next((a for a in range(p) if all(ok(a + beta[i], i, j) for i in range(kappa))), None)
            if aj is None:
                break
            alpha.append(aj)
        else:
            assert all(ok(alpha[j] + beta[i], i, j) for i in range(kappa) for j in range(kappa))
            return tuple(alpha), beta
    return None


bad = []
for p in range(3, PMAX):
    if not isprime(p):
        continue
    for kappa in (2, 3):
        if (p - 1) % kappa:
            continue
        if find(p, kappa) is None:
            bad.append((p, kappa))
print(f'p < {PMAX}: primes with no normalised contraction (kappa in {{2,3}}): {bad or "none"}')
