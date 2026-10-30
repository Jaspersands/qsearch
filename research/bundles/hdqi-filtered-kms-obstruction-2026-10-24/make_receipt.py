"""Reproducible controls and exact comparison certificates; no large matrices."""

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import filtered_kms as k

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt():
    paths = ("filtered_kms.py", "test_filtered_kms.py", "make_receipt.py", "FILTERED_KMS.md", "HANDOFF.md",
             "../hdqi-thermal-flow-obstruction-2026-10-24/thermal_flow.py",
             "../hdqi-thermal-flow-obstruction-2026-10-24/THERMAL_FLOW.md",
             "../hdqi-relative-flow-2026-10-24/relative_flow.py",
             "../hdqi-relative-flow-2026-10-24/RELATIVE_FLOW.md",
             "../hdqi-filtered-parent-2026-10-24/filtered_parent.py",
             "../hdqi-filtered-parent-2026-10-24/FILTERED_PARENT.md",
             "../hdqi-parent-gap-2026-10-23/parent_gap.py",
             "../hdqi-gap-baseline-2026-10-24/GAP_AND_BASELINE.md")
    hashes = {name: digest(ROOT/name) for name in paths}
    ledgers = []
    for d in (16, 256, 4096, 65536, 2**20, 2**24, 2**32):
        beta = F(1, 8*(math.isqrt(d)+1))
        ledgers.append({"formula": k.star_formula(d, float(beta)),
                        "rational_certificate": k.rational_certificate(d, beta)})
    principal = next(row for row in ledgers if row["formula"]["d"] == 2**20)["rational_certificate"]
    if not (principal["same_KMS_filter_commutator_ratio_exceeds_99_over_100"]
            and principal["filtered_to_raw_physical_form_ratio_below_1_over_100"]):
        raise ArithmeticError("fixed rational countercertificates failed")
    result = {"status": "LOCAL_UNREVIEWED_TWO_FILTERED_THERMAL_COMPARISONS_FALSIFIED",
              "principal_degree": 2**20,
              "dense_identity_controls": [k.dense_control(d, 0.37, 0.29) for d in range(2, 8)],
              "analytic_star_ledgers": ledgers,
              "same_family_positive_controls": {
                  "filtered_parent_gap_lower_from_existing_mass_lemma": "25/36",
                  "classical_envelope_upper_from_existing_moment_bound": "128/127",
                  "bounds_reused_not_new_results": True},
              "scope": {"same_KMS_gradient_is_actual_parent_form": False,
                        "original_trace_gradient_lemma_falsified": False,
                        "filtered_parent_gap_falsified": False,
                        "general_filtered_variance_bound_established": False,
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
    rendered = json.dumps(receipt(), indent=2, sort_keys=True, allow_nan=False)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
