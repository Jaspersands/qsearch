"""Classical field-valued oracle attacks and strict access/characteristic limits."""
from fractions import Fraction
from math import factorial
import random

import pytest
import sympy as sp

from theorems.nil3_cocycle_receiver import free_two_step_three
from theorems.folded_rs_decoder import affine_solution
from theorems.nil3_polynomial_hiding_attack import (
    bch_expressions, coefficient_stabilizer, controls, cross_section_fixture,
    derivative_weights, field_evaluator, right_translation_field, sampled_stabilizer,
    bounded_class_right_translation_field, stabilizer_degree_bounds,
)


@pytest.mark.parametrize("degree", [0, 1, 2, 3, 4])
def test_exact_chosen_query_derivative_interpolation(degree):
    p = 11
    weights = derivative_weights(p, degree)
    for monomial_degree in range(degree+1):
        assert sum(weight*pow(t, monomial_degree, p)
                   for t, weight in enumerate(weights)) % p == int(monomial_degree == 1)


def test_infinitesimal_field_matches_direct_bch_polynomial():
    group = free_two_step_three(11)
    t = sp.Symbol("t")
    rng = random.Random(88)
    for _ in range(30):
        z, x = [tuple(rng.randrange(11) for _ in range(5)) for _ in range(2)]
        path = bch_expressions(group, z, [t*a for a in x])
        derivative = tuple(int(sp.diff(f, t).subs(t, 0)) % 11 for f in path)
        assert derivative == right_translation_field(group, z, x)


@pytest.mark.parametrize("hidden", [(1, 2, 3, 4, 5), (1, 0, 1, 0, 0), (1, 4, 2, 3, 1)])
def test_actual_nonsplit_cyclic_hiding_function_is_classically_recovered(hidden):
    group = free_two_step_three(11)
    variables, polynomials = cross_section_fixture(group, hidden)
    exact = coefficient_stabilizer(group, polynomials, variables)
    values = field_evaluator(variables, polynomials, 11)
    calls = 0

    def counted(point):
        nonlocal calls
        calls += 1
        return values(point)

    sampled = sampled_stabilizer(group, counted, exact["degree"], failure=Fraction(1, 128), seed=341)
    assert sampled["basis"] == exact["basis"]
    assert len(exact["basis"]) == 1
    recovered = exact["basis"][0]
    assert tuple(recovered) == group.scale(recovered[0], hidden)
    assert calls == sampled["chosen_evaluator_queries"]
    assert calls == sampled["random_points"]*(1+5*exact["degree"])
    assert not sampled["coefficients_or_hidden_generator_read"]
    assert not sampled["exact_instance_certificate"]


def test_trivial_and_large_stabilizers_are_not_forced_to_a_line():
    group = free_two_step_three(11)
    variables = sp.symbols("z0:5")
    for functions, expected_dimension in [(list(variables), 0), ([sp.Integer(4)], 5),
                                          ([variables[0], variables[1]], 3)]:
        exact = coefficient_stabilizer(group, functions, variables)
        sampled = sampled_stabilizer(group, field_evaluator(variables, functions, 11),
                                     exact["degree"], failure=Fraction(1, 32), seed=75)
        assert len(exact["basis"]) == expected_dimension
        assert sampled["basis"] == exact["basis"]


def test_frobenius_derivative_trap_is_rejected_not_called_full_stabilizer():
    group = free_two_step_three(5)
    variables = sp.symbols("z0:5")
    polynomial = variables[0]**5
    assert sp.Poly(sp.diff(polynomial, variables[0]), *variables, modulus=5).is_zero
    # Yet z0^5=z0 as a field-valued function, so the first direction is NOT a symmetry.
    assert (0**5) % 5 != (1**5) % 5
    with pytest.raises(ValueError, match="p>2"):
        coefficient_stabilizer(group, [polynomial], variables)
    with pytest.raises(ValueError, match="p>2"):
        sampled_stabilizer(group, lambda point: (point[0]**5 % 5,), 5)


def test_opaque_labels_are_not_silently_treated_as_field_polynomial_values():
    group = free_two_step_three(11)
    with pytest.raises(ValueError, match="opaque"):
        sampled_stabilizer(group, lambda point: "opaque-coset-name", 3)
    with pytest.raises(ValueError, match="canonical"):
        sampled_stabilizer(group, lambda point: (11,), 3)


def test_wrong_left_action_fails_for_nonnormal_right_action_cosets():
    group = free_two_step_three(11)
    variables, polynomials = cross_section_fixture(group, (1, 2, 3, 4, 5))
    assert len(coefficient_stabilizer(group, polynomials, variables)["basis"]) == 1
    assert coefficient_stabilizer(group, polynomials, variables, action="left")["basis"] == []


