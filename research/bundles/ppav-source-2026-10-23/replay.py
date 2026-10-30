"""Replay exact arithmetic controls; never invokes a geometric interpolator."""

import hashlib
import json
from pathlib import Path

from weak_marks import auxiliary_plan, descent_countercontrol, repolarization_countercontrol


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    paper_hash = hashlib.sha256((root/"2026-1142.pdf").read_bytes()).hexdigest()
    if paper_hash != "4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318":
        raise ValueError("retained paper differs from the version reviewed")
    receipt = {
        "status": "ARITHMETIC_AND_SOURCE_CONTRACT_AUDIT_ONLY",
        "paper": "https://eprint.iacr.org/2026/1142",
        "paper_sha256": paper_hash,
        "paper_pages": 44,
        "relevant_pages_read": [10, 11, 12, 13, 14, 15, 33, 34, 35, 36, 37, 38, 39, 40],
        "interpolation_theorem_page_visually_checked": 36,
        "countercontrol": repolarization_countercontrol(),
        "descent_false_positive": descent_countercontrol(),
        "auxiliary_plans": [auxiliary_plan(n, 2, 101) for n in [61, 2**127-1, 2**255-19]],
        "claims": {
            "full_paper_obtained": True,
            "joint_mark_canonicalization_given_geometric_models": "deduced_using_published_algorithms",
            "repolarization_converter_supplied_by_theorem_7_1": False,
            "weak_scalar_sign_enumeration_is_polynomial_time": False,
            "native_geometric_workflow_executed": False,
            "new_speedup_admitted": False,
            "novelty_claim": False,
        },
        "files": {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
                  for name in ["weak_marks.py", "test_weak_marks.py", "replay.py", "PPAV_SOURCE_DECISION.md", "HANDOFF.md"]},
    }
    (root/"source_receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))
