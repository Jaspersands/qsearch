"""Independent evaluation of the union-chain thresholds of threshold-7 Section 4 [float, 40 digits].

LHS_U(p) (Proposition 4.1, re-derived in the check report):
  1/E0 + ((1+Delta)^(r-1) - 1) + (D-1) (1/EU + (r Delta)^2 e^(r Delta) / 2),
  c0 = |K|/D, chat_s = D^-1 sum_{m in K} w^{-ms}, G = sum_{s != 0} |chat_s|,
  Delta = (G^2 sqrt p + 2 c0 G + c0^2/p) p / (c0^2 (p-1)^2),
  E0 = (p-1)/D (c0 (p-1)/p)^(r-1),  EU = c0 (p-1) (c0 (p-1)/p)^(r-1).
Last step RC(D; R) with K = {0}: W(D, r) of prop:app-s2-step-threshold(i), and T_R(D, r), the
infimum of p with D^r p^(r-1)/(p-1)^r + E_r(Delta_R) < 1/(D-1), which is the inequality
rho < D/(D-1) of the proof of prop:app-s2-step-threshold(ii) before its closed form.
All three criteria are decreasing in p, so each threshold is an infimum found by bisection.
"""
import sys, cmath, math, itertools
from mpmath import mp, mpf, sqrt, exp, log, ln
mp.dps = 40

def fourier(D, K):
    ch = [sum(cmath.exp(-2j * math.pi * m * s / D) for m in K) / D for s in range(D)]
    return mpf(len(K)) / D, mpf(sum(abs(c) for c in ch[1:]))

def lhs_U(p, D, r, c0, G):
    p = mpf(p)
    Dl = (G * G * sqrt(p) + 2 * c0 * G + c0 * c0 / p) * p / (c0 * c0 * (p - 1) ** 2)
    q = c0 * (p - 1) / p
    E0 = (p - 1) / D * q ** (r - 1)
    EU = c0 * (p - 1) * q ** (r - 1)
    x = r * Dl
    return 1 / E0 + ((1 + Dl) ** (r - 1) - 1) + (D - 1) * (1 / EU + x * x * exp(x) / 2)

def lhs_R(p, D, r):
    p = mpf(p)
    Dl = ((D - 1) * (D - 2) * sqrt(p) + 2 * (D - 1)) / (p - D - 1)
    Er = (r - 1) * Dl ** 2 + (1 + Dl) * exp((r - 1) * Dl) * (r - 1) ** 2 * Dl ** 2 / 2
    return mpf(D) ** r * p ** (r - 1) / (p - 1) ** r + Er

def bisect(ok, lo, hi=mpf(10) ** 700):
    """inf{p >= lo : ok(p)} for a predicate that is monotone (false then true)."""
    assert ok(hi)
    if ok(lo): return lo
    for _ in range(400):
        mid = sqrt(lo * hi)
        if ok(mid): hi = mid
        else: lo = mid
    return hi

def T_U(D, r, K):
    c0, G = fourier(D, K)
    return bisect(lambda p: lhs_U(p, D, r, c0, G) < 1, mpf(D + 2))

def T_R(D, r):
    return bisect(lambda p: lhs_R(p, D, r) < mpf(1) / (D - 1), mpf(D + 2))

def W(D, r):
    A = (r - 1 - mpf(r) / D) * mpf(D) ** r + 1
    return ((A + sqrt(A * A + 4 * r * mpf(D) ** (r - 1))) / 2) ** 2

def last(D, r): return min(W(D, r), T_R(D, r))

def iv(k): return list(range(k))

def theta2(kap):
    best = None
    for k in range(2, kap):
        t = max(T_U(kap, kap, iv(k)), last(kap, k))
        if best is None or t < best[0]: best = (t, k)
    return best

def theta3(kap):
    best = None
    tu1 = {k1: T_U(kap, kap, iv(k1)) for k1 in range(2, kap)}
    ls = {k2: last(kap, k2) for k2 in range(2, kap)}
    for k1 in range(2, kap):
        for k2 in range(2, kap):
            if k2 >= k1: continue
            t = max(tu1[k1], T_U(kap, k1, iv(k2)), ls[k2])
            if best is None or t < best[0]: best = (t, k1, k2)
    return best

def closed_P(D, r, K):
    c0, G = fourier(D, K)
    H = G * G + mpf('0.2') * G + mpf('0.1')
    return max(1 + mpf('4.05') * D * c0 ** (-r), mpf('11.6') * r * r * D * H * H * c0 ** (-4), 100 * r)

