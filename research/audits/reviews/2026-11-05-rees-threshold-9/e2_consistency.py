"""Theorem 1 must never certify a known member of E_2(k).  Reads every 'INFEASIBLE k=.. p=..'
line under the E_2 data folders and evaluates the certificate F (pointwise, best R, K_r)."""
import glob, re, mpmath as mp, cert
mp.mp.dps = 80
mem = set()
for f in glob.glob("../2026-11-04-rees-threshold-5/*.out") + glob.glob("../2026-11-02-rees-schedules/small-prime/*.out") \
        + glob.glob("../2026-11-05-rees-threshold-8/*.out"):
    for line in open(f):
        m = re.match(r"INFEASIBLE k=(\d+) p=(\d+)", line)
        if m:
            mem.add((int(m.group(1)), int(m.group(2))))
bad = 0; maxF = {}
for k, p in sorted(mem):
    val = cert.bestF(k, mp.mpf(p), mp.mpf(p))[0]
    maxF[k] = max(maxF.get(k, -mp.inf), val)
    if val > 0:
        bad += 1; print("CERTIFIED A MEMBER (bug):", k, p, val)
for k in sorted(maxF):
    pm = max(p for kk, p in mem if kk == k)
    print(f"k={k} members={sum(1 for kk,_ in mem if kk==k)} max member p={pm} Lambda={(pm-1)/k**k:.3e} max F over members={mp.nstr(maxF[k],5)}")
print(f"members={len(mem)} certified={bad}")
