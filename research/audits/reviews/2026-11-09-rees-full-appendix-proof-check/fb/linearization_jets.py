"""fb check 4b: driver of linearization_check.study for rem:filters (ii) ("tested with UT_5 blocks and p > 5"):
linear and quadratic forms (Delta = 1, 2) under exp(F_p J_D), D = 5..7 at p = 7 and D = 5, 6 at p = 11,
including cases with (D-1) Delta >= p.  Finite checks only (corroboration, not proof)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linearization_check import study
for p, D in [(7, 5), (7, 6), (7, 7), (11, 5), (11, 6)]:
    for Delta in (1, 2):
        n, f, k, i = study(p, D, Delta)
        print(f'p={p} D={D} Delta={Delta} (D-1)Delta={(D-1)*Delta}: forms={n} dimFix={f} dimKer={k} dimFix∩Ker={i}',
              'equal' if f == k == i else 'DIFFER', flush=True)
