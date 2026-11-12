"""decode_sim.py: classical simulation of the full cyclic-case algorithm (report Secs. C1-C4).

Per trial: random h = (a,b,c) with |a|,|b| < 2^b (half the trials |c| < 2^b, half |c| < 2^{2b}).
Stage 1 (twisted template), per sample: rho_1, rho_2 exactly uniform mod N0; SDA-ISO with FULL
enumeration (common.sda_iso_full, the Lemma-P version), retried on failure (each retry = 2 fresh
coset states); alpha = sum rho_i C(mu_i,2)/N0; y drawn EXACTLY from the ideal law
P*_alpha(y) = Mb^-4 sum_lines F_L(<y,w>/Mb + alpha X3).  (The real output law is within TV 2 eta_s
of P*_alpha per sample by C1/C4; c1_explicit.py checks that inequality with explicit states.)
Direction decoder = report Lemma D (LLL, dim 3+m).  Stage 2 (abelian A_v): if the decoded v is
right, y is drawn exactly from the coset-state Fourier law of the rank-1 lattice Z(d,s0) in
[0,F_A)^2; if wrong, f o iota is injective and y is uniform.  Lemma D (dim 2+m) gives the
direction l^ of (d,s0); then Shor period finding on j -> f(iota(j l^)) (exact law simulated),
candidate periods are accepted only through the membership oracle (in_H = the f(g)=f(1) test),
the gcd of accepted values is reduced prime by prime (factorint stands for Shor factoring),
and h_out = iota(g l^).  Success = h_out in {h, h^-1}.  Up to 3 batches per trial.
Also reported: the direct route (X' = +-X among the first two stage-1 LLL vectors), which needs
an unproved anti-concentration of alpha (report C2, remark) and is NOT part of the theorem.
Finite simulation only falsifies.
Control row: same data, decoder given an unrelated uniform alpha'; expected to fail.
(Giving the decoder -alpha is not a control: it maps the solution X3 to -X3, direction unchanged.)
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python decode_sim.py [trials] [seed] [bmin] [bmax]
"""
import math, random, sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import *

def iota(v, t, s): return (t * v[0], t * v[1], s + C2(t) * v[0] * v[1])

def sample_period(rng, g, Qm):
    """Shor: coset {j0 + gZ} in [0,Qm) (start uniform point), QFT_Qm outcome (exact law)."""
    j0 = rng.randrange(Qm)
    L = len(range(j0 % g, Qm, g))
    gp = math.gcd(g, Qm); Np = Qm // gp
    jj = fejer_sample(rng, L, Np, 0, 1)
    _, s, _ = egcd(g, Qm)                          # s*g = gp mod Qm
    z = rng.randrange(gp) * Np                     # kernel {z : z g = 0 mod Qm} = Np Z_Qm
    return (jj * s + z) % Qm

def sampler_selftest(rng, out):
    """Empirical vs exact P* at a small box (checks fejer_sample / sample_ideal)."""
    Mb, N0 = 64, 1 << 20
    for w, X3, A in (((3, -2), 17, 12345), ((4, 6), -5, 777), ((0, 5), 9, 0), ((8, 4), 3, 99991)):
        exact = {}
        lines = {}
        for u1 in range(Mb):
            for u2 in range(Mb):
                t = 0
                while 0 <= u1 - (t + 1) * w[0] < Mb and 0 <= u2 - (t + 1) * w[1] < Mb: t += 1
                lines.setdefault((u1 - t * w[0], u2 - t * w[1]), []).append(t)
        from collections import Counter
        cntL = Counter(len(ts) for ts in lines.values())
        for y1 in range(Mb):
            for y2 in range(Mb):
                z = ((y1 * w[0] + y2 * w[1]) / Mb + A * X3 / N0) % 1.0
                sz = math.sin(math.pi * z)
                exact[(y1, y2)] = sum(c * (L * L if abs(sz) < 1e-12 else math.sin(math.pi * L * z) ** 2 / sz ** 2)
                                      for L, c in cntL.items()) / Mb ** 4
        S = 40000; emp = {}
        for _ in range(S):
            y = sample_ideal(rng, w, X3, A, N0, Mb); emp[y] = emp.get(y, 0) + 1
        tv = 0.5 * sum(abs(emp.get(y, 0) / S - p) for y, p in exact.items())
        # expected TV of an empirical distribution with S samples ~ sum sqrt(p(1-p)/S)/sqrt(2 pi)*... ; report a
        # same-size empirical draw from the exact law as the null
        ys = list(exact); ps = [exact[y] for y in ys]
        draw = rng.choices(ys, weights=ps, k=S); emp2 = {}
        for y in draw: emp2[y] = emp2.get(y, 0) + 1
        tv0 = 0.5 * sum(abs(emp2.get(y, 0) / S - p) for y, p in exact.items())
        out.append(f'  sampler self-test w={w} X3={X3} A={A}: TV(empirical, exact) = {tv:.4f}; null TV (exact draw) = {tv0:.4f}')

