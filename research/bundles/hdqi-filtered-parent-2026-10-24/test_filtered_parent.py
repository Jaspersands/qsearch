import math

import numpy as np
import pytest
from scipy.linalg import eigh, expm
from scipy.integrate import quad, quad_vec

from filtered_parent import (LCU_NORM, build_model, commutator, control_graphs,
                             discrete_parent_control, filtered_jump, filtered_parent,
                             graph_phase, one_excitation_prediction, parents,
                             quadrature_plan, sech, taylor_coefficients)


@pytest.mark.parametrize("name", ["edge", "cycle4", "weighted-path", "clique5", "commuting-weighted"])
def test_exact_integrated_parent_kernel_and_norm(name):
    model = control_graphs()[name]
    for beta in (0, .1, .6):
        parent, terms = filtered_parent(model, beta)
        pilot = parents(model, beta)["pilot"]
        ev = eigh(parent, eigvals_only=True)
        assert abs(ev[0]) < 1e-11
        assert ev[1] > 1e-3  # finite control only
        assert np.linalg.norm(parent @ pilot) < 1e-11
        for term in terms:
            tev = eigh(term, eigvals_only=True)
            assert tev[0] > -1e-11
            assert tev[-1] <= LCU_NORM**2 + 1e-11
        if beta == 0:
            assert np.allclose(parent, model.number, atol=1e-11)


@pytest.mark.parametrize("s", [-.7, 0, .2, 1.3])
def test_jump_matches_independent_operator_word_map(s):
    model = build_model(3, [(0, 1), (1, 2)])
    beta, size = .4, 1 << model.m
    energies, u = eigh(model.h)
    omega = energies[:, None] - energies[None, :]
    words = []
    for y in range(size):
        word = np.eye(size)
        for i, oi in enumerate(model.operators):
            if y >> i & 1:
                word = word @ oi
        words.append(word)
    pilot = parents(model, beta)["pilot"]
    for i, zi in enumerate(model.z):
        coefficients = (u.T @ zi @ u) * np.exp(-(beta*omega)**2/8 - beta*omega/4 + 1j*beta*s*omega)
        left = u @ coefficients @ u.T
        right = left.conj().T
        direct = np.zeros((size, size), dtype=complex)
        for y, word in enumerate(words):
            image = zi @ (left @ word - word @ right) / 2
            for z, test_word in enumerate(words):
                direct[z, y] = np.trace(test_word.T @ image) / size
        jump = filtered_jump(model, beta, i, s)
        assert np.allclose(jump, direct, atol=2e-12)
        assert np.linalg.norm(jump @ pilot) < 2e-12
        assert np.linalg.norm(jump, 2) <= LCU_NORM + 1e-12


def test_real_time_lcu_identity_without_imaginary_time_inverse():
    model = build_model(3, [(0, 1), (1, 2)])
    beta, s, i = .5, .3, 1
    nodes, weights = np.polynomial.hermite.hermgauss(48)
    phase = graph_phase(model)
    left = np.zeros_like(model.h, dtype=complex)
    for v, weight in zip(nodes / math.sqrt(2), weights / math.sqrt(math.pi)):
        unitary = expm(1j * beta * (v + s) * model.h)
        left += LCU_NORM * weight * np.exp(1j*v) * unitary @ model.z[i] @ unitary.conj().T
    jump = (model.z[i] @ left - phase @ left.conj() @ phase) / 2
    assert np.allclose(jump, filtered_jump(model, beta, i, s), atol=2e-12)


def test_sech_time_law_and_second_moment():
    density = lambda s: 2 * float(sech(2 * math.pi * s))
    assert np.isclose(quad(density, -10, 10)[0], 1, atol=1e-12)
    assert np.isclose(quad(lambda s: s*s*density(s), -10, 10)[0], 1/16, atol=1e-12)
    for omega in (0, .2, 3, 11):
        actual = quad(lambda s: math.cos(omega*s)*density(s), -10, 10, epsabs=1e-12)[0]
        assert np.isclose(actual, sech(omega/4), atol=2e-12)


def test_frequency_contraction_against_independent_time_integration():
    model = build_model(2, [(0, 1)], [1, -.5])
    beta = .4
    exact, _ = filtered_parent(model, beta)
    def integrand(s):
        total = np.zeros_like(exact, dtype=complex)
        for i in range(model.m):
            q = filtered_jump(model, beta, i, float(s))
            total += 2 * sech(2*math.pi*s) * (q.conj().T @ q)
        return total
    total, error = quad_vec(integrand, -6, 6, epsabs=1e-12, epsrel=1e-12)
    assert error < 1e-10
    assert np.allclose(total, exact, atol=3e-12, rtol=0)


@pytest.mark.parametrize("name", list(control_graphs()))
def test_dyadic_linear_cancellation_and_single_excitation_prediction(name):
    model = control_graphs()[name]
    first, coefficient, generator = taylor_coefficients(model)
    assert np.array_equal(first + commutator(generator, model.number), np.zeros_like(first))
    slots = [1 << i for i in range(model.m)]
    assert np.array_equal(coefficient[np.ix_(slots, slots)], one_excitation_prediction(model))
    assert np.array_equal(commutator(coefficient, model.number), np.zeros_like(coefficient))


