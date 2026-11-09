# s2a: exact finite checks (falsification only) of Lemmas lem:app-s2-weil-count,
# lem:app-s2-moments, lem:app-s2-cyclo, lem:app-s2-stage, Prop. prop:app-s2-TW and
# R <= U_kappa(p) (Prop. prop:app-s2-TA(i)), appendix-schedule2.tex.
# Run: nice -n 19 timeout 900 /opt/anaconda3/bin/python -I exact_checks.py
import random, math, itertools
from fractions import Fraction as Fr
import numpy as np
import sympy
import mpmath as mp
mp.mp.dps = 40
random.seed(20261109)

def primes_1mod(k, lo, hi):
    return [p for p in sympy.primerange(lo, hi) if p % k == 1]

_dl_cache = {}
def dlog_table(p):
    """dl[x] = discrete log of x w.r.t. the least primitive root g (dl[0] = -1)."""
    if p in _dl_cache: return _dl_cache[p]
    g = int(sympy.primitive_root(p))
    dl = np.full(p, -1, dtype=np.int64)
    x = 1
    for n in range(p-1):
        dl[x] = n; x = (x*g) % p
    _dl_cache.clear(); _dl_cache[p] = (g, dl)
    return g, dl

def setup(p, k, xi=None):
    """index table ind[x] in Z_k with x in xi^ind Q_0 (x != 0), ind[0] = -1."""
    g, dl = dlog_table(p)
    if xi is None: xi = g
    e = int(dl[xi % p]) % k
    assert math.gcd(e, k) == 1, "not a coset generator"
    einv = pow(e, -1, k) if k > 1 else 0
    ind = np.where(dl >= 0, (dl % k) * einv % k, -1)
    # sanity: xi^m lies in Q_m
    for m in range(k):
        assert ind[pow(xi, m, p)] == m
    return xi, ind

def E_closed(k, l, sp):
    return (l - 1 - Fr(l, k) + Fr(1, k**l))*sp + Fr(l, k) - l*Fr(1, k**l)

def E_sum(k, l, sp):
    return Fr(1, k**l)*sum(math.comb(l, s)*(k-1)**s*((s-1)*sp + (l-s)) for s in range(1, l+1))

out = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True)

# (0) closed form of E_kappa(l,p): compare as polynomials in sqrt p (coefficients)
bad = 0
for k in range(2, 13):
    for l in range(1, 3*k+1):
        for sp in (Fr(0), Fr(1)):
            if E_closed(k, l, sp) != E_sum(k, l, sp): bad += 1
        if l <= k and not (E_closed(k, l, Fr(0)) <= 1 and (E_closed(k, l, Fr(1)) - E_closed(k, l, Fr(0))) <= l-1): bad += 1
log("(0) closed form of E_kappa(l,p), k=2..12, l=1..3k: mismatches =", bad)

# (1) Lemma weil-count on random instances, including k = p-1 and l up to k+2
viol = 0; n = 0; worst = 0.0
for trial in range(2500):
    k = random.choice([2, 3, 4, 5, 6, 8])
    ps = primes_1mod(k, k+1, 400)
    p = random.choice(ps)
    xi, ind = setup(p, k)
    l = random.randint(1, min(k+2, p))
    r = random.sample(range(p), l)
    c = [random.randrange(1, p) for _ in range(l)]
    m = [random.randrange(k) for _ in range(l)]
    xs = np.arange(p)
    ok = np.ones(p, dtype=bool)
    for rk, ck, mk in zip(r, c, m):
        v = (ck*(xs - rk)) % p
        ok &= (ind[v] == mk)
    N = int(ok.sum())
    main = (p - l)/k**l
    E = float(E_closed(k, l, Fr(0))) + float(E_closed(k, l, Fr(1)) - E_closed(k, l, Fr(0)))*math.sqrt(p)
    n += 1
    if abs(N - main) > E + 1e-9: viol += 1
    if E > 0: worst = max(worst, abs(N-main)/E)
log("(1) weil-count: instances", n, "violations", viol, "worst |N-main|/E =", round(worst, 4))

