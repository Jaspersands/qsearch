"""Replay the existing AG control and display explicitly analytic large sizes."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import log, log1p
from pathlib import Path
import sys

from systematic import SystematicFiber, distance_bound

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "ag-divisor-class-control-2026-10-26/receipt.json"


def report():
    source = json.loads(SOURCE.read_text())
    for name, digest in source["sha256"].items():
        if sha256((ROOT.parent/name).read_bytes()).hexdigest() != digest:
            raise ArithmeticError(f"source drift: {name}")
    control = source["control"]
    fiber = SystematicFiber(control["prime"], control["original_parity"],
                            relation="full_support")
    runs = []
    for old in source["matched_classical_witness_runs"]:
        target = old["syndrome"]
        result = fiber.sample(target, seed=20261027+len(runs), attempts=8)
        if result["witness"] is None or not fiber.verifies(result["witness"], target):
            raise ArithmeticError("existing native AG matrix replay failed")
        runs.append({"syndrome": target, "seed": 20261027+len(runs),
                     "result": result, "original_relation_verified": True})
    p = 100003
    rows = []
    for e in (8, 64, 4096, 65536, 1048576):
        k, m, g = 5*e+3, 22*e, 5*e+1
        # These rational upper bounds use alpha < q^-3, not numeric tail evaluation.
        log_sys = Fraction(k, p-1)+Fraction(2, p**3)
        log_aff = Fraction(m, p-1)+Fraction(2, p**3)
        rows.append({"cover_degree": e, "length": m, "rank": k,
                     "systematic_ln_expected_trials_upper_exact": str(log_sys),
                     "affine_ln_expected_trials_upper_exact": str(log_aff),
                     "systematic_log2_upper_display_approx": float(log_sys)/log(2),
                     "affine_log2_upper_display_approx": float(log_aff)/log(2),
                     "four_list_worst_rank_log2_list_length": (2*g+2)//3,
                     "four_list_all_degree_bias_certificate_applies": e >= 64,
                     "actual_rational_two_rank_known": False,
                     "large_matrix_generated_or_run": False,
                     "parameter_row_is_not_an_input_construction": True})
    bound = distance_bound(p, fiber.m, fiber.k, 12*8-3)
    sources = [ROOT/name for name in ("BASELINE.md", "REVIEW_RESOLUTION.md", "systematic.py",
                                    "test_systematic.py", "verify_systematic.py")]
    sources += [SOURCE, ROOT.parent/"ag-affine-sampling-2026-10-26/affine_sampling.py"]
    return {
        "status": "MATCHED_CLASSICAL_BASELINE_NOT_QUANTUM_ADVANTAGE",
        "exact_bound_on_existing_AG_control": {key: str(value) if isinstance(value, Fraction)
                                               else value for key, value in bound.items()},
        "native_replays": runs, "analytic_scaling_only": rows,
        "leading_systematic_log2_trials_per_e_approx": -5*log1p(-1/p)/log(2),
        "displayed_four_list_rate_threshold_r2_per_e_approx": -15*log1p(-1/p)/log(2),
        "fixed_field_polynomial_solver_established": False,
        "quantum_advantage_established": False,
        "sha256": {str(path.relative_to(ROOT.parent)): sha256(path.read_bytes()).hexdigest()
                   for path in sources},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = report()
    path = ROOT/"receipt.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2)+"\n")
    elif args.check:
        if json.loads(path.read_text()) != result:
            raise SystemExit("FAIL: systematic replay differs")
    else:
        print(json.dumps(result, indent=2))
    if args.write or args.check:
        print(f"PASS: {len(result['sha256'])} hashes; SHA256 {sha256(path.read_bytes()).hexdigest()}")
