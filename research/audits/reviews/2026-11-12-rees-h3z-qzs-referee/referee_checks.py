"""Independent referee checks for 2026-11-12-rees-h3z-qzs-attack.md (SDA-ISO / QZS).
Finite checks only: they can falsify, never prove (TRAPS 7).

Part 1  Rigorous-variant SDA-ISO: full Fincke-Pohst enumeration of ALL hits q in [Q/2, Q]
        (|q th_i - c_i| <= eps), Q = C eps^-2 ln(eps^-2), M = 2^(4K+40) (Lemma P' needs
        M >> Q/eps^2).  Reports mean #hits vs the predicted 2 eps^2 Q, P(some good prime)
        vs the Chung-Erdos bound S1/(1+4 S1) and the Poisson guess 1-exp(-S1), and the
        composite-q variant (partial factoring + Tonelli/Hensel/CRT).  Every output is
        verified with exact integers: 3(mu1^2+mu2^2)^2 <= 4 q^2, ||Theta|| * q <=
        |e1| mu1^2 + |e2| mu2^2 (exact), ||Theta|| < 2^-K, gcd(mu1, mu2).
Part 2  Overlap lemma: exact measure of {||p x||<=e} cap {||p' x||<=e} vs 4e^2 +- d^2/(3pp').
Part 3  Discrete uniformity: theta = rho/2^m, q odd -> c mod q given a hit (exact count).
Part 4  Per-factor law for delta_mu with huge mu (exact integers), and the gcd(mu, content w)
        failure of orthogonality.
Part 5  Explicit truncated states: physical preparation of the infinite-index note Sec. 3
        (absolute central window) vs the Part-B law, vs the ISS-Lemma-4 preparation.
Part 6  Independent toy Fourier law at Mb = 32 from the exact formula (no Part-B code).
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python referee_checks.py [part ...]
"""
import math, random, sys, cmath, time
from fractions import Fraction
import numpy as np
from fpylll import IntegerMatrix, LLL
import cypari2
pari = cypari2.Pari()

