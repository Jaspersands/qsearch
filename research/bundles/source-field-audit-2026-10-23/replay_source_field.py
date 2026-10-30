"""Record bounded source-representation controls, never a speedup result."""

import hashlib
import json
from pathlib import Path

from source_field_controls import auxiliary_field_plan, conjugate_curve_control


def main():
    root = Path(__file__).resolve().parent
    records = [auxiliary_field_plan(p, m, sign, tuple((r, 2) for r in (2, 3, 5, 7, 11, 13) if r != p))
               for p, m, sign in ((7, 1, -1), (37, 1, -1), (101, 17, 1))]
    files = [root/name for name in ("source_field_controls.py", "test_source_field_controls.py",
                                   "replay_source_field.py", "SOURCE_FIELD_AUDIT.md", "HANDOFF.md")]
    files.append(root.parent/"ppav-source-2026-10-23"/"2026-1142.pdf")
    record = {"status": "SOURCE_REPRESENTATION_AUDIT_REVIEW_PENDING",
              "fixed_field_result": "conditional_on_common_scalar_field_and_effective_theta_primitives",
              "field_plans": records, "actual_curve_countercontrol": conjugate_curve_control(),
              "source_wrapped_frobenius_escape": "excluded_by_naturality_identity",
              "geometric_quotients_executed": False, "coherent_source_executed": False,
              "general_classical_dequantization_established": False,
              "quantum_speedup_admitted": False,
              "source_sha256": {str(path.relative_to(root.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in files}}
    destination = root/"source_field_receipt.json"
    destination.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "field_plans": len(records),
                      "curve_counts": [record["actual_curve_countercontrol"][name]["points"]
                                       for name in ("curve", "conjugate_curve")],
                      "invalid_galois_canonicalization_falsified": True,
                      "coherent_source_executed": False}, indent=2))


if __name__ == "__main__":
    main()
