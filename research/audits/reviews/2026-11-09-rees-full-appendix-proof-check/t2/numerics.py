"""t2 check 4: numbers in lem:tb-count-exponent, thm:bb-envelope, rem:tb-scope, lem:tb-sylow,
and the comparison remark (main.tex 1336-1339).  Finite computation."""
import math
import numpy as np
from sympy import isprime, mobius, divisors

out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

say("421, 2521, 55441 prime:", isprime(421), isprime(2521), isprime(55441), "; 841 =", 29 * 29)
lcm = lambda c: math.lcm(*range(2, c + 1))
say("lcm(2..c), c=2..13:", [lcm(c) for c in range(2, 14)], "; 16*3^8 =", 16 * 3 ** 8,
    "; 16*d^(2d+2), d=2..5:", [16 * d ** (2 * d + 2) for d in range(2, 6)])
E1 = {c: 1 + sum(d * math.ceil(math.log2(d + 1)) for d in range(2, c + 1)) for c in range(2, 10)}
say("E_1(c), c=2..9:", [E1[c] for c in range(2, 10)])

# E_W(c) by enumeration of all primes c < p <= 2e7 under the combined rule
# (kappa_d = gcd(d, p-1); linear if kappa = 1; two-level if kappa >= 2 and p >= 16 kappa^(2kappa+2);
#  else Schedule 1 at degree kappa).  Above 2e7 > 16*4^10 every grade with kappa in {2,3,4} is
# two-level, so 1 + sum e_d is then at most E_1(c) - 16 for c >= 4 and E_1(c) - 6 for c = 3.
N = 20_000_000
sieve = np.ones(N + 1, dtype=bool); sieve[:2] = False
for i in range(2, int(N ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = False
P = np.nonzero(sieve)[0]
def e_d(d, p):
    k = np.gcd(d, p - 1)
    sched1 = k * np.ceil(np.log2(k + 1)).astype(np.int64)
    out = np.where(k == 1, 1, np.where(p >= 16 * k.astype(object) ** (2 * k + 2) if False else (p >= 16 * np.power(k.astype(np.float64), 2 * k + 2)), 2, sched1))
    return out
EW, arg = {}, {}
for c in range(2, 10):
    Pc = P[P > c]
    tot = 1 + sum(e_d(d, Pc) for d in range(2, c + 1))
    i = int(np.argmax(tot)); EW[c] = int(tot[i]); arg[c] = int(Pc[i])
say("E_W(c), c=2..9 (primes <= 2e7):", [EW[c] for c in range(2, 10)], "first maximizer:", [arg[c] for c in range(2, 10)])
say("paper: E_W = 5, 11, 23, 38, 56, 77, 107, 143; witnesses 3, 7, 13, 61, 61, 421, 2521, 2521")

# K_9 and log2(9 K_9)
lk = sum(d * (d - 1) * math.ceil(math.log2(d + 1)) / 2 * math.log2(d) for d in range(2, 10))
say("log2(9 K_9) =", round(math.log2(9) + lk, 2))

# rank of F_{4,9}
def rank(s, c):
    return sum(sum(mobius(j) * s ** (k // j) for j in divisors(k)) // k for k in range(1, c + 1))
say("rank F_{4,9} =", rank(4, 9), "; rank F_{2,2}, F_{2,3}, F_{3,2} =", rank(2, 2), rank(2, 3), rank(3, 2))

# lem:tb-sylow pair success constant
v = (4 / math.pi ** 2) ** 2 * 6 / math.pi ** 2 - 1 / 200
say("(4/pi^2)^2 * 6/pi^2 - 1/200 =", round(v, 5), "> 1/11 =", round(1 / 11, 5), v > 1 / 11)

# comparison remark: sigma_p and 2 + 8 sigma_p at c = 9
sig = {2: 1}
for p in (3, 5, 7):
    sig[p] = 2 ** math.floor(math.log2((p - 1) / 2)) * math.ceil(math.log2(p))
say("sigma_p:", sig, "; exponents 2 + 8 sigma_p:", {p: 2 + 8 * s for p, s in sig.items()})
open(__file__.replace(".py", ".out"), "w").write("\n".join(out) + "\n")
