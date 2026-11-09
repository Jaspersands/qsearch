"""Exact recursion vs closed form for both variants (proof: WNEST q>=4, KOW pool q+1; code:
wnest.py's WNEST at q>=3), 4 <= n < 3000, with a fast pool_size; per-piece caps vs q+2."""
import math
from strict_wnest import piece_cap, closed_form
def pool_size(q):
    N = max(1, math.floor(1.5 * q))
    while not (2 * N - 3 * q - 6 >= 0 and (2 * N - 3 * q - 6) ** 2 >= 4 * N):
        N += 1
    return N
def guarantee(n, variant):
    consumed, best, q = 0, 0, n
    qmin = 4 if variant == "proof" else 3
    while q > 0:
        if q >= qmin:
            N = pool_size(q); best = max(best, consumed + N); consumed += piece_cap(N); q -= 2
        else:
            best = max(best, consumed + q + 1); consumed += q + 1; q -= 1
    return max(best, consumed + 1)
mn = {}
viol = []
for n in range(4, 3000):
    for var in ("proof", "code"):
        s = closed_form(n) - guarantee(n, var)
        if var not in mn or s < mn[var][0]: mn[var] = (round(s, 2), n)
        if s < 0: viol.append((n, var))
print("min closed_form(n) - guarantee(n) over 4<=n<3000:", mn, "violations:", viol)
print("guarantee(code) - guarantee(proof), n=4..21:", [guarantee(n, "code") - guarantee(n, "proof") for n in range(4, 22)])
print("pool_size(q) <= 1.5q+2sqrt(q)+6 for 4<=q<3000:", all(pool_size(q) <= 1.5 * q + 2 * math.sqrt(q) + 6 for q in range(4, 3000)))
print(" q    N(q)  cap=floor(2N/3+2sqrtN/3)  q+2   q+(8/3)sqrt q+4   cap-(q+2)")
for q in (3, 4, 5, 6, 8, 10, 16, 20, 30, 40, 60, 100, 200, 1000):
    N = pool_size(q); print(f"{q:4d} {N:6d} {piece_cap(N):8d}              {q+2:5d}  {q+8/3*math.sqrt(q)+4:9.2f}      {piece_cap(N)-(q+2)}")
