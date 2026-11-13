"""Step 4: compare own per-prime degrees with the helper's rule.py (imported read-only)."""
import sys, os, json, math
H = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "2026-11-13-rees-headline-below-38"))
sys.path.insert(0, H); os.chdir(H)
import rule
rule.CERTS = rule.load_certs()
raw = json.load(open(os.path.join(H, "tierB.json")))
for k, v in raw.items():
    p, kappa, kind = k.split("|"); rule.TIERB[(int(p), int(kappa), kind)] = v
mine = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "degrees_B_200000.json")))
pmax = int(sys.argv[1])
dis = []
for ps, v in mine.items():
    p = int(ps)
    if p > pmax: continue
    e = rule.degrees(p)
    for k, x in v["e"].items():
        if e[int(k)][0] != x: dis.append((p, int(k), x, e[int(k)][0], v["how"][k], e[int(k)][1]))
dis.sort()
tb = sorted({int(k.split('|')[0]) for k in raw})
print("compared primes <=", pmax, "disagreements:", len(dis))
print("at helper tier-B primes:", [d for d in dis if d[0] in tb])
print("elsewhere (first 40):", [d[:4] for d in dis if d[0] not in tb][:40])
print("all disagreements have mine <= helper:", all(d[2] <= d[3] for d in dis))
print("primes > 523 with disagreement:", [d for d in dis if d[0] > 523][:20])
