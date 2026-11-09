"""Closed form for the F_5 WNEST guarantee.  N(q) = min{N : N - (5/4) q >= 15/4 + sqrt(N)}.
Claim: N(q) <= (5/4) q + sqrt(2q) + 7 for q >= 3 (since then sqrt(N) <= sqrt(2q)), per-piece cost
<= (4/5) N + (4/5) sqrt(N) <= q + (8/5) sqrt(2q)... ; guarantee(n) <= n^2/4 + C n^{3/2} + ... ; checked
against the exact recursion for 3 <= n < 3000."""
import math
from wnest_p import pool_size, guarantee
p = 5
bad = []
for q in range(3, 3000):
    N = pool_size(p, q)
    if not N <= 1.25 * q + math.sqrt(2 * q) + 7:
        bad.append((q, N))
    if not 1.25 * q + math.sqrt(2 * q) + 7 <= 2 * q + 10:  # ensures sqrt(N) <= sqrt(2q+10)
        bad.append(('ineq', q))
print('N(q) <= 1.25 q + sqrt(2q) + 7 for 3 <= q < 3000:', not bad, bad[:3])
# per piece: cost <= floor(0.8 N + 0.8 sqrt N); sum over q = n, n-2, ..., >= 3 ; plus 1-d rounds and pool
def closed(n):
    return n * n / 4 + 2.0 * n ** 1.5 + 12 * n + 40
viol = [n for n in range(3, 3000) if guarantee(p, n)[0] > closed(n)]
print('guarantee(n) <= n^2/4 + 2 n^{3/2} + 12 n + 40 for 3 <= n < 3000:', not viol, viol[:5])
for n in (10, 30, 100, 300, 1000, 2999):
    print(f'  n={n}: guarantee {guarantee(p, n)[0]}  closed {closed(n):.0f}')
