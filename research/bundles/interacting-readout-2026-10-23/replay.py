"""Write bounded contraction diagnostics, not an end-to-end simulation claim."""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from controls import direct_tfd_expectation, exact_ising_mpo, sector_filter
from paired_mpo import dense_to_mpo, error_budget, log_norm_squared, paired_value, sector_value


def evidence():
    filters = [sector_filter(z) for z in range(4)]
    product = [sector_filter(z, False) for z in range(4)]
    normalized = [f/np.linalg.norm(f) for f in filters]
    mpos = [dense_to_mpo(f, 3) for f in filters]
    weights = np.array([np.vdot(f, f).real for f in filters])
    rows = []
    for cl, cr, a, b in (("XI", "XI", "III", "III"),
                         ("II", "II", "ZZI", "III"),
                         ("YI", "XI", "YII", "III"),
                         ("XY", "YX", "YZI", "IZY")):
        vals = [sector_value(z, mpos.__getitem__, cl, cr, a, b) for z in range(4)]
        actual = float(weights @ vals / weights.sum())
        ref = direct_tfd_expectation(filters, cl, cr, a, b)
        rows.append({"central": [cl, cr], "local": [a, b], "paired": actual,
                     "dense_reference": ref, "absolute_error": abs(actual-ref),
                     "maximum_absolute_sector_estimator": max(map(abs, vals))})
    normalization_gap = abs(direct_tfd_expectation(filters, "XI", "XI", "III", "III")
                            - direct_tfd_expectation(normalized, "XI", "XI", "III", "III"))
    product_gap = abs(direct_tfd_expectation(filters, "II", "II", "ZZI", "III")
                      - direct_tfd_expectation(product, "II", "II", "ZZI", "III"))
    n, coupling = 192, 0.3
    easy = exact_ising_mpo(n, coupling)
    long_value = paired_value(easy, easy, "ZZ"+"I"*(n-2), "I"*n)
    long_ref = math.tanh(2*coupling)
    if max(r["absolute_error"] for r in rows) > 2e-12:
        raise ArithmeticError("Dense reference mismatch")
    if normalization_gap <= 0.02 or product_gap <= 0.15:
        raise ArithmeticError("Wrong-backend controls did not fail")
    if abs(long_value-long_ref) > 1e-11:
        raise ArithmeticError("Transfer-matrix reference mismatch")
    return {
        "status": "finite_controls_pass_written_composition_review_pending",
        "speedup_admitted": False,
        "novelty_admitted": False,
        "general_tfd_simulation_admitted": False,
        "scalable_thermal_constructor_implemented": False,
        "end_to_end_sampler_executed": False,
        "arithmetic_interval_certified": False,
        "source_sampling": "Required from existing worldline proof; not replayed here",
        "thermal_dependency": {
            "url": "https://arxiv.org/html/2007.11174v2#S4.SS1",
            "result": "Theorem 3, p=2, half inverse temperature",
        },
        "bounded_dense_control": {"central_bits": 2, "local_spins": 3,
                                  "beta": 0.7, "records": rows,
                                  "distance_window_claimed": False},
        "wrong_controls": {"independent_sector_normalization_gap": normalization_gap,
                           "omitted_interactions_gap": product_gap},
        "easy_transfer_matrix_control": {
            "local_spins": n, "maximum_bond": 2,
            "dense_allocation": False, "hard_instance": False,
            "paired": long_value, "reference": long_ref,
            "log_norm_squared": log_norm_squared(easy),
        },
        "illustrative_error_contract_only": {
            "eta": "1/100", "sampler_tv": "1/200", "arithmetic": "1/1000",
            "these_errors_are_not_certified_by_this_run": True,
            **{k: str(v) for k, v in error_budget(
                Fraction(1, 100), Fraction(1, 200), Fraction(1, 1000)).items()},
        },
    }


def main():
    root = Path(__file__).resolve().parent
    record = evidence()
    names = ("paired_mpo.py", "controls.py", "test_paired_mpo.py", "replay.py",
             "INTERACTING_COHERENT_READOUT.md")
    record["source_sha256"] = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names
    }
    target = root / "readout_receipt.json"
    target.write_text(json.dumps(record, indent=2, allow_nan=False) + "\n", encoding="ascii")
    print(json.dumps({"receipt": str(target), "status": record["status"],
                      "wrong_controls": record["wrong_controls"],
                      "speedup_admitted": record["speedup_admitted"]}))


if __name__ == "__main__":
    main()
