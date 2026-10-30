"""A genuine new AG divisor class, then its matched classical falsifier.

This fixed finite control neither samples Picard classes uniformly nor
certifies behavior of pullbacks in the infinite tower.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from math import prod
from pathlib import Path
import sys

from flint import nmod_mat


ROOT = Path(__file__).resolve().parent
COVER = ROOT.parent / "prime-ag-tower-source-2026-10-26"
sys.path.insert(0, str(COVER))
try:
    import elementary_cover as cover
finally:
    sys.path.pop(0)
AFFINE = ROOT.parent / "ag-affine-sampling-2026-10-26/affine_sampling.py"
spec = importlib.util.spec_from_file_location("divisor_control_affine", AFFINE)
affine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(affine)

EXTRA_X = 51888
DEFAULT_INDICES = (0, 3, 5, 9, 14)


def split_fiber(x):
    p = cover.PRIME
    if type(x) is not int or not 0 <= x < p or x in cover.default_seed().splitting_x:
        raise ValueError("canonical extra x outside the evaluation divisor required")
    roots = [pow((x-i) % p, (p+1)//4, p) for i in range(13)]
    if not all(root and root*root % p == (x-i) % p for i, root in enumerate(roots)):
        raise ValueError("all thirteen branch differences must be nonzero squares")
    y = prod(roots) % p
    points = []
    for signs in product((1, -1), repeat=4):
        r = [roots[0]]+[roots[i]*signs[i-1] % p for i in range(1, 4)]
        points.append({"x": x, "y": signs[3]*y % p, "roots": r,
                       "w": [r[0]*r[i] % p for i in range(1, 4)]})
    return points


def build_control(indices=DEFAULT_INDICES):
    indices = tuple(indices)
    if (len(indices) != 5 or len(set(indices)) != 5
            or any(type(i) is not int or not 0 <= i < 16 for i in indices)):
        raise ValueError("five distinct indices of the degree-sixteen x fiber required")
    p = cover.PRIME
    extra = split_fiber(EXTRA_X)
    zeros = [extra[i] for i in indices]
    functions = cover.monomials(11)
    constraints = nmod_mat([[cover.evaluate(f, point) for f in functions]
                            for point in zeros], p)
    kernel, dimension = constraints.nullspace()
    transform = nmod_mat([[int(kernel[i, j]) for i in range(len(functions))]
                         for j in range(dimension)], p)
    points = cover.points_above_seed()
    evaluation = nmod_mat([[cover.evaluate(f, point) for point in points]
                           for f in functions], p)
    original = cover.schur.rows(transform*evaluation)
    problem = cover.schur.FullSupportProblem(p, original, relation="full_support")
    if (len(functions), constraints.rank(), dimension, problem.k, problem.m,
            len(problem.W)) != (48, 5, 43, 43, 176, 126):
        raise ArithmeticError("complete AG divisor space has unexpected dimensions")
    fiber = affine.AffineFiber(p, original, relation="full_support")
    all_marginals_uniform = all(any(row[i] for row in fiber.kernel)
                               for i in range(fiber.m))
    if not all_marginals_uniform:
        raise ArithmeticError("union bound needs every affine marginal to be uniform")
    small_functions = cover.monomials(1)
    small_constraints = nmod_mat([[cover.evaluate(f, point) for f in small_functions]
                                  for point in zeros], p)
    extra_effective_dimension = len(small_functions)-small_constraints.rank()
    return problem, fiber, {
        "prime": p, "genus": 41, "divisor_degree": 83,
        "divisor": "G=11I-E, I=pi^*(base infinity), E=five explicit extra points",
        "extra_x": EXTRA_X, "chosen_fiber_indices": indices, "zero_divisor_E": zeros,
        "evaluation_points": points, "ambient_monomials": functions,
        "vanishing_constraints": cover.schur.rows(constraints),
        "rr_basis_coefficients": cover.schur.rows(transform),
        "original_parity": original, "dimension": problem.k, "length": problem.m,
        "square_dimension": len(problem.W), "cube_dimension": len(problem.U),
        "same_code_annihilator_dimension": len(problem.annihilator),
        "dimension_L_G_minus_K": extra_effective_dimension,
        "all_affine_coordinate_marginals_verified_uniform": all_marginals_uniform,
        "classical_uniform_fiber_success_lower": 1-Fraction(problem.m, p),
        "classical_expected_trials_upper": Fraction(p, p-problem.m),
        "conditional_quantum_E_upper": cover.exact_small_quantum_bounds(8)["E_upper"],
        "divisor_class_constructed": True, "uniform_Picard_class_sample": False,
        "higher_level_cube_rank_known": False, "quantum_execution": False,
        "classical_hardness_established": False, "quantum_advantage_established": False,
        "registry_admission": False,
    }


def jsonable(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def report():
    problem, fiber, data = build_control()
    if problem.annihilator:
        raise ArithmeticError("fixed class no longer escapes the same-code cubic method")
    targets = [(0,)*43, (1,)*43, tuple(range(43)), tuple((i*i+17) % cover.PRIME for i in range(43))]
    runs = []
    for index, target in enumerate(targets):
        sample = fiber.sample(target, seed=20261026+index, attempts=8)
        if sample["witness"] is None or not problem.verifies(sample["witness"], target):
            raise ArithmeticError("original-relation witness failed")
        runs.append({"syndrome": target, "seed": 20261026+index, "attempt_cap": 8,
                     "result": sample, "original_relation_verified": True})
    sources = [ROOT / name for name in ("divisor_control.py", "test_divisor_control.py", "CONTROL.md")]
    sources += [COVER / "elementary_cover.py", COVER / "tower_seed.py", cover.BASELINE, AFFINE]
    return jsonable({"status": "ACTUAL_CUBE_ESCAPE_BUT_CLASSICALLY_EASY_FINITE_CONTROL",
                     "control": data, "matched_classical_witness_runs": runs,
                     "sha256": {str(path.relative_to(ROOT.parent)): sha256(path.read_bytes()).hexdigest()
                                for path in sources}})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = report()
    destination = ROOT / "receipt.json"
    if args.write:
        destination.write_text(json.dumps(result, indent=2)+"\n")
    elif args.check:
        if json.loads(destination.read_text()) != result:
            raise SystemExit("FAIL: native divisor-class replay differs")
    else:
        print(json.dumps(result, indent=2))
    if args.write or args.check:
        print(f"PASS: {len(result['sha256'])} hashes; SHA256 {sha256(destination.read_bytes()).hexdigest()}")
