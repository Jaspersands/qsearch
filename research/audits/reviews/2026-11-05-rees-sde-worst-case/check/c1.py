import sys, math
sys.path.insert(0, "..")
sys.setrecursionlimit(10000)
from sss import worst_forward_cost
# thresholds
for k, den in ((2, 10), (3, 54)):
    E = 3
    p = 2
    while True:
        if k**-E * (p - E - (k**E - 1) * (E - 1) * math.sqrt(p)) >= p / den:
            break
        p += 1
    print("kappa", k, "Lemma W >= p/%d from p =" % den, p)
# greedy loss vs ceil(r/(E-1))
def ME(a, E):
    q, M = a, 0
    while q >= 1:
        M += q + 1; q -= min(E - 1, q)
    return M + 1
bad = []
for E in range(2, 13):
    memo = {}
    for r in range(1, 301):
        D = worst_forward_cost(r, E, memo)
        if D - (ME(r, E) - 1) > -(-r // (E - 1)):
            bad.append((E, r, D - (ME(r, E) - 1)))
print("greedy loss > ceil(r/(E-1)):", bad[:10], len(bad))
# D_E(a)+a <= a^2/(2(E-1)) + 4a ?
bad = [(E, a) for E in range(2, 13) for a in range(1, 301)
       if worst_forward_cost(a, E, {}) + a > a * a / (2 * (E - 1)) + 4 * a + 1e-9]
print("D_E(a)+a > a^2/(2(E-1))+4a:", bad[:5], len(bad))
# stalled bank
p = 1009
B = [[170,720,640],[72,522,340],[337,384,757],[512,970,855],[724,989,767],[14,606,963],[823,827,687],[966,829,143],[854,768,10]]
x = [0, 0, 0, 0, 442, 0, 0, 0, 1]
print("residual", [sum(x[i]*B[i][t] for i in range(9)) % p for t in range(3)], "442 QR:", pow(442, (p-1)//2, p))
from sss import Field, forward_swap, rank
Fd = Field(p, 2)
import random
rng = random.Random(0)
res = []
for i in range(len(B)):
    pass
reserve, bas = [], []
from sss import solve_in_span
for i in range(9):
    if solve_in_span(bas, B[i], p) is None:
        bas.append(B[i]); reserve.append(i)
for rule in ("first",):
    out = forward_swap(Fd, B, 3, rng, reserve, rule)
    print("stalled bank forward:", out["status"], "pool", out["pool"], "dimU", len(out.get("U", [])), "B", out.get("B"), "swaps", out.get("swaps"))
# GP arc bound sanity: Bush bound M <= p + r - 1 => p >= D_3(r)+1
for a in (4, 10, 20, 50, 100):
    M = worst_forward_cost(a, 3, {}) + a
    print("a=%d budget M=%d needs p >= M-a+1 = %d (Bush); 20a=%d" % (a, M, M - a + 1, 20 * a))
