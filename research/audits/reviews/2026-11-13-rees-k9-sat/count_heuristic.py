#!/opt/anaconda3/bin/python
"""First-moment (variables vs constraints) count for the l-level union-target contraction (HEURISTIC only).

An l-level contraction at (p, k, K) is B : Z_k^l -> F_p in the image of  (F_1..F_l) -> sum_t F_t(x without x_t),
i.e. a subspace of dimension  D_l = k^l - (k-1)^l  (functions killed by the l-fold mixed difference),
with B(x) in {0} u U_{m in K} Q_{m-|x|} at every cell and B(0) != 0.  If B were a uniform element of that
subspace with independent cells, the expected number of solutions would be about
     p^{D_l} * prod_cells (|allowed| / p) = p^{ D_l - k^l * log_p(p / (1 + |K| (p-1)/k)) }.
The printed exponent e = D_l - k^l log_p(p/(1+|K|(p-1)/k)) is the log_p of that expectation.
It is NOT a proof of anything: structured solutions can exist at e < 0 (see the calibration rows).
"""
import math

def e(p, k, l, nK):
    a = 1 + nK * (p - 1) // k
    return k ** l - (k - 1) ** l - k ** l * math.log(p / a, p)

print('calibration (three-level, observed with sat3.py + kissat):')
for p, k, nK, obs in [(41, 4, 1, 'SAT'), (7, 3, 1, 'SAT'), (13, 3, 1, 'SAT'), (13, 4, 1, 'SAT'),
                      (11, 5, 1, 'SAT'), (31, 5, 1, 'SAT'), (19, 3, 1, 'SAT'), (13, 6, 1, 'SAT'),
                      (7, 6, 1, 'UNSAT'), (19, 6, 1, 'UNSAT'), (19, 9, 1, 'UNSAT'), (37, 9, 1, 'UNSAT (LRAT)'),
                      (41, 8, 1, 'timeout'), (29, 7, 1, 'timeout'), (31, 6, 1, 'timeout'),
                      (7, 6, 2, 'K={0,3} SAT, {0,2} UNSAT, {0,1} timeout')]:
    print(f'  (p,k)=({p},{k}) |K|={nK}: e = {e(p, k, 3, nK):8.1f}   observed {obs}')
print('targets at kappa = 9:')
for p in (19, 37, 73):
    for l in (3, 4, 5, 6, 7):
        print(f'  p={p} l={l}: e(K={{0}}) = {e(p, 9, l, 1):9.1f}   e(|K|=2) = {e(p, 9, l, 2):9.1f}')
