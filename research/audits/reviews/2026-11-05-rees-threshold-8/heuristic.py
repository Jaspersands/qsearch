"""Orbit-corrected Poisson model for E_2(kappa) (threshold-8, section 6) [float/conjecture].

mu(p) = p^(2k-2) * ((h+1)/p)^(k^2-1), h = (p-1)/k: expected number of normalised
contractions if the k^2-1 free cells were independent (zero cells allowed).
Model: Pr[p in E_2] = exp(-c * mu(p) / (2 k^2)), 2k^2 = order of the recentring+transpose group.
Fits c per kappa (and per parity of h for even kappa) by maximum likelihood on the exact sets
kappa = 4..7, then forecasts the largest member for kappa = 8, 9.
"""
import math, re, sys
from sympy import primerange
E = {4: {5,13,17,29,37,53}, 5: {11,31,41,61,71,101,131,151,181}}
def load_inf(f):
    s = set()
    for l in open(f):
        m = re.match(r'INFEASIBLE.*p=(\d+)', l)
        if m: s.add(int(m.group(1)))
    return s
E[6] = load_inf('2026-11-02-rees-threshold-2/xval_k6.out')
E[7] = set(int(x) for x in open('2026-11-02-rees-threshold-2/E2_k7.txt').read().split())
def logmu(p, k):
    h = (p-1)//k
    return (2*k-2)*math.log(p) + (k*k-1)*math.log((h+1)/p)
def primes(k, hi):
    return [p for p in primerange(3, hi) if p % k == 1]
def fit(k, ps, members):
    # maximise sum log L over c on a grid (log-space)
    best = None
    for t in range(-400, 401):
        c = math.exp(t/40)
        ll = 0.0
        for p in ps:
            lam = c*math.exp(logmu(p,k))/(2*k*k)
            q = math.exp(-lam)
            if p in members: ll += -lam
            else: ll += math.log(max(1e-300, 1-q))
        if best is None or ll > best[0]: best = (ll, c)
    return best[1]
out = []
for k in (4,5,6,7):
    hi = {4:2000, 5:5000, 6:20000, 7:60000}[k]
    ps = primes(k, hi)
    pm = max(E[k])
    mu_at = math.exp(logmu(pm,k))
    c = fit(k, ps, E[k])
    line = f"k={k} |E2|={len(E[k])} max={pm} max/k^((k+1)/2)={pm/k**((k+1)/2):.3f} mu(max)={mu_at:.3g} mu/(2k^2)={mu_at/(2*k*k):.3g} c_fit={c:.3g}"
    if k % 2 == 0:
        for par in (0,1):
            ps2 = [p for p in ps if ((p-1)//k) % 2 == par]
            c2 = fit(k, ps2, E[k] & set(ps2))
            m2 = max([p for p in E[k] if ((p-1)//k)%2==par], default=None)
            line += f" | h%2={par}: c={c2:.3g} max={m2}"
    print(line); out.append(c)
# forecast: expected number of members above X for kappa = 8, 9 with c in [min,max] of fitted values
for k in (8, 9):
    for c in (min(out), math.exp(sum(map(math.log,out))/len(out)), max(out)):
        ps = primes(k, 400000)
        tail = 0.0; xs = []
        lam = [c*math.exp(logmu(p,k))/(2*k*k) for p in ps]
        pr = [math.exp(-l) for l in lam]
        # predicted max: largest X with expected count of members >= X at least 0.5
        acc = 0.0; X = None
        for p, q in zip(reversed(ps), reversed(pr)):
            acc += q
            if acc >= 0.5: X = p; break
        exp_count = sum(pr)
        print(f"forecast k={k} c={c:.3g}: E|E2| ~ {exp_count:.0f}, predicted max ~ {X} = {X/k**((k+1)/2):.2f} k^((k+1)/2); mu=1 at {next(p for p in ps if logmu(p,k)>0)}")
