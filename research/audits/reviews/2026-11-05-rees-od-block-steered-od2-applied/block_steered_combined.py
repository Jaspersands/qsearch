"""Recompute the combined column of tab:fcs-budget with the block-steered node adopted (OD block-steered).

Read-only reuse of theorems/rees_fcs_budget.py (the generator cited in the caption of tab:fcs-budget):
  1. reproduce the printed (old) combined column from combined_rule();
  2. apply the block-steered option of rem:sde-block-steered at every grade 2 <= kappa_d < p-1, with
     J_d = max(3, kappa_d), M_d = M_{J_d}(g_d), admitted when
       (G1) p not in E_cg(J_d, kappa_d): certified by the Weil bound p - e > (kappa^e-1)(e-1) sqrt p for
            all 2 <= e <= J_d (every Good(beta) nonempty), or by the exhaustive lists for (3,2), (3,3);
       (G2) Lambda_d * C(J_d,2) <= G_lb / 2, G_lb = min_e (p - e - (kappa^e-1)(e-1) sqrt p)/kappa^e,
            so a back substitution fails with probability <= 1/2;
       (G3) (M_d + Lambda_d C(J_d,2))/(p-1) + 1/((p-1) p^(M_d-g_d)) <= tau_d = eps/(9(c-1) S n_d),
     and M_d < the combined-rule arity.  Exact integer/rational arithmetic throughout.
  3. check that the block-steered node never beats the FCS arity of (iii) (so the (iii) columns do not move).
Writes nothing into the repository; prints a JSON summary.
"""
import json
import math
import sys
from fractions import Fraction as F
from math import comb, gcd

sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from theorems import rees_fcs_budget as fb  # noqa: E402

ECG = {(3, 2): set(),
       (3, 3): {7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181, 193, 211, 241}}
PRINTED_OLD = {"11": "202.1", "1031": "167.3", "5281": "852.3", "2^31-1": "944.9", "2^61-1": "555.4", "2^127-1": "61.5"}


def M_J(a, J):
    mu, r0 = divmod(a, J - 1)
    return 1 + mu * (a + 1) - (J - 1) * mu * (mu - 1) // 2 + ((r0 + 1) if r0 > 0 else 0)


for a in range(1, 60):
    assert M_J(a, 2) == (a + 1) * (a + 2) // 2
    assert M_J(a, 3) == (a + 2) ** 2 // 4 + (a % 2)


def weil_ge(p, e, k, rhs):
    """exact test of p - e - (k^e-1)(e-1) sqrt(p) >= rhs (rhs >= 0)."""
    C = (k ** e - 1) * (e - 1)
    lhs = p - e - rhs
    return lhs >= 0 and lhs * lhs >= C * C * p


def admissible(p, k, g, tau):
    J = max(3, k)
    M = M_J(g, J)
    Lam = -(-g // (J - 1))
    pairs = Lam * comb(J, 2)
    weil_pos = all(weil_ge(p, e, k, 1) for e in range(2, J + 1))  # G >= 1/k^e > 0 means Good nonempty
    g1 = weil_pos or ((J, k) in ECG and p not in ECG[(J, k)])
    g2 = all(weil_ge(p, e, k, 2 * pairs * k ** e) for e in range(2, J + 1))
    f = F(M + pairs, p - 1) + F(1, (p - 1) * p ** (M - g))
    g3 = f <= tau
    return dict(J=J, M=M, Lambda=Lam, G1=g1, G2=g2, G3=g3, bank=f, ok=g1 and g2 and g3)


def evaluate(label, p):
    prof = fb.PROFILE
    c, m = len(prof), prof[0]
    eps = fb.EPS
    old = fb.combined_rule(p)
    assert fb.fmt1(old["Q"]) == PRINTED_OLD[label], (label, fb.fmt1(old["Q"]))
    S = old["S"]
    fc = fb.free_coordinate_iii(p)
    acc, rows, bank_sum = 1, {}, F(0)
    for d in range(2, c + 1):
        g = prof[d - 1]
        name, Mc = old["sch"][d]
        k = gcd(d, p - 1)
        choice = (name, Mc)
        info = None
        if 2 <= k < p - 1:
            tau = eps / (9 * (c - 1) * S * acc)
            info = admissible(p, k, g, tau)
            if info["ok"] and info["M"] < Mc:
                choice = (f"BS(J={info['J']})", info["M"])
                bank_sum += S * acc * info["bank"]
            # where admissible, block-steered never beats the FCS node of (iii)
            if info["ok"]:
                assert fc["grades"][d]["M"] <= info["M"], (label, d)
        rows[d] = dict(kappa=k, g=g, combined=[name, str(Mc) if Mc < 10 ** 9 else f"{Mc:.3e}"], chosen=choice[0],
                       M=str(choice[1]) if choice[1] < 10 ** 9 else f"{choice[1]:.3e}",
                       guards=None if info is None else {x: info[x] for x in ("J", "M", "G1", "G2", "G3")})
        acc *= choice[1]
    Q = c * S * acc
    s2_left = [d for d in rows if rows[d]["chosen"] == "S2"]
    bs = [d for d in rows if rows[d]["chosen"].startswith("BS")]
    return dict(label=label, old=fb.fmt1(old["Q"]), new=fb.fmt1(Q), new_exact_log2=round(fb.log2_exact(Q), 4),
                bs_grades=bs, schedule2_grades_left=s2_left, bank_abort_sum=float(bank_sum),
                bank_abort_sum_le_eps_over_9=bank_sum <= eps / 9, grades=rows)


if __name__ == "__main__":
    out = [evaluate(lab, p) for lab, p in fb.PRIMES]
    for r in out:
        print(r["label"], r["old"], "->", r["new"], "BS grades", r["bs_grades"], "S2 left", r["schedule2_grades_left"],
              "bank", f"{r['bank_abort_sum']:.3e}")
    json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)
