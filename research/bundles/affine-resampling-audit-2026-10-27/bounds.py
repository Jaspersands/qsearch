"""Conditional bounds, not generated higher-level matrices or hardness tests."""

from fractions import Fraction
from math import comb, isqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "small-prime-tower-2026-10-27"))
from small_prime import parameter_bounds
from tower_seed import checked_prime


def checked_parameters(p, k, m, delta):
    checked_prime(p)
    if p < 3 or any(type(x) is not int for x in (k, m, delta)):
        raise ValueError("odd prime and integer dimensions required")
    if not 1 <= k <= m or not 1 <= delta <= m-k+1:
        raise ValueError("full-row-rank dimensions and admissible distance required")


def stationary_hitting(p, k, m, delta):
    checked_parameters(p, k, m, delta)
    alpha = Fraction(p**k-1, (p-1)**delta)
    mass_upper = min(Fraction(1), Fraction(p-1, p)**m*(1+alpha))
    r = 1//mass_upper
    exact_tail_sum = r-mass_upper*r*(r+1)/2
    return {"alpha": alpha, "full_support_mass_upper": mass_upper,
            "first_hit_expectation_lower": exact_tail_sum,
            "simpler_expectation_lower": (1-mass_upper)/(2*mass_upper),
            "requires_uniform_initial_state_and_uniform_time_marginals": True,
            "applies_to_adaptive_focused_repair": False,
            "distance_verified_by_helper": False,
            "general_classical_lower_bound": False}


def pair_overlap(p, k, m, delta, weight):
    checked_parameters(p, k, m, delta)
    if type(weight) is not int or not 1 <= weight <= m:
        raise ValueError("nonzero move weight in range required")
    alpha = Fraction(p**k-1, (p-1)**delta)
    eta = (p**k-1)*min(Fraction(1), Fraction(2, p-2))**delta
    upper = None if alpha >= 1 else min(
        Fraction(1), Fraction(p-2, p-1)**weight*(1+eta)/(1-alpha))
    return {"alpha": alpha, "eta": eta, "conditional_overlap_upper": upper,
            "requires_fixed_kernel_move_and_uniform_valid_state": True,
            "distance_verified_by_helper": False}


def prime_source_locality(e):
    """CCX class count transferred to the existing good-prime source law."""
    p = 1019
    old = parameter_bounds(p, e)
    g, d, m, t = old["g"], old["d"], old["m"], 2*e
    lower, upper = isqrt(p)-1, isqrt(p)+2
    uniform_class_bad = Fraction(comb(m, t)*g, p**(g-t+2)*lower**2)
    prime_transfer = Fraction(2*d*p, p-1)*Fraction(upper**2, p)**g
    prime_bad = uniform_class_bad*prime_transfer
    cube_bad = old["bad_prime_upper"]
    conditioned = prime_bad/(1-cube_bad) if cube_bad < 1 else None
    special_class = Fraction(g, p**(4*e+3)*lower**2)
    special_conditioned = special_class*prime_transfer/(1-cube_bad) if cube_bad < 1 else None
    binomial_ratio = Fraction(22*9, 8)**22/(4*20**20)
    degree_ratio = 4*binomial_ratio/Fraction(p**3)*Fraction(upper**2, p)**5
    return {"p": p, "e": e, "g": g, "m": m, "excluded_move_weight": t,
            "uniform_class_bad_upper": uniform_class_bad,
            "prime_class_max_mass_transfer": prime_transfer,
            "unconditioned_prime_bad_upper": prime_bad,
            "good_cube_prime_bad_upper": conditioned,
            "good_cube_prime_special_11I_minus_effective_upper": special_conditioned,
            "one_degree_ratio_upper_for_unconditioned_bound": degree_ratio,
            "prime_count_condition": old["prime_count_condition"],
            "cube_rejection_bound": cube_bad,
            "requires_exact_uniform_closed_prime_then_cube_rejection": True,
            "applies_to_handpicked_11I_minus_E": False,
            "native_higher_input_generated": False,
            "general_classical_lower_bound": False}


def fixed_bank_isolation(e, bank_size):
    """Uniform valid states, fixed bank; NOT first-hit search complexity."""
    if (type(e) is not int or e < 8 or e & (e-1)
            or type(bank_size) is not int or bank_size < 1):
        raise ValueError("dyadic e>=8 and positive bank size required")
    p = 1019
    base = pair_overlap(p, 43, 176, 93, 17)
    eta_ratio = p**5*Fraction(2, p-2)**12
    alpha_ratio = Fraction(p**5, (p-1)**12)
    # Replacing p^k-1 by p^k makes the all-degree geometric bound immediate.
    alpha0 = Fraction(p**43, (p-1)**93)
    eta0 = p**43*Fraction(2, p-2)**93
    if not (base["alpha"] < 1 and eta0+2*alpha0 <= 1
            and eta_ratio < 1 and alpha_ratio < 1):
        raise ArithmeticError("factor-two all-degree argument failed")
    upper = min(Fraction(1), 2*bank_size*(p-1)*Fraction(p-2, p-1)**(2*e+1))
    return {"nonisolated_fraction_upper": upper,
            "conditional_on_kernel_minimum_distance_greater_than_2e": True,
            "fixed_direction_bank_size": bank_size,
            "applies_to_state_adaptive_direction_selection": False,
            "first_hit_lower_bound": False, "general_classical_lower_bound": False}
