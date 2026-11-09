"""Divisor inclusion E_2(D) n {p = 1 mod kappa} c E_2(kappa) for EVERY D | kappa
(threshold-8 checker, 2026-11-05).

The report's Lemma 5 assumes gcd(D, kappa/D) = 1. The plain projection needs no such
hypothesis: a contraction (alpha, beta) at (p, kappa) for xi, restricted to the indices
0..D-1, is a contraction at (p, D) for the same xi, because x in Q_m (mod kappa) implies
x in xi^m P_D = xi^(m mod D) P_D and xi^((p-1)/D) = zeta^(kappa/D) has order D.
(This is Consequence 1 of threshold-7 Prop. 4.6.)

Test: for kappa in {4, 6, 8, 9, 10, 12} take contractions found by e2dfs.solve at feasible
primes, and for every divisor 2 <= D < kappa check
  (a) the restriction to 0..D-1 with generator xi  (no gcd hypothesis), and
  (b) for gcd(D, kappa/D) = 1, the report's map j -> (kappa/D) j with generator xi^(kappa/D),
all cells by pow(). Also check membership consequences against the exact lists.
"""
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from e2dfs import Inst, solve, primes_upto

def is_D_contraction(p, D, xi, alpha, beta):
    h = (p - 1) // D
    zeta = pow(xi, h, p)
    # xi must be a coset generator for D
    if any(pow(zeta, D // q, p) == 1 for q in range(2, D + 1) if D % q == 0 and all(q % r for r in range(2, q))):
        return False
    if (alpha[0] + beta[0]) % p == 0: return False
    for i in range(D):
        for j in range(D):
            c = (alpha[j] + beta[i]) % p
            if c and pow(c, h, p) != pow(zeta, (-(i + j)) % D, p):
                return False
    return True

def main():
    """witnesses: the FEASIBLE lines of e2dfs_c_k*.out (each already pow-checked there)"""
    import glob, re, os
    here = os.path.dirname(os.path.abspath(__file__))
    tot = {"a": 0, "b": 0, "w": 0}
    for f in sorted(glob.glob(os.path.join(here, "e2dfs_c_k*.out"))):
        for line in open(f):
            m = re.search(r"k=(\d+) p=(\d+) FEASIBLE .*xi=(\d+) alpha=(\S+) beta=(\S+)", line)
            if not m: continue
            k, p, xi = int(m.group(1)), int(m.group(2)), int(m.group(3))
            alpha = [int(x) for x in m.group(4).split(",")]
            beta = [int(x) for x in m.group(5).split(",")]
            assert is_D_contraction(p, k, xi, alpha, beta), ("witness itself fails", k, p)
            tot["w"] += 1
            for D in range(2, k):
                if k % D: continue
                assert is_D_contraction(p, D, xi, alpha[:D], beta[:D]), ("projection fails", k, D, p)
                tot["a"] += 1
                mm = k // D
                if math.gcd(D, mm) == 1:
                    a2 = [alpha[(mm * j) % k] for j in range(D)]
                    b2 = [beta[(mm * i) % k] for i in range(D)]
                    assert is_D_contraction(p, D, pow(xi, mm, p), a2, b2), ("Lemma 5 map fails", k, D, p)
                    tot["b"] += 1
    print("witnesses re-checked", tot["w"], "; projections to 0..D-1 (all D | k)", tot["a"],
          "; report's Lemma-5 maps (coprime D)", tot["b"], "; all OK")

if __name__ == "__main__":
    main()
