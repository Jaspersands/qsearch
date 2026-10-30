"""Replay the scoped field deduction, including the opposite-twist falsifier."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from elliptic_fields import normalization_plan, twist_countercontrol


def evidence():
    here = Path(__file__).resolve().parent
    own = ("elliptic_fields.py", "test_elliptic_fields.py", "replay_elliptic_fields.py",
           "FIELD_NORMALIZATION.md")
    return {
        "status": "ELLIPTIC_COMMON_FIELD_PROMISE_DERIVED_WITH_EXACT_TWIST_CONTROL",
        "scope": "supersingular elliptic endpoints over one explicitly represented finite field",
        "field_plan": normalization_plan(11, 2, [(3, 1), (5, 1), (7, 2)]),
        "twist_countercontrol": twist_countercontrol(),
        "scope_flags": {"unknown_isogeny_computed": False, "geometric_source_executed": False,
                        "independent_review": False, "novelty_established": False,
                        "general_surface_field_promise_removed": False,
                        "main_registry_integrated": False},
        "implementation_sha256": {
            name: hashlib.sha256((here / name).read_bytes()).hexdigest() for name in own
        },
        "proof_dependencies": {
            "trace_classification": "https://arxiv.org/html/2501.16321v2#S2.SS2",
            "field_primitives": "https://eprint.iacr.org/2026/1142",
            "previous_field_note_sha256": hashlib.sha256((here.parent /
                "source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md").read_bytes()).hexdigest(),
        },
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
                      "relative_extension": result["field_plan"]["relative_base_extension"],
                      "actual_curve_point_counts": [x["points_over_F121"]
                          for x in result["twist_countercontrol"]["curves"]],
                      "scope_flags": result["scope_flags"]}, indent=2))
