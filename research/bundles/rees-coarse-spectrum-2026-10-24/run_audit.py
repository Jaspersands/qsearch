"""Replay scoped exact/numerical controls; never execute the large copy plan."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from coarse_spectrum import (ROOT, near_degenerate_control, nonnormal_control,
                             nonflat_growth_control, rotated_gap_control, source_plan)


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def receipt():
    files = ["COARSE_SPECTRUM.md", "coarse_spectrum.py", "test_coarse_spectrum.py", "HANDOFF.md", "run_audit.py"]
    dependencies = ["rees-code-support-2026-10-24/code_support.py",
                    "rees-code-support-2026-10-24/CODE_SUPPORT.md",
                    "rees-spectral-mixture-2026-10-24/SPECTRAL_MIXTURE.md",
                    "rees-spectral-mixture-2026-10-24/spectral_mixture.py",
                    "rees-code-support-2026-10-24/code_support_receipt.json",
                    "rees-spectral-mixture-2026-10-24/spectral_mixture_receipt.json"]
    return {"status": "PROPOSED_LOW_RANK_MIXED_CONJUGATION_SOURCE_REVIEW_PENDING",
            "task_is_full_conjugation_not_support_only": True,
            "individual_spectral_gap_and_exact_rank_advice_removed": True,
            "global_gap_and_rank_cap_still_required": True,
            "quantum_algorithm_executed": False, "independently_reviewed": False,
            "novelty_established": False, "classical_input_speedup_established": False,
            "accepted_speedup_candidate": False,
            "literature_primitives_not_claimed_new": ["arxiv:2610.06737v1", "arxiv:1608.00281"],
            "generic_hardness_comparison_with_different_promises": "arxiv:2605.12615v2 section 5.3",
            "tiny_spectrum_exact_control": near_degenerate_control(),
            "nonnormal_exact_control": nonnormal_control(),
            "nonflat_growth_numeric_control": nonflat_growth_control(),
            "nondiagonal_gap_numeric_control": rotated_gap_control(),
            "loose_resource_plan_not_execution": source_plan(rank_cap=7, orbit_gap=F(1, 7),
                error=F(1, 32), receiver_leaves=8, design_size=6, cover_order_bits=16),
            "sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
            "dependency_sha256": {name: hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest() for name in dependencies}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(receipt(), default=encode, sort_keys=True, indent=2)+"\n"
    if args.output:
        args.output.write_text(rendered)
        print(args.output.resolve())
    else:
        print(rendered, end="")