def test_live_negative_result_keeps_general_oracle_candidate_open():
    report = controls()
    assert report["value_only_attack"]["basis"] == report["coefficient_reference"]["basis"]
    assert report["value_only_attack"]["chosen_evaluator_queries"] == 1200
    assert not report["opaque_label_attack_claimed"]
    assert not report["small_characteristic_attack_claimed"]
    assert report["source_phase_polynomial_alone_does_not_enable_attack"]


class FiliformMatrixControl:
    """Test-only class-c algebra [X,Y_j]=Y_(j+1), with abelian Y ideal."""

    def __init__(self, p, c):
        self.p, self.c, self.dimension = p, c, c+1

    def add(self, *vectors):
        return tuple(sum(xs) % self.p for xs in zip(*vectors))

    def scale(self, scalar, vector):
        return tuple(scalar*x % self.p for x in vector)

    def bracket(self, a, b):
        return (0, 0) + tuple((a[0]*b[j]-b[0]*a[j]) % self.p
                              for j in range(1, self.c))

    def matrix(self, point):
        result = sp.zeros(self.c+1)
        for i in range(self.c-1):
            result[i, i+1] = point[0]
        for j, value in enumerate(point[1:]):
            result[self.c-1-j, self.c] = value
        return result

    def coordinates(self, matrix):
        return (int(matrix[0, 1]) % self.p,) + tuple(
            int(matrix[self.c-1-j, self.c]) % self.p for j in range(self.c))

    def mod(self, matrix):
        return matrix.applyfunc(lambda a: int(a) % self.p)

    def exp(self, matrix):
        result = power = sp.eye(self.c+1)
        for k in range(1, self.c+1):
            power = self.mod(power*matrix)
            result = self.mod(result+pow(factorial(k), -1, self.p)*power)
        return result

    def log(self, matrix):
        u = matrix-sp.eye(self.c+1)
        result, power = sp.zeros(self.c+1), sp.eye(self.c+1)
        for k in range(1, self.c+1):
            power = self.mod(power*u)
            result = self.mod(result+((-1)**(k+1)*pow(k, -1, self.p))*power)
        return result

    def matrix_right_derivative(self, point, direction):
        # Differentiate log(E exp(tX)) by the product rule for matrix powers,
        # independently of the Bernoulli/ad formula used by the attack.
        e = self.exp(self.matrix(point))
        u, du = e-sp.eye(self.c+1), self.mod(e*self.matrix(direction))
        powers = [sp.eye(self.c+1)]
        for _ in range(self.c):
            powers.append(self.mod(powers[-1]*u))
        result = sp.zeros(self.c+1)
        for k in range(1, self.c+1):
            derivative = sum((powers[i]*du*powers[k-1-i] for i in range(k)),
                             sp.zeros(self.c+1))
            result = self.mod(result+((-1)**(k+1)*pow(k, -1, self.p))*derivative)
        return self.coordinates(result)


def _filiform_cross_section(group, hidden):
    """Value-only negative control; the attack receives no matrix or hidden log."""
    assert hidden[0] == 1
    p = group.p
    inverse_factorials = [pow(factorial(k+1), -1, p) for k in range(group.c)]

    def evaluate(z):
        # exp(z)exp(-z0*hidden) has zero X coordinate. Its last column is
        # ((exp(z0*J)-I)/(z0*J)) * (z_Y-z0*hidden_Y), a polynomial, no division by z0.
        return tuple(sum(pow(z[0], k, p)*inverse_factorials[k]
                         *(z[1+j-k]-z[0]*hidden[1+j-k]) for k in range(j+1)) % p
                     for j in range(group.c))

    return evaluate


@pytest.mark.parametrize("c", [2, 3, 4, 5, 6, 7])
def test_bounded_class_bernoulli_field_matches_independent_matrix_log_derivative(c):
    group = FiliformMatrixControl(257, c)
    rng = random.Random(182+c)
    for _ in range(3):
        z, x = [tuple(rng.randrange(group.p) for _ in range(group.dimension))
                for _ in range(2)]
        assert group.mod(group.matrix(z)*group.matrix(x)-group.matrix(x)*group.matrix(z)) == (
            group.matrix(group.bracket(z, x)))
        assert bounded_class_right_translation_field(group, z, x, class_bound=c) == (
            group.matrix_right_derivative(z, x))


@pytest.mark.parametrize("c", [4, 5, 6])
def test_actual_matrix_orbit_path_obeys_the_even_degree_bound(c):
    group = FiliformMatrixControl(257, c)
    point, direction = (0, 1) + (0,)*(c-1), (1,) + (0,)*c
    values = [group.coordinates(group.log(group.mod(group.exp(group.matrix(point))
              *group.exp(group.matrix(group.scale(t, direction)))))) for t in range(c+1)]
    vandermonde = [[pow(t, k, group.p) for k in range(c+1)] for t in range(c+1)]
    degrees = []
    for j in range(group.dimension):
        coefficients = affine_solution(group.p, vandermonde, [v[j] for v in values], c+1)
        assert not coefficients["basis"]
        degrees.append(max((k for k, a in enumerate(coefficients["offset"]) if a), default=0))
    assert max(degrees) == stabilizer_degree_bounds(group.p, c, c)["path_degree_bound"]


