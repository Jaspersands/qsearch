"""Referee scan: max over a 0.2% geometric Lambda grid on [0.5, 4k] of Theorem 1's F (cert.point), k = 3..29.
Report claims F never > 0 for k <= 25 (its outputs only show k = 15, 20, 25)."""
import sys, mpmath as mp
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-05-rees-threshold-9")
import cert
for k in range(3, 30):
    mp.mp.dps = 60 + k
    L = mp.mpf("0.5"); best = None; first = None; last = None
    while L <= 4 * k:
        v = cert.point(k, L)[0]
        if best is None or v > best[0]:
            best = (v, L)
        if v > 0:
            first = first or L; last = L
        L *= mp.mpf("1.002")
    print(f"k={k} max F={mp.nstr(best[0],6)} at Lambda={mp.nstr(best[1],5)} window={'none' if first is None else (mp.nstr(first,5), mp.nstr(last,5))}", flush=True)
