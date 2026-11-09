"""Check: at every Gamma_F grade of the six rows, with the tau_d of the (iii) column, the least FCS arity is
below the weight-doubling arity, so the (iii) columns (least public arities) do not move when (R1) gains
the optional nodes (the block-steered case is asserted in block_steered_combined.py)."""
import math, sys
from fractions import Fraction as F
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from theorems import rees_fcs_budget as fb
import wd_budget_indep as wd
for lab, p in fb.PRIMES:
    fc = fb.free_coordinate_iii(p)
    for d, gr in fc["grades"].items():
        if gr["cls"] != "F":
            continue
        g = fb.PROFILE[d - 1]; k = gr["kappa"]; h = (p - 1) // k; tau = gr["tau"]
        A = 2 * (k - 1) * (k - 2) + 4
        if p >= A * A:
            Nbar = 1 + (p - 1).bit_length() * F(p, p - 1) * F(g * (g + 1), 2)
        else:
            Nbar = wd.N0_table(wd.jstar(p, h), F(min(p, math.ceil(2 * math.log2(p - 1)) + 4)), g)
        L = -(-2 * Nbar.numerator // Nbar.denominator)
        Mwd = g + wd.clog(p, 2 / tau) + wd.clog(2, 2 / tau) * L
        assert gr["M"] < Mwd, (lab, d, gr["M"], Mwd)
print("FCS < weight-doubling at every Gamma_F grade of the six rows")
