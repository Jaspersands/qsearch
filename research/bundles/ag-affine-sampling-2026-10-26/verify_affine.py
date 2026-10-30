"""Replay actual original-fiber classical witnesses and analytic certificates."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform

import flint

from curve_countercontrol import BASELINE, control


ROOT = Path(__file__).resolve().parent
FROZEN = {
    BASELINE: "d2ba9a0dc1d83a60f3210efec353b463897269bdc943abf728e2a642bc2129e3",
    ROOT.parent / "unambiguous-reduction-2026-10-26/receipt.json":
        "e6435c5275c7db6d593e5af002a82bf1e7f6e758beea3309af5dd30770949eeb",
    ROOT.parent / "schur-growth-classical-gate-2026-10-26/receipt.json":
        "778b6595a508c482fdfc9e8bb5001c6eb0967329bafbb54d128592fff32c6f64",
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def jsonable(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def report():
    for path, expected in FROZEN.items():
        if digest(path) != expected:
            raise ValueError(f"frozen preceding result changed: {path}")
    fiber, data = control()
    syndromes = [(1, 2, 3, 4, 5), (0,)*5, (12,)*5]
    syndromes.extend(tuple(int(i == j) for j in range(5)) for i in range(5))
    runs = []
    for index, syndrome in enumerate(syndromes):
        seed = 26026+index
        result = fiber.sample(syndrome, seed=seed, attempts=128)
        if result["witness"] is None or not fiber.verifies(result["witness"], syndrome):
            raise ArithmeticError("classical same-input witness replay failed")
        runs.append({"syndrome": syndrome, "seed": seed, "attempt_cap": 128,
                     "result": result, "original_relation_verified": True})
    sources = [ROOT / name for name in ("affine_sampling.py", "curve_countercontrol.py",
               "test_affine_sampling.py", "verify_affine.py", "AFFINE_SAMPLING.md",
               "HANDOFF.md")]+list(FROZEN)
    return jsonable({
        "status": "REFINED_GAP_CONTROL_SOLVED_BY_MATCHED_CLASSICAL_UNIFORM_SAMPLER",
        "proof_status": "WRITTEN_DEDUCTION_WITH_CONTROLS_NOT_INDEPENDENTLY_REVIEWED",
        "scope": {"relation": "By=s and every y_i nonzero",
                  "all_ag_families_solved": False, "usd_refinement_refuted": False,
                  "native_inverse_trace_solved": False, "quantum_execution": False,
                  "quantum_advantage_established": False, "registry_admission": False},
        "actual_curve_control": data, "original_fiber_runs": runs,
        "runtime": {"python": platform.python_version(), "python_flint": flint.__version__},
        "sha256": {str(path.relative_to(ROOT.parent)): digest(path) for path in sources},
    })


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
            raise SystemExit("FAIL: receipt differs from original-input replay")
        print(f"PASS: affine replay; {len(data['sha256'])} hashes; SHA256 {digest(destination)}")
    elif args.write:
        destination.write_text(json.dumps(data, indent=2)+"\n")
        print(f"Wrote {destination}; SHA256 {digest(destination)}")
    else:
        print(json.dumps(data, indent=2))
