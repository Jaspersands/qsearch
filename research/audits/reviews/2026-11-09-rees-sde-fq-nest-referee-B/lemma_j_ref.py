"""Referee B: Lemma J checks.
(a) p = 5, k = 2, EXHAUSTIVE up to GL_2: for every spanning orbit representative L (distinct labels =
    genuine classes) with |L| >= 4 and every mu with <mu, l> != 0 on L taking >= 2 values, some mu'
    independent of mu gives >= 4 distinct joint labels (<mu,l>, <mu',l>).
(b) p = 5, k = 3 and p = 7, k = 2, 3: random label sets (sampled).
(c) p = 3: the note restricts Lemma J to p >= 5 via t < p; in fact t <= 3 proper hyperplanes never
    cover F_p^k for any p >= 3 (a cover needs p + 1), so the lemma also holds at p = 3.
"""
import itertools, numpy as np
rng = np.random.default_rng(11)

def check(L, p, k):
    """returns (#deltas tested, #failures)"""
    mus = [m for m in itertools.product(range(p), repeat=k) if any(m)]
    dot = lambda m, l: sum(a * b for a, b in zip(m, l)) % p
    tested = fails = 0
    for mu in mus:
        vals = [dot(mu, l) for l in L]
        if 0 in vals or len(set(vals)) < 2:
            continue
        tested += 1
        ok = False
        for mu2 in mus:
            # independence of mu2 from mu (as functionals on the span of L = F_p^k)
            if any(all((c * a - b) % p == 0 for a, b in zip(mu, mu2)) for c in range(p)):
                continue
            if len({(dot(mu, l), dot(mu2, l)) for l in L}) >= 4:
                ok = True
                break
        fails += not ok
    return tested, fails

p = 5
vecs = [v for v in itertools.product(range(p), repeat=2) if any(v)]
reps = np.load('reps_f5.npy')
T = F = 0
for r in reps:
    L = [vecs[i] for i in range(24) if int(r) >> i & 1]
    if len(L) < 4:
        continue
    t, f = check(L, 5, 2)
    T += t; F += f
print(f'(a) p=5 k=2 exhaustive over orbits: {T} (L, delta) pairs, failures {F}')

for (p, k, trials) in ((5, 3, 3000), (7, 2, 3000), (7, 3, 1500)):
    allv = [v for v in itertools.product(range(p), repeat=k) if any(v)]
    T = F = 0
    for _ in range(trials):
        c = int(rng.integers(4, 10))
        L = [allv[i] for i in rng.choice(len(allv), size=c, replace=False)]
        M = np.array(L).T % p
        # spanning check by rank over F_p (small): brute force on minors via elimination
        A = M.copy(); r = 0
        for col in range(A.shape[1]):
            piv = next((i for i in range(r, k) if A[i, col] % p), None)
            if piv is None:
                continue
            A[[r, piv]] = A[[piv, r]]
            A[r] = (A[r] * pow(int(A[r, col]), -1, p)) % p
            for i in range(k):
                if i != r and A[i, col]:
                    A[i] = (A[i] - A[i, col] * A[r]) % p
            r += 1
        if r < k:
            continue
        t, f = check(L, p, k)
        T += t; F += f
    print(f'(b) p={p} k={k} sampled: {T} (L, delta) pairs, failures {F}')

# (c) p = 3, exhaustive: all label sets in F_3^2 with >= 4 labels; in F_3^3 all with 4..6 labels
for k in (2, 3):
    allv = [v for v in itertools.product(range(3), repeat=k) if any(v)]
    T = F = 0
    for c in range(4, (len(allv) if k == 2 else 6) + 1):
        for L in itertools.combinations(allv, c):
            t, f = check(list(L), 3, k)
            T += t; F += f
    print(f'(c) p=3 k={k} exhaustive over all label sets with >= 4 labels: {T} (L, delta) pairs, failures {F}')
