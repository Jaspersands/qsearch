"""Replay signed bounded controls; no quantum run or candidate admission."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform

import numpy as np

from usd_reduction import repetition_control, wrong_answer_countercontrol


ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "schur-growth-classical-gate-2026-10-26/receipt.json"
FROZEN = "778b6595a508c482fdfc9e8bb5001c6eb0967329bafbb54d128592fff32c6f64"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def report():
    if digest(PREVIOUS) != FROZEN:
        raise ValueError("previous scoped classical result changed")
    controls = [repetition_control(m) for m in range(1, 5)]
    # Compare numerical identities inside the controls; the receipt retains
    # exact rational predictions, not platform-dependent last floating bits.
    for control in controls:
        for sector in control["syndromes"]:
            sector.pop("direct_target_fidelity", None)
            if "direct_valid_output_probability" in sector:
                sector["direct_valid_output_probability"] = round(
                    sector["direct_valid_output_probability"], 10)
    paths = [ROOT / name for name in ("usd_reduction.py", "test_usd_reduction.py",
             "verify_usd.py", "USD_REDUCTION.md", "HANDOFF.md")]+[PREVIOUS]
    return {"status": "UNAMBIGUOUS_TRANSFER_REFINEMENT_PENDING_INDEPENDENT_REVIEW",
            "quantum_advantage_established": False, "quantum_execution": False,
            "native_inverse_trace_solved": False, "uniform_sampling_claimed": False,
            "registry_admission": False,
            "controls": controls, "wrong_answer_countercontrol": wrong_answer_countercontrol(),
            "numerical_identity_tolerance": 1e-12,
            "runtime": {"python": platform.python_version(), "numpy": np.__version__},
            "sources": ["https://arxiv.org/html/2610.00502v1",
                        "https://arxiv.org/html/2310.20651#S6.SS2",
                        "https://arxiv.org/abs/2607.14650"],
            "sha256": {str(path.relative_to(ROOT.parent)): digest(path) for path in paths}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = report()
    destination = ROOT / "receipt.json"
    if args.check:
        if json.loads(destination.read_text()) != data:
            raise SystemExit("FAIL: receipt differs from verified replay")
        print(f"PASS: signed replay; {len(data['sha256'])} hashes; SHA256 {digest(destination)}")
    elif args.write:
        destination.write_text(json.dumps(data, indent=2)+"\n")
        print(f"Wrote {destination}; SHA256 {digest(destination)}")
    else:
        print(json.dumps(data, indent=2))
