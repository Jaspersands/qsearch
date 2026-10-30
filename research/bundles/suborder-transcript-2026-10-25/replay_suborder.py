"""Replay local suborder controls; never report an executed global solver."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from suborder_transcript import ROOT
from controls_suborder import (
    inseparable_half_control, primitive_degree_countercontrol,
    right_order_inseparability_control, supplied_transcript_control, unknown_depth_control,
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence():
    here = Path(__file__).resolve().parent
    controls = [supplied_transcript_control(phi, prime, multiple)
                for phi, multiple in (([1, 1, 0, 0], 1), ([3, 4, 0, 0], 1),
                                      ([-1, 0, 2, 0], 1), ([-1, -1, 2, 2], 1),
                                      ([1, 1, 0, 0], 121))
                for prime in (3, 7, 13)]
    half = inseparable_half_control()
    own = ("suborder_transcript.py", "controls_suborder.py", "test_suborder_transcript.py",
           "replay_suborder.py", "SUBORDER_TRANSCRIPT.md", "HANDOFF.md")
    imported = set()
    for module in list(sys.modules.values()):
        file = getattr(module, "__file__", None)
        if file:
            path = Path(file).resolve()
            if path.suffix == ".py" and path.is_relative_to(ROOT) and path.parent != here:
                imported.add(path)
    proof_dependencies = [ROOT / name for name in (
        "double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md",
        "cyclic-odd-degree-source-2026-10-25/CYCLIC_ODD_DEGREE.md",
        "elliptic-field-normalization-2026-10-25/FIELD_NORMALIZATION.md",
        "large-prime-source-audit-2026-10-25/LARGE_PRIME_AUDIT.md",
        "large-prime-source-audit-2026-10-25/chen-petit-accepted.pdf",
    )]
    return {
        "status": "DIRECT_SMALL_LEVEL_SUBORDER_TRANSCRIPT_WITH_PROPOSED_GLOBAL_REDUCTION",
        "scope_flags": {name: False for name in (
            "native_curve_backend_executed", "unknown_isogeny_recovered", "geometric_source_executed",
            "quantum_execution", "speedup_established", "novelty_established", "independent_review",
            "main_registry_integrated", "unconditional_full_suborder_algorithm_established")},
        "implemented_local_conversion": {
            "known_source_calls_per_prime": 8, "known_suborder_calls_per_prime": 8,
            "unknown_isogeny_calls": 0, "coordinate_entries": "2*r^2",
            "global_dictionary_required": True, "small_prime_only": True,
            "norm_equation_solver_called": False, "global_promise_verified_from_tests": False},
        "proposed_global_reduction": {
            "status": "WRITTEN_PROOF_PENDING_INDEPENDENT_REVIEW_AND_GEOMETRIC_COMPOSITION",
            "primitive_degree": "D=p^epsilon*d, epsilon in {0,1}, d divides m=N/p^v_p(N)",
            "query_modulus": "m", "marking_degree_bound": "p*m",
            "source_congruence": "2*m; no ramified split or characteristic padding",
            "target_order_output": "right_order of the separable-kernel annihilator ideal",
            "primitive_inclusion_required": False, "local_degree_inference_permitted": False},
        "supplied_map_controls": controls,
        "primitive_degree_countercontrol": primitive_degree_countercontrol(),
        "inseparable_half_control": half,
        "right_order_control": right_order_inseparability_control(),
        "unknown_depth_controls": [unknown_depth_control(q, 4, k, (1, q))
                                   for q in (2, 3, 5) for k in range(5)],
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
    print(json.dumps({"status": result["status"],
                      "supplied_map_controls": len(result["supplied_map_controls"]),
                      "inseparable_half_control": result["inseparable_half_control"],
                      "scope_flags": result["scope_flags"]}, indent=2))
