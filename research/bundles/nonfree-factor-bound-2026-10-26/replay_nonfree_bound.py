"""Replay exact factor certificates, not native geometric recovery."""

import argparse
import hashlib
import json
from pathlib import Path

from sympy import Matrix, eye, zeros

from nonfree_factor_bound import automorphism_certificate, factor_certificate, shear_product_control
from kernel_output import odd_maximal_order

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def receipt():
    order = odd_maximal_order(11)
    i, h = eye(4)[:, 1], eye(4)[:, 2]
    controls = []
    for x, y, reverse in ((h, i, False), (i, h, True), (10**30*h, i, False)):
        a, beta, d, projector = shear_product_control(order, x, y, reverse)
        result = factor_certificate(order, beta, a, beta, d, projector)
        if not result["witness_does_not_commute"] or result["witness_degree"] > result["degree_bound"]:
            raise AssertionError("short noncommuting certificate failed")
        controls.append(result)
    a, beta, d, projector = shear_product_control(order, h, i)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    automorphisms = [automorphism_certificate(order, beta, a, beta, d, identity-2*projector)]
    phase = Matrix.vstack(order.unit, order.multiply(h, order.unit-i), zeros(4, 1), i)
    automorphisms.append(automorphism_certificate(order, h, 1, h, 4, phase))
    paths = [HERE / name for name in (
        "NONFREE_FACTOR_BOUND.md", "nonfree_factor_bound.py",
        "test_nonfree_factor_bound.py", "replay_nonfree_bound.py",
    )]
    paths += [ROOT / name for name in (
        "polarization-completion-probe-2026-10-25/polarization_probe.py",
        "polarization-completion-probe-2026-10-25/receipt.json",
        "kernel-output-2026-10-23/kernel_output.py",
    )]
    return {
        "schema": "nonfree-factor-small-diagonal-bound-v1",
        "status": "deductive binary factor and automorphism bounds; supplied controls only",
        "controls": controls,
        "automorphism_controls": automorphisms,
        "scope": {
            "exact_supplied_order_certificates": True,
            "nonfree_factor_case_is_deductive_not_geometric_test": True,
            "native_nonfree_factor_constructed": False,
            "native_low_degree_enumeration_executed": False,
            "native_unknown_order_recovered": False,
            "all_high_height_families_excluded": False,
            "arbitrary_nonbinary_source_attacks_excluded": False,
            "independent_review": False,
            "quantum_advantage_established": False,
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
