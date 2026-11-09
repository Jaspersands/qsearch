"""Independent verifier for the kappa = 9 sweep over (LO, HI].

Adapted from ../2026-11-04-rees-t1-sweep-hi/verify_hi.py (shares no code with the C
searches; Python ints only for the arithmetic).  Changes: K = 9; FEASIBLE lines (dfs2b)
are parsed as well as FOUND lines; non-strict witnesses (zero cells, e.g. the P family)
are accepted as contractions in the sense of E_2 and counted separately; INFEASIBLE lines
from dfs2b and UNRESOLVED/NOTFOUND primes are reported as the exception list.

Definition checked for a witness line (K, p, g, beta, alpha):
  p prime (gmpy2 and sympy), p = 1 (mod K), h = (p-1)/K, zeta = g^h of exact order K
  (any such g is a valid coset labelling Q_m = g^m Q_0), and for every cell (i, j),
  v = alpha_j + beta_i (mod p):
    STRICT:     v != 0 and v^h = zeta^(-(i+j) mod K)  for all K^2 cells;
    NON-STRICT: v = 0 is allowed except at (0,0); every nonzero v has v^h = zeta^(-(i+j)).
  A non-strict witness is a two-level contraction as in the definition of E_2 (entries in
  A_m = Q_m u {0}, cell (0,0) nonzero), so it shows p notin E_2(K); a strict one also shows
  the strict count N > 0.

Coverage: a prime p = 1 (mod K) in (LO, HI] is COVERED if it has at least one valid line
and no bad line.  Duplicated valid lines are reported (dup) but do not fail coverage
(the retry chain and dfs2b can both certify a prime).  Primes are enumerated by a numpy
sieve cross-checked against sympy.primepi at LO and HI.

Usage: python verify_k9.py LO HI CHUNKFILE [FILE ...]
Prints per-chunk table, X = largest bound such that every prime p = 1 (mod 9) in (LO, X]
is covered or listed in the exception list E (primes with no witness), and E itself, split
into INFEASIBLE (dfs2b complete search) and OPEN (no witness, no decision).  Also prints
the plain contiguous bound X0 with no exceptions.
"""
import re
import sys

import gmpy2
import numpy as np
import sympy

K = 9
LO, HI, chunkfile = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
files = sys.argv[4:]

pat = re.compile(r"^(?:FOUND|FEASIBLE) k=(\d+) p=(\d+) g=(\d+) .*beta=([\d,]+) alpha=([\d,]+)\s*$")
pinf = re.compile(r"^INFEASIBLE k=(\d+) p=(\d+) ")
valid = {}      # p -> number of valid lines
strictp = set()
badp = {}
infeas = set()
nlines = 0
nunparsed = 0


