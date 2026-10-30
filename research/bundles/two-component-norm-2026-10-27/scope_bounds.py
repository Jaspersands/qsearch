"""Exact sufficient bounds, conditional on the stated geometric source."""

from fractions import Fraction
from math import isqrt

from flint import fmpz


def encode_fraction(value):
    if isinstance(value, Fraction):
        if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > 1024:
            return {"numerator_hex": hex(value.numerator), "denominator_hex": hex(value.denominator)}
        return {"numerator": value.numerator, "denominator": value.denominator}
    raise TypeError(type(value).__name__)


def bounds(p, e):
    if type(p) is not int or p < 1019 or not fmpz(p).is_prime():
        raise ValueError("prime p>=1019 required for this bound")
    if type(e) is not int or not 8 <= e <= 256:
        raise ValueError("exact diagnostic restricted to 8<=e<=256; not a theorem bound")
    g, d, m, k, t = 5*e+1, 10*e+3, 22*e, 5*e+3, 4*e+4
    root = isqrt(p)
    beta = (2*d*m*Fraction(p)**(3-e)*Fraction(root+1, root)**(2*g)
            / Fraction(p-1, p)**2)
    return {
        "p": p, "e": e, "g": g, "d": d, "m": m, "k": k, "t": t,
        "auxiliary_dimension_lower": 3*e,
        "annihilator_dimension_lower": e-3,
        "basepoint_failure_upper_raw_prime_source": min(Fraction(1), beta),
        "annihilator_zero_budget_failure_upper": Fraction(m, p*(4*e-3)),
        "offset_failure_upper": min(Fraction(1), Fraction(m)*Fraction(p)**(5-e)),
        "kernel_zero_union_upper": Fraction(m, p*p),
        "pair_stage_constant_success_certified": p*p >= 2*m,
        "source_prime_count_condition_numeric": p**d >= 4*(g+1)**2*(d+6)**2,
        "prime_count_lower_bound_is_imported_prerequisite": True,
        "public_geometry_required": True, "native_matrix_generated": False,
        "full_cube_conditioning_applied": False,
    }


def fixed_prime_cutoff(p):
    if type(p) is not int or p < 1019 or not fmpz(p).is_prime():
        raise ValueError("prime p>=1019 required")
    cutoff = p*p//44
    return {"integer_e_cutoff": cutoff,
            "dyadic_e_cutoff": 1 << (cutoff.bit_length()-1),
            "beyond_cutoff_status": "NO_FIXED_PRIME_ASYMPTOTIC_CERTIFICATE"}


def all_input_bounds(p, e):
    if type(p) is not int or p < 1019 or not fmpz(p).is_prime():
        raise ValueError("prime p>=1019 required")
    if type(e) is not int or e < 8:
        raise ValueError("integer e>=8 required")
    if e < 64:
        return {"p": p, "e": e, "method": "EXISTING_TWO_BASIS_GREEDY",
                "k": 5*e+3, "field_condition": p >= 5*e+5,
                "native_input_generated": False}
    a, m, k = e//4, 22*e-1, 5*e+3
    R = 3*e-a-11
    return {"p": p, "e": e, "method": "TWO_COMPONENT_NORM_WITH_PAID_MATRIX_ADAPTER",
            "m_punctured": m, "k": k, "basepoint_count_upper": 4*e+6,
            "additional_zero_cap": a, "restriction_rank_lower": R,
            "h_failure_upper": Fraction(m, p*(a+1)),
            "offset_failure_upper": min(Fraction(1), Fraction(m)*Fraction(p)**(k+2-2*R)),
            "kernel_zero_union_upper": Fraction(m, p*p),
            "pair_stage_constant_success_certified": p*p >= 44*e,
            "uniform_divisor_source_required": False,
            "matrix_adapter_implemented": False,
            "native_input_generated": False}
