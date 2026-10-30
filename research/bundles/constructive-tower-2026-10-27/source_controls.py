"""Exact source-design controls, NOT a higher-level function-field backend."""

from fractions import Fraction
from math import prod
from pathlib import Path
import sys

from flint import fmpz, nmod_mat

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent/"generic-divisor-class-2026-10-26"))
from class_bound import tower_class_certificate
sys.path.insert(0, str(ROOT.parent/"prime-ag-tower-source-2026-10-26"))
from tower_seed import default_seed


def prime_class_bound(e):
    data = tower_class_certificate(e)
    q, g, d = 100003, data["genus"], data["divisor_degree"]
    if q**d < 4*(g+1)**2*(d+6)**2:
        raise ArithmeticError("prime-count lower bound unavailable")
    inflation = Fraction(2*d*q, q-1)*Fraction(318**2, q)**g
    bad = data["bad_fraction_upper_under_uniform_Pic_d"]*inflation
    section_dim = 3*g+5
    # Lower acceptance for Bruin's corrected section-factor sampler.
    prime_sampler_success = Fraction(q**d, 2*d) * Fraction(
        q**(section_dim-d)-1, q**section_dim-1) / 2
    return {
        "cover_degree": e, "genus": g, "prime_divisor_degree": d,
        "maximum_class_mass_inflation_upper": inflation,
        "bad_prime_probability_upper": min(Fraction(1), bad),
        "corrected_prime_sampler_success_lower": prime_sampler_success,
        "prime_sampler_expected_section_trials_upper": 1/prime_sampler_success,
        "prime_sampler_grading_required": 6,
        "native_curve_or_prime_generated": False,
        "uniform_Picard_class_distribution_claimed": False,
        "classical_hardness_established": False,
        "quantum_advantage_established": False,
    }


def local_split_bit(prime, valuation, leading_unit):
    """Classify supplied local data; this does NOT extract it from a function."""
    if (type(prime) is not int or not 3 <= prime < 2**63
            or not fmpz(prime).is_prime()):
        raise ValueError("verified odd prime below2^63 required")
    if type(valuation) is not int or valuation % 2:
        raise ValueError("even valuation required for an unramified Kummer place")
    if type(leading_unit) is not int or not 1 <= leading_unit < prime:
        raise ValueError("nonzero canonical regularized unit required")
    return int(pow(leading_unit, (prime-1)//2, prime) != 1)


def seed_kernel():
    seed = default_seed()
    q = seed.prime
    if pow(2, (q-1)//2, q) != q-1:
        raise ArithmeticError("constant2 is not a nonsquare")
    # First12 branch radicands form a basis modulo the full13-factor square.
    rows = []
    for x in seed.splitting_x:
        row = [1]+[local_split_bit(q, 0, (x-a) % q) for a in seed.branches[:12]]
        rows.extend([row, row.copy()])
    rows.append([1]+[local_split_bit(q, -2, 1) for _ in range(12)])
    matrix = nmod_mat(rows, 2)
    kernel, dimension = matrix.nullspace()
    columns = [[int(kernel[i, j]) for i in range(13)] for j in range(dimension)]
    if any(any(sum(a*b for a, b in zip(row, column)) % 2 for row in rows)
           for column in columns):
        raise ArithmeticError("split-kernel certificate failed")
    branch_controls = []
    for a in seed.branches:
        derivative = prod((a-b) % q for b in seed.branches if b != a) % q
        unit = pow(derivative, -1, q)
        branch_controls.append({"branch": a, "valuation_of_x_minus_a": 2,
                                "regularized_unit_using_y_parameter": unit,
                                "split_bit": local_split_bit(q, 2, unit)})
    return {"prime": q, "marked_places": len(rows), "split_matrix": rows,
            "matrix_rank": matrix.rank(), "kernel_dimension": dimension,
            "kernel_basis": columns, "branch_place_controls": branch_controls,
            "raw_evaluation_at_branch_is_not_a_unit": True,
            "higher_tower_level_generated": False}
