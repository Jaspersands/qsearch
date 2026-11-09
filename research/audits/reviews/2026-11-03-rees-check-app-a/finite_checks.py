"""Exact finite checks of Lemmas lem:app-s2-weil-count, lem:app-s2-moments,
lem:app-s2-cyclo and Proposition prop:app-s2-TA(i) (R <= U) in appendix-schedule2.tex.
Run: /opt/anaconda3/bin/python -I finite_checks.py
"""
import json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from itertools import product
from sympy import primerange
import mpmath
from ffcommon import coset_table
from thresholds import U as Ufun  # noqa: E402  (re-runs nothing heavy at import? see guard)

random.seed(20261103)
OUT = {}

# ---- Lemma weil-count: exhaustive over small p, random beyond
def Ebound(k, l, p):
    return (l - 1 - l / k + k ** (-l)) * math.sqrt(p) + l / k - l * k ** (-l)

worst = 0.0
n_inst = 0
viol = []
for p in primerange(3, 140):
    for k in range(2, p):
        if (p - 1) % k:
            continue
        ind, _ = coset_table(p, k)
        trials = 60 if p > 40 else 25
        for _ in range(trials):
            l = random.randint(1, min(k + 2, p - 1))
            r = random.sample(range(p), l)
            c = [random.randrange(1, p) for _ in range(l)]
            m = [random.randrange(k) for _ in range(l)]
            N = 0
            for x in range(p):
                ok = True
                for rk, ck, mk in zip(r, c, m):
                    y = ck * (x - rk) % p
                    if y == 0 or ind[y] != mk:
                        ok = False
                        break
                N += ok
            dev = abs(N - (p - l) / k ** l)
            E = Ebound(k, l, p)
            n_inst += 1
            if dev > E + 1e-9:
                viol.append((p, k, l, r, c, m, N, E))
            if E > 0:
                worst = max(worst, dev / E)
OUT['weil_count'] = dict(instances=n_inst, violations=viol[:5], n_viol=len(viol), worst_ratio=worst)

# ---- Lemma moments: brute force over all y (y_0 = 0)
mom = []
for (p, k) in [(7, 2), (11, 2), (7, 3), (13, 3), (19, 3), (31, 3), (13, 4), (17, 4), (11, 5), (31, 5), (13, 6), (29, 7)]:
    if (k - 1) * math.log(p) > math.log(4e5):
        continue
    ind, _ = coset_table(p, k)
    h = (p - 1) // k
    Q = lambda x, mm: x % p != 0 and ind[x % p] == mm % k
    mb = [sum(1 for v in range(1, p) if ind[v] == b and (v + 1) % p and ind[(v + 1) % p] == b) for b in range(k)]
    mc = [sum(1 for w in range(2, p) if ind[w] == 0 and ind[w - 1] == c) for c in range(k)]
    pred1 = Fraction(h ** k, p ** (k - 1))
    corr = Fraction(h, p ** (k - 1)) * sum(mc[c] * math.prod(mb[b] for b in range(k) if b != (-c) % k) for c in range(k))
    ok = True
    for j in range(k):
        s1 = s2 = 0
        cnt = 0
        for ys in product(range(p), repeat=k - 1):
            y = (0,) + ys
            n = sum(1 for x in range(p) if all(Q(x + y[i], -(i + j)) for i in range(k)))
            s1 += n
            s2 += n * n
            cnt += 1
        if Fraction(s1, cnt) != pred1 or Fraction(s2, cnt) != pred1 + corr:
            ok = False
    mom.append((p, k, ok))
OUT['moments'] = mom

# ---- Lemma cyclo and R <= U at every prime p = 1 mod k, p > k+1, below a bound
cyc = {}
for k, B in [(2, 20000), (3, 20000), (4, 20000), (5, 12000), (6, 8000), (7, 8000), (8, 5000)]:
    worst = 0.0
    nprimes = 0
    sum_fail = 0
    RU_fail = []
    for p in primerange(k + 2, B):
        if (p - 1) % k:
            continue
        ind, _ = coset_table(p, k)
        h = (p - 1) // k
        mb = [0] * k
        for v in range(1, p - 1):
            if ind[v] == ind[v + 1]:
                mb[ind[v]] += 1
        mc = [0] * k
        for w in range(2, p):
            if ind[w] == 0:
                mc[ind[w - 1]] += 1
        mu = Fraction(p - k - 1, k * k)
        D = ((k - 1) * (k - 2) * math.sqrt(p) + 2 * (k - 1)) / (p - k - 1)
        if sum(mb) != k * mu or sum(mc) != k * mu:
            sum_fail += 1
        dev = max(abs(float(Fraction(x) / mu) - 1) for x in mb + mc)
        worst = max(worst, dev / D)
        nprimes += 1
        if D <= 0.5:
            R = Fraction(p ** (k - 1), h ** k) + Fraction(p ** (k - 1), h ** (2 * k - 1)) * sum(
                mc[c] * math.prod(mb[b] for b in range(k) if b != (-c) % k) for c in range(k))
            Uv = Ufun(k, p)[0]
            if not mpmath.mpf(R.numerator) / R.denominator <= Uv:
                RU_fail.append(p)
    cyc[k] = dict(primes=nprimes, worst_dev_over_Delta=worst, sum_failures=sum_fail, R_le_U_failures=RU_fail)
OUT['cyclo'] = cyc
print(json.dumps(OUT, indent=1, default=str))