def fmt(x): return "%.4g" % float(x)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'table'
    if mode == 'table':
        ks = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 23, 31, 47]
        print("kappa | k | Theta_2 | (k1,k2) | Theta_3 | (kappa-1)kappa^kappa | kappa^(kappa/2) | log_kappa Theta_2 | Th2<kappa^(k/2) | Th3<kappa^(k/2)")
        for kap in ks:
            t2, k = theta2(kap)
            if kap <= 31:
                t3, k1, k2 = theta3(kap)
            else:
                t3, k1, k2 = mpf('nan'), 0, 0
            ta = (kap - 1) * mpf(kap) ** kap
            half = mpf(kap) ** (mpf(kap) / 2)
            print("%d | %d | %s | (%d,%d) | %s | %s | %s | %.2f | %s | %s" % (
                kap, k, fmt(t2), k1, k2, fmt(t3), fmt(ta), fmt(half), float(log(t2) / log(kap)),
                t2 < half, (t3 < half) if kap <= 31 else '-'), flush=True)
            assert t2 < ta
    elif mode == 'parts':
        for kap in [5, 7, 11, 13]:
            t2, k = theta2(kap)
            print("kappa=%d Theta_2: k=%d  T_U(step1)=%s  W=%s  T_R=%s" % (kap, k, fmt(T_U(kap, kap, iv(k))), fmt(W(kap, k)), fmt(T_R(kap, k))))
            t3, k1, k2 = theta3(kap)
            print("kappa=%d Theta_3: (k1,k2)=(%d,%d)  step1=%s step2=%s step3: W=%s T_R=%s" % (
                kap, k1, k2, fmt(T_U(kap, kap, iv(k1))), fmt(T_U(kap, k1, iv(k2))), fmt(W(kap, k2)), fmt(T_R(kap, k2))))
        # all K containing 0 for kappa = 5, 7 (two-step chains)
        for kap in [5, 7]:
            best = None
            for k in range(2, kap):
                for rest in itertools.combinations(range(1, kap), k - 1):
                    K = [0] + list(rest)
                    t = max(T_U(kap, kap, K), last(kap, k))
                    if best is None or t < best[0]: best = (t, K)
            print("kappa=%d best two-step over all K: %s at K=%s" % (kap, fmt(best[0]), best[1]))
    elif mode == 'closed':
        worst_ratio, worst_lhs = 0, 0
        for D in range(4, 41):
            for k in range(1, D):
                for r in sorted({2, D // 2, D} | ({k} if k >= 2 else set())):
                    if r < 2: continue
                    K = iv(k)
                    c0, G = fourier(D, K)
                    P = closed_P(D, r, K)
                    l = lhs_U(P, D, r, c0, G)
                    tu = T_U(D, r, K)
                    assert l < mpf('0.73'), (D, k, r, l)
                    assert tu <= P
                    worst_lhs = max(worst_lhs, l)
                    assert G <= 1 + ln(D)
        print("closed form: LHS(P) < 0.73 and T_U <= P for 4 <= D <= 40, intervals [0,k), r in {2, D/2, k, D}; max LHS(P) = %s" % fmt(worst_lhs))
    elif mode == 'asym':
        bad = []
        for kap in range(16, 401):
            k = math.ceil(kap * math.log(math.log(kap)) / math.log(kap))
            assert 2 <= k <= kap - 1
            Lk = ln(kap)
            B = mpf('4.05') * kap ** 2 * Lk ** kap
            terms = [1 + mpf('4.05') * kap * (mpf(kap) / k) ** kap,
                     mpf('11.6') * kap ** 3 * (mpf(kap) / k) ** 4 * (mpf('1.2') + Lk) ** 4,
                     100 * kap, 4 * mpf(kap) ** (k + 1), 4 * k * k * mpf(kap) ** 5]
            if max(terms) > B: bad.append(kap)
            if kap >= 19 and not B < mpf(kap) ** (mpf(kap) / 2): bad.append(('half', kap))
            if kap in (16, 32, 64, 128, 256):
                # the exact bisected Theta_2(kap, k) also lies below B (and below kappa^(kappa/2) for kappa >= 19)
                t = max(T_U(kap, kap, iv(k)), last(kap, k))
                print("kappa=%d k=%d Theta_2(kappa,k)=%s  bound 4.05k^2(ln k)^k=%s  closed max=%s" % (kap, k, fmt(t), fmt(B), fmt(max(terms))), flush=True)
                assert t <= max(terms) <= B
        print("asymptotic bound fails at:", bad)
        for kap in range(13, 19):
            t2, k = theta2(kap)
            print("kappa=%d Theta_2=%s (k=%d) kappa^(kappa/2)=%s below: %s" % (kap, fmt(t2), k, fmt(mpf(kap) ** (mpf(kap) / 2)), t2 < mpf(kap) ** (mpf(kap) / 2)))
