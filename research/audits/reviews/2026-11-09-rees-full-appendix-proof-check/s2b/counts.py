"""s2b: primality/residue of every prime quoted in appendix-schedule2.tex 559-729 and
main.tex 721, and the prime counts quoted there (consistency only; the E_2(8)/E_2(9)
verdicts themselves are not re-derived)."""
import numpy as np
from sympy import isprime

out = []
def say(s):
    print(s, flush=True); out.append(s)

quoted = {
    4: [5, 13, 17, 29, 37, 53, 61],
    5: [11, 31, 41, 61, 71, 101, 131, 151, 181, 191, 211, 241, 251],
    6: [7, 13, 19, 31, 43, 67, 859, 223],
    7: [29, 43, 71, 113, 3221],
    8: [17, 41, 73, 89, 137, 233, 761, 14281, 16993, 9473, 9769, 6073, 49417, 22921, 25321, 26681, 26713],
    9: [19, 37, 73, 109, 127, 163, 181, 199, 307, 433, 20107, 16633, 17623, 20071, 20089, 424549, 651727, 6067],
    10: [3361, 3761, 5821, 8191],
    12: [10453],
}
bad = []
for k, ps in quoted.items():
    for p in ps:
        if not isprime(p) or p % k != 1:
            bad.append((k, p, isprime(p), p % k))
say("quoted primes that are not primes = 1 mod kappa: %s" % (bad if bad else "none"))

N = 9**9 // 2 + 2
sieve = np.ones(N + 1, dtype=bool); sieve[:2] = False; sieve[4::2] = False
for i in range(3, int(N**0.5) + 1, 2):
    if sieve[i]: sieve[i*i::2*i] = False
pr = np.flatnonzero(sieve)
def cnt(k, lo, hi):   # primes p = 1 mod k with lo < p <= hi
    a = pr[(pr > lo) & (pr <= hi)]
    return int((a % k == 1).sum())
say("primes = 1 mod 8 below 2442: %d ; = 1 mod 9 below 3584: %d   (paper: 83, 83)" % (cnt(8, 0, 2441), cnt(9, 0, 3583)))
say("primes = 1 mod 8 below 4202: %d ; = 1 mod 9 below 5690: %d   (paper: 137, 122)" % (cnt(8, 0, 4201), cnt(9, 0, 5689)))
say("primes = 1 mod 8 in (9769,20000]: %d ; in (16993,20000]: %d ; in (9769,16993]: %d  (paper: 145 undecided on 4 Nov in (9769,20000])" % (
    cnt(8, 9769, 20000), cnt(8, 16993, 20000), cnt(8, 9769, 16993)))
say("primes = 1 mod 8 in (20000,49417]: %d" % cnt(8, 20000, 49417))
say("primes = 1 mod 8 in (8^8/2, 117441563]: %d   (paper: 1534715)" % cnt(8, 8**8 // 2, 117441563))
say("primes = 1 mod 9 in (20000, 9^9/2]: %d   (paper: 1791117)" % cnt(9, 20000, 9**9 // 2))
say("8^8/2 = %d, 9^9/2 = %.1f" % (8**8 // 2, 9**9 / 2))
say("14281 / 8^4.5 = %.4f ; 20107 / 9^5 = %.4f" % (14281 / 8**4.5, 20107 / 9**5))
open(__file__.replace('.py', '.out'), 'w').write("\n".join(out) + "\n")
