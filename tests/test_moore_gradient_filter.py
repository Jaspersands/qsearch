"""Public-circuit classical falsifiers, not generated oracle benchmarks."""
from fractions import Fraction
from itertools import combinations, product
import random

from flint import fq_default_ctx
import pytest

import theorems.moore_gradient_filter as module
from theorems.frobenius_circuit_lift import lift_frobenius_circuit
from theorems.moore_gradient_filter import CircuitBuilder, moore_circuit, recognize_moore_form
from theorems.polynomial_orbit_module import MooreMinor, discover_orbit_module
from theorems.ut5_matrix_phase_alignment import _basis, _identity, _lists, _matrix


def unit_rows(dimension, indices):
    return tuple(tuple(int(i == j) for j in range(dimension)) for i in indices)


@pytest.mark.parametrize("p,n", [(5, 1), (5, 3), (5, 6), (7, 4)])
def test_division_free_determinant_matches_independent_flint_even_above_characteristic(p, n):
    builder = CircuitBuilder(p)
    matrix = [[builder.node(("var", i*n+j)) for j in range(n)] for i in range(n)]
    output = builder.determinant(matrix)
    circuit = lift_frobenius_circuit(p, n*n, builder.nodes, output)
    field = fq_default_ctx(p, 1)
    rng = random.Random(13)
    for trial in range(6):
        values = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
        if trial == 0 and n > 1:
            values[1] = values[0][:]  # No inverse on a singular evaluation.
        value, gradient = circuit.value_and_gradient([field(a) for row in values for a in row], field)
        assert value == field(int(_matrix(values, p).det()))
        for i, j in product(range(n), repeat=2):
            minor = [[values[r][s] for s in range(n) if s != j] for r in range(n) if r != i]
            determinant = int(_matrix(minor, p).det()) if minor else 1
            assert gradient[i*n+j] == field((-1)**(i+j)*determinant)


def test_unknown_dense_rows_and_scalar_are_recognized_without_template_advice():
    p, dimension = 7, 5
    rows = ((1, 2, 3, 0, 1), (0, 1, 1, 2, 0), (2, 0, 1, 1, 3))
    nodes, output = moore_circuit(p, dimension, rows, scalar=3)
    result = recognize_moore_form(p, dimension, nodes, output, seed=29)
    assert result.accepted and result.rows == tuple(map(tuple, _basis(rows, p)))
    # Independent exterior-coordinate identity for every 3-subset, including scalar.
    for cols in combinations(range(dimension), len(rows)):
        old_minor = int(_matrix([[row[j] for j in cols] for row in rows], p).det())
        new_minor = int(_matrix([[row[j] for j in cols] for row in result.rows], p).det())
        assert (3*old_minor-result.scalar*new_minor) % p == 0
    assert result.error_bound <= Fraction(1, 100)
    assert result.randomness == "seeded_diagnostic"
    assert result.identity_tests == 1


def test_rank_at_characteristic_is_allowed_without_no_carry_guard():
    rows = unit_rows(6, range(5))
    nodes, output = moore_circuit(5, 6, rows)
    result = recognize_moore_form(5, 6, nodes, output, seed=29)
    assert result.accepted and result.rows == rows
    assert result.formal_degree_bound >= 781


def test_127_bit_prime_uses_binary_power_circuit_and_base_field_rows():
    p = 2**127-1
    rows = ((1, 2, 3, 4), (2, 3, 5, 7))
    nodes, output = moore_circuit(p, 4, rows)
    result = recognize_moore_form(p, 4, nodes, output, seed=29)
    assert result.accepted and result.rows == tuple(map(tuple, _basis(rows, p)))
    assert all(node[0] in ("var", "const", "add", "mul") for node in nodes)
    assert len(nodes) < 700 and result.extension_degree < 10
    assert len(result.rows) == 2  # Not the rank of a single vector over E.


