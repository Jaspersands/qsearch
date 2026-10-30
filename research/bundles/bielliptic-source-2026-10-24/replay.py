"""Reproducible finite controls, with native/quantum execution kept false."""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from sympy import Matrix, eye

from bielliptic import (
    action, apply_curve_lift, assemble_kernel, embed_factors,
    even_elliptic_quotients, map_even_quotient, matrix_key, mod, product_actions,
)
from audit_controls import curve_control, order_four_control, rank_census, run_arithmetic, sl2_elements
from residual import nullspace, same_space
from residual_controls import OpaqueLabels, space_key


def rows(matrix):
    return [[int(x) for x in matrix.row(i)] for i in range(matrix.rows)]


def run():
    curves = []
    for prime in (13, 2**127-1):
        curve, points, lifts = curve_control(prime)
        found = next(lift for lift in lifts if lift.matrix == matrix_key(Matrix.diag(-1, 1), prime))
        assert found.status == "ELLIPTIC_INVOLUTION"
        point_checks = [0, 0]
        if prime == 13:
            quotient_equations = even_elliptic_quotients(curve)
            for x, z in [(1, 0)] + [(x, 1) for x in range(prime)]:
                for y in range(prime):
                    if y*y % prime != curve.value(x, z):
                        continue
                    for side in (0, 1):
                        output = map_even_quotient(curve, (x, z, y), side)
                        if output is not None:
                            u, v = output
                            assert v*v % prime == sum(c*pow(u, i, prime)
                                for i, c in enumerate(quotient_equations[side])) % prime
                        point_checks[side] += 1
        curves.append({
            "prime": prime, "actual_curve_coefficients": list(curve.coefficients),
            "supplied_and_checked_branch_points": [list(p) for p in points],
            "projective_triples_checked": 120, "field_enumeration_for_discovery": False,
            "reduced_involutions": [asdict(x) for x in lifts],
            "quotient_curve_points_checked": point_checks,
            "native_weak_isogeny_attached": False,
        })

    curve, lift = order_four_control()
    once = apply_curve_lift(curve, lift, (1, 0, 1), 5)
    twice = apply_curve_lift(curve, lift, once, 5)
    assert twice == (1, 0, 12)
    negative = {"curve_coefficients": list(curve.coefficients),
                "lift": asdict(lift), "start": [1, 0, 1], "once": list(once),
                "twice": list(twice), "self_adjoint_gate_eligible": False}

    arithmetic = []
    for kind in ("mixing", "stable_swap"):
        source, recovered, result = run_arithmetic(kind)
        assert recovered.coordinates == source.reference_pullbacks()
        actual = nullspace(action(source.phi, product_actions(source.split(5))), 5)
        restriction_checks = []
        if result.image.cols == 2:
            assert same_space(actual, result.image, 5)
        else:
            coordinates = mod(result.frame.inv_mod(5)*actual, 5)
            plus = next(coordinates[:2, j] for j in range(2) if any(coordinates[:2, j]))
            minus = next(coordinates[2:, j] for j in range(2) if any(coordinates[2:, j]))
            assert same_space(actual, assemble_kernel(result, plus, minus), 5)
            for side, line in enumerate((plus, minus)):
                oracle, forward, backward = OpaqueLabels(actual, 5), {}, {}
                for a in sl2_elements(5):
                    factors = (a, eye(2)) if side == 0 else (eye(2), a)
                    label = oracle(embed_factors(result, *factors))
                    key = space_key(a*line, 5)
                    assert label not in forward or forward[label] == key
                    assert key not in backward or backward[key] == label
                    forward[label], backward[key] = key, label
                assert len(forward) == len(backward) == 6
                restriction_checks.append({"factor": side, "opaque_queries": oracle.calls,
                                           "distinct_orbit_labels": len(forward)})
        arithmetic.append({
            "fixture": kind, "fixture_target": "PRODUCT_NOT_SMOOTH_JACOBIAN",
            "ell": 5, "characteristic": 11, "status": result.status,
            "pullback_source_coordinates": [int(x) for x in recovered.coordinates[0]],
            "image_rank": result.image.cols, "image": rows(result.image),
            "beta_source_coordinates": [int(x) for x in result.beta_coordinates],
            "source_involution_kind": result.source_split.kind if result.source_split else None,
            "algebra_compatible_lagrangians": result.compatible_lagrangian_count,
            "crt_primes": list(recovered.primes), "crt_modulus": recovered.modulus,
            "weak_basis_points_required_not_executed": recovered.weak_basis_points_required,
            "target_map_points_required_not_executed": recovered.target_basis_points_required,
            "actual_geometric_torsion_points_evaluated": 0,
            "two_factor_restriction_controls": restriction_checks,
            "quantum_receiver_executed": result.quantum_receiver_executed,
        })
    census = {str(ell): rank_census(ell) for ell in (3, 5, 7)}
    for ell, counts in census.items():
        ell = int(ell)
        assert counts == {0: (ell+1)**2, 1: 0, 2: ell*(ell*ell-1)}
    here = Path(__file__).resolve().parent
    paths = [here / name for name in (
        "bielliptic.py", "audit_controls.py", "test_bielliptic.py", "replay.py",
        "BIELLIPTIC_SOURCE.md", "HANDOFF.md")]
    paths += [here.parent / name for name in (
        "source-pullback-2026-10-23/pullback.py", "source-pullback-2026-10-23/controls.py",
        "frobenius-residual-2026-10-23/residual.py",
        "frobenius-residual-2026-10-23/residual_controls.py",
        "kernel-output-2026-10-23/kernel_output.py",
        "scalar-cancellation-2026-10-23/scalar_cancellation.py")]
    return {
        "scope": "native curve-map frontend and conditional bielliptic weak-isogeny reduction",
        "independent_review": False, "novelty_claim": False,
        "complete_native_weak_isogeny_executed": False, "quantum_execution": False,
        "classical_solution_of_rank_zero_claimed": False,
        "generic_surface_solution_claimed": False,
        "curve_controls": curves, "order_four_falsifier": negative,
        "arithmetic_controls": arithmetic, "abstract_rank_census_not_success_probability": census,
        "elliptic_reduction": {
            "theorem_status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "native_geometry_bridge_implemented": False,
            "odd_access_preserved": True,
            "even_access_requires_original_doubled_levels": True,
            "known_elliptic_solver_executed": False,
            "imported_PQLP_runtime_assumptions_not_removed": True,
        },
        "sha256": {str(p.relative_to(here.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in paths},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.output and args.verify:
        parser.error("choose output or verify")
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.verify:
        assert json.loads(encoded) == json.loads(args.verify.read_text())
        print(json.dumps({"receipt_replay_matches": True, "hashes": len(result["sha256"])}))
    elif args.output:
        args.output.write_text(encoded)
        print(json.dumps({"output": str(args.output.resolve()), "hashes": len(result["sha256"]),
                          "statuses": [row["status"] for row in result["arithmetic_controls"]]}))
    else:
        print(encoded, end="")
