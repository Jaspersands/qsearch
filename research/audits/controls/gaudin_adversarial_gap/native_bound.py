"""Exact arithmetic for the reviewed finite-spacing Gaudin counterfamily.

/opt/anaconda3/bin/python. Reuses the frozen compressed Sturm certificate;
this arithmetic does not itself prove the fusion/operator inequalities.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

base = Path(__file__).parent
fused_path = base / "fused_result.json"
fused = json.loads(fused_path.read_text())
assert fused["status"] == "EXACT_COMPRESSED_LOWEST_GAP_LT_HALF"
assert fused["fixed_parameters"]["cluster_size_n"] == 64
lo, hi = map(Q, fused["exact"]["strict_lowest_gap_interval"])
assert (lo, hi) == (Q(67, 250), Q(27, 100))
for j, certificate in enumerate(fused["exact"]["eigenvalue_certificates"]):
    assert certificate["left_inertia"]["number_of_eigenvalues_strictly_below"] == j
    assert certificate["right_inertia"]["number_of_eigenvalues_strictly_below"] == j+1

n = 64
N = 2*n
g = Q(1, 2*n)
delta = Q(1, n**8)
CE = 2*n*(n-1)/g + Q(4, 3)*n*(n*n-1)
CQ = (16*g*(n-1)*CE**2/n**2 + g*n*(n-1)
      + 8*(1+g*n)*CE/n)
e = 400*Q(1, n**4)
upper = Q(2, n)*(hi+6*n*e)**2
checks = {
    "CE_le_6n3": CE <= 6*n**3,
    "CQ_le_400n4": CQ <= 400*n**4,
    "positive_distinct_site_condition": 0 < delta*(n-1) <= Q(1, 2),
    "separator_isolation": delta*CE <= Q(n, 4),
    "compression_error_paid": delta*CQ <= e,
    "two_distinct_anchor_eigenvalues": e < lo/(2*n),
    "strict_native_upper_below_1_over_400": upper < Q(1, 400),
    "one_over_400_below_target_1_over_N": Q(1, 400) < Q(1, N),
}
assert all(checks.values()), checks
out = {
    "status": "EXACT_NATIVE_BOUND_ARITHMETIC_PASS",
    "scope": "Exact finite inequality, conditional on the independently reviewed fusion theorem; no full physical matrix diagonalization.",
    "theory": "research/GAUDIN_TWO_CLUSTER_GAP.md sections1-3",
    "core_review": "research/audits/reviews/2026-11-07-gaudin-fusion-core.md",
    "fused_result_sha256": hashlib.sha256(fused_path.read_bytes()).hexdigest(),
    "parameters": {"cluster_size_n": n, "physical_N": N,
                   "excitation_M": n, "g": str(g), "delta": str(delta),
                   "sites_A": "delta*i, i=0,...,63",
                   "sites_B": "1+delta*i, i=0,...,63",
                   "minimum_spacing": str(delta)},
    "bounds": {"C_E": str(CE), "C_Q": str(CQ),
               "uniform_compression_e": str(e),
               "fused_lowest_gap_lower": str(lo),
               "fused_lowest_gap_upper": str(hi),
               "strict_physical_squared_joint_gap_upper": str(upper),
               "simple_strict_upper": "1/400", "proposed_floor_1_over_N": "1/128"},
    "checks": checks,
    "claim_gates": {"all_family_theorem_from_control": False,
                    "superpolynomial_gap": False, "no_polynomial_algorithm": False,
                    "quantum_execution": False, "novelty": False,
                    "separation": False},
}
(base / "native_bound.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps({"status": out["status"], "checks": len(checks),
                  "strict_native_upper_approximation": float(upper),
                  "simple_strict_upper": "1/400", "target": "1/128"}))
