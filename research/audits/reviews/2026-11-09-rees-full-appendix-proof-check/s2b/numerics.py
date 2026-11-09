"""s2b numerics: re-evaluate the constants and computed thresholds of
appendix-schedule2.tex lines 521-654 (step thresholds, union steps, union chain,
Theta_2/Theta_3, T_R(9,3), W(9,3), barrier, T_A).  Finite evaluations only:
they can falsify a stated number, never prove a statement."""
import math, itertools, sys
import mpmath as mp
mp.mp.dps = 40

out = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); out.append(s)

# ---------------- definitions copied from the paper ----------------
def Delta(p, D):           # Lemma app-s2-cyclo with D in place of kappa
    return ((D-1)*(D-2)*mp.sqrt(p) + 2*(D-1)) / (p - D - 1)

def W(D, r):               # Prop step-threshold (i)
    A = (r - 1 - mp.mpf(r)/D) * mp.mpf(D)**r + 1
    return ((A + mp.sqrt(A*A + 4*r*mp.mpf(D)**(r-1)))/2)**2

def TW(k):                 # Prop app-s2-TW
    A = (k-2)*mp.mpf(k)**k + 1
    return ((A + mp.sqrt(A*A + 4*mp.mpf(k)**k))/2)**2

def Er(p, D, r):
    d = Delta(p, D)
    return (r-1)*d*d + (1+d)*mp.e**((r-1)*d)*(r-1)**2*d*d/2

def TRlhs(p, D, r):        # Remark chains-scope: T_R criterion
    return mp.mpf(D)**r * mp.mpf(p)**(r-1) / (p-1)**r + Er(p, D, r)

def bisect_dec(f, lo, hi, it=400):
    """least p in (lo,hi] with f(p) true, f monotone false->true"""
    assert f(hi), ("hi not true", hi)
    for _ in range(it):
        mid = (lo+hi)/2
        if f(mid): hi = mid
        else: lo = mid
        if hi - lo < mp.mpf(10)**-12 * hi: break
    return hi

def TR(D, r):
    f = lambda p: TRlhs(p, D, r) < mp.mpf(1)/(D-1)
    hi = mp.mpf(D+2)
    while not f(hi): hi *= 2
    return bisect_dec(f, mp.mpf(D+1)*(1+mp.mpf(10)**-30), hi)

def Ghat(D, K):
    w = [mp.e**(-2j*mp.pi*m*0) for m in K]  # placeholder
    cs = []
    for s in range(D):
        z = sum(mp.e**(-2j*mp.pi*m*s/D) for m in K)/D
        cs.append(z)
    G = sum(abs(cs[s]) for s in range(1, D))
    return G

def PsiU(p, D, r, K, G=None):
    k = len(K); c0 = mp.mpf(k)/D
    if G is None: G = Ghat(D, K)
    p = mp.mpf(p)
    DU = (G*G*mp.sqrt(p) + 2*c0*G + c0*c0/p)*p/(c0*c0*(p-1)**2)
    N0 = (p-1)/D*(c0*(p-1)/p)**(r-1)
    N1 = c0*(p-1)*(c0*(p-1)/p)**(r-1)
    x = r*DU
    return 1/N0 + (1+DU)**(r-1) - 1 + (D-1)*(1/N1 + x*x*mp.e**x/2)

def TU(D, r, K):
    G = Ghat(D, K)
    f = lambda p: PsiU(p, D, r, K, G) < 1
    hi = mp.mpf(8)
    while not f(hi): hi *= 2
    return bisect_dec(f, mp.mpf(2)*(1+mp.mpf(10)**-30), hi)

def Ukappa(p, k):          # Prop app-s2-TA
    p = mp.mpf(p); d = Delta(p, k)
    if d > mp.mpf(1)/2: return None
    u = mp.mpf(1)/2 - d/3 - 1/(k*(1-d))
    v = d/(mp.sqrt(k)*(1-d))
    smax = mp.sqrt(k)*d
    cands = [mp.mpf(0), smax]
    if u > 0:
        s0 = v/(2*u)
        if 0 <= s0 <= smax: cands.append(s0)
    Em = max(-u*s*s + v*s for s in cands)
    return mp.mpf(k)**k*p**(k-1)/(p-1)**k + mp.e**Em

