"""Exact check that the 3p-2 cases of cases_gen.py cover every pair of nonzero unit functionals up to
the label symmetries (a,b) -> (lambda a, mu b + nu a) and the swap of the two unit directions."""
import sys, itertools
p = int(sys.argv[1])
A, B = (1, 0), (0, 1)
cases = {(A, B)} | {(A, (g, 0)) for g in range(1, p)} | {(B, (0, g)) for g in range(1, p)} | {(B, (1, g)) for g in range(1, p)}
def act(f, lam, mu, nu):
    return ((f[0] * lam + f[1] * nu) % p, (f[1] * mu) % p)
G = [(lam, mu, nu) for lam in range(1, p) for mu in range(1, p) for nu in range(p)]
# orbit of each case under G and swap
covered = set()
for (w1, w2) in cases:
    for (lam, mu, nu) in G:
        a, b = act(w1, lam, mu, nu), act(w2, lam, mu, nu)
        covered.add((a, b)); covered.add((b, a))
allpairs = {(w1, w2) for w1 in itertools.product(range(p), repeat=2) for w2 in itertools.product(range(p), repeat=2) if any(w1) and any(w2)}
print(f'p={p}: {len(cases)} cases cover {len(covered & allpairs)} of {len(allpairs)} pairs of nonzero functionals; missing {len(allpairs - covered)}')
