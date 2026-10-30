"""Record scoped access falsifiers, not native hardness or a new algorithm."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from access_audit import (
    ROOT, frobenius_product_control, gram_nonclosure_control, odd_maximal_split,
    projective_centralizer_count, same_degree_ambiguity_control, stabilized_controls,
    unbounded_primitive_family_control,
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence():
    here = Path(__file__).resolve().parent
    own = ("access_audit.py", "test_access_audit.py", "replay_access_audit.py",
           "ACCESS_CEILING.md", "HANDOFF.md", "RETAINED_MARKED_RIGIDITY.md")
    retained_hash = digest(here / "RETAINED_MARKED_RIGIDITY.md")
    if retained_hash != "7dc0b41c1dc76dddb6b8ec385fbf25f11ca814da02cf8d27fdef0065b3a0d034":
        raise ValueError("retained read-only rigidity proof changed")
    imported = set()
    for module in list(sys.modules.values()):
        file = getattr(module, "__file__", None)
        if file:
            path = Path(file).resolve()
            if path.suffix == ".py" and path.is_relative_to(ROOT) and path.parent != here:
                imported.add(path)
    dependencies = [ROOT / name for name in (
        "suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md",
        "smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md",
        "source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md",
        "ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md",
        "ppav-source-2026-10-23/2026-1142.pdf",
    )]
    return {
        "status": "SCOPED_FALSIFICATION_OF_ONE_ENDOMORPHISM_ACCESS_SHORTCUTS",
        "scope_flags": {name: False for name in (
            "native_geometric_backend_executed", "unknown_kernel_recovered", "quantum_execution",
            "speedup_established", "native_hardness_established", "general_quantum_no_go",
            "independent_review", "novelty_established", "main_registry_integrated")},
        "negative_records": [
            {"id": "NEG-ONE-ENDO-SCALAR-INTERTWINER-TRANSFER",
             "claim_rejected": "one nonscalar action determines the torsion isogeny up to scalar",
             "scope": "known degree also insufficient; two genuine degree-three maps supplied",
             "surviving_obligation": "remove or coherently process the quadratic centralizer ambiguity"},
            {"id": "NEG-ONE-ENDO-PRIMITIVE-DEGREE-TRANSFER",
             "claim_rejected": "fixed quadratic input bounds every primitive intertwiner degree",
             "scope": "not a lower bound against selecting a small representative",
             "surviving_obligation": "construct a globally consistent bounded representative or another source"},
            {"id": "NEG-ONE-ENDO-STABILIZATION-FROBENIUS-CLOSURE",
             "claim_rejected": "copies and natural Frobenius arrows supply a full quaternion action",
             "scope": "specified known algebra operations; genuinely new maps are not excluded",
             "exception": "known self-Frobenius not commuting with alpha can supply a second operator"},
            {"id": "NEG-ONE-ENDO-GRAM-QUERY-GROUP",
             "claim_rejected": "Gram-in-quadratic-field integral automorphisms form a query group",
             "scope": "explicit two-automorphism nonclosure, not a ban on non-group algorithms"},
        ],
        "projective_counts": [{"prime": r, "count": projective_centralizer_count(odd_maximal_split(11, r)[1], r)}
                              for r in (3, 5, 7, 13, 17)],
        "stabilization_controls": [stabilized_controls(r, copies) for r in (3, 5, 7) for copies in (1, 2, 3)],
        "frobenius_controls": [frobenius_product_control(r) for r in (3, 5, 7, 13)],
        "same_degree_controls": [same_degree_ambiguity_control(r) for r in (5, 7, 13, 17)],
        "unbounded_primitive_family": unbounded_primitive_family_control(),
        "gram_nonclosure": gram_nonclosure_control(),
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
                      "negative_ids": [r["id"] for r in result["negative_records"]],
                      "scope_flags": result["scope_flags"]}, indent=2))