def TA(k, thr=None):
    if thr is None: thr = mp.mpf(k)/(k-1)
    def f(p):
        U = Ukappa(p, k)
        return U is not None and U < thr
    hi = mp.mpf(k+2)
    while not f(hi): hi *= 2
    return bisect_dec(f, mp.mpf(k+1)*(1+mp.mpf(10)**-30), hi)

# ---------------- 1. Prop step-threshold (ii) constants ----------------
say("== 1. step-threshold (ii): sweep D=4..60, r=2..D at p0=max(4D^{r+1},4r^2D^5)")
worst = {}
bad = []
for D in range(4, 61):
    for r in range(2, D+1):
        p0 = max(4*mp.mpf(D)**(r+1), 4*r*r*mp.mpf(D)**5)
        d = Delta(p0, D)
        first = mp.mpf(D)**r*p0**(r-1)/(p0-1)**r
        E = Er(p0, D, r)
        checks = {
            "p0>=16384": p0 >= 16384,
            "first<=1.001/(4D)": first <= mp.mpf('1.001')/(4*D),
            "(D+1)/p<=4e-4": (D+1)/p0 <= mp.mpf('4e-4'),
            "Delta<=1.0005D^2/sqrtp": d <= mp.mpf('1.0005')*D*D/mp.sqrt(p0),
            "Delta<=0.5003/(r sqrtD)": d <= mp.mpf('0.5003')/(r*mp.sqrt(D)),
            "(r-1)Delta<=0.2502": (r-1)*d <= mp.mpf('0.2502'),
            "Delta<=0.1251": d <= mp.mpf('0.1251'),
            "E_r<=0.1809/D": E <= mp.mpf('0.1809')/D,
            "rho2<=1+0.4312/D": first + 1 + E <= 1 + mp.mpf('0.4312')/D,
            "rho2<D/(D-1)": first + 1 + E < mp.mpf(D)/(D-1),
        }
        for kk, v in checks.items():
            if not v: bad.append((D, r, kk))
        rat = (first + E)*(D-1)
        if rat > worst.get('rho', (0,))[0]: worst['rho'] = (rat, D, r)
say("  failures:", bad if bad else "none")
say("  max of (first+E_r)(D-1) [<1 needed]:", mp.nstr(worst['rho'][0], 6), "at (D,r)=", worst['rho'][1:])
# the key constant (1+Delta) e^{(r-1)Delta}/2 <= 0.7225 at the extreme values
say("  (1.1251)*e^0.2502/2 =", mp.nstr(mp.mpf('1.1251')*mp.e**mp.mpf('0.2502')/2, 8))

# ---------------- 2. Prop union-step (ii) ----------------
say("== 2. union-step (ii): Psi_U(p0) < 0.73 at p0 = max(1+4.05 D c0^-r, 11.6 r^2 D H^2 c0^-4, 100 r)")
def Gfloat(D, K):
    G = 0.0
    for s in range(1, D):
        z = sum(complex(math.cos(-2*math.pi*m*s/D), math.sin(-2*math.pi*m*s/D)) for m in K)/D
        G += abs(z)
    return G
def PsiUf(p, D, r, k, G):
    c0 = k/D
    DU = (G*G*math.sqrt(p) + 2*c0*G + c0*c0/p)*p/(c0*c0*(p-1)**2)
    N0 = (p-1)/D*(c0*(p-1)/p)**(r-1)
    N1 = c0*(p-1)*(c0*(p-1)/p)**(r-1)
    x = r*DU
    return 1/N0 + (1+DU)**(r-1) - 1 + (D-1)*(1/N1 + x*x*math.exp(x)/2)
