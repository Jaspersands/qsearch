"""Finite protocol receipt: supplied kernels are never presented as recovered."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from content_reduction import ROOT
from controls_content import content_control, ideal_scaling_control, noncyclic_endomorphism_control


def evidence():
    scenarios = [
        content_control(3**5, ((3, 5),), {3: (5, 1, (1, 3))}),
        content_control(3**5*5**4, ((3, 5), (5, 4)),
                        {3: (5, 1, (3, 1)), 5: (4, 2, (1, 0))}),
        content_control(225, ((3, 2), (5, 2)),
                        {3: (2, 1, (1, 1)), 5: (2, 1, (1, 2))}),
    ]
    assert [s["content"] for s in scenarios] == [3, 75, 15]
    assert [s["cyclic_residual_degree"] for s in scenarios] == [27, 27, 1]
    own = ("content_reduction.py", "controls_content.py", "test_content_reduction.py",
           "replay_content.py", "ODD_CONTENT_REDUCTION.md", "HANDOFF.md")
    dependencies = (
        "cyclic-odd-degree-source-2026-10-25/cyclic_source.py",
        "cyclic-odd-degree-source-2026-10-25/controls_cyclic.py",
        "cyclic-odd-degree-source-2026-10-25/CYCLIC_ODD_DEGREE.md",
        "cyclic-odd-degree-source-2026-10-25/receipt.json",
        "kernel-output-2026-10-23/kernel_output.py",
    )
    return {
        "status": "ODD_CONTENT_REDUCTION_CONDITIONAL_REVIEW_PENDING",
        "scope_flags": {"native_source_executed": False, "quantum_execution": False,
                        "unknown_kernel_recovered": False, "speedup_established": False,
                        "independently_reviewed": False, "main_registry_integrated": False},
        "source_change": "none: original degree, levels, modeled targets and equality source",
        "supplied_smith_controls": scenarios,
        "original_ideal_control": ideal_scaling_control(),
        "degree225_endomorphism_control": noncyclic_endomorphism_control(),
        "implementation_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in own
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
    print(json.dumps({"status": result["status"],
                      "content_and_residual": [[s["content"], s["cyclic_residual_degree"]]
                                               for s in result["supplied_smith_controls"]],
                      "degree225_ideal_matches": result["degree225_endomorphism_control"][
                          "reconstructed_ideal_equals_principal_left_ideal"],
                      "scope_flags": result["scope_flags"]}, indent=2))
