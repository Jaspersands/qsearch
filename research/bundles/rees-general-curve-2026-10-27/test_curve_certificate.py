from fractions import Fraction

import numpy as np
import pytest
from flint import nmod_mat

from curve_certificate import (Span, WeightedTensor, alternating_witness, certificate,
                               determinant, orbit_basis, source_plan, theorem_constants,
                               word_jacobian)


@pytest.mark.parametrize("c,dimensions", [(1, [1]), (2, [1, 1]), (3, [1, 1, 2]),
    (4, [1, 1, 2, 3]), (5, [1, 1, 2, 3, 6]), (6, [1, 1, 2, 3, 6, 9])])
def test_weighted_free_dimensions_and_independent_minor(c, dimensions):
    record = certificate(c, 101)
    assert record["graded_dimensions"] == dimensions
    matrix = nmod_mat(record["derivative_minor_transpose"], 101)
    assert matrix.rank() == sum(dimensions)
    assert int(matrix.det()) == record["minor_determinant_mod_p"]
    assert not record["algorithmic_advantage_certified"]


@pytest.mark.parametrize("c,p", [(1, 2), (2, 3), (3, 5), (4, 5), (5, 7), (6, 7)])
def test_witness_survives_smallest_legal_characteristic(c, p):
    record = certificate(c, p)
    assert record["minor_determinant_mod_p"]
    assert not record["large_prime_gap_certified"]


@pytest.mark.parametrize("c,p", [(0, 7), (True, 7), (4, 4), (5, 5), (3, 9), (3, 2)])
def test_rejects_illegal_characteristic(c, p):
    with pytest.raises(ValueError):
        WeightedTensor(c, p)


@pytest.mark.parametrize("c,p", [(3, 5), (4, 7), (5, 101)])
def test_right_tangent_matches_independent_exponential_derivative(c, p):
    a = WeightedTensor(c, p)
    for t in range(c + 1):
        dg = a.exp_derivative(a.a(t), a.a_prime(t))
        assert a.tangent(t) == a.mul(dg, a.gamma(t, -1))
        assert a.mul(a.gamma(t), a.gamma(t, -1)) == a.one


def test_nonnormal_operator_invalidates_naive_power_inference():
    t = np.array([[0., 1.], [0., 0.]])
    assert np.linalg.norm(t, 2) == 1
    assert np.linalg.norm(t @ t, 2) == 0
    assert np.linalg.norm((t.T @ t) @ (t.T @ t), 2) == 1


@pytest.mark.parametrize("c", [3, 4, 5, 6])
def test_unconjugated_tangents_do_not_span(c):
    a = WeightedTensor(c, 101)
    tangent_span = Span(a.p)
    for t in range(c):
        tangent_span.add(a.tangent(t))
    assert len(tangent_span) == c
    assert len(tangent_span) < sum(map(len, a.lie_basis().values()))
    chosen, growth, _ = orbit_basis(a)
    assert len(growth) >= 2
    assert len(chosen) > c