worstU = (0, None); badU = []; badG = []; n = 0
for D in range(4, 41):
    Ks = []
    if D <= 12:
        for mask in range(0, 2**(D-1)):
            K = [0] + [i for i in range(1, D) if mask >> (i-1) & 1]
            if len(K) < D: Ks.append(tuple(K))
    else:
        Ks = [tuple(range(k)) for k in range(1, D)]
    for K in Ks:
        k = len(K); c0 = k/D; G = Gfloat(D, K); H = G*G + 0.2*G + 0.1
        if K == tuple(range(k)):
            if G > 1 + math.log(D) + 1e-12 or H > (1.2 + math.log(D))**2 + 1e-12: badG.append((D, K))
        for r in range(2, D+1):
            # skip astronomically large p0 (float overflow); check those in mp below
            lg = math.log(4.05*D) - r*math.log(c0)
            if lg > 650: continue
            p0 = max(1 + 4.05*D*c0**(-r), 11.6*r*r*D*H*H*c0**(-4), 100*r)
            v = PsiUf(p0, D, r, k, G); n += 1
            if not v < 0.73: badU.append((D, K, r, v))
            if v > worstU[0]: worstU = (v, (D, K if len(K) < 6 else ('len', k), r))
say("  cases:", n, " failures:", badU[:5] if badU else "none")
say("  max Psi_U(p0):", round(worstU[0], 5), "at", worstU[1])
say("  interval G/H bound failures:", badG if badG else "none")
# a few huge-p0 cases in mpmath
hb = []
for (D, k, r) in [(40, 1, 40), (30, 2, 30), (20, 1, 20), (16, 3, 16), (40, 39, 40)]:
    K = tuple(range(k)); c0 = mp.mpf(k)/D; G = Ghat(D, K); H = G*G + mp.mpf('0.2')*G + mp.mpf('0.1')
    p0 = max(1 + mp.mpf('4.05')*D*c0**(-r), mp.mpf('11.6')*r*r*D*H*H*c0**(-4), 100*r)
    hb.append(((D, k, r), mp.nstr(PsiU(p0, D, r, K, G), 6)))
say("  huge-p0 samples (D,k,r)->Psi_U(p0):", hb)

# ---------------- 3. Cor union-chain: Theta^cf_2 ----------------
say("== 3. Theta^cf_2(kappa,k) minima, and the kappa=16/19 inequalities")
def Thcf(K, k):
    K = mp.mpf(K)
    return max(1 + mp.mpf('4.05')*K*(K/k)**K, mp.mpf('11.6')*K**3*(K/k)**4*(mp.mpf('1.2')+mp.log(K))**4,
               100*K, 4*K**(k+1), 4*k*k*K**5)
for K in range(4, 21):
    vals = [(Thcf(K, k), k) for k in range(2, K)]
    m = min(vals)
    say("  kappa=%d: min_k Theta^cf_2 = %s at k=%d" % (K, mp.nstr(m[0], 4), m[1]))
for K in [16, 17, 18, 19, 20, 25, 30, 40]:
    k = math.ceil(K*math.log(math.log(K))/math.log(K))
    lhs16 = math.log(2.9*K) + 8*math.log(1.2 + math.log(K)); rhs16 = K*math.log(math.log(K))
    th = Thcf(K, k); bnd = mp.mpf('4.05')*K**2*mp.log(K)**K
    say("  kappa=%d k=%d: Theta^cf<=4.05k^2(lnk)^k: %s;  ln(2.9k)+8ln(1.2+lnk)=%.3f <= k lnlnk=%.3f;  4.05k^2(lnk)^k < k^(k/2): %s (%.3f vs %.3f)"
        % (K, k, th <= bnd, lhs16, rhs16, bnd < mp.mpf(K)**(mp.mpf(K)/2),
           math.log(4.05) + 2*math.log(K) + K*math.log(math.log(K)), K/2*math.log(K)))

