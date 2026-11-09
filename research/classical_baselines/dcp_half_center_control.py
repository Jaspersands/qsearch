#!/opt/anaconda3/bin/python
"""Bounded exact modular subset-sum controls; no scaling inference.

Run with /opt/anaconda3/bin/python. The standard-library driver invokes the
local Sage/fpylll interpreter once. No secret or enumerated binary witness
is passed to either lattice solver. Complete enumeration validates outputs
only after both solvers return.
"""

import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import time
from collections import Counter
from fractions import Fraction

SAGE_PYTHON = "/opt/anaconda3/envs/qsearch-cas/bin/python"
SEED = 20261106


def exhaustive_moments():
    n, modulus = 3, 8
    native_histogram = Counter()
    planted_histogram = Counter()
    for weights in itertools.product(range(modulus), repeat=n):
        counts = Counter(
            sum(a * bit for a, bit in zip(weights, bits)) % modulus
            for bits in itertools.product((0, 1), repeat=n)
        )
        for target in range(modulus):
            native_histogram[counts[target]] += 1
        # This is an explicitly separate planted law, with the same IID
        # weights and an independent uniform binary witness. No rejection.
        for bits in itertools.product((0, 1), repeat=n):
            target = sum(a * bit for a, bit in zip(weights, bits)) % modulus
            planted_histogram[counts[target]] += 1
    native_count = modulus ** (n + 1)
    planted_count = modulus**n * 2**n
    mean = Fraction(sum(k * v for k, v in native_histogram.items()), native_count)
    second = Fraction(sum(k * k * v for k, v in native_histogram.items()), native_count)
    planted_mean = Fraction(
        sum(k * v for k, v in planted_histogram.items()), planted_count
    )
    size_bias_verified = all(
        Fraction(planted_histogram[k], planted_count)
        == Fraction(k, 1) * Fraction(v, native_count) / mean
        for k, v in native_histogram.items()
    )
    assert mean == 1 and second == Fraction(15, 8)
    assert planted_mean == Fraction(15, 8) and size_bias_verified
    return {
        "n": n,
        "modulus": modulus,
        "all_native_instances": native_count,
        "native_solution_count_histogram": dict(sorted(native_histogram.items())),
        "native_mean_N": str(mean),
        "native_mean_N_squared": str(second),
        "planted_mean_N": str(planted_mean),
        "planted_solution_count_histogram": dict(sorted(planted_histogram.items())),
        "size_bias_identity_verified": size_bias_verified,
        "native_and_planted_laws_kept_distinct": True,
    }


