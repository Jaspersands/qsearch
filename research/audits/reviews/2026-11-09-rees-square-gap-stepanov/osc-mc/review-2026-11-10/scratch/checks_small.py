"""Referee scratch: (1) brute-force check of pairsym.py's n_T_with_two_pairs / n_T_with_two_units (copied verbatim,
k made a parameter); (2) mob_from involution check; (3) parity obstruction: for even k a 2x2 block
{a, iota a} x {x, iota x} with iota non-split is never rank-1; 4x4 block rates for split / non-split iota at k = 6, 7.
Run from osc-mc."""
import sys, math, itertools
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from sym_confs_lib import mob_from, act_factory


def n_T_with_two_pairs(b, m, k):
    tot = 0
    for j in range(2, m + 1):
        rest = k - 2 * j
        if rest < 0: break
        others = b - 2 * m
        cnt = 0
        for h in range(0, rest + 1):
            if rest - h > others or h > m - j: continue
            cnt += math.comb(m - j, h) * 2 ** h * math.comb(others, rest - h)
        tot += math.comb(m, j) * cnt
    return tot


def n_T_with_two_units(b, m, f, k):
    r = b - 2 * m - f; tot = 0
    for j in range(0, m + 1):
        for i in range(0, f + 1):
            if j + i < 2: continue
            for h in range(0, m - j + 1):
                rest = k - 2 * j - h - i
                if rest < 0 or rest > r: continue
                tot += math.comb(m, j) * math.comb(m - j, h) * 2 ** h * math.comb(f, i) * math.comb(r, rest)
    return tot


bad = 0; ntest = 0
for k in (6, 7):
    for b in range(k, 13):
        for m in range(0, b // 2 + 1):
            for f in range(0, 3):
                if 2 * m + f > b: continue
                pts = list(range(b)); pairs = [(2 * i, 2 * i + 1) for i in range(m)]; fixed = list(range(2 * m, 2 * m + f))
                bp = bu = 0
                for T in itertools.combinations(pts, k):
                    sT = set(T); npairs = sum(1 for u, v in pairs if u in sT and v in sT); nfix = sum(1 for z in fixed if z in sT)
                    bp += npairs >= 2; bu += npairs + nfix >= 2
                ntest += 1
                if f == 0 and bp != n_T_with_two_pairs(b, m, k): bad += 1; print('pairs mismatch', k, b, m, bp, n_T_with_two_pairs(b, m, k))
                if bu != n_T_with_two_units(b, m, f, k): bad += 1; print('units mismatch', k, b, m, f, bu, n_T_with_two_units(b, m, f, k))
print('(1) counting functions: %d cases, %d mismatches' % (ntest, bad))

# (2) mob_from: the map (a, a', b) -> (a', a, b') is an involution mapping b' -> b
p = 1657; act = act_factory(p); rng = np.random.default_rng(1); badinv = 0; nsplit = 0; N = 2000
for _ in range(N):
    a_, a2, b_, b2 = [int(v) for v in rng.choice(p, 4, replace=False)]
    gm = mob_from((a_, a2, b_), (a2, a_, b2))
    y = act(gm, [a_, a2, b_, b2]); z = act(gm, y)
    if y != [a2, a_, b2, b_] or z != [a_, a2, b_, b2]: badinv += 1
    A, B, C, Dd = gm; disc = (A * A + B * C) % p
    nsplit += pow(disc, (p - 1) // 2, p) == 1
print('(2) mob_from: %d of %d not the expected involution; split fraction %.3f' % (badinv, N, nsplit / N))


def index_table(p):
    g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
    for t in range(p - 1):
        ind[x] = t; x = x * g % p
    return ind


def block_rates(k, p, ns, seed=3):
    ind = index_table(p); rng = np.random.default_rng(seed)
    eps = next(e for e in range(2, p) if pow(e, (p - 1) // 2, p) == p - 1)       # a non-square
    inv = lambda v: np.array([pow(int(t), p - 2, p) for t in v]) if False else None
    out = {}
    for kind in ('split', 'nonsplit'):
        a, b, xx, yy = (rng.integers(1, p, ns) for _ in range(4))
        if kind == 'split':
            io = lambda v: (-v) % p
        else:
            io = lambda v: (eps * pow_inv(v, p)) % p
        rows = np.stack([a, io(a), b, io(b)], 1); cols = np.stack([xx, io(xx), yy, io(yy)], 1)
        allp = np.concatenate([rows, cols], 1); srt = np.sort(allp, 1); ok = (np.diff(srt, axis=1) != 0).all(1)
        Mx = ind[(rows[:, :, None] - cols[:, None, :]) % p] % k
        d = (Mx - Mx[:, :1, :] - Mx[:, :, :1] + Mx[:, :1, :1]) % k
        r4 = (d == 0).all((1, 2)) & ok
        r2 = (d[:, :2, :2] == 0).all((1, 2)) & ok
        out[kind] = (r2.sum() / ok.sum(), r4.sum() / ok.sum(), int(r4.sum()))
    return out


def pow_inv(v, p):
    # modular inverse via Fermat, vectorised by repeated squaring
    v = v.astype(np.int64) % p; res = np.ones_like(v); e = p - 2; base = v.copy()
    while e:
        if e & 1: res = res * base % p
        base = base * base % p; e >>= 1
    return res


for k, p, ns in ((6, 1657, 1000000), (6, 1621, 1000000), (7, 35281, 2000000)):
    r = block_rates(k, p, ns); e = 2 if k % 2 == 0 else 1
    print('(3) k=%d p=%d: 2x2 rank-1 rate split %.4f nonsplit %.4f (generic 1/k = %.4f);  4x4 rate / k^-5: split %.3f (%d events) nonsplit %.3f (%d events); heuristic e_k = %d' % (
        k, p, r['split'][0], r['nonsplit'][0], 1 / k, r['split'][1] * k ** 5, r['split'][2], r['nonsplit'][1] * k ** 5, r['nonsplit'][2], e))
