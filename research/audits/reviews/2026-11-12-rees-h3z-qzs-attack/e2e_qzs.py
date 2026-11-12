"""Falsification check of the template step with QZS solutions from qzs_lattice.sda_iso.
Simulates (exact Gram matrices, no hardware) Fourier sampling over the box [0,Mb)^2 of
u -> Psi(u) = psi_{theta_1}.delta_{mu_1}(sigma(u)) (x) psi_{theta_2}.delta_{mu_2}(sigma(u)),
sigma(u) = (u1,u2,0), delta_mu(p,q,r) = (mu p, mu q, mu^2 r), theta_i = rho_i/M exact.
Per-factor Gram law (twist_check.py Part B): <psi.x|psi.x'> = e(theta*sigma) if
x' x^-1 = h^tau z^sigma, else 0. Truncation windows are set to infinity (T, N >> mu-scales).
Reports the largest Fourier mass on an affine strip {|| <y,w>/Mb - beta || <= 0.1}
(max over beta in a grid), and the mass on the exact line beta = 0, for:
QZS solution, random mu of the same size, and the ideal (theta_2 = -theta_1, mu = (1,1)).
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python e2e_qzs.py
"""
import math, random, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
sys.path.insert(0, __file__.rsplit('/', 1)[0].replace('qzs-attack', 'infinite-index'))
from h3z_struct import mul, inv
from twist_check import decomp
from qzs_lattice import sda_iso

def delta(mu, g): return (mu * g[0], mu * g[1], mu * mu * g[2])

def gram(rho, M, mu, h, Mb):
    pts = [(p, q) for p in range(Mb) for q in range(Mb)]
    G = np.zeros((len(pts), len(pts)), complex)
    for i, u in enumerate(pts):
        x = delta(mu, (u[0], u[1], 0))
        for j, v in enumerate(pts):
            d = decomp(mul(delta(mu, (v[0], v[1], 0)), inv(x)), h)
            if d is None: continue
            ph = (rho * d[1]) % M                     # theta*sigma mod 1, exact
            G[i, j] = np.exp(2j * math.pi * ph / M)
    return G, pts

def strip_mass(P, pts, w, Mb, pred=None):
    vals = np.array([((y1 * w[0] + y2 * w[1]) / Mb) % 1 for (y1, y2) in pts])
    if pred is not None:
        out = []
        for beta in pred:
            dd = np.abs(((vals - beta) + 0.5) % 1 - 0.5); out.append(P[dd <= 0.1].sum())
        return out
    best = 0.0; at0 = None
    for beta in np.arange(0, 1, 0.01):
        dd = np.abs(((vals - beta) + 0.5) % 1 - 0.5)
        m = P[dd <= 0.1].sum()
        if at0 is None: at0 = m
        best = max(best, m)
    return best, at0

def run(rhos, M, mus, h, Mb, pred=None):
    G = None
    for rho, mu in zip(rhos, mus):
        Gi, pts = gram(rho, M, mu, h, Mb); G = Gi if G is None else G * Gi
    F = np.array([[np.exp(2j * math.pi * (y1 * p + y2 * q) / Mb) for (p, q) in pts]
                  for (y1, y2) in pts]) / len(pts)
    P = np.real(np.einsum('yu,yv,vu->y', F, F.conj(), G))
    if pred is not None: return P.sum(), strip_mass(P, pts, h[:2], Mb), strip_mass(P, pts, h[:2], Mb, pred)
    return P.sum(), strip_mass(P, pts, h[:2], Mb)

if __name__ == '__main__':
    rng = random.Random(5); Mb = 16; K = 24
    m = 3 * (K + 6) + 40; M = 1 << m
    base_pts = [(a, b) for a in range(Mb) for b in range(Mb)]
    for h in [(2, 3, 5), (1, -2, 7), (3, 1, -4)]:
        vals = np.array([((a * h[0] + b * h[1]) / Mb) % 1 for (a, b) in base_pts])
        base = np.mean(np.abs((vals + 0.5) % 1 - 0.5) <= 0.1)
        while True:
            rhos = [rng.randrange(M), rng.randrange(M)]
            res = sda_iso(rhos, M, K)
            if res[0] != 'fail': break
        mu = res[:2]
        Th = ((rhos[0] * mu[0] ** 2 + rhos[1] * mu[1] ** 2) % M) / M
        Th = min(Th, 1 - Th)
        rmu = [rng.randrange(1, 2 * abs(mu[0]) + 2), rng.randrange(1, 2 * abs(mu[1]) + 2)]
        cases = [('QZS mu (log2|Theta|=%.1f, log2|mu|=%.1f)' % (math.log2(Th), math.log2(max(map(abs, mu)))), rhos, mu),
                 ('random mu same size', rhos, rmu),
                 ('ideal: theta2=-theta1, mu=(1,1)', [rhos[0], (-rhos[0]) % M], (1, 1)),
                 ('single factor, mu=1', [rhos[0]], (1,))]
        print(f'h={h}, Mb={Mb}, K={K}; uniform strip mass {base:.3f}')
        # predicted offset: beta = A c' with A = sum theta_i (mu_i^2 - mu_i), c' = c - ab/2
        # exact: (mu^2-mu) c' = (mu^2-mu)/2 * (2c - ab) is an integer
        Ac = sum(r * ((u * u - u) // 2) * (2 * h[2] - h[0] * h[1]) for r, u in zip(rhos, mu)) % M / M
        pred = [Ac, (-Ac) % 1]
        tot, (best, at0), (pp, pm) = run(rhos, M, mu, h, Mb, pred)
        print(f'  predicted strip beta=+A c\' : mass {pp:.3f};  beta=-A c\' : mass {pm:.3f}  (best {best:.3f})')
        for name, rr, mm in cases:
            tot, (best, at0) = run(rr, M, mm, h, Mb)
            print(f'  {name:48s} total={tot:.4f} best-strip={best:.3f} beta0-strip={at0:.3f}')
        sys.stdout.flush()
