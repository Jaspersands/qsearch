"""Exact arithmetic for a known RR-system existence theorem, not code search.

No curve, divisor class, uniform class sampler or native matrix is generated.
See GENERIC_CLASSES.md for the geometric and distributional premises.
"""

from fractions import Fraction
from math import isqrt

from flint import fmpz


def bad_class_upper(prime, genus, residual_degree):
    if (type(prime) is not int or not 5 <= prime < 2**63 or not fmpz(prime).is_prime()
            or type(genus) is not int or genus < 1 or type(residual_degree) is not int):
        raise ValueError("verified prime >=5, positive genus, integer degree required")
    if residual_degree < 0:
        return Fraction(0)
    if residual_degree >= genus:
        raise ValueError("the cited effective-divisor bound requires residual degree <=g-1")
    denominator = prime**(genus-residual_degree-1)*(isqrt(prime)-1)**2
    return min(Fraction(1), Fraction(9**genus*genus, denominator))


def tower_class_certificate(cover_degree):
    if (type(cover_degree) is not int or cover_degree < 8
            or cover_degree & (cover_degree-1)):
        raise ValueError("dyadic cover degree >=8 required")
    e, p = cover_degree, 100003
    g, d, m = 5*e+1, 10*e+3, 22*e
    residual = 2*g-2-3*d+m
    bound = bad_class_upper(p, g, residual)
    return {"cover_degree": e, "genus": g, "divisor_degree": d, "length": m,
            "residual_degree_K_minus_3G_plus_D": residual,
            "bad_fraction_upper_under_uniform_Pic_d": bound,
            "source_is_certified_in_preceding_tower_note": True,
            "requires_uniform_divisor_class_not_uniform_rational_point": True,
            "divisor_class_constructed": False, "native_matrix_constructed": False,
            "efficient_class_sampling_implemented": False,
            "rules_out_only_the_same_code_cubic_annihilator_method": True,
            "classical_hardness_proved": False, "quantum_advantage_established": False,
            "registry_admission": False}


def preimage_fraction_bound(group_order, kernel_size, bad_image_count):
    if (any(type(x) is not int for x in (group_order, kernel_size, bad_image_count))
            or group_order < 1 or kernel_size < 1 or group_order % kernel_size
            or not 0 <= bad_image_count <= group_order):
        raise ValueError("valid finite group/kernel/cardinality data required")
    return min(Fraction(1), Fraction(kernel_size*bad_image_count, group_order))


if __name__ == "__main__":
    from decimal import Decimal, localcontext
    for e in (8, 16, 32, 64):
        data = tower_class_certificate(e)
        fraction = data["bad_fraction_upper_under_uniform_Pic_d"]
        with localcontext() as context:
            context.prec = 12
            display = Decimal(fraction.numerator)/Decimal(fraction.denominator)
        print(f"e={e}, g={data['genus']}, residual={data['residual_degree_K_minus_3G_plus_D']}, "
              f"bad-class upper={display:.6E}; NO divisor/matrix generated")