# (2) Lemma moments by brute force over all y, including k = p-1 edge cases
def moments_brute(p, k, j):
    xi, ind = setup(p, k)
    h = (p-1)//k
    tot1 = 0; tot2 = 0; cnt = 0
    xs = np.arange(p)
    # precompute for each row i>=1 and each y_i the mask of x with x+y_i in Q_{-(i+j)}
    masks = {}
    for i in range(1, k):
        m = (-(i+j)) % k
        masks[i] = np.array([(ind[(xs + y) % p] == m) for y in range(p)])
    base = (ind[xs] == ((-j) % k))
    for ys in itertools.product(range(p), repeat=k-1):
        ok = base.copy()
        for i, y in enumerate(ys, start=1):
            ok &= masks[i][y]
        nj = int(ok.sum()); tot1 += nj; tot2 += nj*nj; cnt += 1
    return Fr(tot1, cnt), Fr(tot2, cnt)

def mb_mc(p, k, ind):
    xs = np.arange(1, p)
    mb = [0]*k; mc = [0]*k
    for v in range(1, p-1):  # v != 0, -1
        if ind[v] == ind[v+1]: mb[ind[v]] += 1
    for w in range(2, p):  # w != 0,1
        if ind[w] == 0: mc[ind[w-1]] += 1
    return mb, mc

for (p, k) in [(7, 3), (13, 3), (19, 3), (13, 4), (17, 4), (11, 5), (13, 6), (5, 4), (7, 6), (3, 2), (11, 10), (29, 4)]:
    xi, ind = setup(p, k); h = (p-1)//k
    mb, mc = mb_mc(p, k, ind)
    pred1 = Fr(h**k, p**(k-1))
    pred2 = pred1 + Fr(h, p**(k-1))*sum(mc[c]*math.prod(mb[b] for b in range(k) if b != (-c) % k) for c in range(k))
    res = []
    for j in range(k):
        if p**(k-1) > 3e5: break
        e1, e2 = moments_brute(p, k, j)
        res.append((e1 == pred1, e2 == pred2))
    log("(2) moments", (p, k), "all j match:", all(a and b for a, b in res) if res else "skipped", len(res))

# (3) Lemma cyclo + (4) R <= U at primes
def U_of(k, p):
    k_ = mp.mpf(k); p_ = mp.mpf(p)
    D = ((k_-1)*(k_-2)*mp.sqrt(p_) + 2*(k_-1))/(p_-k_-1)
    if D > 0.5: return None, D
    u = mp.mpf(1)/2 - D/3 - 1/(k_*(1-D)); v = D/(mp.sqrt(k_)*(1-D)); smax = mp.sqrt(k_)*D
    f = lambda s: -u*s*s + v*s
    c = [0, f(smax)]
    if u > 0 and 0 <= v/(2*u) <= smax: c.append(f(v/(2*u)))
    return k_**k_*p_**(k_-1)/(p_-1)**k_ + mp.exp(max(c)), D

worst_dev = 0.0; viol_c = 0; nprimes = 0; viol_R = 0; nR = 0; minmargin = None
for k, hi in [(2, 3000), (3, 6000), (4, 6000), (5, 6000), (6, 4000), (7, 4000), (8, 4000), (9, 4000), (10, 3000)]:
    for p in primes_1mod(k, k+2, hi):
        xi, ind = setup(p, k); h = (p-1)//k
        mb, mc = mb_mc(p, k, ind)
        mu = Fr(p-k-1, k*k)
        if sum(mb) != k*mu or sum(mc) != k*mu: viol_c += 1
        D = ((k-1)*(k-2)*math.sqrt(p) + 2*(k-1))/(p-k-1)
        dev = max(max(abs(float(Fr(x)/mu) - 1) for x in mb), max(abs(float(Fr(x)/mu) - 1) for x in mc))
        if dev > D + 1e-12: viol_c += 1
        worst_dev = max(worst_dev, dev/D)
        nprimes += 1
        R = Fr(p**(k-1), h**k) + Fr(p**(k-1), h**(2*k-1))*sum(mc[c]*math.prod(mb[b] for b in range(k) if b != (-c) % k) for c in range(k))
        Uv, Dm = U_of(k, p)
        if Uv is not None:
            nR += 1
            if mp.mpf(R.numerator)/R.denominator > Uv: viol_R += 1
            mg = Uv - mp.mpf(R.numerator)/R.denominator
            minmargin = mg if minmargin is None or mg < minmargin else minmargin
