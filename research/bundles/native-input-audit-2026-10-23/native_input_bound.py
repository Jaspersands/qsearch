"""Exact counting falsifier for independent random weak-mark fabrication.

This is not an oracle generator, a search algorithm, or a hardness bound
against arbitrary input-acquisition algorithms. All counts concern fixed
principally polarized SURFACES and an odd prime isogeny multiplier.
"""

from fractions import Fraction
from math import prod

from sympy import isprime, nextprime


def _odd_prime(value, name):
    if type(value) is not int or value < 3 or not isprime(value):
        raise ValueError(f"{name} must be an odd prime")


def sp4_order(prime):
    _odd_prime(prime, "prime")
    return prime**4*(prime**2-1)*(prime**4-1)


def lagrangian_count(prime):
    _odd_prime(prime, "prime")
    return (prime+1)*(prime**2+1)


def ceil_log2_ratio(numerator, denominator):
    if type(numerator) is not int or type(denominator) is not int or min(numerator, denominator) <= 0:
        raise ValueError("ratio must have positive integer numerator and denominator")
    exponent = numerator.bit_length()-denominator.bit_length()
    too_small = (numerator > denominator << exponent if exponent >= 0
                 else numerator << (-exponent) > denominator)
    return exponent+int(too_small)


def random_mark_probability_bound(ell, characteristic, levels, *, trials=1):
    """Union bound for iid uniform projective symplectic data at each level.

    The source and target varieties are FIXED before marks are sampled.
    A true global isogeny induces only one tuple of projective classes.
    This routine does not check a supplied tuple for global consistency.
    """
    _odd_prime(ell, "ell")
    _odd_prime(characteristic, "characteristic")
    if characteristic <= 3 or characteristic == ell:
        raise ValueError("requires characteristic p>3 different from ell")
    levels = tuple(levels)
    if not levels:
        raise ValueError("at least one auxiliary prime is required")
    for r in levels:
        _odd_prime(r, "auxiliary level")
        if r in (ell, characteristic):
            raise ValueError("auxiliary levels must be coprime to p*ell")
    if len(set(levels)) != len(levels):
        raise ValueError("repeated levels are not independent constraints")
    if type(trials) is not int or trials < 1:
        raise ValueError("trials must be a positive integer")
    kernels = lagrangian_count(ell)
    automorphism_cap = sp4_order(3)
    global_cap = kernels*automorphism_cap//2
    local_counts = [sp4_order(r)//2 for r in levels]
    space = prod(local_counts)
    single = min(Fraction(1), Fraction(global_cap, space))
    union = min(Fraction(1), trials*single)
    return {"ell": ell, "characteristic": characteristic, "levels": list(levels),
            "level_product": prod(levels), "lagrangian_kernels": kernels,
            "polarized_automorphism_cap": automorphism_cap,
            "global_maps_mod_sign_upper_bound": global_cap,
            "local_projective_class_counts": local_counts,
            "independent_mark_space_size": space,
            "single_trial_probability_upper_bound": {"numerator": single.numerator, "denominator": single.denominator},
            "single_trial_probability_at_most_power_of_two": ceil_log2_ratio(single.numerator, single.denominator),
            "trials": trials,
            "union_probability_upper_bound": {"numerator": union.numerator, "denominator": union.denominator},
            "fixed_source_and_target_required": True,
            "uniform_independent_mark_sampling_required": True,
            "global_isogeny_consistency_test_executed": False,
            "arbitrary_algorithm_hardness_established": False}


def small_prime_levels(ell, characteristic):
    """A fixed public example plan with product greater than 8*ell."""
    _odd_prime(ell, "ell")
    _odd_prime(characteristic, "characteristic")
    if characteristic <= 3 or characteristic == ell:
        raise ValueError("requires characteristic p>3 different from ell")
    levels, total, r = [], 1, 3
    while total <= 8*ell:
        if r not in (ell, characteristic):
            levels.append(r)
            total *= r
        r = int(nextprime(r))
    return tuple(levels)
