"""Variant: published Ivanyos-confirmed depth ceil(log2(kappa+1)) for the IS node (no lem:rounds),
plus the half-degree collision descent (Lemmas S/F).  Exact for p <= PMAX, residue formula above."""
import sys, math
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import s1h_independent as S
S.S1t_deg = lambda F, k: 1 if k == 1 else k * math.ceil(math.log2(k + 1))
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
worst = {}
for p in S.primes_upto(PMAX):
    if p < 3: continue
    e, pl = S.e_table(S.Field(p))
    for c, v in S.exponents(p, e).items():
        if c not in worst or v > worst[c][0]: worst[c] = [v, [p]]
        elif v == worst[c][0] and len(worst[c][1]) < 5: worst[c][1].append(p)
print('published depth + HCD, exact p <=', PMAX, {c: worst[c] for c in sorted(worst)})
# tail: kappa_d from p mod 2520; e(k) = min(k*ceil(log2(k+1)), e(k/2)+1) (Weil: F1 after one stage)
tail = {}
for r in range(1, 2520):
    if math.gcd(r, 2520) != 1: continue
    pm1 = (r - 1) % 2520 or 2520; e = {}
    for k in range(1, 10):
        if pm1 % k: continue
        e[k] = 1 if k == 1 else min(k * math.ceil(math.log2(k + 1)), e[k // 2] + 1 if k % 2 == 0 else 10**9)
    for c in range(2, 10):
        v = 1 + sum(e[math.gcd(d, pm1)] for d in range(2, c + 1))
        if c not in tail or v > tail[c][0]: tail[c] = [v, r]
print('tail max over units mod 2520:', tail)
