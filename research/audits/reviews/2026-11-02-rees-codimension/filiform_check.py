"""Exact check of the filiform counterexample in main.tex Remark rem:codim (lines 551-554).

L: basis x=e_0, e_1..e_{m-1}, [x,e_i]=e_{i+1} (i<m-1); h = span(e_1..e_{m-2}).
Claims checked exactly (mod p):
  (1) L is a Lie algebra of class m-1; h is a subalgebra of codimension k = 2.
  (2) a_1 = 2 and a_d = g_d - dim(h cap gamma_d) = 1 at every grade d = 2..m-1;
      the homogeneous lift has hidden codimension sum_d a_d = m, while the filtration
      quotients of the pulled-back subgroup sum to k = 2.
  (3) A single fresh label at grade d (uniform on the 1-dim K_d^perp) has a nonzero witness
      s^d * lambda = 0 with probability exactly 1/p (enumeration over all p labels and all
      s in F_p^*); also the exact witness probability for two labels.
  (4) The abelian-ideal reduction disposes of the instance at once: every random run of the
      Section 1 construction gives A = span(e_1..e_{m-1}), K = h cap A = h, S = N(K) = A,
      S/K is 1-dimensional and abelian with trivial hidden subalgebra.
Run: /opt/anaconda3/bin/python filiform_check.py
"""
import random
from math import gcd
from codim_lib import (filiform, unit, span_basis, intersect, rank, in_span, annihilator)


def next_prime(n):
    def ip(q):
        return q > 1 and all(q % d for d in range(2, int(q ** 0.5) + 1))
    while not ip(n):
        n += 1
    return n


def main():
    rng = random.Random(20261102)
    allok = True
    print("m  p   class  codim  a_1 a_2..a_{m-1}  sum a_d  filt-sum  P1(witness)  min_d P2(witness)  reduction")
    for m in range(4, 15):
        for p in sorted({next_prime(m), 101}):
            L = filiform(m, p)
            n = m
            ok = L.check()
            g = L.lcs()
            cls = len(g)
            h = [unit(i, n) for i in range(1, m - 1)]
            ok &= L.is_subalgebra(h)
            codim = n - rank(h, p, n)
            a = []
            for d in range(1, cls + 1):
                gd = g[d - 1]
                a.append(len(gd) - len(intersect(h, gd, p, n)))
            # pulled-back filtration quotients: dim gamma_d/(gamma_{d+1} + h cap gamma_d)
            filt = 0
            for d in range(1, cls + 1):
                gd = g[d - 1]
                gn = g[d] if d < cls else []
                filt += len(gd) - rank(list(gn) + intersect(h, gd, p, n), p, n)
            ok &= (cls == m - 1 and codim == 2 and a[0] == 2 and all(x == 1 for x in a[1:])
                   and sum(a) == m and filt == 2)
            # (3) exact witness probabilities at each grade d >= 2
            p1s, p2s = set(), set()
            for d in range(2, cls + 1):
                powers = {pow(s, d, p) for s in range(1, p)}
                # one label lambda = t v: witness iff s^d t = 0 for some s != 0
                good1 = sum(1 for t in range(p) if any((sd * t) % p == 0 for sd in powers))
                # two labels t1 v, t2 v: nonzero (s1,s2) with s1^d t1 + s2^d t2 = 0
                P0 = powers | {0}
                good2 = 0
                for t1 in range(p):
                    for t2 in range(p):
                        if any((x * t1 + y * t2) % p == 0 for x in P0 for y in P0 if (x, y) != (0, 0)):
                            good2 += 1
                p1s.add((good1, p))
                p2s.add((good2, p * p, gcd(d, p - 1)))
                ok &= good1 == 1
            # (4) reduction
            red_ok = True
            for _ in range(5):
                A = L.max_abelian_ideal(rng)
                Aspan = span_basis(A, p, n)
                red_ok &= (rank(A, p, n) == m - 1 and
                           all(in_span(unit(i, n), Aspan, p, n) for i in range(1, m)))
                K = intersect(h, A, p, n)
                S = L.normalizer(K)
                red_ok &= len(K) == m - 2 and rank(S, p, n) == m - 1 and \
                    rank(list(S) + Aspan, p, n) == m - 1
                Q, sig = L.quotient(S, K, rng)
                red_ok &= Q.n == 1 and Q.nil_class() == 1
            ok &= red_ok
            allok &= ok
            worst2 = min(g2 / pp for g2, pp, _ in p2s)
            print(f"{m:2d} {p:3d}  {cls:3d}  {codim:4d}   {a[0]}  {'all 1' if all(x == 1 for x in a[1:]) else tuple(a[1:])!s:8s} {sum(a):5d}  {filt:6d}   "
                  f"{'1/p' if all(x == 1 for x, _ in p1s) else 'NO'}         min {worst2:.3f}   "
                  f"{'A=span(e_1..e_{m-1}), S/K=F_p' if red_ok else 'FAIL'}  {'ok' if ok else 'FAIL'}")
    print("\nALL CHECKS PASS" if allok else "\nSOME CHECK FAILED")


if __name__ == "__main__":
    main()
