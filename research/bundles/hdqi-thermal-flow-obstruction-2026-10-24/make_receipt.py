"""Replay the thermal-flow obstruction without large-state simulation."""

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import thermal_flow as t

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt():
    paths = ("thermal_flow.py", "test_thermal_flow.py", "make_receipt.py", "THERMAL_FLOW.md", "HANDOFF.md",
             "../hdqi-relative-flow-2026-10-24/relative_flow.py",
             "../hdqi-relative-flow-2026-10-24/RELATIVE_FLOW.md",
             "../hdqi-filtered-parent-2026-10-24/filtered_parent.py",
             "../hdqi-filtered-parent-2026-10-24/FILTERED_PARENT.md",
             "../hdqi-parent-gap-2026-10-23/parent_gap.py",
             "../hdqi-gap-baseline-2026-10-24/GAP_AND_BASELINE.md")
    hashes = {name: digest(ROOT/name) for name in paths}
    dense = [t.dense_control(d, 1/(8*math.sqrt(d+1))) for d in range(2, 8)]
    ledgers = []
    for d in (16, 256, 4096, 65536, 2**20, 2**24, 2**32):
        beta = F(1, 8*(math.isqrt(d+1)+1))
        cert = t.rational_countercertificate(d, beta)
        ledgers.append({"formula": t.star_formula(d, float(beta)), "rational_certificate": cert})
    principal = next(row for row in ledgers if row["formula"]["d"] == 65536)
    cert = principal["rational_certificate"]
    if not (cert["flow_bound_strictly_falsified"] and cert["defect_bound_strictly_falsified"]):
        raise ArithmeticError("the fixed rational counterexample no longer verifies")
    result = {"status": "LOCAL_UNREVIEWED_THERMAL_GRADIENT_SHORTCUT_FALSIFIED",
              "dense_identity_controls": dense, "analytic_star_ledgers": ledgers,
              "principal_degree": 65536,
              "same_family_positive_controls": {
                  "filtered_parent_gap_lower_from_existing_mass_lemma": "25/36",
                  "classical_envelope_upper_from_existing_moment_bound": "128/127",
                  "bounds_reused_not_new_results": True},
              "scope": {"original_trace_gradient_lemma_falsified": False,
                        "filtered_parent_gap_falsified": False,
                        "general_filtered_KMS_bound_established": False,
                        "Gaussian_claim_is_witness_specific_image_bound_only": True,
                        "quantum_algorithm_executed": False, "classical_hardness_claimed": False,
                        "new_candidate_admitted": False, "independent_review_claimed": False,
                        "main_checkout_changed": False},
              "source_sha256": hashes}
    if hashes != {name: digest(ROOT/name) for name in paths}:
        raise RuntimeError("a bound source changed during replay")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = receipt()
    rendered = json.dumps(data, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    print("Strict rational thermal-flow counterexample at d65536; parent gap NOT falsified.")
