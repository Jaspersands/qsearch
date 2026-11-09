# s2a: exponent of m in the query count under the combined rule (Remark rem:combined-schedule),
# maximised over primes p > c, against Schedule 1 (exponent 1 + sum_d d*ceil(log2(d+1))).
# Above 16*3^8 every grade with kappa_d in {2,3} uses Schedule 2 and the sum only drops
# (e_d <= kappa_d ceil(log2(kappa_d+1)) always), so primes up to 2e5 suffice for the maximum.
import math, sympy
def clog(x): return math.ceil(math.log2(x))
def e(d, p):
    k = math.gcd(d, p-1)
    if k == 1: return 1
    if p >= 16*k**(2*k+2): return 2
    return k*clog(k+1)
primes = list(sympy.primerange(2, 200000))
for c in range(2, 10):
    s1 = 1 + sum(d*clog(d+1) for d in range(2, c+1))
    best = max((1 + sum(e(d, p) for d in range(2, c+1)), p) for p in primes if p > c)
    print("c =", c, " Schedule 1 exponent:", s1, " combined max:", best[0], " at p =", best[1], " drop:", s1 - best[0])
