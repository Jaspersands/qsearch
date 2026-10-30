"""Replay exact controls and conditional conclusions; never native success."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from native_membership import ROOT, content_depth, local_direction
from controls_membership import (
    different_column_masks_counterexample, false_interpolant_control,
    membership_incidence_control, negative_graph_control, smith_contains, supplied_map_control,
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence():
    controls = [supplied_map_control(phi, factors) for phi, factors in (
        ([1, 1, 0, 0], ((2, 1),)), ([1, 2, 0, 0], ((5, 1),)),
        ([3, 4, 0, 0], ((5, 2),)), ([-2, 14, 0, 0], ((2, 3), (5, 2))),
        ([6, 0, 0, 0], ((2, 2), (3, 2))), ([3, 2, 0, 0], ((13, 1),)),
    )]
    scaling = []
    for q, exponents in ((2, (1, 4, 8, 16, 32)), (3, (1, 4, 8))):
        for e in exponents:
            callback = lambda matrix: smith_contains(matrix, q, e, 0, (1, q))
            content = content_depth(q, e, callback)
            direction = local_direction(q, e, content["depth"], callback)
            scaling.append({"prime": q, "exponent": e,
                            "content_calls": content["membership_calls"],
                            "direction_calls": direction["membership_calls"],
                            "supplied_kernel_only": True})
    here = Path(__file__).resolve().parent
    own = ("native_membership.py", "controls_membership.py", "test_native_membership.py",
           "replay_membership.py", "NATIVE_MEMBERSHIP.md", "HANDOFF.md")
    imported = set()
    for module in list(sys.modules.values()):
        file = getattr(module, "__file__", None)
        if file:
            path = Path(file).resolve()
            if path.suffix == ".py" and path.is_relative_to(ROOT) and path.parent != here:
                imported.add(path)
    proof_dependencies = [ROOT / name for name in (
        "ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md",
        "source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md",
        "smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md",
        "double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md",
    )]
    paper = ROOT / "ppav-source-2026-10-23/2026-1142.pdf"
    paper_hash = digest(paper)
    if paper_hash != "4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318":
        raise ValueError("audited interpolation dependency changed")
    return {
        "status": "CONDITIONAL_NATIVE_MEMBERSHIP_REDUCTION_WITH_SUPPLIED_MAP_CONTROLS",
        "scope_flags": {
            "native_geometric_interpolator_executed": False,
            "unknown_native_kernel_recovered": False, "quantum_execution": False,
            "native_classical_hardness_established": False, "speedup_established": False,
            "novelty_established": False, "independent_review": False,
            "main_registry_integrated": False,
        },
        "conditional_negative_result": {
            "id": "NEG-NATIVE-MEMBERSHIP-SMALL-PRIME",
            "status": "CONDITIONAL_ON_NATIVE_PROMISES_AND_PUBLISHED_INTERPOLATION_MODEL",
            "scope": "prime factors bounded polynomially in paid input length, including even/noncyclic degrees",
            "new_coset_source_required": False, "powersmooth_probe_norm_required": False,
            "target_order_advice_required": False, "internal_interpolation_dimension": 8,
            "content_calls": "2*(e+1) per primary component",
            "direction_calls": "2*(q*d+1) for d=e-2a>0; zero for d=0",
            "fixed_transcript_bound": "P>8*n^2*Nmax^2; Nmax=4*(np)^2*sum_basis_norms",
            "native_backend_executed": False,
            "prior_art": "smooth-degree classical tractability is known; novelty not claimed",
        },
        "boolean_interface_bound": {
            "classical_queries": "Theta(q)", "quantum_queries": "Theta(sqrt(q))",
            "scope": "prime-degree Boolean containment oracle with original geometric data discarded",
            "proof": "nonscalar matrix fixes at most two lines; constant-query reduction to unique search",
            "native_problem_hardness_consequence": False,
            "source": "https://arxiv.org/abs/quant-ph/9711070",
            "finite_incidence_controls": [membership_incidence_control(q) for q in (2, 3, 5, 7)],
        },
        "supplied_map_controls": controls,
        "fixed_prime_scaling_controls": scaling,
        "nonintegral_valid_graph": negative_graph_control(),
        "different_column_masks": different_column_masks_counterexample(),
        "insufficient_level_false_positive": false_interpolant_control(),
        "ppav_dependency_sha256": paper_hash,
        "implementation_sha256": {name: digest(here / name) for name in own},
        "dependency_sha256": {str(path.relative_to(ROOT)): digest(path)
                              for path in sorted(imported | set(proof_dependencies))},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = evidence()
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    path = Path(__file__).with_name("receipt.json")
    if args.write:
        path.write_text(encoded)
    if args.check and path.read_text() != encoded:
        sys.exit("receipt mismatch")
    print(json.dumps({
        "status": result["status"],
        "supplied_map_degrees": [x["degree"] for x in result["supplied_map_controls"]],
        "membership_counts": [x["query_count"] for x in result["supplied_map_controls"]],
        "dyadic_scaling": [x for x in result["fixed_prime_scaling_controls"] if x["prime"] == 2],
        "negative_result": result["conditional_negative_result"]["id"],
        "scope_flags": result["scope_flags"],
    }, indent=2))
