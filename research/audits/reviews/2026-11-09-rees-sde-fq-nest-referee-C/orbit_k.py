"""Referee C: orbits of nonzero functionals w on F_p^k under the transpose action of the label
symmetries sigma(a, b) = (lam a, M b + a v) (lam in F_p^*, M in GL_{k-1}(F_p), v in F_p^{k-1}),
which preserve the nested label set F_p^* x F_p^{k-1}.  <w, sigma l> = <sigma^T w, l> with
sigma^T (w_a, w_b) = (lam w_a + <w_b, v>, M^T w_b).  Union-find over generators.
Also: (k = 2) orbits of PAIRS (w1, w2) under the same group plus the swap, to cross-check the
3p - 2 Lemma U cases by an independent computation."""
import sys, itertools
p, k = int(sys.argv[1]), int(sys.argv[2])
pts = [w for w in itertools.product(range(p), repeat=k) if any(w)]
idx = {w: i for i, w in enumerate(pts)}
par = list(range(len(pts)))
def find(x):
    while par[x] != x:
        par[x] = par[par[x]]; x = par[x]
    return x
def union(a, b):
    a, b = find(a), find(b)
    if a != b: par[a] = b
g = next(x for x in range(2, p) if all(pow(x, (p - 1) // q, p) != 1 for q in range(2, p) if (p - 1) % q == 0 and all(q % d for d in range(2, q))))
m = k - 1
gens = []
gens.append(lambda w: ((g * w[0]) % p,) + tuple(w[1:]))                      # lam = g
for i in range(m):                                                              # v = e_i
    gens.append(lambda w, i=i: ((w[0] + w[1 + i]) % p,) + tuple(w[1:]))
if m >= 1:
    gens.append(lambda w: (w[0], (g * w[1]) % p) + tuple(w[2:]))              # M^T = diag(g,1..)
if m >= 2:
    gens.append(lambda w: (w[0], w[2], w[1]) + tuple(w[3:]))                   # swap b-coords
    gens.append(lambda w: (w[0], (w[1] + w[2]) % p) + tuple(w[2:]))           # elementary
    gens.append(lambda w: (w[0],) + tuple(w[2:]) + (w[1],))                    # cycle
for w in pts:
    for f in gens:
        union(idx[w], idx[f(w)])
orb = {}
for w in pts:
    orb.setdefault(find(idx[w]), []).append(w)
print(f'p={p} k={k}: {len(orb)} orbits of nonzero functionals; representatives and sizes:')
for o in orb.values():
    rep = min(o, key=lambda w: (sum(1 for x in w if x), w[::-1]))
    print('   ', rep, len(o))
if k == 2:
    # pairs: act diagonally with the generators, plus the swap
    P2 = [(a, b) for a in pts for b in pts]
    pid = {x: i for i, x in enumerate(P2)}
    par = list(range(len(P2)))
    for (a, b) in P2:
        for f in gens:
            union(pid[(a, b)], pid[(f(a), f(b))])
        union(pid[(a, b)], pid[(b, a)])
    orbs = {}
    for x in P2:
        orbs.setdefault(find(pid[x]), []).append(x)
    A, B = (1, 0), (0, 1)
    cases = [(A, B)] + [(A, (c, 0)) for c in range(1, p)] + [(B, (0, c)) for c in range(1, p)] + [(B, (1, c)) for c in range(1, p)]
    hit = {find(pid[c]) for c in cases}
    print(f'pairs: {len(orbs)} orbits under group+swap; the 3p-2 = {len(cases)} cases meet {len(hit)} of them '
          f'({"all" if len(hit) == len(orbs) else "NOT all"}); cases in distinct orbits: {len(hit) == len(cases)}')
