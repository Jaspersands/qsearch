"""Counterexample to 'L has class <= nu-1' (report Section 2.1): left
multiplication by Lambda^{>=1}(F^2) on Lambda(F^2) (dim 4, strictly upper
triangular in the basis e1e2, e1, e2, 1).  Every element squares to zero
(nu = 2) but [e1, e2] = 2 e1e2 != 0, so the class is 2 > nu - 1 = 1.
Run: /opt/anaconda3/envs/qsearch-cas/bin/python class_vs_nu.py"""
from sage.all import GF, zero_matrix, PolynomialRing, identity_matrix
import itertools
for p in (5, 7, 11, 13):
    Fp = GF(p)
    A1 = zero_matrix(Fp, 4, 4); A1[1, 3] = 1; A1[0, 2] = 1
    A2 = zero_matrix(Fp, 4, 4); A2[2, 3] = 1; A2[0, 1] = -1
    A3 = zero_matrix(Fp, 4, 4); A3[0, 3] = 1
    L = [A1, A2, A3]
    S = PolynomialRing(Fp, 's', 3)
    A = sum(S.gen(j) * L[j].change_ring(S) for j in range(3))
    nu = 1 if A == 0 else (2 if A * A == 0 else None)
    upper = all(M[i, j] == 0 for M in L for i in range(4) for j in range(i + 1))
    br = A1 * A2 - A2 * A1
    third = [X * br - br * X for X in L]
    print('p=%d strictly_upper=%s nu=%s [A1,A2]==2*A3: %s  [L,[L,L]]=0: %s  class=2'
          % (p, upper, nu, br == 2 * A3, all(t == 0 for t in third)))
