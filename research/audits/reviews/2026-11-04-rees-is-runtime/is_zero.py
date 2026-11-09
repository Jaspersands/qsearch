"""Rounds and field-op cost of zero_sum_of_powers vs Z_bound. Run with python -O."""
import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import is_count as C, is_bound as B
S = C.S
calls = [0]
orig = S.selective_root
def sre(*a, **k):
    calls[0] += 1
    return orig(*a, **k)
S.selective_root = sre
worst_r, worst_c, n = 0, 0, 0
primes = [p for p in range(3, 4000) if S.fmpz(p).is_prime()] + [65537, 786433, 536870951, 536871001, 2**61-1, 29*2**57+1, 3*2**30+1]
for p in primes:
    for k in (2, 4, 6, 8, 12):
        if (p-1) % k:
            continue
        C.reset(); C.P[0] = p; calls[0] = 0
        z = S.zero_sum_of_powers(p, k)
        m = sum(C.MUL.values()) + sum(C.pow_mults(v)[0] + C.pow_mults(v)[1] for v in C.POWS.values())
        b = p.bit_length(); nu = C.nu(p, k)
        rb = math.ceil((k+1)*math.log(2)*b) + k + 2
        zb = B.Z_bound(k, b, nu)
        if calls[0] > rb or m > zb:
            print("FAIL", p, k, calls[0], rb, m, zb)
        worst_r = max(worst_r, calls[0]/rb); worst_c = max(worst_c, m/zb); n += 1
print(f"{n} (p,k) pairs; max SRE-rounds/round-bound = {worst_r:.3f}; max field-ops/Z_bound = {worst_c:.3f}")
for p, k in ((2**61-1, 2), (29*2**57+1, 8), (3*2**30+1, 6), (65537, 8)):
    C.reset(); C.P[0] = p; calls[0] = 0
    z = S.zero_sum_of_powers(p, k)
    m = sum(C.MUL.values()) + sum(C.pow_mults(v)[0] + C.pow_mults(v)[1] for v in C.POWS.values())
    print(f"  p={p} k={k} b={p.bit_length()} nu={C.nu(p,k)} t={len(z)} SRE rounds={calls[0]} field ops={m} Z_bound={B.Z_bound(k, p.bit_length(), C.nu(p,k))}")
