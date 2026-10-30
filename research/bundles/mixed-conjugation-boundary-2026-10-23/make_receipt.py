"""Reproduce exact checks and analytical resources; never run a huge-state sampler."""

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from copy_boundary import (
    StripeFamily, canonical_purification_gap, classical_moments,
    classical_sufficient_copies, exhaustive_control, necessary_copies,
    tv_squared_upper,
)


def encoded(value):
    if isinstance(value, F):
        return {"numerator": value.numerator, "denominator": value.denominator}
    raise TypeError(type(value).__name__)


def build_receipt():
    root = Path(__file__).resolve().parent
    controls = [exhaustive_control(StripeFamily(m, v), t)
                for m, v, t in [(1, F(3, 4), 3), (2, F(3, 4), 2),
                                (2, F(3, 4), 3), (2, F(1), 3)]]
    scaling = []
    for n in (8, 32, 64, 128):
        family = StripeFamily(2**n)
        upper = classical_sufficient_copies(family)
        scaling.append({"bucket_bits": n, "metrics": family.metrics(),
                        "necessary_copy_bounds_error_one_third": necessary_copies(family),
                        "classical_sufficient_copies_conservative": upper,
                        "classical_analytical_error_upper":
                            classical_moments(family, upper)["error_upper_chebyshev"],
                        "canonical_sqrt_purification_gap_interval": canonical_purification_gap(family),
                        "tv_squared_upper_at_one_million_copies": tv_squared_upper(family, 10**6),
                        "large_state_enumerated": False,
                        "large_sampling_campaign_run": False})
    names = ["copy_boundary.py", "test_copy_boundary.py", "make_receipt.py",
             "MIXED_CONJUGATION_BOUNDARY.md"]
    return {
        "schema": "isolated-research-receipt/v1",
        "date": "2026-10-23",
        "status": "proved-in-note-copy-bound-with-exact-controls; independent-review-pending",
        "research_effect": "reject-generic-polylog-copy-mixed-conjugation-extension",
        "input_contract": {"group": "C3", "access": "IID copies of one fixed unknown diagonal state",
                           "known_action": "shift last qutrit", "visibility": F(3, 4),
                           "null_stabilizer": "C3", "signal_stabilizer": "identity",
                           "two_cases_isospectral": True,
                           "hidden_orientation_advice": False},
        "finite_controls": controls,
        "analytical_scaling_not_measured": scaling,
        "claims_not_made": ["quantum speedup", "succinct-circuit hardness",
                            "low-rank impossibility", "independent proof review",
                            "full-repository validation", "integration or migration complete"],
        "source_sha256": {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names},
        "primary_references": ["https://sites.stat.columbia.edu/liam/research/pubs/sparse-unif-test.pdf",
                               "https://arxiv.org/html/2609.38085"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = build_receipt()
    args.output.write_text(json.dumps(receipt, default=encoded, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.resolve()),
                      "finite_controls": len(receipt["finite_controls"]),
                      "analytic_scaling_rows": len(receipt["analytical_scaling_not_measured"]),
                      "status": receipt["status"]}, indent=2))
