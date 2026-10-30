"""Reproduce exact local controls and their deliberately limited status."""

import argparse
import hashlib
import json
from pathlib import Path

from sympy import Matrix, eye

from local_orders import contains, neighbor_frames, recover_path_vertex, scalar_order_basis

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def receipt():
    paths = [HERE / name for name in (
        "SCOPE.md", "local_orders.py", "test_local_orders.py", "replay_scope.py",
        "eisentraeger-scullard-v2.html",
    )]
    paths += [ROOT / name for name in (
        "classical-symmetry-harvest-2026-10-26/receipt.json",
        "additive-framed-source-2026-10-26/receipt.json",
        "native-membership-baseline-2026-10-25/NATIVE_MEMBERSHIP.md",
        "combined-source-independent-review-2026-10-25/REVIEW.md",
    )]
    star_controls = []
    for q in (2, 3, 5, 17):
        basis = scalar_order_basis(q)
        frames = (eye(2),)+neighbor_frames(q)
        if not all(contains(f, x, q) for f in frames for x in basis):
            raise AssertionError("radius-one containment failed")
        if all(contains(Matrix.diag(1, q*q), x, q) for x in basis):
            raise AssertionError("distance-two exclusion failed")
        star_controls.append({"prime": q, "index": q**3,
                              "overorders": len(frames), "target_supplied": True})
    q, length, target = 2**61-1, 31, 23
    frame = Matrix.diag(1, q**target)
    selection = recover_path_vertex(q, length, lambda x: contains(frame, x, q))
    if selection["vertex"] != target or selection["membership_calls"] > 4*length.bit_length():
        raise AssertionError("Eichler path selection failed")
    return {
        "schema": "local-order-scope-controls-v1",
        "status": "classical-baseline scope correction; no new quantum candidate",
        "old_fixture_classification": [
            {"index": 17, "prime": 17, "local_type": "Eichler", "overorders": 2},
            {"index": 9, "prime": 3, "local_type": "Eichler", "overorders": 3},
        ],
        "scalar_order_controls": star_controls,
        "large_prime_eichler_selection": dict(selection, prime=q, length=length),
        "source": {
            "url": "https://arxiv.org/html/2402.05059v2",
            "version_date": "2026-01-21",
            "baseline_has_large_prime_value_dependence_in_general": True,
            "bass_local_baseline_has_polynomial_bit_cost": True,
            "factoring_and_native_representations_are_charged": True,
        },
        "execution_scope": {
            "exact_supplied_local_order_controls": True,
            "native_curve_or_division_execution": False,
            "unknown_native_target_recovered": False,
            "native_hard_instance_generated": False,
            "additive_source_independently_reviewed": False,
            "general_classical_dequantization": False,
            "native_hardness_or_quantum_advantage": False,
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
