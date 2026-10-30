"""Replay supplied-coordinate leakage controls; never a native-map solver."""

import argparse
import hashlib
import json
from pathlib import Path
from random import Random

from sympy import Matrix, Rational

from interpolation_closure import (
    adjoint, category_contains, cross_completion_rank, cross_is_new,
    interpolation_diamond, leaf_candidates, terminal_generators,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def control(q):
    psi, auxiliary = interpolation_diamond(q, (1, 2, 1, 1))
    terminal = all(category_contains(adjoint(psi)*a*psi/auxiliary, q, 4)
                   for a in terminal_generators())
    old, new = Matrix.diag(q, 1), Matrix.diag(1, q)
    old_rank, new_rank = cross_completion_rank(old, q), cross_completion_rank(new, q)
    integral = leaf_candidates(Matrix.diag(0, 1), q, Random(7))
    fractional = leaf_candidates(Matrix([[0, Rational(1, q)], [0, 0]]), q)
    if not terminal or cross_is_new(old, q) or not cross_is_new(new, q):
        raise AssertionError("terminal/escape gate changed")
    if (old_rank, new_rank) != (2, 4):
        raise AssertionError("cross-map completion changed")
    if len(integral["lines"]) != 2 or fractional["lines"] != [(1, 0)]:
        raise AssertionError("neighbor selector changed")
    return {"prime": q, "auxiliary_multiplier": auxiliary,
            "terminal_pullbacks_in_known_ring": terminal,
            "old_cross_rank": old_rank, "new_cross_rank": new_rank,
            "integral_candidate_lines": [list(x) for x in integral["lines"]],
            "fractional_candidate_lines": [list(x) for x in fractional["lines"]],
            "all_local_matrices_supplied": True}


def receipt():
    paths = [HERE / name for name in (
        "LEAKAGE.md", "interpolation_closure.py", "test_interpolation_closure.py",
        "replay_leakage.py",
    )]
    paths += [ROOT / name for name in (
        "product-corner-attack-2026-10-23/product_corners.py",
        "source-algebra-splitting-2026-10-25/source_split.py",
        "kernel-output-2026-10-23/kernel_output.py",
        "native-nonbass-realization-2026-10-26/receipt.json",
        "ppav-source-2026-10-23/2026-1142.pdf",
    )]
    return {
        "schema": "interpolation-leakage-controls-v1",
        "status": "terminal closure and conditional native escape criteria",
        "controls": [control(q) for q in (3, 5, 17)],
        "large_prime_selector_candidate_count": len(
            leaf_candidates(Matrix.diag(0, 1), 2**61-1)["lines"]),
        "execution_scope": {
            "exact_supplied_local_coordinate_controls": True,
            "partial_quotient_automorphisms_computed": False,
            "native_escape_map_found": False,
            "native_division_or_ring_recovery": False,
            "native_geometric_hiding_labels": False,
            "classical_hardness_or_quantum_advantage": False,
            "independent_review": False,
        },
        "hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in paths},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = receipt()
    path = HERE / "receipt.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    if args.check and json.loads(path.read_text()) != result:
        raise SystemExit("receipt mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
