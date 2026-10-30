"""An exact smaller-field source and native degree-eight AG control.

No high-level tower or quantum circuit is generated. All witnesses are checked
against the original explicit parity matrix, not a planted solution.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import isqrt, prod
from pathlib import Path
import sys

from flint import nmod_mat

ROOT = Path(__file__).resolve().parent
for sibling in ("prime-ag-tower-source-2026-10-26",
                "schur-growth-classical-gate-2026-10-26",
                "systematic-full-support-2026-10-27"):
    sys.path.insert(0, str(ROOT.parent / sibling))
from tower_seed import TowerSeed
from schur_gate import FullSupportProblem, rows
from systematic import SystematicFiber, distance_bound


P = 1019
BRANCHES = (63, 66, 86, 98, 105, 107, 188, 554, 570, 578, 673, 773, 866)
SPLITTING_X = (0, 468, 568, 571, 614, 634, 696, 882, 926, 942, 965)
LOW = tuple(mask for mask in range(16) if mask.bit_count() % 2 == 0)
FULL = (1 << 13)-1
MASKS = LOW + tuple(FULL ^ mask for mask in LOW)
DEFAULT_INDICES = (0, 3, 5, 9, 14)


def seed():
    return TowerSeed(P, BRANCHES, SPLITTING_X)


def parameter_bounds(p, e):
    """Exact conditional bounds; no assertion that a code at e was built."""
    # Reuse the prior public prime and integer validation, not its fixed-p data.
    from tower_seed import checked_prime
    checked_prime(p)
    if type(e) is not int or e < 8 or e & (e-1):
        raise ValueError("dyadic degree at least eight required")
    if p <= 44:
        raise ValueError("the coarse all-degree argument requires p > 44")
    g, d, k, m, w = 5*e+1, 10*e+3, 5*e+3, 22*e, 15*e+6
    lower, upper = isqrt(p)-1, isqrt(p)+2
    bad_class = Fraction(9**g*g, p**(3*e+9)*lower**2)
    bad_prime = bad_class * Fraction(2*d*p, p-1) * Fraction(upper**2, p)**g
    prime_ratio = Fraction(4*9**5, p**3) * Fraction(upper**2, p)**5
    error = Fraction((p**k-1)*p**w, (p-1)**m)
    baseline = distance_bound(p, m, k, m-d)
    tail = baseline["tail_upper"]
    return {
        "p": p, "e": e, "g": g, "d": d, "k": k, "m": m, "w": w,
        "matrix_entries": k*m, "decoder_error_upper": error,
        "raw_verified_quantum_success_lower": max(Fraction(0), 1-error)**2/(1+tail),
        "systematic": baseline, "bad_prime_upper": bad_prime,
        "bad_prime_one_degree_ratio_upper": prime_ratio,
        "prime_count_condition": p**d >= 4*(g+1)**2*(d+6)**2,
        "coarse_E_at_e8": Fraction(256, p**7),
        "coarse_E_per_degree_ratio": Fraction(2, p*p),
        "conditional_on_actual_complete_AG_input_and_USD_reduction": True,
        "native_matrix_generated_by_this_function": False,
        "quantum_advantage_established": False,
    }


def split_fiber(x):
    """Points on the actual degree-eight cover, not the full Kummer cover."""
    if type(x) is not int or not 0 <= x < P or x in BRANCHES:
        raise ValueError("unramified canonical x required")
    radicands = [(x-BRANCHES[0])*(x-BRANCHES[i]) % P for i in (1, 2, 3)]
    radicands.append(prod((x-a) % P for a in BRANCHES) % P)
    roots = [pow(a, (P+1)//4, P) for a in radicands]
    if any(r*r % P != a for r, a in zip(roots, radicands)):
        return []
    return [{"x": x, "w": [roots[i]*signs[i] % P for i in range(3)],
             "y": roots[3]*signs[3] % P}
            for signs in product((1, -1), repeat=4)]


def monomials(pole_bound):
    return [(mask, j) for mask in MASKS
            for j in range((pole_bound-mask.bit_count())//2+1)]


def evaluate(monomial, point):
    mask, power = monomial
    low = mask if mask in LOW else FULL ^ mask
    count = sum(bool(low & (1 << i)) for i in (1, 2, 3))
    radical = prod(point["w"][i-1] for i in (1, 2, 3) if low & (1 << i)) % P
    # Product w_i has an extra even power of sqrt(x-a_0).
    extra = (count - int(bool(low & 1)))//2
    radical = radical * pow(pow((point["x"]-BRANCHES[0]) % P, extra, P), -1, P) % P
    if mask not in LOW:
        radical = point["y"]*pow(radical, -1, P) % P
    return pow(point["x"], power, P)*radical % P


@lru_cache(maxsize=1)
def build_control():
    seed_certificate = seed().certificate()
    if not seed_certificate["schoof_sufficient_criterion"]:
        raise ArithmeticError("seed does not pass the imported tower criterion")
    points = [point for x in SPLITTING_X for point in split_fiber(x)]
    extra_x = next(x for x in range(P) if x not in SPLITTING_X and x not in BRANCHES
                   and split_fiber(x))
    zeros = [split_fiber(extra_x)[i] for i in DEFAULT_INDICES]
    functions = monomials(11)
    constraints = nmod_mat([[evaluate(f, point) for f in functions] for point in zeros], P)
    kernel, dimension = constraints.nullspace()
    transform = nmod_mat([[int(kernel[i, j]) for i in range(len(functions))]
                         for j in range(dimension)], P)
    evaluation = nmod_mat([[evaluate(f, point) for point in points] for f in functions], P)
    original = rows(transform*evaluation)
    problem = FullSupportProblem(P, original, relation="full_support")
    if (len(functions), constraints.rank(), dimension, problem.k, problem.m,
            len(problem.W)) != (48, 5, 43, 43, 176, 126):
        raise ArithmeticError("complete AG input failed its exact dimension checks")
    fiber = SystematicFiber(P, original, relation="full_support")
    small_functions = monomials(1)
    small_constraints = nmod_mat([[evaluate(f, point) for f in small_functions]
                                  for point in zeros], P)
    return problem, fiber, {
        "seed": seed_certificate, "cover_degree": 8, "genus": 41,
        "curve": "y^2=product(x-a); w_i^2=(x-a_0)(x-a_i), i=1,2,3",
        "divisor": "G=11I-E; I=pullback(infinity); E=five listed distinct points",
        "divisor_degree": 83, "extra_x": extra_x, "zero_divisor": zeros,
        "evaluation_points": points, "monomials": functions,
        "constraints": rows(constraints), "rr_basis": rows(transform),
        "original_parity": original, "k": problem.k, "m": problem.m,
        "square_rank": len(problem.W), "cube_rank": len(problem.U),
        "cube_annihilator_dimension": len(problem.annihilator),
        "dimension_L_G_minus_K": len(small_functions)-small_constraints.rank(),
        "native_degree_eight_matrix_constructed": True,
        "native_higher_levels_constructed": False,
        "uniform_divisor_class_sample": False,
        "quantum_execution": False, "quantum_advantage_established": False,
    }