log("(3) cyclo: primes", nprimes, "violations", viol_c, "worst dev/Delta =", round(worst_dev, 6))
log("(4) R <= U: primes with Delta<=1/2:", nR, "violations", viol_R, "min margin U-R =", mp.nstr(minmargin, 6))

# (5) Prop TW: X_j nonempty for p > T_W with beta_i = xi^{-i} - 1, two coset generators
def TW(k):
    A = (k-2)*k**k + 1
    return ((A + math.sqrt(A*A + 4*k**k))/2)**2
def TW_check(p, k, xi):
    xi, ind = setup(p, k, xi)
    xs = np.arange(p)
    beta = [0] + [(pow(xi, -i, p) - 1) % p for i in range(1, k)]
    sizes = []
    for j in range(1, k):
        ok = np.ones(p, dtype=bool)
        for i in range(k):
            ok &= (ind[(xs + beta[i]) % p] == ((-(i+j)) % k))
        sizes.append(int(ok.sum()))
    return sizes
fails = []; checked = 0; ii_fail = []
for k, lo, hi in [(2, 7, 4000), (3, 838, 9000)]:
    for p in primes_1mod(k, lo, hi):
        g = sympy.primitive_root(p)
        gens = [g, pow(g, 1 + k*random.randrange(1, 50), p)]
        if k == 3: gens.append(pow(g, 2, p))  # a non-primitive coset generator class (u=2)
        for xi in gens:
            sizes = TW_check(p, k, xi); checked += 1
            if min(sizes) == 0: fails.append((p, k, xi))
            if p >= 4*((k-1)*k**k + 1)**2 and min(sizes) < p/(2*k**k): ii_fail.append((p, k, xi, min(sizes)))
for p in primes_1mod(4, 263700, 264400)[:6]:
    g = sympy.primitive_root(p)
    sizes = TW_check(p, 4, g); checked += 1
    if min(sizes) == 0: fails.append((p, 4, g))
log("(5) TW(i): checked", checked, "(p,xi) pairs above T_W for k=2,3,4; failures", fails[:10], "; TW(ii) failures", ii_fail[:5])
# sharpness probe: largest p < T_W(3) with an empty X_j (for information only)
last_empty = None
for p in primes_1mod(3, 7, 838):
    if min(TW_check(p, 3, sympy.primitive_root(p))) == 0: last_empty = p
log("    info: largest p < T_W(3)=837.1 with empty X_j (k=3, least primitive root):", last_empty)

# (6) Lemma stage: Lambda >= p/(2 k^l) for random distinct nonzero t-prefixes at p >= 4k^(2k+2)
def stage_check(p, k, trials):
    xi, ind = setup(p, k)
    z = [pow(xi, m, p) for m in range(k)]
    xs = np.arange(p)
    worst = None
    for _ in range(trials):
        j = random.randint(1, k-1); l = j+1
        ts = [pow(2, p-2, p)] + random.sample(range(1, p), j-1)
        if len(set(ts)) < j or 0 in ts: continue
        ok = (ind[(2*z[j]*z[j]*xs) % p] == 0)
        for i in range(j):
            ok &= (ind[(z[i]*z[j]*(xs + ts[i])) % p] == 0)
        for t in ts: ok[t] = False
        Lam = int(ok.sum())
        ratio = Lam/(p/(2*k**l))
        worst = ratio if worst is None or ratio < worst else worst
        if Lam < p/(2*k**l): return ('FAIL', p, k, j, Lam)
    return ('ok', p, k, round(worst, 4))
res6 = []
for k, base in [(2, 4*2**6), (3, 4*3**8)]:
    for p in primes_1mod(k, base, base + (3000 if k == 2 else 2000))[:5]:
        res6.append(stage_check(p, k, 200))
pk4 = primes_1mod(4, 4*4**10, 4*4**10 + 400)[:1]
for p in pk4:
    res6.append(stage_check(p, 4, 6))
log("(6) stage count at p >= 4k^(2k+2):", res6)
