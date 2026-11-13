"""Exhaustive RC(6;Z6->{0}) search (rcsearch.c of the -21-recompute, DFS mode) at the 53 primes
the author's table lacks.  Also brute-force cross-check of rcsearch at the smallest primes."""
import subprocess, itertools, time
from verify_tl6 import lpr, dclass, check
miss = [7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181, 193, 199, 211, 223, 241, 271, 277, 283, 307, 331, 349, 367, 373, 379, 409, 421, 433, 439, 463, 487, 499, 523, 547, 577, 619, 631, 643, 661, 673, 691, 751, 757, 787, 859]
pr = subprocess.Popen(["./rcsearch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
def q(p, mode, budget, seed=1):
    pr.stdin.write(f"{p} 6 {mode} {budget} {seed} 6 0 1 2 3 4 5 1 0\n"); return pr.stdout.readline().strip()
t0 = time.time(); res = {}
for p in miss:
    res[p] = q(p, "e", 4 * 10**9).split("|")[0].strip()
print("exhaustive at 53 missing primes:", {k: v for k, v in res.items() if v != "NONE"} or "all NONE", round(time.time() - t0, 1), "s")
# brute force at p = 7, 13: all beta (beta0=0), alpha0 = 1 WLOG? do it unnormalised over alpha0 in P_6 representatives
def brute(p):
    xi = lpr(p); D = 6
    cnt = 0
    for b in itertools.product(range(p), repeat=5):
        beta = {0: 0, **{i + 1: b[i] for i in range(5)}}
        # each alpha_j independently: candidates
        cand = []
        for j in range(D):
            cj = [a for a in range(p) if all(((a + beta[i]) % p == 0 and not (i == 0 and j == 0)) or ((a + beta[i]) % p != 0 and (dclass(a + beta[i], p, D, xi) + i + j) % D == 0) for i in range(D))]
            if not cj: break
            cand.append(cj)
        else:
            return True
    return False
for p in (7, 13):
    print("brute force (beta_0 = 0 WLOG by translation) p =", p, "exists:", brute(p))
# positive control: rcsearch must FIND at some certified primes
print("controls FOUND at 229, 313, 2521:", [q(p, "e", 10**9).split()[0] for p in (229, 313, 2521)])
