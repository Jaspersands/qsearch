"""Classical baseline for polynomial-valued bounded-class HSP instances.

This is NOT an attack on opaque coset labels. Field-valued outputs, a
trusted degree bound in public logarithmic coordinates, and the explicit
characteristic guard are essential. The sampled attack supports a public
nilpotency-class bound; dense symbolic references remain class three.
It reads values only, not coefficients or a hidden subgroup.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import json
from math import comb
from pathlib import Path
import random

import sympy as sp
from flint import fmpz_mod_ctx, fmpz_mod_mat

from theorems.folded_rs_decoder import affine_solution
from theorems.nil3_cocycle_receiver import free_two_step_three
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/nil3_polynomial_hiding_attack.json"


def _guard(group, degree):
    if type(degree) is not int or degree < 0 or group.p <= 2*(degree+1):
        raise ValueError("trusted nonnegative degree e and p>2(e+1) required")


def stabilizer_degree_bounds(p, degree, class_bound):
    """Sufficient bounds, not a test of an evaluator's semantic degree promise."""
    ring(p)
    if type(class_bound) is not int or class_bound < 1:
        raise ValueError("positive integer nilpotency class bound required")
    if type(degree) is not int or degree < 0:
        raise ValueError("trusted nonnegative integer degree bound required")
    path_degree = max(1, 2*((class_bound-1)//2))
    derivative_degree = degree-1+path_degree if degree else 0
    threshold = max(class_bound, degree*path_degree, 2*derivative_degree)
    if p <= threshold:
        raise ValueError(
            "requires p>max(c,e*D,2*(e-1+D)), D=max(1,2*floor((c-1)/2)); "
            "for c=3 and e>0 this is p>2(e+1)")
    return {"class_bound": class_bound, "path_degree_bound": path_degree,
            "derivative_degree_bound": derivative_degree,
            "strict_characteristic_threshold": threshold,
            "deficient_rank_detection_probability_lower_bound":
                str(Fraction(p-derivative_degree, p))}


def _nilpotency_profile(group, class_bound):
    """Check the public lower central series, assuming a genuine Lie bracket.

    No group elements or hiding outputs are enumerated. Bilinearity and
    Jacobi are presentation promises; this check does not certify them.
    """
    d, p = group.dimension, group.p
    if type(d) is not int or d < 1:
        raise ValueError("positive public Lie dimension required")
    basis = [tuple(int(i == j) for j in range(d)) for i in range(d)]
    current, dimensions, calls = basis, [d], 0
    for _ in range(class_bound):
        rows = [group.bracket(e, v) for e in basis for v in current]
        calls += len(rows)
        if any(len(row) != d or any(type(a) is not int or not 0 <= a < p for a in row)
               for row in rows):
            raise ValueError("canonical public Lie bracket coordinates required")
        reduced, rank = fmpz_mod_mat(rows, fmpz_mod_ctx(p)).rref()
        current = [tuple(int(reduced[i, j]) for j in range(d)) for i in range(rank)]
        dimensions.append(rank)
        if not rank:
            return {"lower_central_dimensions": dimensions,
                    "class_check_bracket_evaluations": calls,
                    "lie_axioms_are_presentation_promises": True}
    raise ValueError("public lower central series exceeds the class bound")


@lru_cache(maxsize=128)
def _right_field_coefficients(p, class_bound):
    # B_r(1) fixes the +1/2 right-multiplication convention explicitly.
    coefficients = []
    for r in range(class_bound):
        value = sp.bernoulli(r, 1)/sp.factorial(r)
        coefficients.append(int(value.p)*pow(int(value.q), -1, p) % p)
    while len(coefficients) > 1 and not coefficients[-1]:
        coefficients.pop()
    return tuple(coefficients)


def _right_field(group, point, direction, coefficients):
    result, nested = group.scale(0, direction), direction
    for r, coefficient in enumerate(coefficients):
        if r:
            nested = group.bracket(point, nested)
        if coefficient:
            result = group.add(result, group.scale(coefficient, nested))
    return tuple(result)


def bounded_class_right_translation_field(group, point, direction, *, class_bound):
    """d/dt BCH(point,t*direction)|0, under the supplied class<=c<p promise.

    The sampled solver checks the class once. This low-level operation
    trusts it, so callers using it directly must establish the promise.
    """
    ring(group.p)
    if type(class_bound) is not int or not 1 <= class_bound < group.p:
        raise ValueError("positive nilpotency class bound strictly below p required")
    return _right_field(group, point, direction,
                        _right_field_coefficients(group.p, class_bound))


def derivative_weights(p, degree):
    """Derivative at zero from values at 0,...,e; all arithmetic is exact."""
    if type(degree) is not int or not 0 <= degree < p:
        raise ValueError("interpolation degree must be smaller than p")
    weights = [-sum(pow(i, -1, p) for i in range(1, degree+1)) % p]
    weights.extend(((-1)**(i+1) * comb(degree, i) * pow(i, -1, p)) % p
                   for i in range(1, degree+1))
    return tuple(weights)


def right_translation_field(group, point, direction):
    """d/dt BCH(point,t*direction) at t=0, NOT the left-action field."""
    inner = group.bracket(point, direction)
    return group.add(direction, group.scale(pow(2, -1, group.p), inner),
                     group.scale(pow(12, -1, group.p), group.bracket(point, inner)))


def sampled_stabilizer(group, evaluator, degree_bound, failure=Fraction(1, 4096), seed=None,
                       *, class_bound=3):
    """Recover the global right stabilizer with a one-sided rank-error bound.

    Output always contains the true stabilizer under the promises. It can
    be too large with probability <= failure under independent uniform
    sampling. A fixed seed is only a reproducibility control, not that
    randomized guarantee. Repeated chosen queries are all charged. The
    public bracket must satisfy the Lie axioms; its class is checked.
    Pass class_bound explicitly beyond the historical class-three model.
    """
    bounds = stabilizer_degree_bounds(group.p, degree_bound, class_bound)
    if not isinstance(failure, Fraction) or not 0 < failure < 1:
        raise ValueError("failure must be an exact Fraction strictly between zero and one")
    profile = _nilpotency_profile(group, class_bound)
    p, d = group.p, group.dimension
    field_coefficients = _right_field_coefficients(p, class_bound)
    ratio = (d*failure.denominator + failure.numerator-1)//failure.numerator
    block_length = max(1, (ratio-1).bit_length())
    point_count = d*block_length
    weights = derivative_weights(p, degree_bound)
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    queries, output_width = 0, None
    basis = [tuple(int(i == j) for j in range(d)) for i in range(d)]
    rows = []

    def query(point):
        nonlocal queries, output_width
        values = evaluator(tuple(point))
        queries += 1
        if not isinstance(values, (tuple, list)) or not values:
            raise ValueError("evaluator must expose a nonempty vector of field elements, not opaque labels")
        if any(type(value) is not int or not 0 <= value < p for value in values):
            raise ValueError("canonical field-valued outputs required")
        if output_width is None:
            output_width = len(values)
        if len(values) != output_width:
            raise ValueError("evaluator output dimension changed")
        return values

    for _ in range(point_count):
        point = tuple(rng.randrange(p) for _ in range(d))
        base = query(point)
        gradients = [[0]*d for _ in base]
        for j in range(d):
            samples = [base]
            for t in range(1, degree_bound+1):
                shifted = list(point)
                shifted[j] = (shifted[j]+t) % p
                samples.append(query(shifted))
            for component in range(len(base)):
                gradients[component][j] = sum(
                    weight*sample[component] for weight, sample in zip(weights, samples)) % p
        fields = [_right_field(group, point, e, field_coefficients) for e in basis]
        rows.extend(tuple(sum(a*b for a, b in zip(gradient, field)) % p for field in fields)
                    for gradient in gradients)
    solution = affine_solution(p, rows, [0]*len(rows), d)
    return {
        **bounds, **profile,
        "basis": solution["basis"], "rank": d-len(solution["basis"]),
        "chosen_evaluator_queries": queries, "random_points": point_count,
        "queries_per_point": 1+d*degree_bound,
        "degree_bound": degree_bound, "output_width": output_width,
        "ideal_uniform_sampling_failure_bound": str(failure),
        "fixed_seed_reproducibility_control": seed is not None,
        "bound_not_a_certificate_for_fixed_seed": seed is not None,
        "false_negative_probability_under_promises": "0",
        "exact_instance_certificate": False,
        "coefficients_or_hidden_generator_read": False,
        "right_field_nonzero_ad_powers": [r for r, a in enumerate(field_coefficients) if a],
        "field_bracket_evaluations_per_point": d*(len(field_coefficients)-1),
    }


def bracket_expressions(group, left, right):
    return [sp.expand(sum((left[i]*right[j]-left[j]*right[i])*value[k]
                          for (i, j), value in group.brackets.items()))
            for k in range(group.dimension)]


def bch_expressions(group, left, right):
    inner = bracket_expressions(group, left, right)
    twice_left = bracket_expressions(group, left, inner)
    twice_right = bracket_expressions(group, right, inner)
    return [sp.expand(a+b+pow(2, -1, group.p)*c
                      +pow(12, -1, group.p)*(u-v))
            for a, b, c, u, v in zip(left, right, inner, twice_left, twice_right)]


def coefficient_stabilizer(group, expressions, variables, *, action="right"):
    """Exact dense-coefficient reference; the sampled attack never calls this."""
    if len(variables) != group.dimension or action not in {"right", "left"}:
        raise ValueError("matching coordinates and right/left action required")
    polynomials = [sp.Poly(f, *variables, modulus=group.p) for f in expressions]
    if not polynomials:
        raise ValueError("nonempty polynomial vector required")
    degree = max(int(f.total_degree()) if not f.is_zero else 0 for f in polynomials)
    _guard(group, degree)
    fields = []
    for j in range(group.dimension):
        e = [int(i == j) for i in range(group.dimension)]
        inner = bracket_expressions(group, variables, e)
        nested = bracket_expressions(group, variables, inner)
        sign = 1 if action == "right" else -1
        fields.append([a+sign*pow(2, -1, group.p)*b+pow(12, -1, group.p)*c
                       for a, b, c in zip(e, inner, nested)])
    rows = []
    for polynomial in polynomials:
        gradient = [sp.diff(polynomial.as_expr(), x) for x in variables]
        columns = [sp.Poly(sum(a*b for a, b in zip(gradient, field)),
                           *variables, modulus=group.p).as_dict() for field in fields]
        monomials = sorted(set().union(*columns))
        rows.extend(tuple(int(column.get(alpha, 0)) % group.p for column in columns)
                    for alpha in monomials)
    solution = affine_solution(group.p, rows, [0]*len(rows), group.dimension)
    return {"basis": solution["basis"], "rank": group.dimension-len(solution["basis"]),
            "coefficient_rows": len(rows), "degree": degree,
            "exact_under_degree_and_characteristic_promises": True}


def cross_section_fixture(group, hidden_log):
    """Negative-control fixture only: labels of gH cosets under right action."""
    if len(hidden_log) != group.dimension or hidden_log[0] != 1:
        raise ValueError("fixture normalizes its generator's first quotient coordinate to one")
    variables = sp.symbols(f"z0:{group.dimension}")
    tau = variables[0]
    representative = bch_expressions(group, variables, [-tau*x for x in hidden_log])
    polynomials = [sp.Poly(f, *variables, modulus=group.p).as_expr()
                   for f in representative[1:]]
    return variables, polynomials


def field_evaluator(variables, polynomials, p):
    evaluate = sp.lambdify(variables, tuple(polynomials), modules="math")
    return lambda point: tuple(int(x) % p for x in evaluate(*point))


def controls():
    group = free_two_step_three(11)
    hidden = (1, 2, 3, 4, 5)
    variables, polynomials = cross_section_fixture(group, hidden)
    evaluator = field_evaluator(variables, polynomials, group.p)
    exact = coefficient_stabilizer(group, polynomials, variables)
    sampled = sampled_stabilizer(group, evaluator, exact["degree"], seed=20261025)
    wrong_action = coefficient_stabilizer(group, polynomials, variables, action="left")
    expected = tuple(group.scale(pow(hidden[-1], -1, group.p), hidden))
    if exact["basis"] != [list(expected)] or sampled["basis"] != exact["basis"]:
        raise ArithmeticError("classical attack failed to recover the known fixture subgroup")
    if wrong_action["basis"]:
        raise ArithmeticError("wrong-side control unexpectedly retained a global stabilizer")
    rng = random.Random(761)
    for _ in range(64):
        z = tuple(rng.randrange(11) for _ in hidden)
        for t in range(11):
            if evaluator(group.bch(z, group.scale(t, hidden))) != evaluator(z):
                raise ArithmeticError("fixture does not label true gH cosets")
    return {
        "id": "NIL3-POLYNOMIAL-VALUED-HIDING-CLASSICAL-ATTACK",
        "status": "scoped-classical-recovery-not-general-hsp-dequantization",
        "p": group.p, "dimension": group.dimension, "fixture_hidden_generator": list(hidden),
        "coefficient_reference": exact, "value_only_attack": sampled,
        "actual_orbit_checks": 64*11, "wrong_left_action_rank": wrong_action["rank"],
        "source_phase_polynomial_alone_does_not_enable_attack": True,
        "opaque_label_attack_claimed": False,
        "small_characteristic_attack_claimed": False,
        "classical_polynomial_time_under_stated_promises": True,
        "promises": [
            "Hiding outputs are canonical Fp vectors, not opaque names or an unknown hash.",
            "A trusted total-degree bound e in public Lie coordinates, with p>2(e+1).",
            "Explicit class<=3 Lie presentation and chosen classical evaluator access.",
            "For recovering H itself, the evaluator really separates gH cosets (right action).",
        ],
        "research_decision": (
            "Reject polynomial-valued explicit hiding functions in this characteristic regime "
            "as evidence of a new quantum speedup. Preserve the arbitrary-label HSP candidate."
        ),
        "novelty_claimed_for_derivative_method": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = controls()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        REPORT.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
