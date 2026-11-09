"""Chart readout from Fourier samples: column selection modulo p is NOT enough.

G = C_9 x C_3 (p=3, class 1 < p, exponent 9 = p^e exactly), generators
g1=(1,0), g2=(0,1); F = (Z/9)^2, pi(u) = (u1 mod 9, u2 mod 3).
Samples are uniform on (ker pi)^perp; Y = sample matrix (k x d).
The chart F/ker pi is isomorphic to im Y = Y F (order 27).
Rule A ("choose Hall columns whose Y-columns span im Y mod p", the argued step
in 2026-11-02-rees-bb-envelope.md section 2.4) selects only column 1: order 9.
Rule B (greedy: add column j iff Y_j is not in the subgroup generated so far)
selects both: order 27. Rule B needs at most log_p|A| additions.
"""
import random
from itertools import product

random.seed(1)
p, M, d = 3, 9, 2
F = list(product(range(M), repeat=d))
ker = [u for u in F if (u[0] % 9, u[1] % 3) == (0, 0)]
perp = [a for a in F if all((a[0]*u[0] + a[1]*u[1]) % M == 0 for u in ker)]
k = 6
Y = [random.choice(perp) for _ in range(k)]
cols = [tuple(Y[i][j] for i in range(k)) for j in range(d)]

def span(vecs):
    S, fr = {(0,)*k}, [(0,)*k]
    while fr:
        nf = []
        for s in fr:
            for v in vecs:
                t = tuple((a+b) % M for a, b in zip(s, v))
                if t not in S:
                    S.add(t); nf.append(t)
        fr = nf
    return S

A = span(cols)
print("|ker pi| =", len(ker), " |F/ker pi| =", len(F)//len(ker), " |im Y| =", len(A))
# Rule A: Gaussian elimination mod p on the columns
def rank_mod_p(vecs):
    rows = [list(x % p for x in v) for v in vecs]
    r = 0
    for c in range(k):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], -1, p)
        rows[r] = [x*inv % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [(x - f*y) % p for x, y in zip(rows[i], rows[r])]
        r += 1
    return r
chosen, cur = [], 0
for j in range(d):
    if rank_mod_p([cols[i] for i in chosen] + [cols[j]]) > cur:
        chosen.append(j); cur += 1
print("Rule A (mod p span) picks columns", chosen, "-> generated order", len(span([cols[j] for j in chosen])))
chosenB, S = [], {(0,)*k}
for j in range(d):
    if cols[j] not in S:
        chosenB.append(j); S = span([cols[i] for i in chosenB])
print("Rule B (greedy membership) picks columns", chosenB, "-> generated order", len(S))
assert len(span([cols[j] for j in chosen])) < len(A) == len(S) == 27
