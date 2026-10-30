"""Regenerate the bounded code-support audit; no production registry writes."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import code_support


def run():
    root = Path(__file__).resolve().parent
    report = code_support.audit()
    report["resource_example"] = code_support.source_plan(
        rank=8, receiver_leaves=7, design_size=6, cover_order_bits=31,
        support_operator_gap=Fraction(1, 4), error=Fraction(1, 20))
    report["source_sha256"] = {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
                             for name in ("code_support.py", "test_code_support.py", "run_audit.py", "CODE_SUPPORT.md",
                                          "HANDOFF.md", "literature_transfer.json")}
    dependencies = ("rees-spectral-mixture-2026-10-24/spectral_mixture.py",
                    "rees-spectral-mixture-2026-10-24/spectral_mixture_receipt.json",
                    "rees-formal-core-2026-10-24/native_source_controls.py",
                    "rees-formal-core-2026-10-24/native_source_receipt.json")
    report["dependencies_sha256"] = {name: hashlib.sha256((root.parent/name).read_bytes()).hexdigest()
                                    for name in dependencies}
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    print(payload, end="")
