"""Headline-20 referee: re-verify every certificate the schedule uses (author's certs_stage1.json
for TL3/TL4/TL5/TW9/U7 and v2/certs_tl6_all.json for TL6) with this referee's own checker
(verify_tl6.dclass/lpr), and save the accepted sets for plus2.py."""
import json
from verify_tl6 import lpr, dclass, isprime
A = "../2026-11-13-rees-headline-below-38/"
def check(p, D, R, K, alpha, beta, xi):
    K = {x % D for x in K}
    if 0 not in R or 0 not in K or len(alpha) != D or sorted(beta) != sorted(R): return False
    s = (alpha[0] + beta[0]) % p
    if s == 0 or dclass(s, p, D, xi) != 0: return False
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v and (dclass(v, p, D, xi) + i + j) % D not in K: return False
    return True
st = json.load(open(A + "certs_stage1.json"))
spec = {"two-level 3": ("TL3", 3, [0, 1, 2]), "two-level 4": ("TL4", 4, [0, 1, 2, 3]), "two-level 5": ("TL5", 5, list(range(5))),
        "tower (9;{0,3,6})": ("TW9", 9, [0, 3, 6]), "union (7;Z7->{0,m})": ("U7", 7, list(range(7)))}
out = {}
for key, (name, D, R) in spec.items():
    e = st[key]; assert e["D"] == D and sorted(e["R"]) == R
    acc = {}; rej = 0
    for ps, c in e["found"].items():
        p = int(ps); assert isprime(p) and (p - 1) % D == 0 and p < e["bound"]
        xi = lpr(p); assert c["g"] == xi
        K = c["K"]
        if name != "U7": assert K == [0]
        else: assert len(K) == 2 and K[0] == 0
        beta = {int(k): v for k, v in c["beta"].items()}
        if check(p, D, R, K, c["alpha"], beta, xi): acc[p] = K[1] if name == "U7" else 1
        else: rej += 1
    allp = [q for q in range(D + 1, e["bound"], D) if isprime(q)]
    miss = [q for q in allp if q not in acc]
    out[name] = {str(p): v for p, v in acc.items()}
    print(f"{name}: bound {e['bound']}, primes {len(allp)}, accepted {len(acc)}, rejected {rej}, uncovered {len(miss)} {miss[:20]}")
t6 = json.load(open(A + "v2/certs_tl6_all.json"))
acc = {}
for ps, c in t6["found"].items():
    p = int(ps); xi = lpr(p)
    if check(p, 6, list(range(6)), [0], c["alpha"], {int(k): v for k, v in c["beta"].items()}, xi): acc[p] = 1
out["TL6"] = {str(p): 1 for p in acc}
print("TL6 accepted", len(acc))
json.dump(out, open("certs_accepted.json", "w"))
