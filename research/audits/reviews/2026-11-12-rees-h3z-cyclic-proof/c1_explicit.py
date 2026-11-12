"""C1 falsification check with EXPLICIT physical states (independent of the Part-B Gram law).

For each instance: random h, two independent chirp-line coset states
    psi_i(p_t, r) = e(theta_i c_t - theta_i r) / sqrt(|I| N),  t in I, r in [0,N),
where {g_i h^t : t in I} is the coset segment over the square [-P,P)^2 and c_t its central
coordinate; theta_i = rho_i/N0.  Gram entries <R_x psi | R_x' psi> = sum_y conj psi(y) psi(y x x'^-1)
are computed from the group law only: explicit sum over t (lookup of the translated point), exact
closed-form sum over r (both windows carry the same character, so the r-sum is a count times a
phase).  Phases are exact mod N0.  mu = (mu1,mu2) with small ||theta1 mu1^2 + theta2 mu2^2|| found by
brute force.  Then the Fourier law P(y) on Z_Mb^2 of u -> Psi(u) = (x)_i R_{delta_mu_i(u,0)} psi_i is
compared with the ideal law P*(y) = Mb^-4 sum_lines F_L(<y,w>/Mb + alpha X3) of the report (C1):
reports TV(P,P*), ||Phi - Phi*|| (must be >= TV), the report's analytic bound on ||Phi-Phi*||^2
(must be >= the explicit value), cross-line orthogonality, and strip masses.
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python c1_explicit.py [instances] [seed]
"""
import math, random, sys, cmath
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import mul, inv, pw, C2