@pytest.mark.parametrize("c,p", [(4, 11), (5, 23), (6, 29), (5, 2**127-1)])
def test_higher_class_cosets_are_recovered_from_charged_values_only(c, p):
    group = FiliformMatrixControl(p, c)
    hidden = tuple(range(1, c+2))
    evaluator = _filiform_cross_section(group, hidden)
    rng = random.Random(37)
    for _ in range(5):
        z = tuple(rng.randrange(p) for _ in hidden)
        representative = group.log(group.mod(group.exp(group.matrix(z))
            *group.exp(group.matrix(group.scale(-z[0], hidden)))))
        assert group.coordinates(representative) == (0,) + evaluator(z)
        t = rng.randrange(p)
        shifted = group.coordinates(group.log(group.mod(group.exp(group.matrix(z))
            *group.exp(group.matrix(group.scale(t, hidden))))))
        assert evaluator(shifted) == evaluator(z)
    calls = 0

    def counted(z):
        nonlocal calls
        calls += 1
        return evaluator(z)

    result = sampled_stabilizer(group, counted, c, failure=Fraction(1, 32),
                                seed=341, class_bound=c)
    assert result["basis"] == [list(group.scale(pow(hidden[-1], -1, p), hidden))]
    assert result["lower_central_dimensions"] == [c+1] + list(range(c-1, -1, -1))
    assert result["class_check_bracket_evaluations"] == (c+1)*sum(
        result["lower_central_dimensions"][:-1])
    assert calls == result["chosen_evaluator_queries"] == (
        result["random_points"]*(1+(c+1)*c))
    assert Fraction(result["deficient_rank_detection_probability_lower_bound"]) > Fraction(1, 2)
    assert not result["coefficients_or_hidden_generator_read"]
    assert not result["exact_instance_certificate"]
    assert result["right_field_nonzero_ad_powers"] == ([0, 1, 2] if c == 4 else [0, 1, 2, 4])


def test_first_missing_class_three_field_term_is_class_five_not_four():
    group = FiliformMatrixControl(23, 5)
    point = (1, 0, 0, 0, 0, 0)
    direction = (0, 1, 0, 0, 0, 0)
    old = right_translation_field(group, point, direction)
    assert bounded_class_right_translation_field(group, point, direction, class_bound=4) == old
    actual = group.matrix_right_derivative(point, direction)
    assert group.add(actual, group.scale(-1, old)) == (0, 0, 0, 0, 0, -pow(720, -1, 23) % 23)
    assert bounded_class_right_translation_field(group, point, direction, class_bound=5) == actual


def test_truncated_field_would_remove_a_true_class_five_stabilizer_direction():
    group = FiliformMatrixControl(23, 5)
    point, hidden = (1, 0, 0, 0, 0, 0), (1, 2, 3, 4, 5, 6)
    evaluator = _filiform_cross_section(group, hidden)
    weights = derivative_weights(23, 5)
    gradient = []
    for j in range(group.dimension):
        e = tuple(int(i == j) for i in range(group.dimension))
        gradient.append(sum(w*evaluator(group.add(point, group.scale(t, e)))[-1]
                            for t, w in enumerate(weights)) % 23)
    actual = bounded_class_right_translation_field(group, point, hidden, class_bound=5)
    old = right_translation_field(group, point, hidden)
    assert sum(a*b for a, b in zip(gradient, actual)) % 23 == 0
    assert sum(a*b for a, b in zip(gradient, old)) % 23 != 0


@pytest.mark.parametrize("c", [3, 4])
def test_understated_class_is_rejected_before_any_hiding_query(c):
    def forbidden(_):
        raise AssertionError("must reject the public class before querying F")

    with pytest.raises(ValueError, match="lower central series"):
        sampled_stabilizer(FiliformMatrixControl(101, 5), forbidden, 5, class_bound=c)


@pytest.mark.parametrize("p,e,c", [(19, 5, 5), (5, 0, 5), (25, 2, 3), (23, True, 5),
                                   (23, 2, True), (23, -1, 5), (23, 2, 0)])
def test_bounded_class_characteristic_and_integer_guards(p, e, c):
    with pytest.raises(ValueError):
        stabilizer_degree_bounds(p, e, c)


def test_bounded_class_degree_formula_retains_even_class_bernoulli_cancellation():
    assert [stabilizer_degree_bounds(257, 5, c)["path_degree_bound"]
            for c in range(1, 9)] == [1, 1, 2, 2, 4, 4, 6, 6]
    bounds = stabilizer_degree_bounds(23, 5, 5)
    assert bounds["derivative_degree_bound"] == 8
    assert bounds["strict_characteristic_threshold"] == 20
    assert stabilizer_degree_bounds(7, 0, 5)["derivative_degree_bound"] == 0
