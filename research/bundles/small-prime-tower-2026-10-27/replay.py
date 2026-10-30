"""Reproduce the small-prime source, actual code and matched classical outputs."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import log2

from avoidance import solve_native
from seed_search import search
from small_prime import P, ROOT, build_control, parameter_bounds


def jsonable(value):
    if isinstance(value, Fraction):
        return {"numerator_hex": hex(value.numerator), "denominator_hex": hex(value.denominator)}
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def report():
    problem, fiber, data = build_control()
    targets = [(0,)*43, (1,)*43, tuple(range(43)), tuple((i*i+17) % P for i in range(43))]
    runs = []
    for i, target in enumerate(targets):
        greedy = solve_native(P, data["original_parity"], target)
        systematic = fiber.sample(target, seed=20261027+i, attempts=16)
        for result in (greedy, systematic):
            if result["witness"] is None or not problem.verifies(result["witness"], target):
                raise ArithmeticError("matched classical attack failed original native verification")
        runs.append({"syndrome": target, "greedy": greedy, "systematic": systematic})
    if problem.annihilator:
        raise ArithmeticError("this actual control no longer escapes the same-code cubic method")
    forecasts = []
    for p in (P, 100003):
        for e in (128, 256, 512, 1024, 4096):
            k, m = 5*e+3, 22*e
            forecasts.append({
                "prime": p, "e": e, "k": k, "m": m, "dense_matrix_entries": k*m,
                "greedy_guarantee": k <= p-2,
                "systematic_log2_trials_leading_term": k*log2(p/(p-1)),
                "tail_bound_formula": "alpha < p^(5-e)",
                "status": "CONDITIONAL_PARAMETER_FORECAST_NOT_GENERATED_INPUT",
                "measured_runtime": False, "classical_lower_bound": False,
            })
    files = [ROOT / name for name in (
        "seed_search.py", "small_prime.py", "avoidance.py", "test_small_prime.py", "replay.py", "RESULT.md")]
    files += [ROOT.parent / path for path in (
        "prime-ag-tower-source-2026-10-26/tower_seed.py",
        "schur-growth-classical-gate-2026-10-26/schur_gate.py",
        "systematic-full-support-2026-10-27/systematic.py",
        "ag-affine-sampling-2026-10-26/affine_sampling.py")]
    return jsonable({
        "status": "SMALLER_PRIME_SOURCE_AND_NATIVE_CONTROL_CLASSICALLY_SOLVED",
        "discovery": search(P, width=120), "native_control": data,
        "exact_conditional_bounds_at_e8": parameter_bounds(P, 8),
        "verified_native_runs": runs, "unexecuted_scaling_forecasts": forecasts,
        "quantum_advantage_established": False, "registry_admission": False,
        "higher_level_backend_implemented": False,
        "sha256": {str(path.relative_to(ROOT.parent)): sha256(path.read_bytes()).hexdigest()
                   for path in files},
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = report()
    path = ROOT / "receipt.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2)+"\n")
    elif args.check:
        if json.loads(path.read_text()) != result:
            raise SystemExit("FAIL: small-prime replay changed")
    else:
        print(json.dumps(result, indent=2))
    if args.write or args.check:
        print(f"PASS: native matrix and eight witnesses; {len(result['sha256'])} hashes; SHA256 {sha256(path.read_bytes()).hexdigest()}")
