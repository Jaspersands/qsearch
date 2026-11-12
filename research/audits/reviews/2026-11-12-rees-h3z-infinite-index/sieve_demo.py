"""Classical binary zero-sum sieve on central characters theta_i in R/Z (exact
rationals k/2^P).  Goal: disjoint subsets S with ||sum_S theta_i|| <= 2^-K.
Each level pairs x with y such that x + y falls into a 2^{-b}-times smaller window
(sums only: every theta gets coefficient 0 or 1, as the twist requires).
Reports samples used, subset size 2^levels, and achieved |Theta|.  Finite demo of the
2^{O(sqrt K)} scaling only.  Usage: nice -n 19 /opt/anaconda3/bin/python sieve_demo.py
"""
import random, math
P = 200
def sieve(K, levels, n, rng):
    # elements: (value in Z/2^P as centered int, size)
    L = [(rng.randrange(2**P), 1) for _ in range(n)]
    cen = lambda v: v - 2**P if v >= 2**(P-1) else v
    L = [(cen(v), s) for v, s in L]
    width = 2**(P-1)             # |value| <= width
    step = math.ceil(K / levels)
    for lev in range(levels):
        new_w = max(width >> step, 2**(P - K))
        nb = width // new_w      # buckets of size new_w over [-width, width]
        buckets = {}
        for v, s in L: buckets.setdefault(math.floor(v / new_w), []).append((v, s))
        out = []
        for key in list(buckets):
            mate = -key - 1      # v in [key*nw,(key+1)nw), u in [(-key-1)nw,-key nw) -> |v+u| < nw
            A, B = buckets.get(key, []), buckets.get(mate, [])
            if key == mate:
                while len(A) >= 2:
                    (v, s), (u, t) = A.pop(), A.pop(); out.append((v + u, s + t))
            elif key < mate:
                while A and B:
                    (v, s), (u, t) = A.pop(), B.pop(); out.append((v + u, s + t))
        L = [(v, s) for v, s in out if abs(v) <= new_w]
        width = new_w
        if not L: return 0, None
    best = min(L, key=lambda e: abs(e[0]))
    return len(L), best

rng = random.Random(5)
print(' K  levels  samples   survivors  subset_size  log2|Theta|')
for K in (16, 24, 32, 40, 48):
    lv = max(1, round(math.sqrt(K)))
    n = 2**(lv + math.ceil(K / lv) + 3)
    cnt, best = sieve(K, lv, n, rng)
    if best: print(f'{K:3d} {lv:5d} {n:10d} {cnt:9d} {best[1]:10d}   {math.log2(abs(best[0])+1e-300) - P:8.1f}')
    else: print(f'{K:3d} {lv:5d} {n:10d}   none')