def test_every_ut3_stabilizer_decision_matches_formal_exterior_coordinates():
    p = 5
    nodes, output = moore_circuit(p, 3, unit_rows(3, (0, 1)))
    result = recognize_moore_form(p, 3, nodes, output, seed=29)
    polynomial = MooreMinor(p, 3, (0, 1))
    target = polynomial.exterior_coefficients(_identity(3))
    count = 0
    for a, b, c in product(range(p), repeat=3):
        g = ((1, a, c), (0, 1, b), (0, 0, 1))
        decision = result.matrix_fixes_polynomial(g)
        assert decision == (polynomial.exterior_coefficients(g) == target) == (b == c == 0)
        count += decision
    assert count == p


def test_non_p_group_must_retain_determinant_character():
    nodes, output = moore_circuit(5, 3, unit_rows(3, (0, 1)))
    result = recognize_moore_form(5, 3, nodes, output, seed=29)
    assert not result.matrix_fixes_polynomial(((2, 0, 0), (0, 1, 0), (0, 0, 1)))
    assert result.matrix_fixes_polynomial(((2, 0, 0), (0, 3, 0), (0, 0, 1)))
    with pytest.raises(ValueError, match="invertible"):
        result.matrix_fixes_polynomial(((0, 0, 0), (0, 1, 0), (0, 0, 1)))


def test_elementary_log_subspace_route_matches_every_ut3_matrix():
    p = 5
    rows = unit_rows(3, (0, 1))
    nodes, output = moore_circuit(p, 3, rows)
    result = recognize_moore_form(p, 3, nodes, output, seed=29)
    identity = _matrix(_identity(3), p)
    for a, b, c in product(range(p), repeat=3):
        g = _matrix(((1, a, c), (0, 1, b), (0, 0, 1)), p)
        x = g-identity
        logarithm = x-pow(2, -1, p)*(x*x)
        # W*A annihilates the third basis column iff W*A is contained in W.
        linear_condition = all(int(logarithm[i, 2]) == 0 for i in (0, 1))
        assert linear_condition == result.matrix_fixes_polynomial(_lists(g))
        assert identity+logarithm+pow(2, -1, p)*(logarithm*logarithm) == g


def test_order_p_and_abelian_class_do_not_make_individual_matrix_logs_additive():
    p, dimension = 5, 25
    identity = _matrix(_identity(dimension), p)
    x, y = [[0]*dimension for _ in range(dimension)], [[0]*dimension for _ in range(dimension)]
    for i, j in product(range(p), repeat=2):
        if i+1 < p:
            x[i*p+j][(i+1)*p+j] = 1
        if j+1 < p:
            y[i*p+j][i*p+j+1] = 1
    x, y = _matrix(x, p), _matrix(y, p)
    g, h = identity+x, identity+y
    assert g*h == h*g and g**p == h**p == (g*h)**p == identity
    assert x**(p-1)*y**(p-1) != identity-identity  # J^(2p-2) != 0.

    def individual_log(matrix):
        delta = matrix-identity
        value, power = identity-identity, identity
        for exponent in range(1, p):
            power = power*delta
            value += ((-1)**(exponent+1)*pow(exponent, -1, p))*power
        return value

    assert individual_log(g*h) != individual_log(g)+individual_log(h)


def test_exponential_orbit_rank_can_still_be_recognized_classically():
    # Two UT3 blocks: the EXACT orbit span is 3**2, yet its row space has rank2.
    p, dimension = 5, 6
    rows = unit_rows(dimension, (0, 3))
    nodes, output = moore_circuit(p, dimension, rows)
    circuit = lift_frobenius_circuit(p, dimension, nodes, output)
    evaluator = lambda point, field: circuit.value_and_gradient(point, field)[0]
    generators = []
    for start in (0, 3):
        for i in (start, start+1):
            g = _identity(dimension)
            g[i][i+1] = 1
            generators.append(g)
    capped = discover_orbit_module(p, dimension, evaluator, circuit.degree_bound,
                                   generators, 4, seed=29)
    assert capped.status == "RANK_CAP_EXCEEDED" and capped.rank == 5
    full = discover_orbit_module(p, dimension, evaluator, circuit.degree_bound,
                                 generators, 9, seed=29)
    assert full.closed and full.rank == 9
    assert MooreMinor(p, dimension, (0, 3)).verify_representation(full)
    result = recognize_moore_form(p, dimension, nodes, output, seed=29)
    assert result.accepted and result.rows == rows