def integer_coset_and_kernel(weights, target, modulus):
    from sage.all import ZZ, matrix, vector, xgcd

    n = len(weights)
    # Saturated integer kernel of [a_1,...,a_n,-D], followed by projection.
    augmented = matrix(ZZ, 1, n + 1, list(weights) + [-modulus])
    kernel = augmented.right_kernel_matrix()
    basis = kernel.matrix_from_columns(range(n)).hermite_form()
    common_gcd = ZZ(modulus)
    coefficients = vector(ZZ, n)
    for i, weight in enumerate(weights):
        new_gcd, old_multiplier, new_multiplier = xgcd(common_gcd, ZZ(weight))
        coefficients *= old_multiplier
        coefficients[i] += new_multiplier
        common_gcd = new_gcd
    assert basis.nrows() == n and basis.ncols() == n
    assert abs(basis.det()) == modulus // common_gcd
    assert all(sum(row[i] * weights[i] for i in range(n)) % modulus == 0 for row in basis)
    if target % common_gcd:
        return basis, int(common_gcd), None
    particular = coefficients * (target // common_gcd)
    assert sum(particular[i] * weights[i] for i in range(n)) % modulus == target
    return basis, int(common_gcd), particular


def nearest_plane_exact(reduced_basis, target):
    from sage.all import QQ, floor, vector

    # Exact Gram-Schmidt vectors, followed by Babai's reversed projections.
    # This is not rounding the coordinates in the original basis.
    rows = [vector(QQ, row) for row in reduced_basis.rows()]
    orthogonal = []
    for row in rows:
        star = vector(QQ, list(row))
        for earlier in orthogonal:
            star -= (row.dot_product(earlier) / earlier.dot_product(earlier)) * earlier
        orthogonal.append(star)
    residual = vector(QQ, target)
    lattice_point = vector(QQ, len(target))
    projections = []
    for index in reversed(range(len(rows))):
        star = orthogonal[index]
        projection = residual.dot_product(star) / star.dot_product(star)
        rounded = floor(projection + QQ(1) / 2)
        lattice_point += rounded * rows[index]
        residual -= rounded * rows[index]
        projections.append({"basis_index": index, "GS_projection": str(projection), "rounded": int(rounded)})
    return lattice_point, projections


def decode_lattice_point(point, particular, target_vector, weights, target, modulus):
    from sage.all import ZZ, vector

    assert all(ZZ(value) % 2 == 0 for value in point)
    candidate = particular + vector(ZZ, [ZZ(value) // 2 for value in point])
    binary = all(value in (0, 1) for value in candidate)
    congruence = sum(candidate[i] * weights[i] for i in range(len(weights))) % modulus == target
    distance_squared = sum((target_vector[i] - point[i]) ** 2 for i in range(len(weights)))
    return {
        "lattice_point": [int(value) for value in point],
        "decoded_integer_candidate": [int(value) for value in candidate],
        "binary": binary,
        "native_congruence_satisfied": bool(congruence),
        "binary_solution_returned": bool(binary and congruence),
        "squared_distance_to_scaled_half_center": int(distance_squared),
    }


def solve_native(weights, target, modulus):
    from sage.all import ZZ, vector
    from fpylll import CVP, IntegerMatrix

    begin = time.perf_counter()
    basis, common_gcd, particular = integer_coset_and_kernel(weights, target, modulus)
    out = {
        "n": len(weights), "modulus": modulus, "weights": list(weights), "target": target,
        "gcd_weights_and_modulus": common_gcd,
        "integer_coset_exists": particular is not None,
        "kernel_basis_HNF": [[int(x) for x in row] for row in basis],
        "kernel_determinant": int(abs(basis.det())),
        "scaled_kernel_determinant": int(abs((2 * basis).det())),
    }
    if particular is None:
        out["solver_seconds"] = time.perf_counter() - begin
        return out
    scaled_basis = 2 * basis
    scaled_target = vector(ZZ, [1] * len(weights)) - 2 * particular
    reduced = scaled_basis.LLL(delta=0.99)
    out.update({
        "particular_integer_solution": [int(x) for x in particular],
        "scaled_target_1_minus_2z0": [int(x) for x in scaled_target],
        "LLL_reduced_scaled_basis": [[int(x) for x in row] for row in reduced],
    })
    start = time.perf_counter()
    babai, projections = nearest_plane_exact(reduced, scaled_target)
    out["nearest_plane"] = decode_lattice_point(babai, particular, scaled_target, weights, target, modulus)
    out["nearest_plane"]["GS_steps"] = projections
    out["nearest_plane"]["seconds_after_LLL"] = time.perf_counter() - start
    fpylll_basis = IntegerMatrix.from_matrix([[int(x) for x in row] for row in reduced])
    start = time.perf_counter()
    closest = CVP.closest_vector(fpylll_basis, tuple(int(x) for x in scaled_target), method="proved")
    out["exact_CVP"] = decode_lattice_point(closest, particular, scaled_target, weights, target, modulus)
    out["exact_CVP"]["fpylll_method"] = "proved"
    out["exact_CVP"]["seconds_after_LLL"] = time.perf_counter() - start
    out["solver_seconds"] = time.perf_counter() - begin
    return out


def validate_after_solver(output):
    weights, target, modulus = output["weights"], output["target"], output["modulus"]
    witnesses = [
        list(bits) for bits in itertools.product((0, 1), repeat=len(weights))
        if sum(a * bit for a, bit in zip(weights, bits)) % modulus == target
    ]
    output["validator_binary_solution_count"] = len(witnesses)
    output["validator_binary_witnesses"] = witnesses
    if output["integer_coset_exists"]:
        for label in ("nearest_plane", "exact_CVP"):
            result = output[label]
            result["matches_enumerated_witness"] = result["decoded_integer_candidate"] in witnesses
            assert result["binary_solution_returned"] == result["matches_enumerated_witness"]
        cvp = output["exact_CVP"]
        assert (cvp["squared_distance_to_scaled_half_center"] == len(weights)) == bool(witnesses)
    else:
        assert not witnesses
    return output


def parity_toy():
    from sage.all import vector, ZZ

    weights, target, modulus = (1, 1), 1, 4
    basis, common_gcd, particular = integer_coset_and_kernel(weights, target, modulus)
    rhs = 2 * target - sum(weights)
    signed = [list(y) for y in itertools.product((-1, 1), repeat=2) if sum(a * b for a, b in zip(weights, y)) % (2 * modulus) == rhs % (2 * modulus)]
    relaxed_zero_satisfies = 0 == rhs % (2 * modulus)
    assert signed == [[-1, 1], [1, -1]] and relaxed_zero_satisfies
    assert abs(basis.det()) == 4 and abs((2 * basis).det()) == 16
    return {
        "n": 2, "modulus": 4, "weights": list(weights), "target": target,
        "relaxed_signed_modulus": 8, "relaxed_signed_rhs": rhs,
        "zero_satisfies_relaxed_congruence": relaxed_zero_satisfies,
        "zero_is_odd": False, "true_signed_binary_solutions": signed,
        "true_signed_squared_norm": 2,
        "kernel_determinant": int(abs(basis.det())),
        "scaled_kernel_determinant": int(abs((2 * basis).det())),
    }


def run_control():
    started = time.perf_counter()
    result = {
        "scope": "Exact tiny classical controls only; no quantum execution or asymptotic success claim.",
        "moments": exhaustive_moments(),
        "parity_toy": parity_toy(),
        "native_seed": SEED,
        "native_generation": "Python random.Random(seed), IID randrange(D) weights, then independent randrange(D) target; no witness planting or feasibility rejection.",
        "native_instances": [],
        "source_scope": {
            "quantum_dgs_2605_20133": {
                "application_c_zero_lines": "886-900", "final_theorem_lines": "1071-1083",
                "statement": "Application and final Theorem 7 assume c=0; theorem retains a square-root rejection/mass-ratio gate factor. Generic Theorem 6 is not a constructed arbitrary-center lattice sampler.",
            },
            "coster_low_density_1992": {
                "oracle_definition_lines": "80-95", "theorem_3_1_lines": "279-284",
                "statement": "Random positive integer weights, an arbitrary fixed binary e, and planted exact integer target s=sum e_i a_i. Density below 0.9408 gives almost-all reduction with one shortest-nonzero-vector oracle call, not an unconditional LLL guarantee or an independent modular target theorem.",
            },
        },
    }
    rng = random.Random(SEED)
    for attempt in range(2):
        weights = [rng.randrange(256) for _ in range(8)]
        target = rng.randrange(256)
        # No validator enumeration has occurred for this instance yet.
        output = solve_native(weights, target, 256)
        output["draw_index"] = attempt
        result["native_instances"].append(validate_after_solver(output))
        if output["integer_coset_exists"]:
            break
    result["total_worker_seconds"] = time.perf_counter() - started
    artifact = Path(__file__).with_suffix(".json")
    artifact.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "artifact": str(artifact),
        "moments": [result["moments"][key] for key in ("native_mean_N", "native_mean_N_squared", "planted_mean_N")],
        "toy_determinants": [result["parity_toy"][key] for key in ("kernel_determinant", "scaled_kernel_determinant")],
        "native": [{
            "weights": item["weights"], "target": item["target"],
            "gcd": item["gcd_weights_and_modulus"],
            "integer_coset_exists": item["integer_coset_exists"],
            "binary_count": item["validator_binary_solution_count"],
            "nearest_plane_success": item.get("nearest_plane", {}).get("binary_solution_returned"),
            "exact_CVP_success": item.get("exact_CVP", {}).get("binary_solution_returned"),
            "solver_seconds": item["solver_seconds"],
        } for item in result["native_instances"]],
        "worker_seconds": result["total_worker_seconds"],
    }))


if __name__ == "__main__":
    if sys.argv[1:] == ["--sage-worker"]:
        run_control()
    elif not sys.argv[1:]:
        subprocess.run([SAGE_PYTHON, str(Path(__file__).resolve()), "--sage-worker"], check=True)
    else:
        raise SystemExit("Usage: dcp_half_center_control.py")
