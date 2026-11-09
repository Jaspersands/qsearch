"""Thresholds for union-target refinement steps RC(kappa; R -> K) by a second moment over beta
(report Section 4, Proposition 4.1), and for union chains Z_kappa -> K_1 -> ... -> {0}.

LHS(p) = 1/E n_0 + [(1+Delta)^(r-1) - 1] + (kappa-1) [ 1/E n_U + E2(r Delta) ],   E2(x) = x^2 e^x / 2
  c0 = k/kappa,  G = sum_{s != 0} |chat_s|,  chat_s = kappa^{-1} sum_{m in K} omega^{-m s}
  Delta(p) = (G^2 sqrt p + 2 c0 G + c0^2/p) * p / (c0^2 (p-1)^2)
  E n_0 = ((p-1)/kappa) (c0 (p-1)/p)^(r-1),  E n_U = c0 (p-1) (c0 (p-1)/p)^(r-1)
A step contraction exists for every prime p = 1 (mod kappa) with LHS(p) < 1; LHS is decreasing in p,
so T_U = inf{p : LHS(p) < 1} is a threshold.  For K = {0} (last step) we use instead
min(W(kappa,r), T_R(kappa,r)) of threshold-6 Propositions 3.1/3.2 (= prop:app-s2-step-threshold).
Interpreter: /opt/anaconda3/bin/python.  All numbers are [float] (40 digits).
"""
import sys, cmath, math, itertools
from mpmath import mp, mpf, sqrt, exp, log
mp.dps = 40

def fourier(kappa, K):
    c = [abs(sum(cmath.exp(-2j*cmath.pi*m*s/kappa) for m in K))/kappa for s in range(kappa)]
    return mpf(c[0]), mpf(sum(c[1:]))

def Delta_U(p, c0, G):
    p = mpf(p)
    return (G*G*sqrt(p) + 2*c0*G + c0*c0/p)*p/(c0*c0*(p-1)**2)

def lhs_union(kappa, r, K, p, c0=None, G=None):
    if c0 is None: c0, G = fourier(kappa, K)
    p = mpf(p)
    D = Delta_U(p, c0, G)
    q = c0*(p-1)/p
    En0 = (p-1)/kappa * q**(r-1)
    EnU = c0*(p-1) * q**(r-1)
    E2 = lambda x: x*x*exp(x)/2
    return 1/En0 + ((1+D)**(r-1) - 1) + (kappa-1)*(1/EnU + E2(r*D))

def bisect(f, lo=mpf(10), hi=mpf(10)**200):
    if f(hi) >= 1: return None
    for _ in range(400):
        mid = sqrt(lo*hi)
        if f(mid) < 1: hi = mid
        else: lo = mid
    return hi

def T_U(kappa, r, K):
    c0, G = fourier(kappa, K)
    return bisect(lambda p: lhs_union(kappa, r, K, p, c0, G), lo=mpf(kappa+2))

# ---- K = {0} step thresholds (threshold-6 Prop 3.1 and 3.2) ----
def W(D, r):
    A = mpf(r - 1 - mpf(r)/D) * D**r + 1
    c = mpf(r) * D**(r - 1)
    return ((A + sqrt(A*A + 4*c))/2)**2

def lhs_R(D, r, p):
    p = mpf(p)
    Delta = ((D-1)*(D-2)*sqrt(p) + 2*(D-1))/(p - D - 1)
    first = mpf(D)**r * p**(r-1)/(p-1)**r
    E = (r-1)*Delta**2 + (1+Delta)*exp((r-1)*Delta)*(r-1)**2*Delta**2/2
    return first + E

def T_R(D, r):
    target = mpf(1)/(D-1)
    return bisect(lambda p: lhs_R(D, r, p)/target, lo=mpf(D+2))

def T_last(kappa, k):
    """threshold of RC(kappa; R) with |R| = k rows, target {0}"""
    t = T_R(kappa, k)
    w = W(kappa, k)
    return min(w, t) if t is not None else w

def interval(k): return list(range(k))

def best_two_step(kappa, sets=None):
    """chain Z_kappa -> K -> {0}; returns list of (Theta, k, K, T1, T2)"""
    out = []
    for k in range(2, kappa):
        Ks = [interval(k)] if sets is None else sets(k)
        for K in Ks:
            T1 = T_U(kappa, kappa, K); T2 = T_last(kappa, k)
            out.append((max(T1, T2), k, tuple(K), T1, T2))
    out.sort(key=lambda t: t[0])
    return out

def best_three_step(kappa):
    """chain Z_kappa -> K1 -> K2 -> {0} with intervals K1 = [0,k1), K2 = [0,k2), k1 > k2 >= 2"""
    best = None
    T1c = {k1: T_U(kappa, kappa, interval(k1)) for k1 in range(3, kappa)}
    T3c = {k2: T_last(kappa, k2) for k2 in range(2, kappa-1)}
    for k1 in range(3, kappa):
        for k2 in range(2, k1):
            T2 = T_U(kappa, k1, interval(k2))
            th = max(T1c[k1], T2, T3c[k2])
            if best is None or th < best[0]: best = (th, k1, k2, T1c[k1], T2, T3c[k2])
    return best

