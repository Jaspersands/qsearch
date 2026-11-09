"""Referee run 3: banks aimed at the rarer branches (case 3 rec-U+, CODIM1 closure / top pair /
rec-H, codimension q >= 3 stalls) and at heavy stalls at a = 8..10.  Own code only.
Usage: run_target.py kappa seed n [primes...]"""
import sys, os, random, json
import myq1
myq1.CC = int(os.environ.get('CC', '3'))
from collections import Counter
from myq1 import GF, solve, verify, f

k, seed, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
primes = [int(x) for x in sys.argv[4:]] or ([10007] if k == 2 else [10009])
rng = random.Random(seed)
def rv(p, a): return [rng.randrange(p) for _ in range(a)]
def cmb(p, Bs, a):
    c = [rng.randrange(1, p) for _ in Bs]
    return [sum(x * v[t] for x, v in zip(c, Bs)) % p for t in range(a)]
def sc(p, v):
    c = rng.randrange(1, p); return [c * x % p for x in v]

def gen(p, a, M, nr):
    Bs = [rv(p, a) for _ in range(a)]
    kind = rng.choice(["flatcodim", "lowpool", "pairs_low", "bigcirc_pairs", "twoflats"])
    if kind == "flatcodim":           # dense flat of codim 2..3, few columns outside
        c = rng.choice([2, 3]); H = Bs[:a - c]
        out = rng.randrange(c, c + 3)
        cols = [cmb(p, H, a) for _ in range(M - out)] + [cmb(p, Bs, a) for _ in range(out)]
    elif kind == "lowpool":           # basis first, a few big circuits, the rest in a low flat
        cols = list(Bs)
        while len(cols) < M // 2:
            d = rng.randrange(2, a + 1); cols.append(cmb(p, Bs[:d], a))
        lo = Bs[:rng.randrange(1, 4)]
        while len(cols) < M: cols.append(cmb(p, lo, a))
    elif kind == "pairs_low":         # proportional pairs (ratio a non-residue) in nested flats
        cols = list(Bs)
        while len(cols) + 2 <= M:
            v = cmb(p, Bs[:rng.randrange(1, a + 1)], a); c = rng.randrange(1, p)
            cols += [[c * x % p for x in v], [(-c * nr) * x % p for x in v]]
        while len(cols) < M: cols.append(cmb(p, Bs[:2], a))
    elif kind == "bigcirc_pairs":     # one early full circuit in a flat, then pairs, then a low pool
        cols = list(Bs)
        d = rng.randrange(4, a + 1)
        cols += [cmb(p, Bs[:d], a) for _ in range(d + 1)]
        while len(cols) < (2 * M) // 3:
            v = cmb(p, Bs[:rng.randrange(1, a + 1)], a); cols += [v, sc(p, v)]
        lo = Bs[:rng.randrange(2, max(3, a - 3))]
        while len(cols) < M: cols.append(cmb(p, lo, a))
    else:                             # two flats meeting in a line
        h = a // 2 + 1
        F1, F2 = Bs[:h], Bs[h - 1:]
        cols = [cmb(p, F1 if rng.random() < 0.5 else F2, a) for _ in range(M)]
    cols = cols[:M]
    if rng.random() < 0.5:
        rng.shuffle(cols)
    return kind, cols

cases, kinds, n, bad = Counter(), Counter(), 0, 0
heavy = []
for p in primes:
    F = GF(p, k)
    nr = next(z for z in range(2, p) if F.cls(z) != 0)
    for t in range(N):
        a = rng.choice([4, 5, 6, 7, 8] + ([9, 10] if t % 4 == 0 else []))
        M = f(a)
        kind, cols = gen(p, a, M, nr)
        tr = []
        try:
            x = solve(F, cols, rng, rule=rng.choice(["last", "first", "random"]), fallback=True, passes=8, trace=tr)
        except AssertionError as e:
            print("ASSERTION", p, k, a, kind, repr(e), json.dumps(cols), flush=True); bad += 1; continue
        n += 1
        if x is None:
            bad += 1; print("FAIL", p, k, a, kind, tr, flush=True)
        else:
            assert verify(p, k, cols, x)
        for d, c, info in tr:
            cases[c] += 1
            if c == "stall":
                kinds[(info["q"], info["qplus"], min(info["eps"], 2))] += 1
            if c == "heavy":
                heavy.append(dict(a=a, kind=kind, info=info))
    print(p, k, "n", n, dict(cases), flush=True)
print("banks", n, "unsolved/assertion", bad)
print("cases", dict(cases))
print("stall shapes (q, q+, min(eps,2))", dict(sorted(kinds.items())))
print("heavy (optimal load >= 3):", len(heavy))
for h in heavy[:10]: print("  ", h)
