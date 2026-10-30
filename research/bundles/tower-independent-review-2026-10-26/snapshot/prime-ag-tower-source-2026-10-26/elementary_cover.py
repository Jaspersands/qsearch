"""Actual degree-eight AG input and its persistent classical annihilator.

The cover adjoins sqrt(x*(x-i)), i=1,2,3, to the genus-six base. Its full
Riemann-Roch evaluation code is constructed by character decomposition and
local expansions, not by supplying a made-up parity matrix.
"""

import importlib.util
from functools import lru_cache
from itertools import product
from math import prod
from pathlib import Path

from flint import nmod_mat

from tower_seed import PRIME, default_seed, exact_small_quantum_bounds, specialization


BASELINE = Path(__file__).resolve().parent.parent / "schur-growth-classical-gate-2026-10-26/schur_gate.py"
spec = importlib.util.spec_from_file_location("tower_prior_schur", BASELINE)
schur = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schur)

FULL_MASK = (1 << 13)-1
LOW_MASKS = tuple(mask for mask in range(16) if mask.bit_count() % 2 == 0)
MASKS = LOW_MASKS+tuple(FULL_MASK ^ mask for mask in LOW_MASKS)


@lru_cache(maxsize=None)
def sqrt_series(mask, order):
    """Coefficients of sqrt(product_(i in mask)(1-i*v)), constant term1."""
    polynomial = [1]+[0]*order
    for i in range(13):
        if mask & (1 << i):
            for j in range(order, 0, -1):
                polynomial[j] = (polynomial[j]-i*polynomial[j-1]) % PRIME
    answer = [1]
    for n in range(1, order+1):
        value = polynomial[n]-sum(answer[i]*answer[n-i] for i in range(1, n))
        answer.append(value*pow(2, -1, PRIME) % PRIME)
    return tuple(answer)


