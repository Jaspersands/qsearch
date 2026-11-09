"""First Lambda (1% grid from 2.0) where the threshold-9 certificate F > 0 (pointwise), large k."""
import sys, time, mpmath as mp, cert
for k in [int(x) for x in sys.argv[1].split(",")]:
    mp.mp.dps = 60 + k
    L = mp.mpf(2); t = time.time()
    while True:
        val, R, Ks, Km = cert.point(k, L)
        if val > 0:
            break
        L *= mp.mpf("1.01")
    mu = k * mp.e ** (-L)
    print(f"k={k} Lambda*~{mp.nstr(L,5)} ln k={float(mp.log(k)):.3f} R={R} Kmax={Km} mu={mp.nstr(mu,4)} "
          f"F={mp.nstr(val,4)} K_R={Ks[R]} secs={time.time()-t:.0f}", flush=True)