def check(k, p, g, be, al):
    """returns 'strict', 'nonstrict' or None"""
    if k != K or len(al) != K or len(be) != K:
        return None
    if not (gmpy2.is_prime(p) and sympy.isprime(p)) or (p - 1) % K:
        return None
    h = (p - 1) // K
    z = pow(g, h, p)
    # exact order 9 = 3^2: z^9 = 1 and z^3 != 1
    if pow(z, K, p) != 1 or any(pow(z, K // q, p) == 1 for q in sympy.primefactors(K)):
        return None
    zp = [pow(z, e, p) for e in range(K)]
    nz = 0
    for i in range(K):
        for j in range(K):
            v = (al[j] + be[i]) % p
            if v == 0:
                if i == 0 and j == 0:
                    return None
                nz += 1
            elif pow(v, h, p) != zp[(-(i + j)) % K]:
                return None
    return "strict" if nz == 0 else "nonstrict"


for f in files:
    for line in open(f):
        m0 = pinf.match(line)
        if m0 and int(m0.group(1)) == K:
            infeas.add(int(m0.group(2)))
            continue
        if line.startswith("FOUND") or line.startswith("FEASIBLE"):
            nlines += 1
            m = pat.match(line)
            if not m:
                nunparsed += 1
                print("UNPARSED", f, line.strip()[:120])
                continue
            k, p, g = int(m.group(1)), int(m.group(2)), int(m.group(3))
            be = [int(x) for x in m.group(4).split(",")]
            al = [int(x) for x in m.group(5).split(",")]
            r = check(k, p, g, be, al)
            if r:
                valid[p] = valid.get(p, 0) + 1
                if r == "strict":
                    strictp.add(p)
            else:
                badp[p] = badp.get(p, 0) + 1
                print("BAD", f, line.strip()[:160])

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
del sv, cand


def ok(p):
    return valid.get(p, 0) >= 1 and badp.get(p, 0) == 0


conflict = sorted(p for p in infeas if valid.get(p, 0))
nxt0 = next((p for p in plist if not ok(p)), None)
X0 = HI if nxt0 is None else nxt0 - 1
# X: exceptions allowed, but a BAD line (or a witness contradicting INFEASIBLE) stops it.
# A prime with no line at all is an exception only if it is at or below the last prime
# that has some line (otherwise the sweep simply has not reached it).
seen = set(valid) | set(badp) | infeas
for f in files:
    for line in open(f):
        if line.startswith("NOTFOUND") or line.startswith("UNRESOLVED"):
            mm = re.search(r" p=(\d+)", line)
            if mm:
                seen.add(int(mm.group(1)))
exc = []
X = LO
for p in plist:
    if ok(p) and p not in infeas:
        X = p
        continue
    if badp.get(p, 0) or p in conflict or p not in seen:
        break
    exc.append(p)
    X = p
nxt = next((p for p in plist if p > X), None)
Xbound = HI if nxt is None else nxt - 1
if nxt is not None and (badp.get(nxt, 0) or nxt in conflict):
    pass

print(f"witness lines={nlines} unparsed={nunparsed} valid distinct p={len(valid)} "
      f"(strict {len(strictp & set(valid))}, non-strict only {len(set(valid) - strictp)}) "
      f"bad lines={sum(badp.values())} INFEASIBLE lines (K=9)={len(infeas)} witness-vs-INFEASIBLE conflicts={conflict}")
print(f"{'chunk':<14}{'lo':>11}{'hi':>11}{'primes':>9}{'covered':>9}{'strict':>9}{'bad':>6}{'dup':>6}{'nowit':>7}")
tot = [0] * 6
for cl in open(chunkfile):
    if not cl.strip() or cl.startswith("#"):
        continue
    name, lo, hi = cl.split()[:3]
    lo, hi = int(lo), int(hi)
    ps = [p for p in plist if lo < p <= hi]
    row = (len(ps), sum(1 for p in ps if ok(p)), sum(1 for p in ps if ok(p) and p in strictp),
           sum(1 for p in ps if badp.get(p, 0)), sum(1 for p in ps if valid.get(p, 0) > 1),
           sum(1 for p in ps if valid.get(p, 0) == 0 and not badp.get(p, 0)))
    for t, x in enumerate(row):
        tot[t] += x
    print(f"{name:<14}{lo:>11}{hi:>11}" + "".join(f"{x:>{w}}" for x, w in zip(row, (9, 9, 9, 6, 6, 7))))
print(f"{'TOTAL':<14}{LO:>11}{HI:>11}" + "".join(f"{x:>{w}}" for x, w in zip(tot, (9, 9, 9, 6, 6, 7))))
print(f"primes p=1 mod {K} in ({LO},{HI}]: {len(plist)}")
nonstrict_in = sorted(p for p in valid if p not in strictp and LO < p <= Xbound and ok(p))
print(f"non-strict-only witnesses in ({LO},{Xbound}]: {len(nonstrict_in)}: {nonstrict_in}")
print(f"exceptions in ({LO},{Xbound}] (no witness): {len(exc)}; of these dfs2b INFEASIBLE: "
      f"{len([p for p in exc if p in infeas])}: {[p for p in exc if p in infeas]}")
print(f"OPEN (no witness, no dfs2b decision): {[p for p in exc if p not in infeas]}")
print(f"STRICT-OR-NOT, NO EXCEPTIONS: every prime p=1 mod {K} in ({LO},{X0}] has a valid witness (first gap {nxt0})")
print(f"CONTIGUOUS: every prime p=1 mod {K} in ({LO},{Xbound}] has a valid witness or is one of the {len(exc)} listed exceptions")
