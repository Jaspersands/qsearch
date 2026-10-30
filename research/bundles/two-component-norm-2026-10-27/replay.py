"""Replay the same explicit degree-eight input; not a scaling experiment."""

import argparse
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import random
import sys

from flint import nmod_mat

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "small-prime-tower-2026-10-27"))
from small_prime import P, build_control, evaluate, monomials
from schur_gate import basis
from norm_completion import NormCompletion
from scope_bounds import all_input_bounds, bounds, encode_fraction, fixed_prime_cutoff


def make_receipt():
    problem, _, native = build_control()
    A = basis([[evaluate(f, point) for point in native["evaluation_points"]]
               for f in monomials(8)], P)
    W = basis([[a[i]*b[i] % P for i in range(problem.m)]
               for a, b in combinations_with_replacement(A, 2)], P)
    mixed = basis([[v[i]*w[i] % P for i in range(problem.m)]
                   for v in problem.V for w in W], P)
    kernel, dimension = nmod_mat(mixed, P).nullspace()
    rng = random.Random(27104)
    coefficients = [rng.randrange(P) for _ in range(dimension)]
    h = [sum(int(kernel[i, j])*coefficients[j] for j in range(dimension)) % P
         for i in range(problem.m)]
    case = NormCompletion(P, native["original_parity"], A, h, 2)
    syndromes = [[0]*case.k, [1]*case.k,
                 [i % P for i in range(case.k)],
                 [rng.randrange(P) for _ in range(case.k)],
                 [(i*i+17*i+3) % P for i in range(case.k)]]
    results = [case.solve(s, seed=27110+j) for j, s in enumerate(syndromes)]
    if any(result["status"] != "VERIFIED_NATIVE_WITNESS" for result in results):
        raise ArithmeticError("fixed native control did not finish; do not resample input")
    # Verify against raw input entries, independently of the solver verifier.
    for result in results:
        if not all(result["word"]) or any(
                sum(a*b for a, b in zip(row, result["word"])) % P != s
                for row, s in zip(native["original_parity"], result["syndrome"])):
            raise ArithmeticError("original-matrix witness mismatch")
    dependencies = [ROOT / "norm_completion.py", ROOT / "replay.py", ROOT / "scope_bounds.py",
                    ROOT.parent / "small-prime-tower-2026-10-27/small_prime.py",
                    ROOT.parent / "prime-ag-tower-source-2026-10-26/tower_seed.py",
                    ROOT.parent / "schur-growth-classical-gate-2026-10-26/schur_gate.py",
                    ROOT.parent / "systematic-full-support-2026-10-27/systematic.py",
                    ROOT.parent / "ag-affine-sampling-2026-10-26/affine_sampling.py"]
    return {
        "status": "SCOPED_CLASSICAL_CONTROL_NOT_NEW_NATIVE_DEQUANTIZATION",
        "p": P, "k": case.k, "m": case.m, "auxiliary_dimension": case.r,
        "auxiliary_square_dimension": len(W), "mixed_dimension": len(mixed),
        "annihilator_dimension": dimension, "annihilator": h,
        "original_parity": native["original_parity"], "auxiliary": A,
        "same_auxiliary_one_variable_rank_ceiling": case.r,
        "full_cube_rank": len(problem.U), "native_witnesses": results,
        "annihilator_zero_count": sum(x == 0 for x in h),
        "auxiliary_zero_column_count": sum(all(row[i] == 0 for row in A) for i in range(problem.m)),
        "conditional_geometric_bounds": [bounds(P, e) for e in (8, 16, 32, 64, 128, 256)],
        "all_input_theoretical_bounds": [all_input_bounds(P, e) for e in (8, 64, 128, 256, 16384, 32768)],
        "fixed_prime_certificate_cutoff": fixed_prime_cutoff(P),
        "fixed_prime_asymptotic_solver": False, "native_input_already_classically_easy": True,
        "higher_tower_input_generated": False, "quantum_execution": False,
        "source_hashes": {str(path.relative_to(ROOT.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in dependencies},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    receipt = make_receipt()
    serialized = json.dumps(receipt, sort_keys=True, indent=2, default=encode_fraction)+"\n"
    path = ROOT / "receipt.json"
    if arguments.write:
        path.write_text(serialized)
    elif path.read_text() != serialized:
        raise SystemExit("receipt mismatch")
    print(json.dumps({"status": "PASS", "mode": "write" if arguments.write else "check",
                      "native_witnesses": len(receipt["native_witnesses"]),
                      "dimensions": [receipt["k"], receipt["auxiliary_dimension"], receipt["m"]],
                      "native_already_classically_easy": True}))
