"""Deterministic arithmetic receipt; no geometric or quantum execution."""

import hashlib
import json
from pathlib import Path
import sys

import cm_gate as c

ROOT = Path(__file__).resolve().parent


def build():
    files = ("cm_gate.py", "test_cm_gate.py", "replay.py", "CM_SOURCE_GATE.md")
    prior = ("regular-spectrum-kernel-2026-10-25/REGULAR_SPECTRUM.md",
             "native-input-audit-2026-10-23/NATIVE_INPUT_GATE.md")
    return {
        "status": "LOCAL_DEDUCTION_REVIEW_PENDING",
        "source": "https://arxiv.org/html/2610.27922v1#S4.SS3",
        "source_sha256": {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},
        "context_sha256": {f: hashlib.sha256((ROOT.parent/f).read_bytes()).hexdigest() for f in prior},
        "cm8_controls": [{"prime": p, **c.exhaustive_cm8(p),
                          "local_counts": c.etale_counts(p, c.cm8_permutation(p))}
                         for p in (3, 5, 7, 17)],
        "independent_completion": c.independent_completion_bound(5, [(r, c.cm8_permutation(r)) for r in (17, 41, 73)]),
        "large_prime_count": c.etale_counts(2**127-1, c.cm8_permutation(2**127-1)),
        "scope": {"native_weak_isogeny_constructed": False, "published_protocol_broken": False,
                  "independent_review": False, "novelty_established": False,
                  "main_registry_changed": False, "quantum_algorithm_executed": False},
    }


def main():
    if sys.argv[1:] not in (["write"], ["check"]):
        raise SystemExit("usage: replay.py write|check")
    payload = json.dumps(build(), indent=2, sort_keys=True) + "\n"
    destination = ROOT / "receipt.json"
    if sys.argv[1] == "write":
        destination.write_text(payload)
    elif destination.read_text() != payload:
        raise SystemExit("receipt differs")
    print(sys.argv[1], "PASS; receipt sha256", hashlib.sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()
