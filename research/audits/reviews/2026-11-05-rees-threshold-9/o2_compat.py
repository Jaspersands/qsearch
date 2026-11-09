"""Remark 5 check: the brackets of Lemma 2 are satisfied by i.i.d. copies of any single-column law
that satisfies the r = 1 brackets.  Elementary sufficient inequality, for m = m1 + m2, m1, m2 >= 1:
  (1+eta_{m1})(1+eta_{m2}) * (p-m1)(p-m2)/(p(p-m)) <= 1 + eta_m     (upper)
  (1-eta_{m1})(1-eta_{m2}) >= 1 - eta_m                               (lower; the rho ratio is >= 1)
(induction over the number of parts then gives every composition).  Checked for k = 3..400 with p >= 1000(4k+2),
p = Lambda k^k + 1 with Lambda in {1/16, 1/4, 1/2}, all m <= Kmax(p) (eta_m < 1)."""
import mpmath as mp, cert
mp.mp.dps = 60
bad = 0; n = 0
for k in range(3, 401):
    for L in [mp.mpf(1)/16, mp.mpf(1)/4, mp.mpf(1)/2]:
        p = L * mp.mpf(k) ** k + 1
        if p < 1000 * (4 * k + 2): continue
        eta = [cert.eta(k, m, p) for m in range(0, 4 * k + 2)]
        Km = max(m for m in range(len(eta)) if eta[m] < 1)
        for m in range(2, Km + 1):
            for m1 in range(1, m):
                m2 = m - m1
                up = (1 + eta[m1]) * (1 + eta[m2]) * (p - m1) * (p - m2) / (p * (p - m))
                lo = (1 - eta[m1]) * (1 - eta[m2])
                n += 1
                if up > 1 + eta[m] or lo < 1 - eta[m]:
                    bad += 1
                    if bad < 10: print("FAIL", k, mp.nstr(L, 3), m1, m2)
print(f"pairs checked={n} failures={bad}")