# ---------------- group H_3(Z): (a,b,c) = [[1,a,c],[0,1,b],[0,0,1]] ----------------
def mul(g, h): return (g[0]+h[0], g[1]+h[1], g[2]+h[2]+g[0]*h[1])
def inv(g): return (-g[0], -g[1], -g[2]+g[0]*g[1])
def pw(g, t): return (t*g[0], t*g[1], t*g[2] + (t*(t-1)//2)*g[0]*g[1])
def delta(mu, g): return (mu*g[0], mu*g[1], mu*mu*g[2])

def dist(num, den):
    """exact ||num/den|| as a Fraction"""
    r = num % den
    return Fraction(min(r, den - r), den)

# ---------------- Part 1 ----------------
def lll(rows):
    A = IntegerMatrix.from_matrix(rows); LLL.reduction(A)
    return [[int(A[i, j]) for j in range(3)] for i in range(3)]

def fincke_pohst(B, R2, shift):
    """all integer coefficient vectors x != 0 with |x B|^2 <= R2 (floats after >> shift;
    slack 1.01); returns lattice vectors (exact ints)."""
    Bf = np.array([[float(x >> shift) if x >= 0 else -float((-x) >> shift) for x in row] for row in B])
    n = 3
    Bs = np.zeros_like(Bf); mu = np.zeros((n, n))
    for i in range(n):
        v = Bf[i].copy()
        for j in range(i):
            mu[i, j] = Bf[i] @ Bs[j] / (Bs[j] @ Bs[j]); v -= mu[i, j] * Bs[j]
        Bs[i] = v
    bn = [Bs[i] @ Bs[i] for i in range(n)]
    R2f = float(R2 >> (2 * shift)) * 1.01
    out = []
    x = [0] * n
    def rec(k, partial):
        c = -sum(mu[j, k] * x[j] for j in range(k + 1, n))
        rem = R2f - partial
        if rem < 0: return
        w = math.sqrt(rem / bn[k])
        for xk in range(math.ceil(c - w), math.floor(c + w) + 1):
            x[k] = xk
            p2 = partial + (xk - c) ** 2 * bn[k]
            if k == 0:
                if any(x): out.append([sum(x[i] * B[i][j] for i in range(n)) for j in range(n)])
            else:
                rec(k - 1, p2)
        x[k] = 0
    rec(n - 1, 0.0)
    return out

def gauss_shortest(q, r):
    u, v = [q, 0], [r % q, 1]
    n2 = lambda a: a[0]*a[0] + a[1]*a[1]
    if n2(u) > n2(v): u, v = v, u
    while True:
        d = u[0]*v[0] + u[1]*v[1]
        m = round(Fraction(d, n2(u)))
        v = [v[0] - m*u[0], v[1] - m*u[1]]
        if n2(v) >= n2(u): return u
        u, v = v, u

def sqrt_mod_prime(t, p):
    return int(pari(f"lift(sqrt(Mod({t},{p})))"))

def sqrt_mod_composite(t, fac):
    """fac: list of (p, e), all p odd and coprime to t; returns r with r^2 = t mod prod p^e or None"""
    rs, mods = [], []
    for p, e in fac:
        if pow(t % p, (p - 1) // 2, p) != 1: return None
        r = sqrt_mod_prime(t % p, p); pk = p
        for _ in range(1, e):
            pk2 = pk * p
            r = (r - (r * r - t) * pow(2 * r, -1, pk2)) % pk2; pk = pk2
        assert (r * r - t) % pk == 0
        rs.append(r); mods.append(pk)
    r, Mo = 0, 1
    for ri, mi in zip(rs, mods):  # CRT
        r = r + Mo * (((ri - r) * pow(Mo, -1, mi)) % mi); Mo *= mi
    return r % Mo

def partial_factor(q, lim=1 << 22):
    F = pari(f"factor({q},{lim})")
    fac = [(int(F[0][i]), int(F[1][i])) for i in range(len(F[0]))]
    if fac and not pari(f"ispseudoprime({fac[-1][0]})"):
        return None
    return fac

def check_output(rho, M, q, c, e_num, mu, K, out):
    """exact verification of Lemma Q; e_num[i] = q rho_i - c_i M  (so e_i = e_num[i]/M)"""
    m1, m2 = mu
    assert (m1, m2) != (0, 0)
    assert 3 * (m1*m1 + m2*m2) ** 2 <= 4 * q * q, 'Hermite bound violated'
    assert (c[0]*m1*m1 + c[1]*m2*m2) % q == 0, 'not isotropic mod q'
    D = dist(rho[0]*m1*m1 + rho[1]*m2*m2, M)
    bound = Fraction(abs(e_num[0])*m1*m1 + abs(e_num[1])*m2*m2, M * q)
    assert D <= bound, 'Lemma Q error identity violated'
    assert D < Fraction(1, 1 << K), 'precision not met'
    out['g'] += (math.gcd(m1, m2) != 1)
    out['maxmu'] = max(out['maxmu'], math.log2(max(abs(m1), abs(m2))))

def part1(rng, Ks=(20, 40, 60, 100, 200), trials=200, C=2.0):
    print('Part 1: rigorous-variant SDA-ISO (full enumeration of hits q in [Q/2,Q])')
    print('| K | log2 M | log2 Q | mean #hits [pred 2eps^2Q] | P(good prime) | CE bound | 1-exp(-S1) | P(good q incl. composite) | composite not factored | non-primitive mu (prime / comp) | max log2|mu| | s/trial |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for K in Ks:
        eb = K + 2                                  # eps = 2^-(K+2) -> (2/sqrt3) eps < 2^-K
        m = 4 * K + 40; M = 1 << m
        lnq = math.log(2) * 2 * eb
        Q = int(C * (1 << (2 * eb)) * lnq)
        W = (M >> eb) // Q                          # cube: q W ~ eps M at q = Q
        assert W >= 1
        R2 = 3 * (M >> eb) ** 2
        shift = max(0, (M >> eb).bit_length() - 50)
        S1 = (Q / 2) / math.log(Q) * (2 * 2 ** (-2 * eb)) * 1.0   # #primes in [Q/2,Q] * P(E_p)
        S1 = (Q / (2 * math.log(Q))) * 2 * 2.0 ** (-2 * eb)
        hits_tot = good_p = good_any = notfac = 0
        st = {'g': 0, 'maxmu': 0.0}; stc = {'g': 0, 'maxmu': 0.0}
        t0 = time.time()
        for _ in range(trials):
            rho = [rng.randrange(M), rng.randrange(M)]
            B = lll([[W, rho[0], rho[1]], [0, M, 0], [0, 0, M]])
            pts = fincke_pohst(B, R2, shift)
            qs = {}
            for v in pts:
                if v[0] < 0: v = [-x for x in v]
                if v[0] == 0 or v[0] % W: continue
                q = v[0] // W
                if not (Q // 2 <= q <= Q): continue
                if max(abs(v[1]), abs(v[2])) << eb > M: continue      # |e_i| <= eps
                qs[q] = v
            hits_tot += len(qs)
            fp = fa = False
            for q in sorted(qs):
                v = qs[q]
                c = [(q * rho[i] - v[i + 1]) // M for i in range(2)]
                e_num = [v[1], v[2]]
                if q % 2 == 0 or math.gcd(c[0] * c[1], q) != 1: continue
                t = (-c[1] * pow(c[0], -1, q)) % q
                if pari(f"ispseudoprime({q})"):   # BPSW; finite check only
                    if pow(t, (q - 1) // 2, q) != 1: continue
                    r = sqrt_mod_prime(t, q)
                    mu = gauss_shortest(q, r)
                    if not fp:
                        check_output(rho, M, q, c, e_num, mu, K, st); fp = True
                    if not fa: fa = True
                else:
                    if fa: continue
                    fac = partial_factor(q)
                    if fac is None: notfac += 1; continue
                    r = sqrt_mod_composite(t, fac)
                    if r is None: continue
                    mu = gauss_shortest(q, r)
                    check_output(rho, M, q, c, e_num, mu, K, stc); fa = True
            good_p += fp; good_any += (fp or fa)
        dt = (time.time() - t0) / trials
        print(f'| {K} | {m} | {math.log2(Q):.1f} | {hits_tot/trials:.2f} [{2*Q*2.0**(-2*eb):.2f}] | '
              f'{good_p}/{trials} | {S1/(1+4*S1):.3f} | {1-math.exp(-S1):.3f} | {good_any}/{trials} | '
              f'{notfac} | {st["g"]} / {stc["g"]} | {max(st["maxmu"], stc["maxmu"]):.1f} | {dt:.3f} |')
        sys.stdout.flush()

# ---------------- Part 2 ----------------
def measure_inter(p, pp, e):
    """exact Lebesgue measure of {x in [0,1): ||p x|| <= e and ||p' x|| <= e}, e < 1/2"""
    def ivs(n):
        L = []
        for j in range(n + 1):
            lo, hi = Fraction(j, n) - e / n, Fraction(j, n) + e / n
            lo, hi = max(lo, Fraction(0)), min(hi, Fraction(1))
            if lo < hi: L.append((lo, hi))
        return L
    A, B = ivs(p), ivs(pp)
    i = j = 0; tot = Fraction(0)
    while i < len(A) and j < len(B):
        lo, hi = max(A[i][0], B[j][0]), min(A[i][1], B[j][1])
        if lo < hi: tot += hi - lo
        if A[i][1] < B[j][1]: i += 1
        else: j += 1
    return tot

def part2(rng):
    print('Part 2: overlap lemma  |lambda(A_p cap A_p\') - 4e^2| <= d^2/(3 p p\'), d = gcd(p,p\')')
    worst = 0.0; n = 0; viol = 0
    cases = []
    for _ in range(60):
        p = int(pari(f"nextprime({rng.randrange(50, 600)})")); pp = int(pari(f"nextprime({rng.randrange(50, 600)})"))
        if p == pp: continue
        cases.append((p, pp))
    for _ in range(15):
        p = rng.randrange(30, 300); cases.append((p, p * rng.randrange(2, 4)))
        a = rng.randrange(20, 200); cases.append((6 * a + 1 if False else 6 * a, 10 * a))
    for p, pp in cases:
        for e in (Fraction(1, 7), Fraction(1, 31), Fraction(1, 2 * min(p, pp)), Fraction(1, 5 * max(p, pp))):
            lam = measure_inter(p, pp, e)
            d = math.gcd(p, pp)
            err = abs(lam - 4 * e * e); bnd = Fraction(d * d, 3 * p * pp)
            n += 1; viol += err > bnd
            worst = max(worst, float(err / bnd))
    print(f'  {n} (p,p\',eps) cases: violations {viol}; max |err|/bound = {worst:.3f}')

# ---------------- Part 3 ----------------
def part3(rng):
    print('Part 3: theta = rho/2^m, q odd: #hits and distribution of c mod q given a hit (exact)')
    for (m, q, eden) in [(20, 101, 8), (22, 997, 16), (24, 1009, 32), (18, 15, 4)]:
        M = 1 << m; e = Fraction(1, eden)
        cnt = [0] * q; hits = 0
        for rho in range(M):
            x = q * rho; c = (2 * x + M) // (2 * M); r = x - c * M
            if abs(r) * eden <= M:
                hits += 1; cnt[c % q] += 1
        print(f'  m={m} q={q} eps=1/{eden}: hits={hits} (2 floor(eps M)+1 = {2*(M//eden)+1}); '
              f'c mod q counts min/max = {min(cnt)}/{max(cnt)} (mean {hits/q:.1f})')

# ---------------- Part 4 ----------------
def part4(rng):
    print('Part 4: per-factor law for delta_mu, huge mu (exact integers)')
    bad = 0; n = 0
    for _ in range(300):
        while True:
            h = (rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(-99, 99))
            if h[0] or h[1]: break
        mu = rng.randrange(-(1 << 90), 1 << 90) or 1
        u = (rng.randint(-50, 50), rng.randint(-50, 50))
        t = rng.randint(-6, 6)
        g = (u[0], u[1], 0)
        gk_pi = (u[0] + t*h[0], u[1] + t*h[1])
        gp = (gk_pi[0], gk_pi[1], 0)                 # sigma(u + t w): section r = 0
        k = mul(inv(g), gp)                          # g k = g'
        # k = h^t z^s0 ?
        ht = pw(h, t); s0 = k[2] - ht[2]
        assert (k[0], k[1]) == (ht[0], ht[1])
        x = mul(delta(mu, gp), inv(delta(mu, g)))    # x' x^-1
        mt = pw(h, mu * t)
        assert (x[0], x[1]) == (mt[0], mt[1]); s = x[2] - mt[2]
        Om = u[0]*h[1] - u[1]*h[0]
        two_cp = 2*h[2] - h[0]*h[1]
        pred = mu*mu*(s0 + t*Om) + ((mu*mu - mu)//2) * two_cp * t
        n += 1; bad += (s != pred)
    print(f'  {n} cases: sigma == mu^2 (s0 + t Omega(u)) + (mu^2-mu)/2 (2c-ab) t :  {n-bad}/{n}')
    # orthogonality failure when gcd(mu, content(w)) > 1
    h = (4, 6, 1); mu = 6
    u, v = (0, 0), (2, 3)                            # v - u = w/2, not in Z w
    x = mul(delta(mu, (v[0], v[1], 0)), inv(delta(mu, (u[0], u[1], 0))))
    inK = (x[0] % h[0] == 0) and (x[0] // h[0]) * h[1] == x[1]
    print(f'  h={h}, mu={mu}: delta_mu(sigma(w/2)) in K = {inK}  (a single factor does NOT separate u, u+w/2)')
    mu2 = 5
    x2 = mul(delta(mu2, (v[0], v[1], 0)), inv(delta(mu2, (u[0], u[1], 0))))
    inK2 = (x2[0] % h[0] == 0) and (x2[0] // h[0]) * h[1] == x2[1]
    print(f'  same pair with mu={mu2}: in K = {inK2}; product of factors (6,5) separates (gcd(mu1,mu2)=1)')

# ---------------- Part 5 ----------------
def part5(rng):
    print('Part 5: explicit truncated states, overlap <psi | psi.k>, k = h^tau z^sigma')
    h = (2, 3, 5); w = (2, 3)
    for a in [(1, -2, 7), (40, -2, 7), (400, 11, -30)]:
        th = rng.random(); N = 2000; T = 30
        def cen(t):  # central coordinate of a h^t
            return mul(a, pw(h, t))[2]
        def phys(x):
            """infinite-index note Sec.3: sum_t sum_{r<N} e(theta(c_t - r)) |(pi_a + t w, r)>, then .x"""
            st = {}
            for t in range(T):
                pi = (a[0] + t*w[0], a[1] + t*w[1]); ct = cen(t)
                for r in range(N):
                    y = mul((pi[0], pi[1], r), x)
                    st[y] = cmath.exp(2j*math.pi*th*(ct - r)) / math.sqrt(T*N)
            return st
        def iss(x):
            """ISS Lemma 4 / hardness note Sec.7: sum_{j<T, s<N} e(-theta s) |a h^j z^s>, then .x"""
            st = {}
            for j in range(T):
                base = mul(a, pw(h, j))
                for s in range(N):
                    y = mul(mul(base, (0, 0, s)), x)
                    st[y] = cmath.exp(-2j*math.pi*th*s) / math.sqrt(T*N)
            return st
        def ip(s1, s2): return sum(s1[k].conjugate()*s2.get(k, 0) for k in s1)
        P0, I0 = phys((0, 0, 0)), iss((0, 0, 0))
        for tau, sig in [(1, 0), (2, 5), (-1, 9)]:
            k = mul(pw(h, tau), (0, 0, sig))
            vp, vi = ip(P0, phys(k)), ip(I0, iss(k))
            ph = lambda v, sgn: abs(v/abs(v) - cmath.exp(sgn*2j*math.pi*th*sig)) if abs(v) > 1e-12 else float('nan')
            drift = [sig + cen(tp) - cen(tp - tau) for tp in range(max(0, tau), min(T, T + tau))]
            pred_p = sum(max(0, N - abs(d)) for d in drift) / (T * N)
            print(f'  a={a} tau={tau} sigma={sig}: phys |ov|={abs(vp):.4f} (drift formula {pred_p:.4f}; '
                  f'Part-B law 1-|s|/N={1-abs(sig)/N:.4f}); ISS |ov|={abs(vi):.4f} '
                  f'(pred (1-|tau|/T)(1-|s|/N)={(1-abs(tau)/T)*(1-abs(sig)/N):.4f}); '
                  f'phase err vs e(+theta sigma): phys {ph(vp,1):.1e}, ISS {ph(vi,1):.1e}')

# ---------------- Part 6 ----------------
def part6(rng, Mb=32, K=24):
    print(f'Part 6: independent toy Fourier law, Mb={Mb}, K={K}, exact phases from the Part-4 formula')
    sys.path.insert(0, __file__.rsplit('/', 1)[0].replace('qzs-referee', 'qzs-attack'))
    from qzs_lattice import sda_iso
    m = 3 * (K + 6) + 40; M = 1 << m
    for h in [(2, 3, 5), (3, 1, -4), (1, 4, 2)]:
        w = (h[0], h[1])
        while True:
            rho = [rng.randrange(M), rng.randrange(M)]
            res = sda_iso(rho, M, K)
            if res[0] != 'fail': break
        mu = res[:2]
        two_cp = 2*h[2] - h[0]*h[1]
        pts = [(p, q) for p in range(Mb) for q in range(Mb)]
        Y = np.array(pts)
        amp = np.zeros(len(pts), complex)  # P(y) = |sum_{u,u'} e(<y,u'-u>/Mb) G(u,u')| / Mb^4
        Pm = np.zeros(len(pts))
        acc = np.zeros(len(pts), complex)
        for u in pts:
            for t in range(-2*Mb, 2*Mb + 1):
                up = (u[0] + t*w[0], u[1] + t*w[1])
                if not (0 <= up[0] < Mb and 0 <= up[1] < Mb): continue
                s0 = -(t*h[2] + (t*(t-1)//2)*h[0]*h[1] + u[0]*t*h[1])
                Om = u[0]*h[1] - u[1]*h[0]
                ph = 0
                for r_, m_ in zip(rho, mu):
                    sig = m_*m_*(s0 + t*Om) + ((m_*m_ - m_)//2)*two_cp*t
                    ph += r_ * sig
                ph = (ph % M) / M
                acc += np.exp(2j*math.pi*((Y @ np.array([t*w[0], t*w[1]])) / Mb + ph))
        P = np.real(acc) / Mb**4
        gam = (sum(r_*((m_*m_ - m_)//2)*two_cp for r_, m_ in zip(rho, mu)) % M) / M
        vals = (Y @ np.array(w)) / Mb
        for lab, off in (('<y,w>/Mb + gamma', gam), ('<y,w>/Mb - gamma', -gam), ('<y,w>/Mb (no offset)', 0.0)):
            dd = np.abs(((vals + off) + 0.5) % 1 - 0.5)
            print(f'  h={h} mu~2^{math.log2(max(map(abs,mu))):.1f}: total={P.sum():.4f}; mass with ||{lab}|| <= 1/Mb: '
                  f'{P[dd <= 1/Mb + 1e-12].sum():.3f}; <= 0.1: {P[dd <= 0.1].sum():.3f}')
        base = np.mean(np.abs(((vals) + 0.5) % 1 - 0.5) <= 1/Mb + 1e-12)
        print(f'  uniform mass in a 1/Mb strip: {base:.3f}')

if __name__ == '__main__':
    parts = sys.argv[1:] or ['1', '2', '3', '4', '5', '6']
    rng = random.Random(2026)
    for p in parts:
        {'1': part1, '2': part2, '3': part3, '4': part4, '5': part5, '6': part6}[p](rng)
        sys.stdout.flush()
