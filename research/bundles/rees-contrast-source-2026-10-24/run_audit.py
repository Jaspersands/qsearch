"""Replay contrast-source controls and symbolic budgets, not quantum execution."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from contrast_source import (ROOT, broken_symmetry_falsifier, empty_control,
    full_rank_control, high_rank_bias_falsifier, noncommuting_control, source_plan)


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def receipt():
    local = ["CONTRAST_SOURCE.md", "HANDOFF.md", "contrast_source.py",
             "test_contrast_source.py", "run_audit.py"]
    dependencies = ["rees-coarse-spectrum-2026-10-24/coarse_spectrum.py",
                    "rees-coarse-spectrum-2026-10-24/COARSE_SPECTRUM.md",
                    "rees-coarse-spectrum-2026-10-24/receipt.json",
                    "diagonal-source-baseline-2026-10-24/DIAGONAL_BASELINE.md"]
    return {"status": "LOCAL_CONDITIONAL_CONTRAST_SOURCE_EXTENSION_REVIEW_PENDING",
            "same_exact_mixed_conjugation_task": True,
            "unknown_background_and_spectral_rank_advice_not_supplied": True,
            "global_orbit_gap_and_contrast_compressibility_still_promised": True,
            "full_rank_symbolic_control": full_rank_control(),
            "empty_filter_control": empty_control(),
            "noncommuting_nonnormal_control": noncommuting_control(),
            "insufficient_promise_falsifier": high_rank_bias_falsifier(),
            "symmetry_breaking_noise_falsifier": broken_symmetry_falsifier(),
            "loose_copy_ledger_not_executed": source_plan(dimension=2**256,
                contrast_rank=3, orbit_gap=F(1, 10), error=F(1, 32),
                receiver_leaves=8, design_size=6, cover_order_bits=16),
            "known_basis_classical_baseline_available": True,
            "luks_classical_backend_implemented": False,
            "quantum_algorithm_executed": False, "independently_reviewed": False,
            "novelty_established": False, "classical_input_speedup_established": False,
            "accepted_speedup_candidate": False,
            "imported_literature": ["arxiv:2412.02134v3", "arxiv:2610.06737v1"],
            "sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in local},
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
