import sys, time, json
from fp import primes_upto
from rc import RCSearch
from plus import PlusDegrees, grade_sum
PMAX = int(sys.argv[1]); variant = sys.argv[2] if len(sys.argv) > 2 else "B"
S = RCSearch("rc_cache.json")
kw = {}
if variant == "noB": kw["tierB"] = lambda p: False
if variant == "Blift": kw["lift_variant"] = True
if variant == "noS1": kw["no_S1"] = True
PD = PlusDegrees(S, **kw)
t0 = time.time(); rows = {}
for p in primes_upto(PMAX):
    if p < 3: continue
    e, how = PD.degrees(p, want_trace=True)
    rows[p] = (e, how)
    if p % 50 == 1 or p < 100: S.save()
S.save()
res = {}
for c in range(2, 10):
    best, at = 0, []
    for p, (e, how) in rows.items():
        if p <= c: continue
        v = 1 + grade_sum(p, e, c)
        if v > best: best, at = v, [p]
        elif v == best: at.append(p)
    res[c] = (best, at)
    print(c, best, at[:12], len(at))
print("unknowns", len(PD.unknowns), PD.unknowns[:20])
print("time", time.time() - t0)
json.dump({str(p): {"e": {str(k): v for k, v in e.items()}, "how": {str(k): v for k, v in h.items()}} for p, (e, h) in rows.items()},
          open(f"degrees_{variant}_{PMAX}.json", "w"), indent=0)
