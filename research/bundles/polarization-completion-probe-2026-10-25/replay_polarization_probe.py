"""Replay finite supplied-order controls, with explicit non-native scope."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from polarization_probe import ROOT, completion_control
sys.path.insert(0, str(ROOT / "smooth-repolarization-2026-10-23"))
from smooth_repolarization import certificate, verify_certificate


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence():
    here = Path(__file__).resolve().parent
    controls = [completion_control(), completion_control(characteristic=47, twisted=True),
                completion_control(a_max=16, characteristic=47, twisted=True)]
    cert = certificate(26, 30)
    checks = verify_certificate(cert)
    if not all(checks.values()):
        raise ValueError("conversion algebra failed")
    try:
        completion_control(characteristic=23, twisted=True)
    except ValueError as exc:
        if "extra-automorphism" not in str(exc):
            raise
        exclusion = str(exc)
    else:
        raise ValueError("easy fixture was silently admitted")
    imported = set()
    for module in list(sys.modules.values()):
        file = getattr(module, "__file__", None)
        if file:
            path = Path(file).resolve()
            if path.suffix == ".py" and path.is_relative_to(ROOT) and path.parent != here:
                imported.add(path)
    dependencies = {ROOT / name for name in (
        "smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md",
        "ppav-source-2026-10-23/2026-1142.pdf",
        "one-endomorphism-access-audit-2026-10-25/ACCESS_CEILING.md")}
    own = ("polarization_probe.py", "test_polarization_probe.py",
           "replay_polarization_probe.py", "POLARIZATION_COMPLETION.md", "HANDOFF.md")
    return {
        "status": "CONDITIONAL_CLASSICAL_COMPLETION_WITH_SCOPED_FALSIFIERS",
        "scope_flags": {name: False for name in (
            "native_geometry_executed", "native_degree_enumerator_executed",
            "unknown_map_recovered", "speedup_established", "native_hardness_established",
            "global_nonexistence", "independent_review", "novelty_established",
            "main_registry_integrated")},
        "negative_records": [
            {"id": "NEG-POLARIZATION-SMALL-TRACE",
             "scope": "outside-K orthogonal projector implies degree<=trace(H)^2 noncommuting map",
             "classification": "classical competitor polynomial in bound value, not its bit length"},
            {"id": "NEG-POLARIZATION-FREE-FACTOR-SMALL-A",
             "scope": "norm-one original-E-factor witness with beta in K implies degree<=a map",
             "classification": "does not cover arbitrary elliptic factors"},
            {"id": "NEG-POLARIZATION-SCALAR-FROBENIUS-TWO",
             "scope": "E/F_p, K=Q(pi), pi scalar on E[2], any height/copy count",
             "classification": "all decomposition projectors stay in the known algebra"},
            {"id": "NEG-POLARIZATION-STABILIZATION-FACTORS",
             "scope": "powers of an indecomposable polarized surface",
             "classification": "copying creates no new primitive polarized factors"},
        ],
        "proof_status": "written deductions; independent review pending; finite controls not proofs",
        "controls": controls,
        "easy_fixture_exclusion": exclusion,
        "conversion_algebra": {"trace": 26, "D": 30, "multiplier": 900,
                               "coin_x": cert["coin_x"], "coin_y": cert["coin_y"],
                               "checks": checks, "native_geometry_executed": False},
        "implementation_sha256": {name: digest(here / name) for name in own},
        "dependency_sha256": {str(path.relative_to(ROOT)): digest(path)
                              for path in sorted(imported | dependencies)},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = evidence()
    encoded = json.dumps(result, sort_keys=True, indent=2)+"\n"
    path = Path(__file__).with_name("receipt.json")
    if args.write:
        path.write_text(encoded)
    if args.check and path.read_text() != encoded:
        sys.exit("receipt mismatch")
    print(json.dumps({"status": result["status"],
                      "forms_tested": [c["forms_tested"] for c in result["controls"]],
                      "found": [c["found"] for c in result["controls"]],
                      "receipt_sha256": hashlib.sha256(encoded.encode()).hexdigest()}, indent=2))
