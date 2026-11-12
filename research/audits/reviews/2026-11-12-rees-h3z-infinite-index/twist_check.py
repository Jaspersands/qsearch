"""Checks of the central-character twist mechanism in H_3(Z) for a hidden
H = <h>, H cap Z = 1.  Convention: f(gk) = f(g) for k in H (left cosets gH).
psi_theta(a) = sum_{r<N} e^{-2 pi i theta r} |a z^r H>,  psi.x = right translate by x.
If y = x' x^{-1} = h^tau z^sigma then psi.x' = e^{2 pi i theta sigma} psi.x (exactly, up to
the truncation of r).  Part A fits sigma for twist maps phi and checks the invariant
2*beta - alpha = mu^2 (mu = scalar induced on G/Z).  Part B builds truncated states
explicitly and checks phases/orthogonality and the binary zero-sum product.
Finite checks only.  Usage: nice -n 19 /opt/anaconda3/bin/python twist_check.py [seed]
"""
import random, sys, cmath, math
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h3z_struct import mul, inv, pw, ONE

def delta(m, g): return (m*g[0], m*g[1], m*m*g[2])          # endomorphism x->x^m, y->y^m
def Omega(g, w): return g[0]*w[1] - g[1]*w[0]

def decomp(y, h):
    """y = h^tau z^sigma ? return (tau, sigma) or None."""
    if h[0] != 0:
        if y[0] % h[0]: return None
        tau = y[0] // h[0]
    else:
        if y[1] % h[1]: return None
        tau = y[1] // h[1]
    r = mul(pw(h, -tau), y)
    if r[0] or r[1]: return None
    return tau, r[2]

MAPS = {
    'id':        (1, lambda g: g),
    'inv':       (-1, lambda g: inv(g)),
    'delta2':    (2, lambda g: delta(2, g)),
    'delta3':    (3, lambda g: delta(3, g)),
    'delta2^-1': (-2, lambda g: inv(delta(2, g))),
    'pow3':      (3, lambda g: pw(g, 3)),
    'pow-2':     (-2, lambda g: pw(g, -2)),
    'd1*d2':     (3, lambda g: mul(delta(1, g), delta(2, g))),
    'd2*d3^-1':  (-1, lambda g: mul(delta(2, g), inv(delta(3, g)))),
    'd3*pow2':   (5, lambda g: mul(delta(3, g), pw(g, 2))),
}

def partA(rng, out):
    out.append('Part A: sigma(g,k) for k = h^t z^s fitted as alpha*s + beta*t*Omega(g) + gamma*t')
    bad = 0
    for trial in range(40):
        while True:
            h = (rng.randint(-6, 6), rng.randint(-6, 6), rng.randint(-40, 40))
            if h[0] or h[1]: break
        w = (h[0], h[1])
        for name, (mu, phi) in MAPS.items():
            rows, rhs = [], []
            for _ in range(30):
                g = (rng.randint(-30, 30), rng.randint(-30, 30), rng.randint(-99, 99))
                t, s = rng.randint(-5, 5), rng.randint(-20, 20)
                k = mul(pw(h, t), (0, 0, s))
                x, xp = phi(g), phi(mul(g, k))
                d = decomp(mul(xp, inv(x)), h)
                if d is None: bad += 1; out.append(f'  NOT IN HZ: {name} h={h}'); continue
                rows.append([s, t*Omega(g, w), t]); rhs.append(d[1])
            A = np.array(rows, float); bvec = np.array(rhs, float)
            coef, *_ = np.linalg.lstsq(A, bvec, rcond=None)
            res = np.max(np.abs(A @ coef - bvec))
            al, be, ga = coef
            inv_ok = abs(2*be - al - mu*mu) < 1e-6
            if res > 1e-6 or not inv_ok:
                bad += 1
                out.append(f'  FAIL {name} h={h} coef={coef} res={res:.2e} mu^2={mu*mu}')
            if trial == 0:
                out.append(f'  h={h} {name:10s} mu={mu:3d} alpha={al:7.2f} beta={be:7.2f} '
                           f'gamma={ga:9.2f}  2beta-alpha={2*be-al:6.2f}  resid={res:.1e}')
    out.append(f'Part A failures: {bad} (40 random h x {len(MAPS)} maps x 30 (g,k))')

def coset_label(elt, h):
    """canonical element of the set elt*<h>... we need sets a z^r H x = {a z^r h^t x}."""
    raise NotImplementedError