# ---------------- 4. Theta_2, Theta_3, T_R, W ----------------
say("== 4. Theta_2, Theta_3 for kappa = 5,7,11,13; T_R(9,3), W(9,3)")
TUc = {}
def TUcached(D, r, k):
    key = (D, r, k)
    if key not in TUc: TUc[key] = TU(D, r, tuple(range(k)))
    return TUc[key]
TRc = {}
def TRcached(D, r):
    if (D, r) not in TRc: TRc[(D, r)] = TR(D, r)
    return TRc[(D, r)]
for K in [5, 7, 11, 13]:
    best2 = None
    for k in range(2, K):
        step1 = TUcached(K, K, k); step2 = min(W(K, k), TRcached(K, k))
        v = max(step1, step2)
        if best2 is None or v < best2[0]:
            best2 = (v, k, step1, step2, 'TR' if TRcached(K, k) < W(K, k) else 'W')
    best3 = None
    for k1 in range(2, K):
        for k2 in range(1, k1):
            if k2 == 1:
                last = mp.mpf(0)   # RC(kappa;{0}) is trivial
            else:
                last = min(W(K, k2), TRcached(K, k2))
            v = max(TUcached(K, K, k1), TUcached(K, k1, k2), last)
            if best3 is None or v < best3[0]: best3 = (v, k1, k2)
    best3b = None
    for k1 in range(3, K):
        for k2 in range(2, k1):
            v = max(TUcached(K, K, k1), TUcached(K, k1, k2), min(W(K, k2), TRcached(K, k2)))
            if best3b is None or v < best3b[0]: best3b = (v, k1, k2)
    say("  kappa=%d: Theta_2=%s (k=%d; T_U=%s, last=%s via %s);  Theta_3(k2>=1)=%s (k1=%d,k2=%d);  Theta_3(k2>=2)=%s (k1=%d,k2=%d);  (k-1)k^k=%s; T_R(k,3)=%s"
        % (K, mp.nstr(best2[0], 6), best2[1], mp.nstr(best2[2], 6), mp.nstr(best2[3], 6), best2[4],
           mp.nstr(best3[0], 6), best3[1], best3[2], mp.nstr(best3b[0], 6), best3b[1], best3b[2],
           mp.nstr((K-1)*mp.mpf(K)**K, 4), mp.nstr(TRcached(K, 3), 6)))
say("  T_R(9,3) =", mp.nstr(TR(9, 3), 8), "  W(9,3) =", mp.nstr(W(9, 3), 8))
say("  W(4,2), W(8,2), W(6,2) =", mp.nstr(W(4, 2), 6), mp.nstr(W(8, 2), 6), mp.nstr(W(6, 2), 6),
    "  bounds ((D-1)^2+1)^2:", 100, 2500, 676)
say("  T_W(2) =", mp.nstr(TW(2), 6), " T_W(4) =", mp.nstr(TW(4), 6))

# ---------------- 5. barrier ----------------
say("== 5. barrier bound at kappa=4, p=17, h'=2")
def barrier(K, p, h, a):
    p = mp.mpf(p)
    v = K*p**h*(1 - (1 - 1/p)/K)**(a+h)
    for s in range(2, K):
        v += p**(s*(K-1+h))*(1 - (1 - p**(-s))/K)**(a+h)
    return v
a = 0
while barrier(4, 17, 2, a) >= 1: a += 1
say("  least a' with bound < 1:", a, " (bound at a'-1:", mp.nstr(barrier(4, 17, 2, a-1), 6), ")")

# ---------------- 6. T_A, T_S ----------------
say("== 6. T_A(kappa)")
for K in range(3, 10):
    ta = TA(K)
    say("  T_A(%d) = %s   ceil = %d   (k-1)k^k = %d   k^(k+1) = %d" % (K, mp.nstr(ta, 12), int(mp.ceil(ta)), (K-1)*K**K, K**(K+1)))
say("  T_S(3..8) =", [mp.nstr(TA(K, 1 + mp.mpf(1)/(8*K)), 8) for K in range(3, 9)])

open(__file__.replace('.py', '.out'), 'w').write("\n".join(out) + "\n")