def coset_segment(g, h, P):
    """t-interval I with pi(g h^t) in [-P,P)^2 (I is an interval: convex set cut by a line)."""
    lo, hi = -10 ** 9, 10 ** 9
    for gi, wi in ((g[0], h[0]), (g[1], h[1])):
        if wi == 0: continue
        if wi > 0: l, u = -((gi + P) // wi), (P - 1 - gi) // wi
        else: l, u = -((P - 1 - gi) // (-wi)), (gi + P) // (-wi)
        lo, hi = max(lo, l), min(hi, u)
    ts = np.arange(lo, hi + 1, dtype=object)
    pts = [mul(g, pw(h, int(t))) for t in ts]
    return pts

def gram_factor(pts, rho, N0, N, mu, h, us):
    """G[u,u'] = <R_{x(u)} psi | R_{x(u')} psi>, x(u) = (mu u1, mu u2, 0)."""
    w = (h[0], h[1]); L = len(pts)
    p0 = pts[0]
    P1 = np.array([p[0] for p in pts], dtype=np.int64); P2 = np.array([p[1] for p in pts], dtype=np.int64)
    Cc = [p[2] for p in pts]
    n = len(us); G = np.zeros((n, n), complex)
    for i, u in enumerate(us):
        x = (mu * u[0], mu * u[1], 0)
        for j, u2 in enumerate(us):
            xp = (mu * u2[0], mu * u2[1], 0)
            kap = mul(x, inv(xp))                       # y -> y kap  (kap = x x'^-1)
            # translated point of p_t: p_t + pi(kap); look it up on the line p_0 + t w
            if w[0]:
                if kap[0] % w[0]: continue
                dt = kap[0] // w[0]
            else:
                if kap[1] % w[1]: continue
                dt = kap[1] // w[1]
            if (dt * w[0], dt * w[1]) != (kap[0], kap[1]): continue
            acc = 0j
            for t in range(max(0, -dt), min(L, L - dt)):
                p = pts[t]; q = pts[t + dt]
                assert (p[0] + kap[0], p[1] + kap[1]) == (q[0], q[1])
                shift = kap[2] + p[0] * kap[1]          # central coord of (p, r) kap = r + shift
                cnt = N - abs(shift)
                if cnt <= 0: continue
                ph = (rho * (q[2] - p[2] - shift)) % N0
                acc += cnt * cmath.exp(2j * math.pi * ph / N0)
            G[i, j] = acc / (L * N)
    return G

def run(rng, Mb, P, N, N0, mu_range, Kbits, out):
    while True:
        h = (rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-12, 12))
        if h[0] or h[1]: break
    w = (h[0], h[1]); X3 = 2 * h[2] - h[0] * h[1]
    # theta pair and small-||Theta|| mu by brute force (gcd(mu1,mu2)=1, both nonzero)
    R = np.arange(-mu_range, mu_range + 1, dtype=object)
    while True:
        rho = [rng.randrange(N0), rng.randrange(N0)]
        best = None
        for m1 in range(1, mu_range + 1):
            for m2 in range(-mu_range, mu_range + 1):
                if m2 == 0 or math.gcd(m1, m2) != 1: continue
                v = (rho[0] * m1 * m1 + rho[1] * m2 * m2) % N0
                d = min(v, N0 - v)
                if d * (1 << Kbits) <= N0 and (best is None or d < best[0]): best = (d, m1, m2)
        if best: break
    d, m1, m2 = best; mus = (m1, m2)
    Thp = ((rho[0] * m1 * m1 + rho[1] * m2 * m2) % N0); Thp = Thp / N0 if Thp <= N0 // 2 else Thp / N0 - 1
    A = sum(r * C2(m) for r, m in zip(rho, mus)) % N0          # alpha = A/N0
    us = [(u1, u2) for u1 in range(Mb) for u2 in range(Mb)]
    Gs, segs = [], []
    for i in range(2):
        g = (rng.randint(-P // 2, P // 2), rng.randint(-P // 2, P // 2), rng.randint(-10 ** 6, 10 ** 6))
        pts = coset_segment(g, h, P); segs.append(len(pts))
        Gs.append(gram_factor(pts, rho[i], N0, N, mus[i], h, us))
    G = Gs[0] * Gs[1]
    n = len(us)
    F = np.array([[cmath.exp(2j * math.pi * (y[0] * u[0] + y[1] * u[1]) / Mb) for y in us] for u in us])  # F[u,y]
    Pact = np.real(np.einsum('uy,uv,vy->y', F.conj(), G, F)) / Mb ** 4
    # ideal law
    idx = {u: i for i, u in enumerate(us)}
    def on_line(u, v):
        dd = (v[0] - u[0], v[1] - u[1])
        if w[0]:
            if dd[0] % w[0]: return None
            t = dd[0] // w[0]
        else:
            if dd[1] % w[1]: return None
            t = dd[1] // w[1]
        return t if (t * w[0], t * w[1]) == dd else None
    base = {}
    for u in us:
        t = 0
        while 0 <= u[0] - (t + 1) * w[0] < Mb and 0 <= u[1] - (t + 1) * w[1] < Mb: t += 1
        base[u] = ((u[0] - t * w[0], u[1] - t * w[1]), t)
    lines = {}
    for u in us: lines.setdefault(base[u][0], []).append(base[u][1])
    Pid = np.zeros(n)
    for yi, y in enumerate(us):
        z = (y[0] * w[0] + y[1] * w[1]) / Mb + A * X3 / N0
        for r, ts in lines.items():
            Pid[yi] += abs(sum(cmath.exp(2j * math.pi * t * z) for t in ts)) ** 2
    Pid /= Mb ** 4
    TV = 0.5 * np.abs(Pact - Pid).sum()
    # ||Phi - Phi*||^2 and analytic bound
    dist2 = 0.0; bound2 = 0.0; orth = 0.0
    S_of = lambda r, t: t * h[0] * r[1] + C2(t) * h[0] * h[1] + t * h[2]
    for u in us:
        r, t = base[u]
        Gu = G[idx[r], idx[u]]
        dist2 += 2 - 2 * (cmath.exp(-2j * math.pi * ((A * t * X3) % N0) / N0) * Gu).real
        tr = sum(1 - abs(Gs[i][idx[r], idx[u]]) for i in range(2))
        bound2 += 2 * tr + 4 * math.pi ** 2 * (Thp * S_of(r, t)) ** 2
    for i, u in enumerate(us):
        for j, v in enumerate(us):
            if on_line(u, v) is None: orth = max(orth, abs(G[i, j]))
    dist2 /= n; bound2 /= n
    zeta = np.array([((y[0] * w[0] + y[1] * w[1]) / Mb + A * X3 / N0) % 1 for y in us])
    zz = np.minimum(zeta, 1 - zeta)
    gam = 1 / 8
    out.append(f'| {h} | {mus} | {math.log2(abs(Thp)):.1f} | {segs} | {N:.0e} | {Pact.sum():.6f} | {TV:.4f} | '
               f'{math.sqrt(max(dist2,0)):.4f} | {math.sqrt(bound2):.4f} | {orth:.1e} | {Pact[zz<=gam].sum():.3f} | {Pid[zz<=gam].sum():.3f} |')
    return TV <= math.sqrt(max(dist2, 0)) + 1e-9 and dist2 <= bound2 + 1e-9 and orth < 1e-12

if __name__ == '__main__':
    inst = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 11)
    out = ['| h | mu | log2 |Theta\'| | |I_1|,|I_2| | N | sum P | TV(P,P*) | ||Phi-Phi*|| | analytic bound | max cross-line |G| | P(strip 1/8) | P*(strip 1/8) |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|']
    ok = True
    for k in range(inst):
        N = 10 ** 9 if k % 3 else 10 ** 6
        P = 3000 if k % 2 == 0 else 600
        ok &= run(rng, Mb=8, P=P, N=N, N0=1 << 24, mu_range=40, Kbits=14, out=out)
        print(out[-1] if k else '\n'.join(out), flush=True)
    # scaling rows: longer coset segments and wider windows (truncation term shrinks; phase term stays)
    for k in range(2):
        ok &= run(rng, Mb=8, P=30000, N=10 ** 12, N0=1 << 24, mu_range=40, Kbits=14, out=out)
        print(out[-1], flush=True)
    print('ALL INEQUALITIES HOLD' if ok else 'VIOLATION FOUND')
