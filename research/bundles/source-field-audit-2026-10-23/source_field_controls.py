"""Source-field accounting and an actual supersingular-curve countercontrol.

These are not PPAV canonicalization, quotient, or isogeny-search routines.
SymPy supplies all extension-field arithmetic. The p=37 enumeration is a
bounded mathematical control, not a scalable method of finding curves.
"""

from functools import lru_cache
from math import gcd

from sympy import Poly, isprime, symbols
from sympy.polys.agca.extensions import MonogenicFiniteExtension


def auxiliary_field_plan(characteristic, half_base_degree, scalar_sign, levels):
    """Bounds conditional on a supplied common field with scalar Frobenius.

    The original base is F_(p^(2m)) with Frobenius [sign*p^m]. Replace it
    ONCE by its quadratic extension. Each auxiliary field is separate;
    degrees in this result must never be multiplied into a compositum.
    """
    if type(characteristic) is not int or characteristic <= 3 or not isprime(characteristic):
        raise ValueError("requires prime characteristic p>3")
    if type(half_base_degree) is not int or half_base_degree < 1:
        raise ValueError("half_base_degree must be a positive integer")
    if type(scalar_sign) is not int or scalar_sign not in (-1, 1):
        raise ValueError("scalar_sign must be -1 or 1")
    levels = tuple(levels)
    if not levels:
        raise ValueError("levels must be nonempty")
    rows = []
    for level in levels:
        if not isinstance(level, tuple) or len(level) != 2:
            raise ValueError("each level must be (auxiliary_prime, exponent)")
        r, exponent = level
        if type(r) is not int or not isprime(r) or r == characteristic:
            raise ValueError("auxiliary prime must differ from the characteristic")
        if type(exponent) is not int or exponent not in (1, 2):
            raise ValueError("only prime and prime-square auxiliary levels are supported")
        order = r**exponent
        degree = r**(exponent-1)*(r-1)
        scalar_mod_order = pow(characteristic, 2*half_base_degree, order)
        if gcd(scalar_mod_order, order) != 1 or pow(scalar_mod_order, degree, order) != 1:
            raise AssertionError("Euler field bound failed")
        rows.append({"auxiliary_prime": r, "exponent": exponent,
                     "torsion_order": order, "extension_degree_over_fixed_base": degree,
                     "absolute_field_degree": 4*half_base_degree*degree,
                     "scalar_frobenius_mod_order": scalar_mod_order,
                     "annihilates_frobenius_action": True})
    if len(set(levels)) != len(levels):
        raise ValueError("levels must not contain duplicates")
    return {"characteristic": characteristic,
            "original_base_degree": 2*half_base_degree,
            "original_scalar_sign": scalar_sign,
            "fixed_base_degree": 4*half_base_degree,
            "fixed_scalar_mod_8": pow(characteristic, 2*half_base_degree, 8),
            "all_8_torsion_rational_over_fixed_base": True,
            "max_point_field_degree": max(row["absolute_field_degree"] for row in rows),
            "sum_separate_field_degrees": sum(row["absolute_field_degree"] for row in rows),
            "auxiliary_fields": rows,
            "common_field_and_scalar_promises_verified": False,
            "geometric_descent_executed": False,
            "compositum_constructed": False}


@lru_cache(maxsize=1)
def field37():
    u = symbols("u")
    return MonogenicFiniteExtension(Poly(u*u-15, u, modulus=37))


def embedding_key37(value):
    """Coordinates in the ONE fixed embedding u^2=15, not modulo Galois."""
    field = field37()
    terms = field.convert(value).rep.to_list()
    terms = [0]*(2-len(terms)) + terms
    return int(terms[1]) % 37, int(terms[0]) % 37


def unsafe_galois_key37(value):
    """Deliberately wrong geometric key, retained ONLY as a falsifier."""
    value = field37().convert(value)
    return min(embedding_key37(value), embedding_key37(value**37))


def _curve_invariants(field, a, b):
    x = symbols("x")
    denominator = 4*a**3 + 27*b**2
    if not denominator:
        raise ValueError("singular curve")
    polynomial = Poly.from_list([field.one, field.zero, a, b], x, domain=field)
    hasse = field.convert((polynomial**18).nth(36))
    return field(1728)*4*a**3/denominator, hasse


@lru_cache(maxsize=1)
def conjugate_curve_control():
    """Count both actual curves, and check their Hasse invariants exactly."""
    field = field37()
    u = field.generator
    j = field(3)+u
    k = j/(field(1728)-j)
    a, b = 3*k, 2*k
    conjugate_a, conjugate_b = a**37, b**37
    j1, hasse1 = _curve_invariants(field, a, b)
    j2, hasse2 = _curve_invariants(field, conjugate_a, conjugate_b)
    values = [field(a0)+b0*u for a0 in range(37) for b0 in range(37)]
    nonzero_squares = {y*y for y in values if y}

    def point_count(aa, bb):
        count = 1
        for xx in values:
            rhs = xx**3+aa*xx+bb
            count += 1 if not rhs else 2 if rhs in nonzero_squares else 0
        return count

    counts = point_count(a, b), point_count(conjugate_a, conjugate_b)
    checks = {
        "defining_polynomial_irreducible": pow(15, 18, 37) == 36,
        "j_formula_verified": j1 == j and j2 == j**37,
        "both_hasse_invariants_zero": not hasse1 and not hasse2,
        "both_curves_maximal_over_base": counts == (38**2, 38**2),
        "different_geometric_j_invariants": j1 != j2,
        "both_j_satisfy_same_minimal_polynomial": all(v*v-6*v-6 == field.zero for v in (j1, j2)),
        "j_not_prime_field_rational": j1**37 != j1,
        "j_base_field_rational": j1**(37**2) == j1,
        "unsafe_galois_keys_collide": unsafe_galois_key37(j1) == unsafe_galois_key37(j2),
        "fixed_embedding_keys_separate": embedding_key37(j1) != embedding_key37(j2),
        "theta_8_torsion_needs_extension": (-37) % 8 != 1,
        "one_quadratic_extension_fixes_8_torsion": ((-37)**2) % 8 == 1,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {"characteristic": 37, "base_field": "F_37[u]/(u^2-15)",
            "coefficient_encoding": "(constant, u_coefficient) in the fixed embedding",
            "curve": {"a": embedding_key37(a), "b": embedding_key37(b),
                      "j": embedding_key37(j1), "points": counts[0]},
            "conjugate_curve": {"a": embedding_key37(conjugate_a),
                                "b": embedding_key37(conjugate_b),
                                "j": embedding_key37(j2), "points": counts[1]},
            "q_frobenius_scalar_from_maximal_count": -37,
            "p_frobenius_self_isomorphism_exists": False,
            "geometric_isomorphism_between_curves_exists": False,
            "checks": checks,
            "target_order_recovery_executed": False,
            "ppav_geometric_label_generator_executed": False}