def monomials(pole_bound):
    return [(mask, j) for mask in MASKS
            for j in range((pole_bound-mask.bit_count())//2+1)]


def infinity_sign(mask, signs):
    low = mask if mask in LOW_MASKS else FULL_MASK ^ mask
    return prod(signs[i-1] for i in range(1, 4) if low & (1 << i))


def local_coefficient(monomial, pole_order, signs=(1, 1, 1)):
    mask, degree = monomial
    difference = mask.bit_count()+2*degree-pole_order
    if difference < 0 or difference % 2:
        return 0
    order = difference//2
    return infinity_sign(mask, signs)*sqrt_series(mask, order)[order] % PRIME


def evaluate(monomial, point):
    mask, degree = monomial
    low = mask if mask in LOW_MASKS else FULL_MASK ^ mask
    radical = prod(point["roots"][i] for i in range(4) if low & (1 << i)) % PRIME
    if mask not in LOW_MASKS:
        radical = point["y"]*pow(radical, -1, PRIME) % PRIME
    return pow(point["x"], degree, PRIME)*radical % PRIME


def points_above_seed():
    answer = []
    for pair in default_seed().certificate()["affine_splitting_pairs"]:
        for y in pair["y_pair"]:
            for signs in product((1, -1), repeat=3):
                roots = [pair["square_roots"][0]]+[
                    pair["square_roots"][i]*signs[i-1] % PRIME for i in range(1, 4)]
                answer.append({"x": pair["x"], "y": y, "roots": roots,
                               "w": [roots[0]*roots[i] % PRIME for i in range(1, 4)]})
    return answer


def geometric_annihilator(points):
    functions = monomials(2)
    constraints = nmod_mat([[local_coefficient(monomial, pole) for monomial in functions]
                            for pole in (2, 0, -2, -4, -6)], PRIME)
    kernel, nullity = constraints.nullspace()
    if nullity != 3:
        raise ArithmeticError("changed low-pole cancellation space")
    coefficients = [int(kernel[i, 0]) for i in range(len(functions))]
    local = {exponent: sum(c*local_coefficient(monomial, -exponent)
                          for c, monomial in zip(coefficients, functions)) % PRIME
             for exponent in range(-2, 17)}
    leading = next(exponent for exponent, coefficient in local.items() if coefficient)
    if leading < 7:
        raise ArithmeticError("annihilator function fails its required zero at R")
    xs = default_seed().splitting_x
    h = []
    for point in points:
        derivative = prod((point["x"]-x) % PRIME for x in xs if x != point["x"]) % PRIME
        value = sum(c*evaluate(monomial, point)
                    for c, monomial in zip(coefficients, functions)) % PRIME
        h.append(value*pow(point["y"]*derivative % PRIME, -1, PRIME) % PRIME)
    return h, {"monomials_mask_and_x_degree": functions, "coefficients": coefficients,
               "constraint_rank": constraints.rank(), "function_space_dimension": nullity,
               "order_at_distinguished_infinity": leading,
               "residue_formula": "f(P) / (y(P) * H_prime(x(P)))",
               "annihilator": h}


def control():
    points = points_above_seed()
    functions = monomials(13)
    constraints = []
    for signs in product((1, -1), repeat=3):
        if signs != (1, 1, 1):
            constraints.extend([[local_coefficient(monomial, pole, signs)
                                 for monomial in functions] for pole in (11, 12, 13)])
    constraint_matrix = nmod_mat(constraints, PRIME)
    kernel, dimension = constraint_matrix.nullspace()
    transform = nmod_mat([[int(kernel[i, j]) for i in range(len(functions))]
                         for j in range(dimension)], PRIME)
    evaluations = nmod_mat([[evaluate(monomial, point) for point in points]
                            for monomial in functions], PRIME)
    original = schur.rows(transform*evaluations)
    problem = schur.FullSupportProblem(PRIME, original, relation="full_support")
    if (len(functions), constraint_matrix.rank(), dimension, problem.m,
            len(problem.W), len(problem.U), len(problem.annihilator)) != (64, 21, 43, 176, 126, 173, 3):
        raise ArithmeticError("actual cover no longer matches its geometric dimensions")
    h, certificate = geometric_annihilator(points)
    if any(sum(a*b for a, b in zip(row, h)) % PRIME for row in problem.U):
        raise ArithmeticError("geometric residues do not annihilate the computed Schur cube")
    support = [i for i, value in enumerate(h) if value]
    if schur.selected(problem.B, support).rank() != problem.k:
        raise ArithmeticError("analytic annihilator fails original full-rank restriction")
    return problem, h, {
        "curve_description": "y^2=product_(i=0..12)(x-i), w_j^2=x*(x-j), j=1,2,3",
        "normalization_and_smooth_projective_model_required": True,
        "divisor": "G=10*pi^*(infinity)+3R; R has all three positive infinity signs",
        "parameters": specialization(8), "ambient_monomials": functions,
        "infinity_constraint_rank": constraint_matrix.rank(),
        "original_parity": original, "points": points,
        "square_dimension": len(problem.W), "cube_dimension": len(problem.U),
        "cube_annihilator_dimension": len(problem.annihilator),
        "analytic_annihilator": certificate, "analytic_support_size": len(support),
        "analytic_support_parity_rank": problem.k,
        "conditional_refined_quantum_bounds": exact_small_quantum_bounds(8),
        "native_parity_matrix_constructed": True,
        "all_higher_covers_constructed": False, "quantum_advantage_established": False,
    }


def one_point_control():
    """Scope falsifier: replace K+3R by 83R on the SAME degree-eight curve."""
    points = points_above_seed()
    functions = monomials(83)
    constraints = []
    for signs in product((1, -1), repeat=3):
        if signs != (1, 1, 1):
            constraints.extend([[local_coefficient(monomial, pole, signs)
                                 for monomial in functions] for pole in range(1, 84)])
    constraint_matrix = nmod_mat(constraints, PRIME)
    kernel, dimension = constraint_matrix.nullspace()
    transform = nmod_mat([[int(kernel[i, j]) for i in range(len(functions))]
                         for j in range(dimension)], PRIME)
    evaluation = nmod_mat([[evaluate(monomial, point) for point in points]
                           for monomial in functions], PRIME)
    problem = schur.FullSupportProblem(PRIME, schur.rows(transform*evaluation), relation="full_support")
    return problem, {"divisor": "83R, not assumed equivalent to K+an effective degree-three divisor",
                     "ambient_dimension": len(functions), "jet_constraint_rank": constraint_matrix.rank(),
                     "dimension": dimension, "length": problem.m,
                     "square_dimension": len(problem.W), "cube_dimension": len(problem.U),
                     "cube_annihilator_dimension": len(problem.annihilator),
                     "original_parity": schur.rows(problem.B),
                     "asymptotic_classical_hardness": False,
                     "quantum_advantage_established": False}
