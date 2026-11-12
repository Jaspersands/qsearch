"""Exact check of Lemma 2.3: for u' = u + t w, delta_mu(sigma(u')) delta_mu(sigma(u))^-1 = h^{mu t} z^{sigma}
with sigma = -mu^2 S(u,t) + C(mu,2) t (2c-ab), S(u,t) = t a u2 + C(t,2) ab + t c.  Random integers; finite check.
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python sigma_identity_check.py"""
import random, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import mul, inv, pw, C2
rng = random.Random(3); bad = 0; n = 0
for _ in range(200000):
    a, b, c = rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6), rng.randint(-10**12, 10**12)
    if a == 0 and b == 0: continue
    h = (a, b, c); mu = rng.randint(-10**9, 10**9); t = rng.randint(-10**6, 10**6)
    u = (rng.randint(-10**8, 10**8), rng.randint(-10**8, 10**8)); up = (u[0] + t * a, u[1] + t * b)
    d = lambda g: (mu * g[0], mu * g[1], mu * mu * g[2])
    k = mul(d((up[0], up[1], 0)), inv(d((u[0], u[1], 0))))
    S = t * a * u[1] + C2(t) * a * b + t * c
    sig = -mu * mu * S + C2(mu) * t * (2 * c - a * b)
    n += 1; bad += (k != mul(pw(h, mu * t), (0, 0, sig)))
print(f'{n} random cases, {bad} mismatches')

# symbolic identity (polynomial in a,b,c,mu,t,u1,u2; C(n,2) = n(n-1)/2)
import sympy as sp
a, b, c, mu, t, u1, u2 = sp.symbols('a b c mu t u1 u2')
C = lambda n: n * (n - 1) / 2
M = lambda g, h: (g[0] + h[0], g[1] + h[1], g[2] + h[2] + g[0] * h[1])
I = lambda g: (-g[0], -g[1], -g[2] + g[0] * g[1])
P = lambda g, n: (n * g[0], n * g[1], n * g[2] + C(n) * g[0] * g[1])
d = lambda g: (mu * g[0], mu * g[1], mu ** 2 * g[2])
k = M(d((u1 + t * a, u2 + t * b, 0)), I(d((u1, u2, 0))))
S = t * a * u2 + C(t) * a * b + t * c
sig = -mu ** 2 * S + C(mu) * t * (2 * c - a * b)
rhs = M(P((a, b, c), mu * t), (0, 0, sig))
print('symbolic differences:', [sp.expand(k[i] - rhs[i]) for i in range(3)])
