"""Replay projective calibration controls without claiming native execution."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from sympy import eye

from calibration_controls import ROOT, incomplete_frame_countercontrol, quaternion_control, vector_control


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence():
    here = Path(__file__).resolve().parent
    controls = [quaternion_control(r) for r in (3, 5, 7, 13, 17)]
    surface = vector_control(eye(4), 3, (2, 1, 2, 1, 2, 1, 2))
    own = ("projective_calibration.py", "calibration_controls.py", "test_projective_calibration.py",
           "replay_calibration.py", "LARGE_PRIME_AUDIT.md", "HANDOFF.md", "SOURCE_MANIFEST.md")
    imported = set()
    for module in list(sys.modules.values()):
        file = getattr(module, "__file__", None)
        if file:
            path = Path(file).resolve()
            if path.suffix == ".py" and path.is_relative_to(ROOT) and path.parent != here:
                imported.add(path)
    dependencies = [ROOT / name for name in (
        "double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md",
        "native-membership-baseline-2026-10-25/NATIVE_MEMBERSHIP.md",
        "elliptic-field-normalization-2026-10-25/FIELD_NORMALIZATION.md",
    )]
    pdf_hash = digest(here / "chen-petit-accepted.pdf")
    if pdf_hash != "554c6a9f0f49cc13a59e38bf20a351a797137938dce18bd546a9ecf47a656402":
        raise ValueError("audited primary manuscript changed")
    return {
        "status": "SMALL_PRIME_PROJECTIVE_CALIBRATION_WITH_SUPPLIED_MAP_CONTROLS",
        "scope_flags": {name: False for name in (
            "native_curve_backend_executed", "unknown_isogeny_recovered", "quantum_execution",
            "speedup_established", "novelty_established", "global_isogeny_promise_verified",
            "independent_review", "main_registry_integrated", "upstream_suborder_heuristics_removed")},
        "contract": {
            "weak_model": "arbitrary nonzero generator independently for each queried point",
            "extra_queries": "P0+Pj for every j>0; must be available from the original evaluator",
            "weak_calls": "2d-1", "coordinate_entries": "2*r^d",
            "small_prime_only": True, "cache_once_per_prime": True,
            "copies_reuse_same_tuple": True, "global_consistency_is_a_promise": True},
        "quaternion_controls": controls,
        "surface_control": {"prime": 3, "dimension": 4,
                            "weak_point_calls": surface["weak_point_calls"],
                            "coordinate_table_entries": surface["coordinate_table_entries"],
                            "supplied_linear_map_only": True},
        "basis_only_countercontrol": incomplete_frame_countercontrol(),
        "primary_pdf_sha256": pdf_hash,
        "implementation_sha256": {name: digest(here / name) for name in own},
        "dependency_sha256": {str(path.relative_to(ROOT)): digest(path)
                              for path in sorted(imported | set(dependencies))},
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
                      "quaternion_primes": [x["prime"] for x in result["quaternion_controls"]],
                      "surface_control": result["surface_control"],
                      "scope_flags": result["scope_flags"]}, indent=2))
