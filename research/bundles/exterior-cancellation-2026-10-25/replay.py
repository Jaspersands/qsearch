"""Reproduce exact public-label witnesses, not a quantum experiment."""

import argparse
from dataclasses import asdict
import hashlib
from importlib.metadata import version
import json
from math import prod
from pathlib import Path
import random
import sys

from exterior_sde import collision_arity, plan, solve


ROOT = Path(__file__).resolve().parent
SOURCES = ("EXTERIOR_CANCELLATION.md", "exterior_sde.py", "test_exterior_sde.py",
           "replay.py", "HANDOFF.md")
CONTEXT = ("rees-class-three-2026-10-24/CLASS_THREE.md",
           "quadratic-cancellation-2026-10-23/RESULT.md",
           "rees-independent-review-2026-10-23/RESPONSE.md")
LARGE = 2**128 - 275


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")


def sha(value):
    return hashlib.sha256(value).hexdigest()


def control(p, degree, width, family, seed=305):
    setup = plan(p, degree, width)
    rng = random.Random(seed)
    if family == "seeded_public_matrix":
        columns = [tuple(rng.randrange(p) for _ in range(width))
                   for _ in range(setup.required_columns)]
    elif family == "all_one_full_recursion":
        columns = [(1,)*width] * setup.required_columns
    elif family == "zero_with_charged_suffix":
        columns = [(0,)*width] * (setup.required_columns+7)
    else:
        raise ValueError("unknown public control family")
    witness = solve(columns, setup, rng=random.Random(seed), attempt_cap=256)
    residual = [sum(v[j]*pow(s, degree, p) for v, s in zip(columns, witness.weights)) % p
                for j in range(width)]
    if any(residual) or not any(witness.weights):
        raise ArithmeticError("independent original-moment replay failed")
    if family == "all_one_full_recursion" and witness.statistics["zero_representation_early_exit"]:
        raise ArithmeticError("full-round fixture took an early exit")
    return {
        "plan": asdict(setup), "label_family": family, "seed": seed,
        "input_matrix_sha256": sha(encoded(columns)),
        "expanded_weights_sha256": sha(encoded(witness.weights)),
        "sparse_nonzero_weights": [[i, s] for i, s in enumerate(witness.weights) if s],
        "original_moment": residual, "acquired_columns": witness.acquired_columns,
        "statistics": witness.statistics,
        "uniform_independent_sampling_abort_bound": str(witness.sampling_abort_bound),
        "root_runtime_locally_clocked": witness.root_runtime_locally_clocked,
    }


def make_receipt():
    cases = [
        (43, 3, 3, "seeded_public_matrix"),
        (41, 4, 2, "seeded_public_matrix"),
        (101, 5, 2, "seeded_public_matrix"),
        (13, 9, 2, "seeded_public_matrix"),
        (2**127-295, 4, 3, "seeded_public_matrix"),
        (LARGE, 5, 2, "seeded_public_matrix"),
        (LARGE, 4, 1, "all_one_full_recursion"),
        (13, 4, 1, "all_one_full_recursion"),
        (17, 4, 2, "zero_with_charged_suffix"),
    ]
    comparison = [{"index": d, "width": r,
                   "exterior_collision_columns": collision_arity(d, r),
                   "uncompressed_tensor_recurrence_columns": prod(r*d**j+1 for j in range(d))}
                  for d, r in ((2, 3), (3, 3), (4, 2), (5, 2))]
    return {
        "status": "local_unreviewed_constructive_arithmetic_with_exact_controls",
        "quantum_receiver_implemented": False, "quantum_advantage_claim": False,
        "novelty_certified": False, "whole_repository_validated": False,
        "main_repository_modified": False,
        "root_runtime_locally_clocked": False,
        "seeded_replay_certifies_random_failure_probability": False,
        "source_hashes": {name: sha((ROOT/name).read_bytes()) for name in SOURCES},
        "context_hashes": {name: sha((ROOT.parent/name).read_bytes()) for name in CONTEXT},
        "runtime": {"python": sys.version.split()[0], "python_flint": version("python-flint")},
        "comparison_not_best_known_claim": comparison,
        "cases": [control(*case) for case in cases],
    }


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = json.dumps(make_receipt(), indent=2, sort_keys=True)+"\n"
    target = ROOT/"receipt.json"
    if args.write:
        target.write_text(value, encoding="ascii")
    elif target.read_text(encoding="ascii") != value:
        raise SystemExit("receipt mismatch")
    print(sha(value.encode("ascii")))


if __name__ == "__main__":
    main()
