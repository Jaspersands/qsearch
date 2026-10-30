"""Record deterministic bounded controls and exact resource arithmetic."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import spectral_mixture as s


def run():
    root = Path(__file__).resolve().parent
    report = s.audit()
    report["resource_example"] = s.packet_budget(receiver_leaves=7, design_size=6, cover_order_bits=31,
                                               minimum_weight=Fraction(1, 10), spectral_gap=Fraction(1, 100),
                                               orbit_trace_gap=Fraction(1, 4), error=Fraction(1, 20))
    report["source_sha256"] = {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
                               for name in ("spectral_mixture.py", "test_spectral_mixture.py", "run_audit.py", "SPECTRAL_MIXTURE.md")}
    formal = root.parent / "rees-formal-core-2026-10-24"
    report["dependencies_sha256"] = {name: hashlib.sha256((formal/name).read_bytes()).hexdigest()
                                     for name in ("native_source_controls.py", "native_source_receipt.json")}
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    print(payload, end="")
