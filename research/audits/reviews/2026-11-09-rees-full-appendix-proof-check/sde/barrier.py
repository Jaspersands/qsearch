"""rem:sde-side-barrier: 'exact searches find primes, such as p = 37, 53 for kappa = 4 and
p = 131 for kappa = 5, where any kappa-1 columns can be filled simultaneously but no
contraction with every entry nonzero exists.'
Nonzero version: X_j(beta) = {alpha : alpha + beta_i in Q_{-i-j} for all i} (no zeros).
Normalise beta_0 = 0 (translation) and beta_1 to a coset representative (scaling by Q_0).
For every subset Jset of kappa-1 columns: is there beta with X_j(beta) nonempty for j in Jset?
And for all kappa columns at once.
"""
import itertools, sys
import sympy

def run(p, kappa):
    g = sympy.primitive_root(p)
    cos = [None] * p
    x = 1
    for e in range(p - 1):
        cos[x] = e % kappa; x = x * g % p
    Q = [0] * kappa
    for y in range(1, p):
        Q[cos[y]] |= 1 << y
    mask = (1 << p) - 1
    def shift(bits, b):
        b %= p
        return ((bits >> b) | (bits << (p - b))) & mask
    reps = [pow(g, c, p) for c in range(kappa)]
    K = kappa
    found = {}  # frozenset of filled columns -> example beta
    need = K - 1
    def dfs(i, cols, betas):
        nz = [j for j in range(K) if cols[j]]
        if len(nz) < need:
            return
        if i == K:
            key = frozenset(nz)
            if key not in found:
                found[key] = list(betas)
            return
        choices = reps if i == 1 else range(p)
        for b in choices:
            if b in betas:
                continue
            new = [cols[j] & shift(Q[(-i - j) % K], b) for j in range(K)]
            dfs(i + 1, new, betas + [b])
    init = [Q[(-j) % K] for j in range(K)]  # i = 0, beta_0 = 0
    dfs(1, init, [0])
    filled_sets = set()
    for key in found:
        for sub in itertools.combinations(sorted(key), K - 1):
            filled_sets.add(frozenset(sub))
    all_subsets = [frozenset(s) for s in itertools.combinations(range(K), K - 1)]
    every = all(s in filled_sets for s in all_subsets)
    full = frozenset(range(K)) in found
    print(f"kappa={kappa} p={p}: every {K-1}-subset of columns fillable: {every}; "
          f"all {K} columns fillable (nonzero contraction exists): {full}; "
          f"example betas: {[found[k] for k in list(found)[:2]]}")
    sys.stdout.flush()

for p, k in [(37, 4), (53, 4), (131, 5), (29, 4), (13, 4), (17, 4), (61, 4)]:
    run(p, k)
