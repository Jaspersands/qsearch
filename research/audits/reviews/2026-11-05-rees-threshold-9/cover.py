"""Rigorous interval cover: Theorem 1's certificate F > 0 on every interval of a chain of
p-intervals covering [L_start k^k + 1, L_C k^k + 1], where L_C = T_C(k)/k^k is TH2's
central-moment threshold (2026-11-02-rees-threshold-2, Theorem 5; computed with its
central_moment.py).  Interval bounds: cert.bestF(k, p_lo, p_hi) uses p_lo for eta and every
lower bound and p_hi for the upper bounds of the binomial and rho factors (all monotone).

Usage: python cover.py k[,k...] [L_start_factor]
Prints T_9(k)/k^k = L_start, number of intervals, min F, and T_C/k^k.
"""
import sys, time
import mpmath as mp
sys.path.insert(0, "../2026-11-02-rees-threshold-2")
import cert
import central_moment as cm


def tc_ratio(k, mmax=10):
    best = None
    for m in range(1, mmax + 1):
        t = cm.threshold(k, m)
        if t is not None and (best is None or t < best):
            best = t
    return None if best is None else mp.mpf(best - 1) / mp.mpf(k) ** k


def first_pointwise(k, L=mp.mpf(2)):
    while cert.point(k, L)[0] <= 0:
        L *= mp.mpf("1.002")
        if L > 30:
            return None
    return L


def cover(k, Lstart, Lend, tmax=1500):
    kk = mp.mpf(k) ** k
    L = Lstart; s = mp.mpf("0.0005"); n = 0; minF = None; t0 = time.time()
    while L < Lend:
        if time.time() - t0 > tmax:
            return None, n, minF, L
        Ln = min(L * (1 + s), Lend)
        val = cert.bestF(k, L * kk + 1, Ln * kk + 1)[0]
        if val > 0:
            n += 1
            minF = val if minF is None or val < minF else minF
            L = Ln; s = min(s * 1.5, mp.mpf("0.05"))
        else:
            s /= 2
            if s < mp.mpf(10) ** -7:
                return None, n, minF, L
    return True, n, minF, L


if __name__ == "__main__":
    ks = [int(x) for x in sys.argv[1].split(",")]
    fac = mp.mpf(sys.argv[2]) if len(sys.argv) > 2 else mp.mpf("1.01")
    for k in ks:
        mp.mp.dps = 60 + k
        t = time.time()
        cm.mp.dps = 50
        LC = tc_ratio(k)
        mp.mp.dps = 60 + k
        L0 = first_pointwise(k)
        if L0 is None or LC is None:
            print(f"k={k} no pointwise certificate or no T_C", flush=True); continue
        Ls = L0 * fac
        ok, n, minF, Lr = cover(k, Ls, LC)
        if ok:
            print(f"k={k} COVERED Lambda in [{mp.nstr(Ls,6)}, {mp.nstr(LC,6)}] (T_C/k^k={mp.nstr(LC,6)}) "
                  f"intervals={n} minF={mp.nstr(minF,4)} pointwise start={mp.nstr(L0,6)} secs={time.time()-t:.0f}", flush=True)
        else:
            print(f"k={k} STUCK at Lambda={mp.nstr(Lr,6)} after {n} intervals (start {mp.nstr(Ls,6)}, T_C/k^k={mp.nstr(LC,6)})", flush=True)
