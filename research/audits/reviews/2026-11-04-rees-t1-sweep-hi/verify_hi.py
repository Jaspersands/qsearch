"""Independent verifier for the kappa = 8 high sweep (8388608, 117441563].

Shares no code with the C search.  Python ints only for the arithmetic.

Definition checked (strict two-level contraction at p, as in
../2026-11-04-rees-threshold-5.md section 5 and verify_witnesses.py):
  p prime, p = 1 (mod K), h = (p-1)/K, zeta = g^h of exact order K (any such g is a valid
  coset labelling Q_m = g^m Q_0), and for all i, j in 0..K-1 the cell
  v = alpha_j + beta_i (mod p) satisfies v != 0 and v^h = zeta^(-(i+j) mod K).
No zero cells are accepted.

Coverage: every prime p = 1 (mod K) in (LO, HI] must have exactly one valid witness line
(a prime with two lines is reported as DUP even if both are valid; a prime with an invalid
line is reported as BAD).  Primes are enumerated by a numpy sieve of Eratosthenes and the
prime count is cross-checked against sympy.primepi at LO and HI; each witness p is also
checked with gmpy2.is_prime and sympy.isprime.

Usage: python verify_hi.py LO HI CHUNKFILE [FILE ...]
  CHUNKFILE lists "name lo hi" per line (chunk = (lo, hi]); the per-chunk table counts
  primes, valid, bad, dup and missing in each chunk, using all witness FILEs together.
  The script prints X = the largest bound such that every prime p = 1 (mod K) in (LO, X]
  has exactly one valid line and no bad line.
"""
import re
import sys

import gmpy2
import numpy as np
import sympy

K = 8
LO, HI, chunkfile = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
files = sys.argv[4:]

pat = re.compile(r"^FOUND k=(\d+) p=(\d+) g=(\d+) .*beta=([\d,]+) alpha=([\d,]+)\s*$")
valid = {}     # p -> count of valid lines
badp = {}      # p -> count of bad lines
nlines = 0
nbad_unparsed = 0


def check(k, p, g, be, al):
    if k != K or len(al) != K or len(be) != K:
        return False
    if not (gmpy2.is_prime(p) and sympy.isprime(p)) or (p - 1) % K:
        return False
    h = (p - 1) // K
    z = pow(g, h, p)
    # exact order K = 8 = 2^3: z^8 = 1 and z^4 != 1
    if pow(z, K, p) != 1 or any(pow(z, K // q, p) == 1 for q in sympy.primefactors(K)):
        return False
    zp = [pow(z, e, p) for e in range(K)]
    for i in range(K):
        for j in range(K):
            v = (al[j] + be[i]) % p
            if v == 0 or pow(v, h, p) != zp[(-(i + j)) % K]:
                return False
    return True


for f in files:
    for line in open(f):
        if line.startswith("FOUND"):
            nlines += 1
            m = pat.match(line)
            if not m:
                nbad_unparsed += 1
                print("UNPARSED", f, line.strip()[:120])
                continue
            k, p, g = int(m.group(1)), int(m.group(2)), int(m.group(3))
            be = [int(x) for x in m.group(4).split(",")]
            al = [int(x) for x in m.group(5).split(",")]
            if check(k, p, g, be, al):
                valid[p] = valid.get(p, 0) + 1
            else:
                badp[p] = badp.get(p, 0) + 1
                print("BAD", f, line.strip()[:160])

# primes p = 1 (mod 8) in (LO, HI]
sv = np.ones(HI + 1, dtype=bool)
sv[:2] = False
for q in range(2, int(HI ** 0.5) + 1):
    if sv[q]:
        sv[q * q::q] = False
assert int(sv[: LO + 1].sum()) == int(sympy.primepi(LO)), "sieve/primepi mismatch at LO"
assert int(sv.sum()) == int(sympy.primepi(HI)), "sieve/primepi mismatch at HI"
cand = np.nonzero(sv)[0]
cand = cand[(cand > LO) & (cand % K == 1)]
plist = [int(x) for x in cand]

outside = sorted(p for p in set(valid) | set(badp) if not (LO < p <= HI))


def ok(p):
    return valid.get(p, 0) == 1 and badp.get(p, 0) == 0


X = LO
for p in plist:
    if ok(p):
        X = p
    else:
        break
# X is the last prime reached; the claim is for (LO, X'] where X' is just below the next
# prime p = 1 mod 8 that fails (or HI if none fails).
nxt = next((p for p in plist if not ok(p)), None)
Xbound = HI if nxt is None else nxt - 1

print(f"witness FOUND lines={nlines} unparsed={nbad_unparsed} valid distinct p={len(valid)} "
      f"bad lines={sum(badp.values())} lines outside (LO,HI]={len(outside)}")
print(f"{'chunk':<14}{'lo':>11}{'hi':>11}{'primes':>9}{'valid':>9}{'bad':>6}{'dup':>6}{'missing':>9}")
tot = [0, 0, 0, 0, 0]
for cl in open(chunkfile):
    if not cl.strip() or cl.startswith("#"):
        continue
    name, lo, hi = cl.split()[:3]
    lo, hi = int(lo), int(hi)
    ps = [p for p in plist if lo < p <= hi]
    nv = sum(1 for p in ps if ok(p))
    nb = sum(1 for p in ps if badp.get(p, 0))
    nd = sum(1 for p in ps if valid.get(p, 0) > 1)
    nm = sum(1 for p in ps if valid.get(p, 0) == 0 and not badp.get(p, 0))
    for t, x in enumerate((len(ps), nv, nb, nd, nm)):
        tot[t] += x
    print(f"{name:<14}{lo:>11}{hi:>11}{len(ps):>9}{nv:>9}{nb:>6}{nd:>6}{nm:>9}")
print(f"{'TOTAL':<14}{LO:>11}{HI:>11}{tot[0]:>9}{tot[1]:>9}{tot[2]:>6}{tot[3]:>6}{tot[4]:>9}")
print(f"primes p=1 mod {K} in ({LO},{HI}]: {len(plist)}")
print(f"first failing prime: {nxt}; last prime of the contiguous verified run: {X}")
print(f"CONTIGUOUS: every prime p=1 mod {K} in ({LO},{Xbound}] has exactly one valid strict witness")