def closed_form_step1(kappa, k, G):
    """sufficient bound of Lemma 4.2 for the step Z_kappa -> K (r = kappa rows)"""
    r = kappa
    c0 = mpf(k)/kappa
    return max(1 + mpf('4.05')*kappa*(1/c0)**r, mpf('11.6')*r*r*kappa*(G*G + mpf('0.2')*G + mpf('0.1'))**2/c0**4, 100*r)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "table"
    if mode == "sanity":
        # K = {0}: the union formula must be no better than the cyclotomic second moment (it uses cruder bounds)
        for kappa in [4, 5, 6, 7, 8]:
            print("K={0} sanity", kappa, "T_U(r=kappa)=%.4g" % float(T_U(kappa, kappa, [0])), "kappa^(kappa+1)=%.4g" % kappa**(kappa+1))
        # G bound for intervals: G <= 1 + ln kappa
        worst = -1e9
        for kappa in range(3, 200):
            for k in range(1, kappa):
                c0, G = fourier(kappa, interval(k))
                worst = max(worst, float(G - (1 + math.log(kappa))))
        print("max over 3<=kappa<200, 1<=k<kappa of G(interval) - (1+ln kappa) =", worst)
        # closed form dominates bisected T_U
        bad = 0
        for kappa in range(4, 41):
            for k in range(2, kappa):
                c0, G = fourier(kappa, interval(k))
                cf = closed_form_step1(kappa, k, G); t = T_U(kappa, kappa, interval(k))
                if not (cf >= t and lhs_union(kappa, kappa, interval(k), cf) < 1): bad += 1
        print("closed form >= T_U and LHS(closed form) < 1 for 4<=kappa<=40, 2<=k<kappa; failures:", bad)
    if mode == "table":
        print("Two-step union chains Z_kappa -> [0,k) -> {0} (cubic arity), best k; and three-step (quartic)")
        print("kappa  k  T1(step1)   T2(step2)   Theta2      | k1 k2  Theta3      | (kappa-1)kappa^kappa  kappa^(kappa+1)  kappa^(kappa/2)  ratio log_kappa Theta2")
        for kappa in list(range(4, 32)) + [37, 41, 43, 47, 53, 59, 61, 64]:
            b2 = best_two_step(kappa)[0]
            b3 = best_three_step(kappa) if kappa <= 47 else None
            th2 = b2[0]
            s3 = "%2d %2d  %10.4g" % (b3[1], b3[2], float(b3[0])) if b3 else "   -   -"
            print("%5d %2d  %10.4g  %10.4g  %10.4g  | %s | %12.4g  %12.4g  %12.4g  %6.3f" % (
                kappa, b2[1], float(b2[3]), float(b2[4]), float(th2), s3,
                (kappa-1)*mpf(kappa)**kappa, mpf(kappa)**(kappa+1), mpf(kappa)**(mpf(kappa)/2), float(log(th2)/log(kappa))))
    if mode == "smallsets":
        # kappa = 5, 7: all K containing 0 (not only intervals), two-step chains
        for kappa in [5, 7]:
            res = []
            for k in range(2, kappa):
                for rest in itertools.combinations(range(1, kappa), k-1):
                    K = (0,) + rest
                    T1 = T_U(kappa, kappa, K); T2 = T_last(kappa, k)
                    res.append((max(T1, T2), K, T1, T2))
            res.sort(key=lambda t: t[0])
            print("kappa=%d best two-step chains over all K:" % kappa)
            for th, K, T1, T2 in res[:6]:
                print("   K=%s  T1=%.6g  T2=%.6g  Theta=%.6g" % (K, float(T1), float(T2), float(th)))
    if mode == "asym":
        # k = ceil(kappa lnln kappa / ln kappa): Theta2 vs 6 kappa^2 (ln kappa)^kappa
        print("kappa  k  Theta2(k)  6 kappa^2 (ln kappa)^kappa  log_kappa Theta2  kappa lnln/ln")
        for kappa in [16, 20, 32, 50, 64, 100, 128, 200, 256]:
            k = max(2, math.ceil(kappa*math.log(math.log(kappa))/math.log(kappa)))
            T1 = T_U(kappa, kappa, interval(k)); T2 = T_last(kappa, k)
            th = max(T1, T2); ref = 6*mpf(kappa)**2*log(kappa)**kappa
            print("%5d %3d  %.4g  %.4g  %s  %.3f  %.3f" % (kappa, k, float(th), float(ref), th <= ref,
                  float(log(th)/log(kappa)), kappa*math.log(math.log(kappa))/math.log(kappa)))
