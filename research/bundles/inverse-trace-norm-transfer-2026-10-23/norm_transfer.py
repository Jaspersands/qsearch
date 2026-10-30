"""Certificate for one restricted classical ansatz, not native hardness.

FLINT handles finite-field polynomials. The existing independent integer
field implementation checks the same-input witness and parity equations.
"""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import random
import sys

from flint import fmpz_mod_poly_ctx, fq_default_ctx, fq_default_poly_ctx


ROOT = Path(__file__).resolve().parent
DEPENDENCY = ROOT.parent / "inverse-trace-residual-2026-10-23/residual_sat.py"
SPEC = importlib.util.spec_from_file_location("norm_transfer_native_dependency", DEPENDENCY)
NATIVE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = NATIVE
SPEC.loader.exec_module(NATIVE)

POINTS = (
    58, 81, 125, 5, 123, 18, 49, 62, 113, 57, 65, 98, 53, 14, 61, 69,
    91, 79, 94, 29, 34, 32, 99, 27, 121, 106, 74, 80, 9, 127, 25, 108,
    28, 102, 11, 21, 83, 1, 112, 107, 88, 23, 24, 86, 119, 66, 48, 40, 109,
)


def contexts(bits, modulus):
    native = NATIVE.BinaryField(bits, modulus)
    coefficients = [(modulus >> j) & 1 for j in range(bits + 1)]
    field = fq_default_ctx(modulus=fmpz_mod_poly_ctx(2)(coefficients))
    return native, field, fq_default_poly_ctx(field)


def element(field, value, bits):
    if type(value) is not int or not 0 <= value < 1 << bits:
        raise ValueError("canonical field element required")
    return field([(value >> j) & 1 for j in range(bits)])


def encoded(poly):
    return [sum(int(bit) << j for j, bit in enumerate(c.to_list()))
            for c in poly.coeffs()]


def odd_factor_carrier(poly):
    """The full odd-degree primary part of D must divide Q."""
    if poly.is_zero():
        raise ValueError("nonzero polynomial required")
    unit, factors = poly.factor()
    product = poly.context()(unit)
    rows = []
    degree = 0
    for factor, multiplicity in factors:
        if not factor.is_irreducible():
            raise ArithmeticError("uncertified irreducible factor")
        product *= factor ** multiplicity
        forced = factor.degree() % 2 == 1
        degree += factor.degree() * multiplicity if forced else 0
        rows.append({"coefficients": encoded(factor), "degree": factor.degree(),
                     "multiplicity": multiplicity, "forced_in_Q": forced})
    if product != poly:
        raise ArithmeticError("factorization does not reconstruct polynomial")
    return degree, sorted(rows, key=lambda row: (row["degree"], row["coefficients"]))


def certificate(points=POINTS, bits=7, modulus=131):
    native, field, ring = contexts(bits, modulus)
    size, checks = bits * bits, bits * bits // 8
    if bits < 5 or bits % 2 == 0 or len(points) != size or len(set(points)) != size:
        raise ValueError("odd-degree native shape and distinct points required")
    polynomial = ring.one()
    for value in points:
        native.element(value)
        polynomial *= ring.gen() + element(field, value, bits)
    derivative = polynomial.derivative()
    root = ring([derivative[2*j].sqrt() for j in range(derivative.degree() // 2 + 1)])
    if root * root != derivative or any(root(element(field, a, bits)) == 0 for a in points):
        raise ArithmeticError("invalid derivative square root")
    lower_bound, factors = odd_factor_carrier(root)
    budget = (size - checks - 1) // 2
    return {
        "bits": bits, "modulus": modulus, "N": size, "K": checks,
        "points": list(points), "targets": [1] * size,
        "F_coefficients": encoded(polynomial), "D_coefficients": encoded(root),
        "D_degree": root.degree(), "D_factors": factors,
        "forced_Q_degree_lower_bound": lower_bound,
        "code_Q_degree_budget": budget,
        "low_degree_U_budget": (size - 1) // 2,
        "global_norm_ansatz_excluded": lower_bound > budget,
        "scope": "P=Q^2_and_global_Artin_Schreier_identity_only",
    }


def same_input_witness(points=POINTS, bits=7, modulus=131, seed=23, trial_cap=4096):
    """Existing systematic-root baseline, with every attempted trial counted."""
    data = certificate(points, bits, modulus)
    field = NATIVE.BinaryField(bits, modulus)
    checks = data["K"]
    constants, rows = NATIVE.affine_chart(field, points, checks, (0,) * checks)
    rng = random.Random(seed)
    draws = 0
    for attempt in range(1, trial_cap + 1):
        free = []
        for _ in range(len(points) - checks):
            # A bounded reference sampler; this run does not claim scalable search.
            for _ in range(128):
                draws += 1
                value = rng.randrange(field.order)
                if field.trace(field.inverse(value)) == 1:
                    free.append(value)
                    break
            else:
                raise RuntimeError("accepted-root draw cap reached")
        pivots = []
        for constant, row in zip(constants, rows):
            value = constant
            for coefficient, x in zip(row, free):
                value ^= field.multiply(coefficient, x)
            pivots.append(value)
        values = tuple(pivots + free)
        if NATIVE.verify(field, points, values, checks, (1,) * len(points), (0,) * checks):
            return {"values": list(values), "trials": attempt,
                    "field_draws": draws, "trial_cap": trial_cap, "seed": seed,
                    "native_valid": True,
                    "method": "existing_exponential_systematic_root_baseline"}
    raise RuntimeError("no witness found within charged trial cap")


def report():
    data = certificate()
    if not data["global_norm_ansatz_excluded"]:
        raise ArithmeticError("the fixed counterexample did not exclude the ansatz")
    result = {
        "status": "RESTRICTED_NORM_TRANSFER_REJECTED_NOT_NATIVE_HARDNESS",
        "certificate": data, "same_input_witness": same_input_witness(),
        "universal_classical_attack_excluded": False,
        "all_square_polynomial_witnesses_excluded": False,
        "quantum_advantage_established": False,
        "repository_registry_admission": False,
        "sha256": {str(p): sha256(p.read_bytes()).hexdigest()
                   for p in (ROOT / "norm_transfer.py", ROOT / "test_norm_transfer.py",
                             ROOT / "NORM_TRANSFER.md", DEPENDENCY)},
    }
    (ROOT / "receipt.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
