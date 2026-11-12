"""Finite simulation (no quantum hardware; exact linear algebra) of the last step for
H = <h>, H cap Z = 1: Fourier sampling over the box [0,M)^2 of
u -> Psi(u) = (x)_i psi_{theta_i}(a_i).sigma(u),  sigma(u) = (p,q,0).
Gram entries use the formula checked in twist_check.py Part B:
<psi.x|psi.x'> = e^{2 pi i theta sigma}(1-|sigma|/N) if x'x^{-1} = h^tau z^sigma, else 0.
Reports the mass of the Fourier distribution on {y : ||<y,w>/M|| <= 0.1}
(uniform baseline ~ 0.2) for Theta = sum theta_i ~ 0, Theta random, and a single factor.
Usage: nice -n 19 /opt/anaconda3/bin/python e2e_fourier.py
"""
import cmath, math, random, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h3z_struct import mul, inv
from twist_check import decomp

def gram_factor(theta, h, M, N):
    pts = [(p, q) for p in range(M) for q in range(M)]
    G = np.zeros((M*M, M*M), complex)
    for i, u in enumerate(pts):
        x = (u[0], u[1], 0)
        for j, v in enumerate(pts):
            xp = (v[0], v[1], 0)
            d = decomp(mul(xp, inv(x)), h)
            if d is None: continue
            sig = d[1]
            G[i, j] = cmath.exp(2j*math.pi*theta*sig) * max(0.0, 1 - abs(sig)/N)
    return G, pts

def run(h, M, thetas, N=10**9):
    G = np.ones((M*M, M*M), complex)
    for th in thetas:
        Gi, pts = gram_factor(th, h, M, N); G = G * Gi
    F = np.array([[cmath.exp(2j*math.pi*(y1*p + y2*q)/M) for (p, q) in pts]
                  for y1 in range(M) for y2 in range(M)]) / (M*M)
    # P(y) = sum_{u,u'} F[y,u] conj(F[y,u']) <Psi(u')|Psi(u)>, G[i,j] = <Psi(u_i)|Psi(u_j)>
    P = np.real(np.einsum('yu,yv,vu->y', F, F.conj(), G))
    w = (h[0], h[1]); good = 0.0
    for idx, (y1, y2) in enumerate((a, b) for a in range(M) for b in range(M)):
        val = ((y1*w[0] + y2*w[1]) / M) % 1
        if min(val, 1 - val) <= 0.1: good += P[idx]
    return P.sum(), good

if __name__ == '__main__':
    rng = random.Random(3)
    h, M = (2, 3, 5), 18
    th1 = rng.random()
    cases = [('single factor (Theta = theta_1 random)', [th1]),
             ('two factors, Theta = 1e-6', [th1, (1 - th1 + 1e-6) % 1]),
             ('two factors, Theta = 0.37', [th1, (0.37 - th1) % 1]),
             ('three factors, Theta = 2e-6', [th1, 0.25, (1 - th1 - 0.25 + 2e-6) % 1])]
    print(f'h={h}, box M={M}; baseline mass for uniform y on the window: ', end='')
    w = h[:2]
    base = sum(1 for a in range(M) for b in range(M)
               if min(((a*w[0]+b*w[1])/M) % 1, 1-((a*w[0]+b*w[1])/M) % 1) <= 0.1) / M**2
    print(round(base, 3))
    for name, ths in cases:
        tot, good = run(h, M, ths)
        print(f'  {name:42s} total={tot:.4f}  mass(||<y,w>/M||<=0.1)={good:.3f}')
