"""Replay finite evidence while keeping native-source and quantum claims false."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

from sympy import Matrix, eye, zeros

from cyclic_source import (
    ROOT, certificate_queries, combine_local_lines, cyclic_annihilator,
    odd_ring_lift, uniform_plan,
)
from controls_cyclic import (
    cyclic_degree25_control, preserves_doubled, split_fixture, square_phase_control,
)
from kernel_output import action, matrix_multiply, mod, odd_maximal_order, product_actions


def evidence():
    order, n, factors = odd_maximal_order(11), 45, ((3, 2), (5, 1))
    split = split_fixture(11, n, factors)
    query = certificate_queries((3, 5), n, factors)[1]
    lift = odd_ring_lift(order, split, query, n, factors)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, lift["sigma"], lift["inverse"]) == identity
    assert mod(action(lift["sigma"], product_actions(split)), n) == query
    plan = uniform_plan(order, n, factors, 11)
    assert lift["trace"] <= plan["trace_bound"]
    lines = combine_local_lines(n, factors, [(0, 1), (1, 0)])
    ideal = cyclic_annihilator(order, split, lines, n, factors)
    assert abs(ideal.det()) == n*n
    checks = certificate_queries((1, 0), 9, ((3, 2),))
    counterexample = {
        str(v): [preserves_doubled(g, v, 9) for g in checks]
        for v in ((1, 0), (1, 3), (1, 6))
    }
    phases = [square_phase_control(p, e, 2, 4)
              for p, e in ((3, 1), (3, 2), (3, 3), (5, 2), (5, 3), (7, 2))]
    for record in phases:
        assert abs(record["normalization"]-1) < 1e-12
        assert abs(record["correct_probability"]-record["predicted_probability"]) < 1e-12
        for key, value in record.items():
            if isinstance(value, float):
                record[key] = round(value, 12)
    attempts, failure_target = 0, Fraction(1, 2**40)
    while len(factors)*Fraction(7, 9)**attempts > failure_target:
        attempts += 1
    paper = ROOT / "ppav-source-2026-10-23" / "2026-1142.pdf"
    paper_hash = hashlib.sha256(paper.read_bytes()).hexdigest()
    if paper_hash != "4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318":
        raise ValueError("PPAV dependency differs from the audited version")
    own_files = ("cyclic_source.py", "controls_cyclic.py", "test_cyclic_source.py",
                 "replay_cyclic.py", "CYCLIC_ODD_DEGREE.md", "HANDOFF.md")
    dependencies = (
        "kernel-output-2026-10-23/kernel_output.py",
        "kernel-output-2026-10-23/uniform_source_bound.py",
        "smooth-repolarization-2026-10-23/smooth_repolarization.py",
        "smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md",
        "prime-only-source-2026-10-25/prime_source.py",
        "prime-only-source-2026-10-25/PRIME_ONLY_SOURCE.md",
        "prime-only-source-2026-10-25/ELLIPTIC_COROLLARY.md",
        "source-pullback-2026-10-23/pullback.py",
        "source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md",
    )
    return {
        "status": "PROPOSED_ODD_CYCLIC_SOURCE_REVIEW_PENDING",
        "scope_flags": {
            "geometric_source_executed": False, "quantum_execution": False,
            "unknown_kernel_recovered": False, "ideal_to_isogeny_executed": False,
            "advantage_established": False, "novelty_established": False,
            "independent_review": False, "main_registry_integrated": False,
        },
        "input_scope": "genuine odd cyclic weak isogeny, full known source order, paid fields",
        "uniform_plan": {
            "degree": n, "factors": [list(f) for f in factors], "characteristic": 11,
            "trace_bound_hex": hex(plan["trace_bound"]),
            "trace_bound_bits": plan["trace_bound"].bit_length(),
            "multiplier_hex": hex(plan["multiplier"]),
            "multiplier_bits": plan["multiplier"].bit_length(),
            "quotient_primes": plan["quotient_primes"],
            "marking_primes": plan["marking_primes"],
            "maximum_weak_order": max(plan["weak_query_orders"]),
            "weak_query_exponent": 1, "stabilized_dimension": 16,
            "largest_kernel_point_list_hex": hex(max(plan["quotient_primes"])**16),
            "kernel_points_actually_enumerated": 0,
            "theta_level_four_still_required": True,
            "physical_length_bound": 36, "quaternion_length_bound": 145,
        },
        "compiler_control": {
            "query": [list(map(int, query.row(i))) for i in range(4)],
            "trace_hex": hex(lift["trace"]), "trace_is_odd": lift["trace"] % 2 == 1,
            "trace_within_bound": True, "same_query_reduction": True,
            "exact_integral_inverse": True, "physical_length": lift["physical_length"],
            "quaternion_length": len(lift["quaternion_factors"]),
            "split_fixture_enumerative": True,
        },
        "mod9_certificate_control": counterexample,
        "local_phase_controls": phases,
        "conditional_receiver_bound": {
            "components": len(factors), "attempts_per_chart": attempts,
            "coherent_source_queries_at_most": 2*len(factors)*attempts,
            "classical_source_evaluations_at_most": 4*len(factors)*attempts+1,
            "ideal_sampling_failure_target": str(failure_target),
            "source_clock_and_approximation_error_separate": True,
            "not_an_executed_receiver": True,
        },
        "supplied_line_postprocessing": {
            "vector": list(map(int, lines)),
            "ideal_hnf": [list(map(int, ideal.row(i))) for i in range(4)],
            "ideal_index": int(abs(ideal.det())), "ideal_norm": n,
            "secret_line_supplied_not_recovered": True,
        },
        "degree25_algebraic_control": cyclic_degree25_control(),
        "imported_ppav_dependency_sha256": paper_hash,
        "implementation_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in own_files
        },
        "dependency_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in dependencies
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = evidence()
    path = Path(__file__).with_name("receipt.json")
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    if args.check and json.loads(path.read_text()) != result:
        sys.exit("receipt mismatch")
    print(json.dumps({
        "status": result["status"],
        "quotient_prime_count": len(result["uniform_plan"]["quotient_primes"]),
        "maximum_weak_order": result["uniform_plan"]["maximum_weak_order"],
        "trace_bound_bits": result["uniform_plan"]["trace_bound_bits"],
        "multiplier_bits": result["uniform_plan"]["multiplier_bits"],
        "receiver_bound": result["conditional_receiver_bound"],
        "mod9_certificate_control": result["mod9_certificate_control"],
        "scope_flags": result["scope_flags"],
    }, indent=2))
