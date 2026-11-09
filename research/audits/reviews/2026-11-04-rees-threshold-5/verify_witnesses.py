"""Independent check of FOUND witnesses (famsym / famsearch / dfs2b FEASIBLE lines).
For each witness: p is prime (sympy.isprime), p = 1 (mod K), zeta = g^h has exact order K,
and every cell v = alpha_j + beta_i satisfies v != 0 and v^h = zeta^(-(i+j)) (STRICT
two-level contraction; the labelling Q_m = g^m Q_0 is valid for any coset generator g, and
existence does not depend on it, appendix-schedule2.tex, Section "Two-level contractions").
With --cover K P0 P1 it also checks that every prime p = 1 (mod K) in [P0, P1] has a witness.
With --zeros, a zero cell is also accepted, except at (0,0): that is a (non-strict) two-level
contraction as in the definition of E_2 (entries in A_m = Q_m u {0}, C_00 != 0).  Such
witnesses are counted separately; strict ones remain strict.
Usage: python verify_witnesses.py [--zeros] [--cover K P0 P1] FILE [FILE ...]"""
import re, sys
from sympy import isprime, primerange, primefactors
args = sys.argv[1:]
zeros = False
if args and args[0] == "--zeros":
    zeros = True; args = args[1:]
cover = None
if args and args[0] == "--cover":
    cover = tuple(int(x) for x in args[1:4]); args = args[4:]
pat = re.compile(r"(?:FOUND|FEASIBLE) k=(\d+) p=(\d+) g=(\d+).*beta=([\d,]+) alpha=([\d,]+)")
ok = {}; strict = {}; bad = 0; n = 0
for f in args:
    for line in open(f):
        m = pat.search(line)
        if not m: continue
        K, p, g = int(m.group(1)), int(m.group(2)), int(m.group(3))
        be = [int(x) for x in m.group(4).split(",")]; al = [int(x) for x in m.group(5).split(",")]
        n += 1
        good = isprime(p) and (p - 1) % K == 0 and len(al) == K and len(be) == K
        h = (p - 1) // K
        z = pow(g, h, p)
        good = good and pow(z, K, p) == 1 and all(pow(z, K // q, p) != 1 for q in primefactors(K))
        if good:
            zp = [pow(z, e, p) for e in range(K)]
            nz = 0
            for i in range(K):
                for j in range(K):
                    v = (al[j] + be[i]) % p
                    if v == 0:
                        nz += 1
                        if not zeros or (i, j) == (0, 0):
                            good = False; break
                    elif pow(v, h, p) != zp[(-(i + j)) % K]:
                        good = False; break
                if not good: break
        if good:
            ok[(K, p)] = True
            if nz == 0: strict[(K, p)] = True
        else:
            bad += 1; print("BAD", line.strip()[:120])
print(f"witness lines={n} valid distinct (K,p)={len(ok)} bad={bad}" + (f" (zeros allowed; strict distinct={len(strict)}, with zero cells only={len(set(ok) - set(strict))}: {sorted(p for (_, p) in set(ok) - set(strict))})" if zeros else ""))
if cover:
    K, P0, P1 = cover
    miss = [p for p in primerange(P0, P1 + 1) if p % K == 1 and (K, p) not in ok]
    tot = sum(1 for p in primerange(P0, P1 + 1) if p % K == 1)
    print(f"cover K={K} [{P0},{P1}]: primes={tot} missing={len(miss)} missing list={miss[:300]}")