def test_fixed_graph_second_order_against_exact_integral():
    model = control_graphs()["weighted-path"]
    _, coefficient, generator = taylor_coefficients(model)
    errors = []
    for beta in (.02, .01, .005):
        parent, _ = filtered_parent(model, beta)
        rotation = expm(beta * generator)
        errors.append(np.linalg.norm((rotation @ parent @ rotation.T - model.number) / beta**2 - coefficient, 2))
    assert errors[1] < .56 * errors[0]
    assert errors[2] < .56 * errors[1]
    assert errors[-1] < .005


def test_all_four_vertex_graphs_with_signed_couplings():
    possible_edges = [(i, j) for i in range(4) for j in range(i+1, 4)]
    for mask in range(1 << len(possible_edges)):
        edges = [edge for k, edge in enumerate(possible_edges) if mask >> k & 1]
        model = build_model(4, edges, [1, -.5, .25, 0])
        first, coefficient, generator = taylor_coefficients(model)
        assert np.array_equal(first + commutator(generator, model.number), np.zeros_like(first))
        slots = [1, 2, 4, 8]
        assert np.array_equal(coefficient[np.ix_(slots, slots)], one_excitation_prediction(model))


def test_commuting_exact_gap_and_missing_temperature_guard_counterexample():
    for coupling, beta in ((1, .3), (-.5, .7), (1, 4), (0, 10)):
        model = build_model(1, [], [coupling])
        parent, _ = filtered_parent(model, beta)
        expected = math.exp(-(beta*coupling)**2) * math.cosh(beta*coupling)
        assert np.isclose(eigh(parent, eigvals_only=True)[1], expected, atol=0, rtol=2e-13)
    assert math.exp(-100) * math.cosh(10) < 1e-39
    # At beta=10, eigensolver leakage of an exactly zero Bohr component can
    # dominate the true ~4e-40 gap. Use the exact two-frequency representation.
    a, b = math.exp(-50 - 5), math.exp(-50 + 5)
    ratio = a / b
    scaled_gram = np.array([[1, -ratio], [-ratio, ratio*ratio]]) / 2
    assert np.isclose(b*b * eigh(scaled_gram, eigvals_only=True)[1],
                      math.exp(-100) * math.cosh(10), atol=0, rtol=2e-13)
    tiny_reference, _ = filtered_parent(build_model(1, []), 10)
    assert eigh(tiny_reference, eigvals_only=True)[1] < 1e-11
    # d=0 makes beta^2*d=0 at every temperature, including this slow parent.
    # This is not hardness: the commuting pilot is an explicit product state.


def test_path_derivative_bounds_against_finite_differences():
    model = build_model(3, [(0, 1), (1, 2)], [1, -.5, .25])
    beta, step = .4, 1e-4
    plus, _ = filtered_parent(model, beta + step)
    center, _ = filtered_parent(model, beta)
    minus, _ = filtered_parent(model, beta - step)
    first = (plus - minus) / (2 * step)
    second = (plus - 2 * center + minus) / step**2
    lam = sum(abs(x) for x in model.couplings)
    assert np.linalg.norm(first, 2) <= math.sqrt(5) * model.m * LCU_NORM**2 * lam
    assert np.linalg.norm(second, 2) <= 5 * model.m * LCU_NORM**2 * lam**2


def test_priced_quadrature_error_and_ground_error_are_not_silently_zero():
    model = build_model(2, [(0, 1)])
    exact, _ = filtered_parent(model, .3)
    approximate, _, plan = discrete_parent_control(model, .3, .05)
    measured = np.linalg.norm(exact - approximate, 2)
    assert plan["total_analytic_error_bound"] <= .05 * (1 + 1e-12)
    assert 1e-12 < measured < plan["total_analytic_error_bound"]
    pilot = parents(model, .3)["pilot"]
    assert np.linalg.norm(approximate @ pilot) <= measured + 1e-12
    assert plan["circuit_executed"] is False
    assert "Hamiltonian simulation error" in plan["unbudgeted_errors"]


def test_resource_plan_uses_public_norm_sum_and_is_not_a_gap_certificate():
    model = build_model(8, [(i, i+1) for i in range(7)])
    plan = quadrature_plan(model, .2, 1e-4)
    assert plan["public_pauli_norm_sum"] == 8
    assert np.isclose(plan["parent_lcu_normalization_bound"], 8 * math.exp(.25))
    assert plan["total_analytic_error_bound"] <= 1.00001e-4
    assert plan["outer_bins"] > 100000
    assert plan["circuit_executed"] is False
    with pytest.raises(ValueError):
        discrete_parent_control(model, .2, 1e-4)
    with pytest.raises(ValueError):
        filtered_parent(model, .2)


@pytest.mark.parametrize("beta,delta", [(0, .1), (-1, .1), (.1, 0), (.1, 1), (.1, float("nan"))])
def test_invalid_quadrature_inputs(beta, delta):
    with pytest.raises(ValueError):
        quadrature_plan(build_model(2, []), beta, delta)


def test_zero_hamiltonian_retains_unique_vacuum_and_finite_cost_plan():
    model = build_model(3, [(0, 1)], [0, 0, 0])
    parent, _ = filtered_parent(model, 2)
    assert np.array_equal(parent, model.number)
    plan = quadrature_plan(model, .3, .1)
    assert plan["outer_bins"] == 1
    assert plan["total_analytic_error_bound"] <= .1
