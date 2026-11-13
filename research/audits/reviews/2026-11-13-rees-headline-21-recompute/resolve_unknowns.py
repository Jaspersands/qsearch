import sys, time
from rc import RCSearch
S = RCSearch("rc_cache.json")
pmin = int(sys.argv[1]); pmax = int(sys.argv[2]); rt = int(sys.argv[3]); ecap = int(sys.argv[4])
keys = [k for k, v in S.cache.items() if v[0] == "UNKNOWN" and pmin <= int(k.split("|")[0]) <= pmax]
print(len(keys), "unknown entries"); t0 = time.time(); out = {"FOUND": 0, "NONE": 0, "UNKNOWN": 0}
for n, k in enumerate(sorted(keys, key=lambda k: int(k.split("|")[0]))):
    p, D, R, K = k.split("|"); p, D = int(p), int(D)
    R = list(map(int, R.split(","))); K = list(map(int, K.split(",")))
    st, cert = S.query(p, D, R, K, "r", rt, seed=p + 7)
    if st != "FOUND": st, cert = S.query(p, D, R, K, "e", ecap)
    S.cache[k] = [st, cert]; out[st] += 1
    if n % 20 == 0: S.save(); print(n, k, st, round(time.time() - t0, 1), flush=True)
S.save(); print(out, time.time() - t0)
