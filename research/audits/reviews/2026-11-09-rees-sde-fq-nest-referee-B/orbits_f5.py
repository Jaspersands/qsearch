"""Referee B, independent re-implementation: GL_2(F_5)-orbits on subsets of F_5^2 minus 0.

(1) Enumerate all 480 matrices of GL_2(F_5) explicitly (not from generators).
(2) Canonical form of every subset (24-bit mask) = min over the 480 images (vectorised).
(3) Burnside / cycle-index count of orbits by size, as an independent count.
(4) Check that the orbit sizes 480/|Stab| sum to 2^24.
Writes orbit representatives (masks) to reps_f5.npy.
"""
import itertools, numpy as np, sys
p = 5
vecs = [v for v in itertools.product(range(p), repeat=2) if any(v)]
idx = {v: i for i, v in enumerate(vecs)}
G = []
for a, b, c, d in itertools.product(range(p), repeat=4):
    if (a * d - b * c) % p:
        G.append(((a, b), (c, d)))
assert len(G) == 480

def perm(M):
    (a, b), (c, d) = M
    return [idx[((a * x + b * y) % p, (c * x + d * y) % p)] for x, y in vecs]

perms = [perm(M) for M in G]
N = 1 << 24
x = np.arange(N, dtype=np.int64)
bytes_ = [(x >> (8 * t)) & 255 for t in range(3)]

def image(pm):
    out = np.zeros(N, dtype=np.int64)
    for t in range(3):
        tab = np.zeros(256, dtype=np.int64)
        for b in range(256):
            v = 0
            for bit in range(8):
                if b >> bit & 1:
                    v |= 1 << pm[8 * t + bit]
            tab[b] = v
        out |= tab[bytes_[t]]
    return out

canon = x.copy()
stab = np.zeros(N, dtype=np.int32)
for i, pm in enumerate(perms):
    im = image(pm)
    np.minimum(canon, im, out=canon)
    stab += (im == x)
    if i % 80 == 0:
        print('  group element', i, flush=True)
reps = np.nonzero(canon == x)[0]
print('orbits (canonical forms):', len(reps))
assert int((480 // stab[reps]).sum()) == N, 'orbit-stabilizer sum mismatch'
assert np.all(480 % stab == 0)
print('sum of orbit sizes 480/|Stab| over reps = 2^24: OK')
pc = np.array([bin(int(r)).count('1') for r in reps])
by = {s: int((pc == s).sum()) for s in range(25)}

# Burnside via cycle index: number of orbits of size-s subsets = (1/|G|) sum_g [x^s] prod_cycles (1 + x^len)
tot = np.zeros(25, dtype=object)
for pm in perms:
    seen = [False] * 24; poly = [1] + [0] * 24
    for s0 in range(24):
        if seen[s0]:
            continue
        L = 0; j = s0
        while not seen[j]:
            seen[j] = True; j = pm[j]; L += 1
        new = poly[:]
        for e in range(24 - L, -1, -1):
            if poly[e]:
                new[e + L] += poly[e]
        poly = new
    for e in range(25):
        tot[e] += poly[e]
burn = {s: tot[s] // 480 for s in range(25)}
assert all(tot[s] % 480 == 0 for s in range(25))
print('size: canonical-form count, Burnside count')
for s in range(25):
    print(f'  {s:2d}: {by[s]:5d} {burn[s]:5d}')
assert all(by[s] == burn[s] for s in range(25))
print('Burnside total', sum(burn.values()))

def spans(mask):
    L = [vecs[i] for i in range(24) if mask >> i & 1]
    return any((u[0] * v[1] - u[1] * v[0]) % p for u in L for v in L)
sp = np.array([spans(int(r)) for r in reps])
print('spanning orbits by size:', [int(((pc == s) & sp).sum()) for s in range(2, 25)])
print('non-spanning orbits by size:', {s: int(((pc == s) & ~sp).sum()) for s in range(25) if ((pc == s) & ~sp).sum()})
np.save('reps_f5.npy', reps[sp])
print('saved', int(sp.sum()), 'spanning representatives')
