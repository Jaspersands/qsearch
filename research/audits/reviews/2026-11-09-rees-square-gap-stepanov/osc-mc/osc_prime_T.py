"""Threshold implied by OSC'(B) (section 11.8 of the topic note).  OSC'(B; m0): (N), and
  |V| <= B                      for one-sided non-pair classes and two-sided classes with m <= m0,
  |V| <= B k^2/p + 2 noise      for two-sided classes with m > m0   (m0 = 6 is what kappa = 4..6 show).
Then PW_pair <= (B/n) W_L + (B k^2/(p n)) W_D + B (2/sqrt(pi)) noisePW(p), where W_L, W_D are the
permanent weights of the two groups and noisePW is the noise-only PW_pair (Rayleigh mean; the bound
uses the rms).  PW_pair < 1 once each term is < 1/3, so T = max(T_1, T_2, T_3).
Table 1: B = 3 and 8.5 with m0 = 6.  Table 2: how far m0(k) may grow before T reaches k^k (B = 3).
Table 3: the group-rms form OSC'_rms(B_L, B_D) of section 11.8: by Cauchy-Schwarz the L and D groups
contribute at most (W_L/n) rms_L and (W_D/n) rms_D, so per-class bounds are replaced by
rms_L <= B_L and rms_D <= B_D k^2/p (plus the noise rms; the noise term is taken with factor 2).
Constants from equal_p_chain.out: typical primes (0.5, 1.6) and the largest values seen at any tested
prime above the noise crossing, spikes included (1.2, 3.7; kappa = 6, p = 1933, Monte Carlo).
Usage: python osc_prime_T.py"""
import math, numpy as np
w = np.load('weights_k.npz')
def T(k, B, m0=6, rho=0.8, BD=None, Bn=None):
    BD = B if BD is None else BD; Bn = B if Bn is None else Bn
    A = w['A%d' % k]; Ap = w['Ap%d' % k]; kf = math.factorial(k)
    WL = 2 * (A.sum() - A[0] - A[2])                       # one-sided, not pairs (A[0] = 1)
    WD = 0.0
    for a in range(2, k + 1):
        for b in range(a, k + 1):
            wt = (1 if a == b else 2) * A[a] * A[b]
            if a + b <= m0: WL += wt
            else: WD += wt
    As = Ap.sum() ** 2 - Ap[0] ** 2 - 2 * Ap[0] * Ap[2]
    def noise(p):
        n = p + 1 - 2 * k
        T1 = math.prod(range(p - k + 1, p - 1)) * math.prod(range(p - 2 * k + 1, p - k + 1))
        Nunl = rho * T1 * float(k) ** (-(k - 1) ** 2) / (kf ** 2 * n)
        return As / math.sqrt(n * Nunl)                    # = (2/sqrt(pi)) * noise-only PW_pair
    t1 = 3 * B * WL + 2 * k
    t2 = int(k * math.sqrt(3 * BD * WD)) + 2 * k
    p = 2 * k + 3
    while Bn * noise(p) > 1 / 3: p = int(p * 1.005) + 1
    return t1, t2, p, WL, WD
lk = lambda x, k: math.log(x) / math.log(k)
for B in (3.0, 8.5):
    print('Table 1, B = %.1f, m0 = 6' % B)
    print('  k      W_L        W_D        T_1 (log_k)     T_2 (log_k)     T_3 (log_k)   max log_k   k/2+k/(2 ln k)  (k+1)/2')
    for k in range(4, 11):
        t1, t2, t3, WL, WD = T(k, B)
        print('%3d %10.3g %10.3g  %9d (%5.2f) %9d (%5.2f) %9d (%5.2f)   %5.2f       %5.2f        %4.1f' % (
            k, WL, WD, t1, lk(t1, k), t2, lk(t2, k), t3, lk(t3, k), max(lk(t1, k), lk(t2, k), lk(t3, k)),
            k / 2 + k / (2 * math.log(k)), (k + 1) / 2))
print('Table 2, B = 3: log_k T as m0 grows (m0 = 2k: no decay anywhere); last m0 with T < k^k')
for k in range(4, 11):
    row = []; last = None
    for m0 in range(6, 2 * k + 1):
        t = max(T(k, 3.0, m0)[:3]); row.append('%d:%.2f' % (m0, lk(t, k)))
        if t < k ** k: last = m0
    print('  k=%2d  last m0 with T < k^k: %s   (%s)' % (k, last, ' '.join(row)))
for BL, BD in ((0.5, 1.6), (1.2, 3.7)):
    print('Table 3, group-rms constants B_L = %.1f, B_D = %.1f, m0 = 6, noise factor 2' % (BL, BD))
    print('  k     T_1 (log_k)     T_2 (log_k)     T_3 (log_k)   max log_k   lambda at T   k/2+k/(2 ln k)')
    for k in range(4, 11):
        t1, t2, t3, WL, WD = T(k, BL, BD=BD, Bn=2.0)
        t = max(t1, t2, t3)
        print('%3d  %9d (%5.2f) %9d (%5.2f) %9d (%5.2f)   %5.2f      %8.3g        %5.2f' % (
            k, t1, lk(t1, k), t2, lk(t2, k), t3, lk(t3, k), lk(t, k), t / k ** (k - 1), k / 2 + k / (2 * math.log(k))))