def test_derivative_invisible_perturbation_is_checked_at_a_fresh_point(monkeypatch):
    # x0+x1**5 has the same gradient as x0, but a different finite symmetry.
    builder = CircuitBuilder(5)
    x, y = builder.node(("var", 0)), builder.node(("var", 1))
    output = builder.add(x, builder.power(y, 5))
    # n=2, bound=6, eps=.01 give extension degree5. The chosen anchor
    # conceals the perturbation; the independent final point reveals it.
    draws = iter([digit for point in [(0, 0), (0, 0), (1, 0), (1, 1)]
                  for value in point for digit in [value, 0, 0, 0, 0]])
    class ScriptedRandom:
        def randrange(self, p):
            return next(draws)
    monkeypatch.setattr(module.random, "Random", lambda seed: ScriptedRandom())
    result = recognize_moore_form(5, 2, builder.nodes, output, seed=29)
    assert result.rows == ((1, 0),)
    assert not result.accepted and result.status == "MOORE_IDENTITY_REJECTED"
    assert result.identity_tests == 1
    with pytest.raises(ValueError, match="no accepted"):
        result.matrix_fixes_polynomial(_identity(2))


def test_pth_power_without_gradient_and_zero_are_not_promoted():
    builder = CircuitBuilder(5)
    x = builder.node(("var", 0))
    output = builder.power(x, 5)
    result = recognize_moore_form(5, 1, builder.nodes, output, seed=29)
    assert not result.accepted and result.status == "NO_NONZERO_GRADIENT"
    zero = recognize_moore_form(5, 1, [("const", 0)], seed=29)
    assert not zero.accepted  # No inference that this sampled gradient solves arbitrary F.


def test_randomness_failure_does_not_turn_recognition_into_a_certificate(monkeypatch):
    class AlwaysZero:
        def randrange(self, p):
            return 0
    monkeypatch.setattr(module.random, "Random", lambda seed: AlwaysZero())
    nodes, output = moore_circuit(5, 3, unit_rows(3, (0, 1)))
    result = recognize_moore_form(5, 3, nodes, output, seed=29)
    assert not result.accepted and result.randomness == "seeded_diagnostic"


@pytest.mark.parametrize("kwargs", [{"error_budget": 0.1}, {"error_budget": Fraction(0)},
                                      {"seed": True}])
def test_invalid_contracts_fail_closed(kwargs):
    with pytest.raises(ValueError):
        recognize_moore_form(5, 1, [("var", 0)], **kwargs)


def test_frobenius_annotations_are_not_silently_treated_as_ordinary_derivatives():
    with pytest.raises(ValueError, match="ordinary"):
        recognize_moore_form(5, 1, [("var", 0), ("frob", 0)])
    with pytest.raises(ValueError, match="prime"):
        recognize_moore_form(6, 1, [("var", 0)])


def test_report_has_no_discovery_or_executed_group_solver_claim():
    result = module.report()
    assert all(example["recovered_correct_space"] for example in result["examples"])
    assert all(Fraction(example["ideal_random_error_bound"]) < Fraction(1, 100)
               for example in result["examples"])
    assert result["scalable_family"]["live_example_orbit_rank"] == 100000
    for flag in ("stabilizer_solver_executed", "formal_proof_verified", "independently_reviewed",
                 "novel_algorithm_claimed", "quantum_advantage_claimed", "quantum_copies_only_covered"):
        assert result[flag] is False
