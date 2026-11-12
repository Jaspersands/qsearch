# Referee: Outlook "Halving at the confirmed depth" (95): Schedule 1H with candidate (a) at the full
# depth ceil(log2(kappa+1)) instead of L = ceil(log2 t). Rule D otherwise. Exact to LIM + residue tail.
import math, sys, json
sys.path.insert(0, '.')
import s1h_referee as R
LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
orig_t = R.t_value
def t_full(add0, m1, k):
    orig_t(add0, m1, k)          # still computed (sanity: Chevalley-Warning)
    return k + 1                 # ceil(log2(t)) then equals ceil(log2(k+1))
R.t_value = t_full
best, at = -1, []
for p in R.primes_upto(LIM):
    if p <= 9: continue
    o = R.S1H(p, "D")
    tot = 1 + sum(o.info[math.gcd(d, p - 1)]["e"] for d in range(2, 10))
    if tot > best: best, at = tot, [p]
    elif tot == best: at.append(p)
def e_tail(k):
    if k == 1: return 1
    e = k * math.ceil(math.log2(k + 1))
    if k % 2 == 0: e = min(e, e_tail(k // 2) + 1)
    return e
tail = max(1 + sum(e_tail(math.gcd(d, r - 1)) for d in range(2, 10)) for r in range(1, 2520) if math.gcd(r, 2520) == 1)
print(json.dumps({"LIM": LIM, "max_exact": best, "attained": at[:10], "n_att": len(at), "tail_max": tail}))