def state(a, theta, N, x, h):
    """dict: label -> amplitude, for psi_theta(a).x ; label = canonical element of a z^r H x."""
    st = {}
    hx = mul(mul(inv(x), h), x)          # a z^r H x = (a z^r x) <x^-1 h x>
    for r in range(N):
        base = mul(mul(a, (0, 0, r)), x)
        # canonical: first coordinate (or second) reduced into [0,|hx_a|)
        if hx[0]:
            t = -(base[0] // hx[0]) if hx[0] > 0 else -((base[0]) // hx[0])
            t = (-base[0]) // hx[0] if False else None
            # find t with base[0] + t*hx[0] in [0, |hx[0]|)
            A = abs(hx[0]); q = (base[0] % A - base[0]) // hx[0]
            lab = mul(base, pw(hx, q))
            assert 0 <= lab[0] < A
        else:
            A = abs(hx[1]); q = (base[1] % A - base[1]) // hx[1]
            lab = mul(base, pw(hx, q)); assert 0 <= lab[1] < A
        st[lab] = st.get(lab, 0) + cmath.exp(-2j*math.pi*theta*r) / math.sqrt(N)
    return st

def ip(s1, s2): return sum(s1[k].conjugate()*s2.get(k, 0) for k in s1)

def partB(rng, out):
    out.append('Part B: explicit truncated states, N = 4000')
    N = 4000; worst_phase = 0; worst_orth = 0; worst_mag = 0; cnt = 0
    for trial in range(12):
        while True:
            h = (rng.randint(-4, 4), rng.randint(-4, 4), rng.randint(-20, 20))
            if h[0] or h[1]: break
        w = (h[0], h[1])
        a = (rng.randint(-50, 50), rng.randint(-50, 50), rng.randint(-500, 500))
        theta = rng.random()
        for _ in range(3):
            g = (rng.randint(-8, 8), rng.randint(-8, 8), rng.randint(-30, 30))
            t, s = rng.randint(-3, 3), rng.randint(-10, 10)
            k = mul(pw(h, t), (0, 0, s))
            s1, s2 = state(a, theta, N, g, h), state(a, theta, N, mul(g, k), h)
            tau, sig = decomp(mul(mul(g, k), inv(g)), h)
            pred = cmath.exp(2j*math.pi*theta*sig)
            v = ip(s1, s2)
            worst_mag = max(worst_mag, abs(abs(v) - (1 - abs(sig)/N)))
            worst_phase = max(worst_phase, abs(v/abs(v) - pred))
            # different HZ coset: perturb by x (not in HZ direction)
            gp = mul(g, (w[1] + 1 if w[0] == 0 else 0, 1 if w[0] != 0 else 0, 0))
            if Omega(gp, w) - Omega(g, w) != 0 or True:
                s3 = state(a, theta, N, gp, h)
                worst_orth = max(worst_orth, abs(ip(s1, s3)))
            cnt += 1
    out.append(f'  {cnt} pairs: max |phase - e^(2 pi i theta sigma)| = {worst_phase:.2e}; '
               f'max ||<.,.>| - (1-|sigma|/N)| = {worst_mag:.2e}; max overlap across cosets = {worst_orth:.2e}')
    # binary zero-sum product: theta_1 + theta_2 = 1 - 1e-7  vs random
    h = (2, 3, 7); w = (2, 3)
    a1 = (5, -7, 11); a2 = (-13, 4, 2)
    for label, th in (('Theta~0', None), ('Theta random', 0)):
        th1 = 0.3141592
        th2 = (1 - th1 + 1e-7) if th is None else 0.71828
        Theta = (th1 + th2) % 1
        maxdev = 0
        for _ in range(6):
            g = (rng.randint(-6, 6), rng.randint(-6, 6), rng.randint(-20, 20))
            t, s = rng.randint(-3, 3), rng.randint(-10, 10)
            k = mul(pw(h, t), (0, 0, s))
            v = ip(state(a1, th1, N, g, h), state(a1, th1, N, mul(g, k), h)) * \
                ip(state(a2, th2, N, g, h), state(a2, th2, N, mul(g, k), h))
            maxdev = max(maxdev, abs(v - 1))
        out.append(f'  product of 2 factors, {label} (Theta={Theta:.3e}): max |<Psi(g)|Psi(gk)> - 1| = {maxdev:.3e}')

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
    out = []
    partA(rng, out); partB(rng, out)
    print('\n'.join(out))
