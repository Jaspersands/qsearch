"""Replay bounded classical countercontrols; never expand the huge product."""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

import sympy as sp

from power_product import solve_ut_power_product, transformed


def digit_sum(value, base):
    total = 0
    while value:
        value, digit = divmod(value, base)
        total += digit
    return total


def mersenne_127_certificate():
    # Lucas-Lehmer for the known prime exponent 127, not a general primality API.
    assert all(127 % divisor for divisor in range(2, 12))
    modulus, value = 2**127-1, 4
    for _ in range(125):
        value = (value*value-2) % modulus
    assert value == 0
    return {"exponent": 127, "iterations": 125, "final_residue": value}


def audit():
    p = 2**127-1
    exponents = (p**8-1, p**9+2)
    controls = []
    for d in (4, 6, 10):
        variables = sp.symbols(f"x:{d}")
        result = solve_ut_power_product((variables[0], variables[0]+variables[1]**2), exponents, p, variables)
        expected_dimension = (d-2)*(d-3)//2
        assert len(result.lie_basis) == expected_dimension
        assert all(not matrix[i][j] for matrix in result.lie_basis for i in range(2) for j in range(d))
        assert all(not matrix[i][j] for matrix in result.lie_basis for i in range(d) for j in range(i+1))
        row = asdict(result)
        row["formal_degree_bits"] = result.total_degree.bit_length()
        row["binary_exponent_bits"] = [e.bit_length() for e in exponents]
        row["expected_stabilizer_description"] = "first two rows fixed; UT_(D-2) on the remaining coordinates"
        row["old_raw_degree_guard"] = p > max(d, (d-1)*result.total_degree)
        mixed_degree = digit_sum(exponents[0], p)+2*digit_sum(exponents[1], p)
        row["exposed_base_p_mixed_degree"] = mixed_degree
        row["old_mixed_no_carry_guard"] = mixed_degree < p
        row["exact_finite_generators_checked"] = len(result.group_generators)
        controls.append(row)
    x, y = sp.symbols("x y")
    threshold = []
    for prime in (3, 5, 7):
        atoms = tuple(x+a*y for a in range(prime))
        polynomial = sp.Poly(sp.prod(atoms), x, y, modulus=prime)
        shear = sp.Matrix([[1, 1], [0, 1]])
        assert polynomial == sp.Poly(x**prime-x*y**(prime-1), x, y, modulus=prime)
        assert transformed(polynomial, shear) == polynomial
        result = solve_ut_power_product(atoms, (1,)*prime, prime, (x, y))
        threshold.append({"prime": prime, "distinct_factors": prime,
                          "product_preserved_by_nontrivial_shear": True,
                          "first_atom_preserved": transformed(sp.Poly(x, x, y, modulus=prime), shear) == sp.Poly(x, x, y, modulus=prime),
                          "filter_status": result.status})
    return {
        "status": "EXPOSED_POWER_PRODUCT_FAMILY_CLASSICALLY_SOLVED",
        "theorem_status": "LOCAL_WRITTEN_PROOF_NOT_INDEPENDENTLY_REVIEWED",
        "prime_certificate": mersenne_127_certificate(),
        "controls": controls, "sharp_boundary_controls": threshold,
        "original_problem_preserved": "formal polynomial stabilizer, not equality on base-field points",
        "arbitrary_circuit_factorization_implemented": False,
        "general_matrix_group_backend_implemented": False,
        "new_quantum_algorithm": False, "speedup_claim": False,
        "new_classical_theorem_novelty_claim": False,
    }


def record():
    result = audit()
    root = Path(__file__).resolve().parent
    names = ("power_product.py", "test_power_product.py", "power_product_replay.py", "RESULT.md", "HANDOFF.md")
    result["source_sha256"] = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = record()
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(payload)
    print(json.dumps({"status": result["status"],
                      "controls": [{"D": c["dimension"], "degree_bits": c["formal_degree_bits"],
                                    "stabilizer_dimension": len(c["lie_basis"])} for c in result["controls"]]}, indent=2))
