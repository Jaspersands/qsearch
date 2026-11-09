"""Referee run 2: own ALG-Q1 on fresh structured / adversarial banks at f(a) = D_3(a)+3a, plus a
hill climb that maximises (optimal absorption load, stall codimension, eps>0).  Families are
written here independently.  Usage: run_fresh.py kappa seed climb [primes...]"""
import sys, os, random, json
import myq1
myq1.CC = int(os.environ.get('CC', '3'))
from collections import Counter
from myq1 import GF, solve, verify, f, rk

k = int(sys.argv[1]); seed = int(sys.argv[2]); climb = int(sys.argv[3])
primes = [int(x) for x in sys.argv[4:]] or ([1009, 10007] if k == 2 else [1009, 10009])
amax = int(__import__("os").environ.get("AMAX", "8"))
rng = random.Random(seed)


def rv(p, a): return [rng.randrange(p) for _ in range(a)]
def cmb(p, Bs, a): 
    c = [rng.randrange(1, p) for _ in Bs]
    return [sum(x * v[t] for x, v in zip(c, Bs)) % p for t in range(a)]
def sc(p, v): 
    c = rng.randrange(1, p); return [c * x % p for x in v]


def fam(p, a, M, nr):
    def lines():
        m = rng.randrange(a + 1, a + 4)
        vs = [rv(p, a) for _ in range(m)]
        return [sc(p, vs[i % m]) for i in range(M)]
    def pairs():
        cols = []
        while len(cols) + 2 <= M:
            v = rv(p, a); c = rng.randrange(1, p)
            cols += [[c * x % p for x in v], [(-c * nr) * x % p for x in v]]
        return cols + [rv(p, a) for _ in range(M - len(cols))]
    def flat():
        y = rng.randrange(1, a); Y = [rv(p, a) for _ in range(y)]
        fr = rng.choice([0.5, 0.7, 0.85])
        return [cmb(p, Y, a) if i < fr * M else rv(p, a) for i in range(M)]
    def nested():
        Bs = [rv(p, a) for _ in range(a)]
        cols = []
        for d in range(1, a + 1):
            cols += [cmb(p, Bs[:d], a) for _ in range(rng.randrange(1, d + 3))]
        while len(cols) < M: cols.append(cmb(p, Bs, a))
        rng.shuffle(cols); return cols[:M]
    def hyper():
        H = [rv(p, a) for _ in range(a - 1)]; out = rng.randrange(1, 4)
        return [cmb(p, H, a) for _ in range(M - out)] + [rv(p, a) for _ in range(out)]
    def bigcircuit():
        # one early large circuit (6 columns in a 5-flat), then proportional pairs, then a low pool
        Bs = [rv(p, a) for _ in range(a)]
        cols = [Bs[i] for i in range(a)]
        F5 = Bs[:min(5, a)]
        c5 = [cmb(p, F5, a) for _ in range(6)]
        cols += c5
        while len(cols) < M - (M // 3):
            v = cmb(p, Bs[:rng.randrange(1, a + 1)], a)
            cols += [v, sc(p, v)]
        lo = Bs[:2]
        while len(cols) < M: cols.append(cmb(p, lo, a))
        return cols[:M]
    def sparse():
        cols = []
        for _ in range(M):
            v = [0] * a
            for t in rng.sample(range(a), rng.choice([1, 2, 2, 3])):
                v[t] = rng.choice([1, p - 1, 2, nr])
            cols.append(v)
        return cols
    return dict(lines=lines, pairs=pairs, flat=flat, nested=nested, hyper=hyper,
                bigcircuit=bigcircuit, sparse=sparse)


def run(F, cols):
    tr = []
    x = solve(F, cols, rng, rule=rng.choice(["last", "first", "random"]), fallback=True, passes=8, trace=tr)
    if x is not None:
        assert verify(F.p, F.k, cols, x)
    load = max([d.get("load", 0) for _, c, d in tr if c in ("heavy", "absorb")] + [0])
    q = max([d["q"] for _, c, d in tr if c == "stall"] + [0])
    eps = max([d["eps"] for _, c, d in tr if c == "stall"] + [0])
    return x, tr, (load, q, eps)


cases, n, fails, maxload = Counter(), 0, 0, 0
leafload = Counter(); singlefails = Counter(); heavy = []
for p in primes:
    F = GF(p, k)
    nr = next(z for z in range(2, p) if F.cls(z) != 0)
    for a in range(3, amax + 1):
        M = f(a)
        for name, gen in fam(p, a, M, nr).items():
            cols = gen()
            best, bs = cols, None
            for it in range(climb + 1):
                if it:
                    c2 = [list(v) for v in best]
                    i = rng.randrange(M); u = rng.random()
                    if u < 0.4: c2[i] = sc(p, best[rng.randrange(M)])
                    elif u < 0.75: c2[i] = cmb(p, [best[rng.randrange(M)], best[rng.randrange(M)]], a)
                    else: c2[i] = rv(p, a)
                    rng.shuffle(c2)
                    cols = c2
                try:
                    x, tr, s = run(F, cols)
                except AssertionError as e:
                    print("ASSERTION", p, k, a, name, repr(e), json.dumps(cols), flush=True)
                    fails += 1; continue
                n += 1
                fails += x is None
                for d, c, info in tr:
                    cases[c] += 1
                    if c in ("thm2", "closure", "absorb-leaf", "codim1-closure", "top-pair"):
                        leafload[info["load"]] += 1
                        singlefails[c] += info["fails"]
                    if c == "heavy":
                        heavy.append(dict(p=p, a=a, fam=name, info=info))
                if x is None:
                    print("FAIL", p, k, a, name, tr, json.dumps(cols), flush=True)
                if bs is None or s >= bs:
                    best, bs = cols, s
        print(p, k, "done", n, dict(cases), flush=True)
print("banks", n, "unsolved/assertion", fails)
print("cases", dict(cases))
print("leaf loads", dict(leafload), "total single-pass failures before success, by leaf kind", dict(singlefails))
print("heavy stalls (optimal load >= 3):", len(heavy))
for h in heavy[:20]:
    print("  ", h)
