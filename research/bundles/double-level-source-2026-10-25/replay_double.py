"""Replay algebraic evidence, retaining explicit native/quantum scope limits."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from sympy import Matrix, eye, zeros

from double_level_source import ROOT, congruence_lift, resource_plan
from controls_double import (
    classical_control, even_isogeny_control, full_split_fixture, mixed_even_ideal_control,
)
from half_norm import half_certificate, verify_half_certificate
from kernel_output import action, alternating_form, matrix_multiply, mod, odd_maximal_order, product_actions


def evidence():
    order, n, factors = odd_maximal_order(11), 6, ((2, 1), (3, 1))
    split = full_split_fixture(11, n, factors)
    vector = Matrix([1, 2, 3, 4])
    query = mod(eye(4)+vector*vector.T*alternating_form(2), n)
    lift = congruence_lift(order, split, query, n, factors)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, lift["sigma"], lift["inverse"]) == identity
    assert mod(action(lift["sigma"], product_actions(split)), n) == query
    assert mod(lift["S"]-identity, 2*n) == zeros(16, 1)
    plan = resource_plan(order, n, factors, 11)
    assert lift["trace"] <= plan["trace_bound"]
    boundary = verify_half_certificate(half_certificate(2, 15))
    assert all(boundary.values())
    baselines = [classical_control(2, e, 0, (1, 2)) for e in (1, 4, 8, 16, 32)]
    baselines += [classical_control(p, 5, 1, (1, p)) for p in (3, 5, 7)]
    paper = ROOT / "ppav-source-2026-10-23" / "2026-1142.pdf"
    paper_hash = hashlib.sha256(paper.read_bytes()).hexdigest()
    if paper_hash != "4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318":
        raise ValueError("audited PPAV dependency changed")
    own = ("double_level_source.py", "half_norm.py", "local_baseline.py",
           "controls_double.py", "test_double_level.py", "replay_double.py",
           "DOUBLE_LEVEL_SOURCE.md", "HANDOFF.md")
    dependencies = (
        "kernel-output-2026-10-23/kernel_output.py",
        "kernel-output-2026-10-23/uniform_source_bound.py",
        "smooth-repolarization-2026-10-23/smooth_repolarization.py",
        "smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md",
        "cyclic-odd-degree-source-2026-10-25/controls_cyclic.py",
        "cyclic-odd-degree-source-2026-10-25/cyclic_source.py",
        "cyclic-odd-degree-source-2026-10-25/CYCLIC_ODD_DEGREE.md",
        "odd-content-reduction-2026-10-25/ODD_CONTENT_REDUCTION.md",
        "source-pullback-2026-10-23/pullback.py",
        "source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md",
        "prime-only-source-2026-10-25/PRIME_ONLY_SOURCE.md",
    )
    return {
        "status": "CONDITIONAL_DOUBLE_LEVEL_SOURCE_AND_CLASSICAL_SMALL_PRIME_BASELINE",
        "scope_flags": {
            "native_geometric_source_executed": False, "quantum_execution": False,
            "unknown_native_kernel_recovered": False, "speedup_established": False,
            "novelty_established": False, "independent_review": False,
            "main_registry_integrated": False,
        },
        "uniform_plan": {
            "original_degree": n, "compiler_modulus": 2*n, "characteristic": 11,
            "trace_bound_hex": hex(plan["trace_bound"]),
            "trace_bound_bits": plan["trace_bound"].bit_length(),
            "multiplier_hex": hex(plan["multiplier"]),
            "multiplier_bits": plan["multiplier"].bit_length(),
            "quotient_primes": plan["quotient_primes"],
            "marking_primes": plan["marking_primes"],
            "maximum_weak_order": max(plan["quotient_primes"]+plan["marking_primes"]),
            "weak_query_exponent": 1, "weak_even_order_required": False,
            "public_theta_level_four_still_required": True,
            "stabilized_dimension": 16, "kernel_points_enumerated": 0,
            "largest_kernel_point_list_hex": hex(max(plan["quotient_primes"])**16),
            "physical_factor_bound": 36, "quaternion_factor_bound": 144,
        },
        "compiler_control": {
            "same_original_query": True, "exact_inverse": True,
            "gram_identity_mod_2n": True, "trace_mod4": lift["trace"] % 4,
            "trace_hex": hex(lift["trace"]), "physical_factors": lift["physical_length"],
            "quaternion_factors": len(lift["quaternion_factors"]),
            "dyadic_split_computed_from_source_order": True,
            "odd_prime_split_fixture_enumerative": True,
        },
        "trace_two_formal_certificate": boundary,
        "even_degree2_control": even_isogeny_control(),
        "mixed_degree200_ideal_control": mixed_even_ideal_control(),
        "classical_scaling_controls": baselines,
        "conditional_negative_result": {
            "id": "NEG-DOUBLE-LEVEL-SMALL-PRIME-EXPONENT",
            "status": "CONDITIONAL_DEQUANTIZATION_UNDER_SAME_SOURCE_PROMISE",
            "scope": "prime factors bounded polynomially in paid input length; fixed-prime exponent sweeps",
            "attack": "two scaled prefix certificates per candidate digit, plus content period probes",
            "direction_source_comparisons": "2*(q*d+1) per positive-depth primary component",
            "content_source_comparisons": "2*(e+1) per primary component",
            "identity_evaluation": "one globally cached source evaluation",
            "falsifier": "small-prime growing-exponent success is not a superpolynomial quantum separation",
            "not_excluded": "large-prime directions; attacks exploiting actual geometric label contents",
            "same_source_backend_executed": False,
            "native_classical_hardness_established": False,
        },
        "ppav_dependency_sha256": paper_hash,
        "implementation_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in own
        },
        "dependency_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in dependencies
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
        "dyadic_direction_counts": [[r["exponent"], r["direction"]["source_comparisons"]]
                                     for r in result["classical_scaling_controls"] if r["prime"] == 2],
        "negative_result": result["conditional_negative_result"]["id"],
        "scope_flags": result["scope_flags"],
    }, indent=2))