def test_padding_signs_and_removed_variable_negative_control():
    a = WeightedTensor(4, 101)
    chosen, _, _ = orbit_basis(a)
    word = alternating_witness(chosen)
    assert [x[0] for x in word] == [-1, 1] * (len(word) // 2)
    assert len(word) <= 2 * (2 * len(chosen)**2 + 1)
    broken = [(s, t, None if v == 0 else v) for s, t, v in word]
    value, derivatives = word_jacobian(a, broken, len(chosen))
    assert value == a.one
    span = Span(a.p)
    for v in derivatives:
        span.add(v)
    assert len(span) == len(chosen) - 1


def test_abelian_quotient_and_wrong_inverse_control():
    a = WeightedTensor(4, 101)
    chosen, _, _ = orbit_basis(a)
    _, derivatives = word_jacobian(a, alternating_witness(chosen), len(chosen))
    span = Span(a.p)
    for v in derivatives:
        span.add({w: x for w, x in v.items() if len(w) == 1})
    assert len(span) == 4
    assert a.gamma(-1) != a.gamma(1, -1)


@pytest.mark.parametrize("c", range(1, 9))
def test_rational_gap_lower_bound(c):
    constants = theorem_constants(c, 2**c - 1)
    m = constants["alternating_pairs"]
    # Bernoulli proves this for all m; exact finite diagnostics only.
    if m < 500:
        assert (1 - Fraction(1, 4*m))**(2*m) >= Fraction(1, 2)
    assert constants["minor_degree_bound"] == (2**c - 1) * (c - 1)


def test_source_plan_charges_copies_and_action_error_without_gate_claim():
    plan = source_plan(4, 15, 2**61 - 1, Fraction(1, 3), Fraction(1, 100), 10, 50, 120)
    assert plan["native_copies"] == plan["coherent_select_calls"]
    assert plan["native_copies"] == plan["packets_per_leaf"] * 1200
    assert Fraction(plan["per_select_half_diamond_error"]) * plan["coherent_select_calls"] == Fraction(1, 800)
    assert not plan["total_gate_bound_certified"]
    assert "native width q" in plan["uncharged_here"]


@pytest.mark.parametrize("change", [{"p": 101}, {"dimension": 7}, {"delta": 0},
    {"epsilon": 1}, {"leaves": 0}, {"address_bits": True}, {"packet_size": -1}])
def test_planner_rejects_unsupported_claims(change):
    kwargs = dict(c=4, dimension=15, p=2**61-1, delta=Fraction(1, 3),
                  epsilon=Fraction(1, 100), leaves=10, address_bits=50, packet_size=120)
    kwargs.update(change)
    with pytest.raises(ValueError):
        source_plan(**kwargs)


def test_determinant_singular_and_row_swap():
    assert determinant([[0, 1], [1, 0]], 101) == 100
    assert determinant([[1, 2], [2, 4]], 101) == 0


@pytest.mark.parametrize("d", [2, 3, 7, 31])
def test_population_twirl_control_keeps_dimension_obstruction(d):
    # The existing two-sector Choi falsifier, not a new generated candidate.
    weights = np.array([1 - 1/d, 1/d])
    psi = np.sqrt(weights)
    rho = np.outer(psi, psi)
    twirl = np.diag(weights)
    distance = np.linalg.norm(rho - twirl, ord="nuc") / 2
    assert np.isclose(distance**2, (d - 1) / d**2)
    assert np.isclose(1 - np.trace(rho @ twirl), 2 * (d - 1) / d**2)
    assert np.isclose(1 - max(weights), 1/d)


def test_adjacent_phases_have_constant_twirl_defect_but_vanishing_point_gap():
    twirl_defect = 1 - 2 * Fraction(1, 2)**2
    assert twirl_defect == Fraction(1, 2)
    gaps = [1 - abs((1 + np.exp(2j*np.pi/p)) / 2) for p in (101, 1009, 10007)]
    assert gaps[0] > gaps[1] > gaps[2] > 0


def test_independent_scales_inside_packet_destroy_exact_ray_cancellation():
    p = 7
    omega = np.exp(2j*np.pi/p)
    shared = sum(omega**((u-u) % p) for u in range(p)) / p
    independent = sum(omega**((u-v) % p) for u in range(p) for v in range(p)) / p**2
    assert np.isclose(shared, 1)
    assert abs(independent) < 1e-12


def test_weighted_quotient_requires_lower_central_coefficient_membership():
    a = WeightedTensor(2, 101)
    assert a.bracket({(1,): 1}, {(2,): 1}) == {}
    # Sending the weight-two generator outside gamma_2 fails already in UT_3.
    x = np.zeros((3, 3), dtype=int)
    y = np.zeros((3, 3), dtype=int)
    x[0, 1], y[1, 2] = 1, 1
    assert np.any(x @ y - y @ x)
