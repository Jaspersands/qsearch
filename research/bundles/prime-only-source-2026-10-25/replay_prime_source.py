"""Deterministic receipt; no geometric or quantum execution flags are promoted."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from sympy import Matrix, eye

from prime_source import ROOT, odd_trace_bound, odd_trace_lift, prime_resource_plan
from kernel_output import odd_maximal_order, odd_maximal_split
from controls_prime_source import integral_control
from elliptic_reduction import annihilator_ideal, line_from_doubled_kernel


def evidence():
    order, ell = odd_maximal_order(11), 5
    bound = odd_trace_bound(order, ell)
    plan = prime_resource_plan(bound["trace_bound"], ell, 11)
    query = eye(4)
    query[0, 1] = 1
    lift = odd_trace_lift(order, odd_maximal_split(11, ell), query, ell)
    supplied_plane = Matrix([[1, 0], [2, 0], [0, 1], [0, 2]])
    line = line_from_doubled_kernel(supplied_plane, ell)
    ideal = annihilator_ideal(order, odd_maximal_split(11, ell), line, ell)
    paper = ROOT / "ppav-source-2026-10-23" / "2026-1142.pdf"
    paper_hash = hashlib.sha256(paper.read_bytes()).hexdigest()
    if paper_hash != "4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318":
        raise ValueError("PPAV dependency differs from the audited version")
    return {
        "status": "PROPOSED_PRIME_ONLY_SOURCE_REVIEW_PENDING",
        "input_scope": "same weak surface isogeny; sufficient fixed odd prime levels",
        "scope_flags": {"geometric_execution": False, "quantum_execution": False,
                        "novelty_established": False, "advantage_established": False,
                        "independent_review": False},
        "uniform_plan": {
            "ell": ell, "characteristic": 11,
            "trace_bound_hex": hex(bound["trace_bound"]),
            "trace_bound_bits": bound["trace_bound"].bit_length(),
            "multiplier_hex": hex(plan["multiplier"]),
            "multiplier_bits": plan["multiplier"].bit_length(),
            "quotient_primes": plan["quotient_primes"],
            "marking_primes": plan["marking_primes"],
            "maximum_weak_order": max(plan["weak_evaluation_orders"]),
            "weak_query_exponent": plan["quotient_torsion_exponent"],
            "maximum_auxiliary_relative_field_degree": max(plan["auxiliary_field_degree_bounds"].values()),
            "largest_kernel_point_list_hex": hex(plan["largest_quotient_kernel_point_list"]),
            "stabilized_dimension": 16,
            "theta_level_four_still_required": True,
            "kernel_points_actually_enumerated": 0,
        },
        "compiler_control": {
            "query": [[int(x) for x in query.row(i)] for i in range(4)],
            "trace_hex": hex(lift["trace"]), "trace_is_odd": bool(lift["trace"] % 2),
            "trace_within_uniform_bound": lift["trace"] <= bound["trace_bound"],
            "quaternion_length": lift["quaternion_length"],
            "quaternion_length_bound": bound["quaternion_length_bound"],
            "public_split_backend": "small enumerative fixture, not scalable",
        },
        "integral_control": integral_control(),
        "elliptic_postprocessing_control": {
            "input_plane_supplied_not_recovered": True,
            "recovered_line": [int(x) for x in line],
            "annihilator_ideal_hnf": [[int(x) for x in ideal.row(i)] for i in range(4)],
            "ideal_index": int(abs(ideal.det())), "ideal_norm": ell,
            "secret_recovery_executed": False, "ideal_to_isogeny_executed": False,
        },
        "imported_ppav_dependency_sha256": paper_hash,
        "implementation_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ("prime_source.py", "controls_prime_source.py", "test_prime_source.py",
                         "elliptic_reduction.py", "test_elliptic_reduction.py",
                         "PRIME_ONLY_SOURCE.md", "ELLIPTIC_COROLLARY.md")
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
    print(json.dumps({"status": result["status"],
                      "quotient_prime_count": len(result["uniform_plan"]["quotient_primes"]),
                      "maximum_weak_order": result["uniform_plan"]["maximum_weak_order"],
                      "weak_query_exponent": result["uniform_plan"]["weak_query_exponent"],
                      "trace_bound_bits": result["uniform_plan"]["trace_bound_bits"],
                      "multiplier_bits": result["uniform_plan"]["multiplier_bits"],
                      "local_kernel_checks": result["integral_control"]["local_kernels"],
                      "scope_flags": result["scope_flags"]}, indent=2))