def trial(rng, b, p, out_stats, control=False):
    a_ = 0; b_ = 0
    while a_ == 0 and b_ == 0:
        a_, b_ = rng.randrange(-(1 << b) + 1, 1 << b), rng.randrange(-(1 << b) + 1, 1 << b)
    cbits = b if rng.random() < 0.5 else 2 * b
    c_ = rng.randrange(-(1 << cbits) + 1, 1 << cbits)
    h = (a_, b_, c_); w = (a_, b_); X3 = 2 * c_ - a_ * b_
    vtrue = prim(w)
    N0, Mb, K = p['N0'], p['Mb'], p['K']
    gam1 = Fraction(1, 1 << (-p['log_gamma1']))
    res = {'first': False, 'any': False, 'direct': False, 'sda_tries': 0, 'samples': 0, 'bad_strip': 0,
           'dir_ok': 0, 'batches': 0, 'dir_first': False}
    for batch in range(3):
        res['batches'] += 1
        samples = []
        for _ in range(p['m1']):
            while True:
                res['sda_tries'] += 1
                rho = [rng.randrange(N0), rng.randrange(N0)]
                r = sda_iso_full(rho, N0, p['logeps'], p['Q'])
                if r[0] is not None: break
            mu = r[:2]
            assert theta_dist(rho, mu, N0) <= Fraction(1, 1 << K)
            assert mu[0] ** 2 + mu[1] ** 2 <= p['mu_max'] ** 2
            A = sum(rr * C2(m) for rr, m in zip(rho, mu)) % N0
            y = sample_ideal(rng, w, X3, A, N0, Mb)
            zeta = (Fraction(y[0] * w[0] + y[1] * w[1], Mb) + Fraction(A * X3, N0)) % 1
            if min(zeta, 1 - zeta) > gam1: res['bad_strip'] += 1
            res['samples'] += 1
            samples.append((y, rng.randrange(N0) if control else A))   # control: decoder gets an unrelated uniform alpha
        v, Xs = decode_stage1(samples, b, N0, Mb, p['log_gamma1'])
        if any(X is not None and (X == (a_, b_, X3) or X == (-a_, -b_, -X3)) for X in Xs): res['direct'] = res['direct'] or batch == 0
        right = v is not None and (v == vtrue or v == tuple(-x for x in vtrue))
        res['dir_ok'] += right
        if batch == 0: res['dir_first'] = right
        if v is None: continue
        # ---- stage 2 in A_v
        FA = p['FA']
        if right:
            d = a_ // v[0] if v[0] else b_ // v[1]
            s0 = c_ - C2(d) * v[0] * v[1]
            assert iota(v, d, s0) == h and abs(s0) < (1 << (2 * b + 2))
            ell = (d, s0)
            ys = [sample_ideal(rng, ell, 0, 0, 1, FA) for _ in range(p['m2'])]
        else:
            ys = [(rng.randrange(FA), rng.randrange(FA)) for _ in range(p['m2'])]
        lh = decode_stage2(ys, [1 << b, 1 << (2 * b + 2)], FA, p['log_gamma2'])
        if lh is None: continue
        # ---- period finding along l^ (membership oracle only)
        Qm = 1 << p['logQpf']
        member = lambda j: in_H(iota(v, j * lh[0], j * lh[1]), h)
        gtrue = None
        if right and (lh[0] * ell[1] - lh[1] * ell[0]) == 0:
            gtrue = abs(ell[0] // lh[0]) if lh[0] else abs(ell[1] // lh[1])
        dens = set()
        for _ in range(12):
            yv = sample_period(rng, gtrue, Qm) if gtrue else rng.randrange(Qm)
            dens.update(r for r in contfrac_denoms(yv, Qm, 1 << b) if r > 0)
        cands = set(dens) | {x * y // math.gcd(x, y) for x in dens for y in dens}
        acc = [r for r in cands if r < (1 << (2 * b + 2)) and member(r)]
        if not acc: continue
        gh = 0
        for r in acc: gh = math.gcd(gh, r)
        for pr in factorint(gh):
            while gh % pr == 0 and member(gh // pr): gh //= pr
        hout = iota(v, gh * lh[0], gh * lh[1])
        assert in_H(hout, h)                     # verified output is always in H
        if hout == h or hout == inv(h):
            res['any'] = True
            if batch == 0: res['first'] = True
            break
    out_stats.append(res)

def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    bmin = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    bmax = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    rng = random.Random(seed)
    lines = []
    sampler_selftest(rng, lines); print('\n'.join(lines), flush=True)
    print('| b | log2 Mb | K | log2 N0 | trials | h recovered, 1st batch | h recovered, <=3 batches | direction ok / batches | '
          'SDA tries per sample | off-strip samples (bound 2^-7+2^-14 = 0.0079) | direct X decode, 1st batch (heuristic route) | s/trial |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|', flush=True)
    for b in range(bmin, bmax + 1):
        p = params(b); st = []; t0 = time.time()
        for _ in range(trials): trial(rng, b, p, st)
        nb = sum(s['batches'] for s in st)
        print(f"| {b} | {p['logMb']} | {p['K']} | {p['n0']} | {trials} | {sum(s['first'] for s in st)}/{trials} | "
              f"{sum(s['any'] for s in st)}/{trials} | {sum(s['dir_ok'] for s in st)}/{nb} | "
              f"{sum(s['sda_tries'] for s in st)/sum(s['samples'] for s in st):.3f} | "
              f"{sum(s['bad_strip'] for s in st)}/{sum(s['samples'] for s in st)} | {sum(s['direct'] for s in st)}/{trials} | "
              f"{(time.time()-t0)/trials:.2f} |", flush=True)
    # negative control: decoder fed an unrelated uniform alpha' (note -alpha would NOT be a control: it is X3 -> -X3)
    b = bmax; p = params(b); st = []
    for _ in range(trials // 2): trial(rng, b, p, st, control=True)
    nb = sum(s['batches'] for s in st)
    print(f"| control (decoder given unrelated uniform alpha), b={b} | | | | {trials//2} | {sum(s['first'] for s in st)}/{trials//2} | "
          f"{sum(s['any'] for s in st)}/{trials//2} | {sum(s['dir_ok'] for s in st)}/{nb} | | | {sum(s['direct'] for s in st)}/{trials//2} | |")

if __name__ == '__main__':
    main()
