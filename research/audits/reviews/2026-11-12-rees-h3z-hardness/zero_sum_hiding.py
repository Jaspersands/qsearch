"""Zero-sum tensor of twisted coset states as a hiding procedure for HZ (H = <h>, H cap Z = 1).

Run: nice -n 19 /opt/anaconda3/bin/python zero_sum_hiding.py
Finite check only (TRAPS 7): it checks the closed form and shows the effect on
Fourier sampling over G/Z = Z^2 at toy sizes; it proves nothing asymptotically.

Copy i: |chi_i> = (JW)^{-1/2} sum_{0<=j<J, 0<=t<W} e(-k_i t / W) |a_i h^j z^t>,
measured central frequency k_i/W.  Hiding procedure: g -> (x)_i |chi_i . g>.
Section sigma(u) = x^{u1} y^{u2}.  Gram Gamma(u,u') = prod_i <chi_i sigma(u') | chi_i sigma(u)>,
computed by brute force from the supports and compared with the closed form
  (1-|m|/J)(1-|s|/W) e(k_i s / W)   if sigma(u) sigma(u')^{-1} = h^m z^s, else 0.
Fourier sampling over Z_B^2: p(xi) = B^{-4} sum_{u,u'} Gamma(u,u') e(xi.(u-u')/B).
We print the mass of p on the dual line {xi : xi . v = 0 mod B}.
"""
import cmath, random
import numpy as np

def mul(g, h):
    return (g[0] + h[0], g[1] + h[1], g[2] + h[2] + g[0] * h[1])

def inv(g):
    return (-g[0], -g[1], g[0] * g[1] - g[2])

def power(g, m):
    a, b, c = g
    return (m * a, m * b, m * c + (m * (m - 1) // 2) * a * b)

def e(x):
    return cmath.exp(2j * cmath.pi * x)

def state(a0, h, J, W, k):
    st = {}
    for j in range(J):
        hj = mul(a0, power(h, j))
        for t in range(W):
            st[mul(hj, (0, 0, t))] = e(-k * t / W) / (J * W) ** 0.5
    return st

def act(st, g):
    return {mul(x, g): amp for x, amp in st.items()}

def ip(s1, s2):
    # <s1|s2>
    if len(s1) > len(s2):
        return sum(amp.conjugate() * s1[x] for x, amp in s2.items() if x in s1).conjugate()
    return sum(amp.conjugate() * s2[x] for x, amp in s1.items() if x in s2)

def sigma(u):
    return (u[0], u[1], u[0] * u[1])

def closed_form(u, w, h, J, W, k):
    d = mul(sigma(u), inv(sigma(w)))
    v1, v2 = h[0], h[1]
    if v1 != 0:
        if d[0] % v1: return 0
        m = d[0] // v1
    else:
        if d[1] % v2: return 0
        m = d[1] // v2
    if (m * v1, m * v2) != (d[0], d[1]): return 0
    s = mul(d, inv(power(h, m)))[2]
    if abs(m) >= J or abs(s) >= W: return 0
    return (1 - abs(m) / J) * (1 - abs(s) / W) * e(k * s / W)

def gram(points, h, J, W, ks, a0s, brute):
    n = len(points)
    G = np.ones((n, n), dtype=complex)
    for k, a0 in zip(ks, a0s):
        base = state(a0, h, J, W, k) if brute else None
        acted = [act(base, sigma(u)) for u in points] if brute else None
        for i in range(n):
            for jj in range(n):
                if brute:
                    val = ip(acted[jj], acted[i])
                else:
                    val = closed_form(points[i], points[jj], h, J, W, k)
                G[i, jj] *= val
    return G

def dual_line_mass(G, points, B, v):
    n = len(points)
    U = np.array(points)
    mass = 0.0; total = 0.0
    for x1 in range(B):
        for x2 in range(B):
            ph = np.exp(2j * np.pi * (U @ np.array([x1, x2])) / B)
            p = np.real(ph.conj() @ G @ ph) / n ** 2
            total += p
            if (x1 * v[0] + x2 * v[1]) % B == 0:
                mass += p
    return mass, total

if __name__ == "__main__":
    rng = random.Random(7)
    h = (1, 2, 3)            # v = (1, 2), primitive
    B = 8
    points = [(a, b) for a in range(B) for b in range(B)]
    # closed form vs brute force, small sizes
    J, W = 20, 300
    ks = [37, W - 37]; a0s = [(5, -3, 11), (-2, 7, 4)]
    Gb = gram(points[:16], h, J, W, ks, a0s, brute=True)
    Gc = gram(points[:16], h, J, W, ks, a0s, brute=False)
    print(f"closed form vs brute force (16 points, 2 copies): max |diff| = {np.abs(Gb - Gc).max():.2e}")
    # Fourier sampling over Z_B^2 with the closed form, larger windows
    J, W = 400, 4000
    line_frac = sum(1 for x1 in range(B) for x2 in range(B) if (x1 * h[0] + x2 * h[1]) % B == 0) / B ** 2
    print(f"\nv = {h[:2]}, B = {B}, J = {J}, W = {W}; dual line is {line_frac:.3f} of Z_B^2 (uniform baseline)")
    cases = [("ideal HZ-hiding (theta = 0)", [0]),
             ("zero-sum pair k1 + k2 = 0 mod W", [1234, W - 1234]),
             ("zero-sum triple", [1000, 1500, W - 2500]),
             ("single copy, k = 1234", [1234]),
             ("non-zero-sum pair (sum 1)", [1234, W - 1233]),
             ("non-zero-sum pair (sum 400)", [1234, W - 834])]
    for name, ks in cases:
        G = gram(points, h, J, W, ks, [None] * len(ks), brute=False)
        m, tot = dual_line_mass(G, points, B, h)
        print(f"{name:<34}: dual-line mass {m:.3f} (total {tot:.3f})")
    G = np.eye(len(points))
    m, tot = dual_line_mass(G, points, B, h)
    print(f"{'H = 1 control (identity Gram)':<34}: dual-line mass {m:.3f} (total {tot:.3f})")
