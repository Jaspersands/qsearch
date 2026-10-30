"""Algebra and finite controls only; passing does not prove an asymptotic gap."""

import math
from dataclasses import replace
from decimal import Decimal, localcontext

import numpy as np
import pytest
from scipy.linalg import eigh, expm

from parent_gap import (build_model, commutator, control_graphs, one_excitation_prediction,
                        parents, rotated_parent, second_order,
                        second_order_from_commutators, star_log2_raw_norm, star_pair_log2_gap)


@pytest.mark.parametrize("name", list(control_graphs()))
def test_canonical_relations_and_preconditioner(name):
    model = control_graphs()[name]
    identity = np.eye(1 << model.m)
    for i, oi in enumerate(model.operators):
        assert np.array_equal(oi @ oi, identity)
        assert np.array_equal(oi, oi.T)
        for j in range(i):
            sign = -1 if (j, i) in model.edges else 1
            assert np.array_equal(oi @ model.operators[j], sign * model.operators[j] @ oi)
    assert np.array_equal(model.k.T, -model.k)
    assert np.array_equal(commutator(model.k, model.number), -model.h)


@pytest.mark.parametrize("name", list(control_graphs()))
@pytest.mark.parametrize("flattened", [False, True])
def test_exact_second_order_and_form_bound(name, flattened):
    model = control_graphs()[name]
    coefficient = second_order(model, flattened)
    assert np.array_equal(coefficient, second_order_from_commutators(model, flattened))
    assert np.array_equal(coefficient.T, coefficient)
    assert np.array_equal(commutator(coefficient, model.number), np.zeros_like(coefficient))
    slots = [1 << i for i in range(model.m)]
    assert np.array_equal(coefficient[np.ix_(slots, slots)], one_excitation_prediction(model, flattened))
    constant = model.degree if flattened else max(0, model.degree - 1)
    assert eigh(coefficient + constant * model.number, eigvals_only=True)[0] >= -1e-12


@pytest.mark.parametrize("name", ["edge", "cycle4", "K3,3", "weighted-path"])
def test_parents_kernel_projectors_and_parity(name):
    model = control_graphs()[name]
    beta = .31
    data = parents(model, beta)
    parity = np.diag([(-1) ** y.bit_count() for y in range(1 << model.m)])
    assert np.array_equal(parity @ model.h @ parity, -model.h)
    assert np.array_equal(parity @ model.k @ parity, -model.k)
    for qi, raw, flat in zip(data["q"], data["raw_terms"], data["flat_terms"]):
        assert np.allclose(qi @ qi, qi, atol=2e-12)
        assert np.linalg.norm(qi @ data["pilot"]) < 2e-12
        assert np.allclose(flat @ flat, flat, atol=2e-12)
        assert np.allclose(raw @ flat, raw, atol=2e-12)
        assert eigh(raw - flat, eigvals_only=True)[0] >= -2e-12
        assert np.linalg.norm(flat @ data["pilot"]) < 2e-12
        assert np.isclose(np.trace(flat), 1 << (model.m - 1))
    for parent in (data["raw"], data["flat"]):
        eigenvalues = eigh(parent, eigvals_only=True)
        assert abs(eigenvalues[0]) < 2e-12
        assert eigenvalues[1] > .1
    for left in data["q"]:
        for right in data["q"]:
            assert np.allclose(commutator(left, right), 0, atol=2e-12)


@pytest.mark.parametrize("flattened", [False, True])
def test_second_order_against_independent_exponentials_and_qr(flattened):
    model = control_graphs()["weighted-path"]
    errors = []
    for beta in (.02, .01, .005):
        estimate = (rotated_parent(model, beta, flattened) - model.number) / beta**2
        errors.append(np.linalg.norm(estimate - second_order(model, flattened), ord=2))
    # The full operator has cubic terms; convergence here is only first order.
    assert errors[1] < .55 * errors[0]
    assert errors[2] < .55 * errors[1]
    assert errors[-1] < .003


@pytest.mark.parametrize("degree", [1, 2, 3, 5])
def test_star_raw_norm_formula(degree):
    model = build_model(degree + 1, [(0, j) for j in range(1, degree + 1)])
    for beta in (.03, .4, 1):
        actual = eigh(parents(model, beta)["raw_terms"][0], eigvals_only=True)[-1]
        assert np.isclose(math.log2(actual), star_log2_raw_norm(degree, beta), atol=2e-11)


def test_scalable_star_obstruction_and_zero_limits():
    assert star_log2_raw_norm(100, 0) == 0
    assert np.isclose(star_log2_raw_norm(0, .5), 2 * math.log2(math.cosh(.5)))
    d = 100000000
    assert star_log2_raw_norm(d, .1 / math.sqrt(d)) > 2800
    assert star_log2_raw_norm(3, 1e-10) >= 0


@pytest.mark.parametrize("degree", [1, 2, 3, 5, 10, 30])
def test_star_pair_angle_against_independent_dense_projectors(degree):
    pair = build_model(2, [(0, 1)])
    # A restriction of the full star onto other leaves' X=+1 eigenspaces.
    restricted = replace(pair, h=pair.h + (degree - 1) * pair.z[0])
    for c in (.1, .5, 1):
        beta = c / math.sqrt(degree)
        actual = eigh(parents(restricted, beta)["flat"], eigvals_only=True)[1]
        assert np.isclose(math.log2(actual), star_pair_log2_gap(degree, beta), atol=2e-8)


def test_pair_formula_is_actual_invariant_block_of_full_parent_terms():
    degree = 4
    model = build_model(degree + 1, [(0, j) for j in range(1, degree + 1)])
    data = parents(model, .3)
    # Isometry fixes qubits 2..d in |+>, keeping hub and leaf 1 free.
    basis = np.zeros((1 << (degree + 1), 4))
    for y in range(basis.shape[0]):
        basis[y, y & 3] = 2 ** (-(degree - 1) / 2)
    pair = data["flat_terms"][0] + data["flat_terms"][1]
    block = basis.T @ pair @ basis
    assert np.allclose(pair @ basis, basis @ block, atol=2e-12)
    ev = eigh(block, eigvals_only=True)
    assert abs(ev[0]) < 1e-12
    assert np.isclose(ev[-1], 2)
    assert np.isclose(math.log2(ev[1]), star_pair_log2_gap(degree, .3), atol=1e-10)


def test_pair_gap_obstruction_does_not_claim_full_parent_gap():
    assert star_pair_log2_gap(10, 0) == 0
    assert star_pair_log2_gap(100000000, .00001) < -2700
    # A separate exact two-term edge formula controls the a=0 boundary.
    beta = .7
    expected = 2 / (2 + math.sinh(beta * math.sqrt(2))**2)
    assert np.isclose(2 ** star_pair_log2_gap(1, beta), expected)
    with pytest.raises(ValueError):
        star_pair_log2_gap(0, .1)


def test_large_star_pair_log_against_high_precision_direct_formula():
    with localcontext() as ctx:
        ctx.prec = 100
        one, two = Decimal(1), Decimal(2)
        for degree in (100, 10000, 100000000):
            a = Decimal(degree - 1)
            beta = Decimal("0.1") / Decimal(degree).sqrt()
            rp, rm = (1 + (a + 1)**2).sqrt(), (1 + (a - 1)**2).sqrt()
            ep, em = (beta * rp).exp(), (beta * rm).exp()
            cp, cm = (ep + 1 / ep) / 2, (em + 1 / em) / 2
            sp, sm = (ep - 1 / ep) / 2, (em - 1 / em) / 2
            vp, vm = cp - (a + 1) / rp * sp, cm - (a - 1) / rm * sm
            determinant = two + two * (cp * cm - a * a / (rp * rm) * sp * sm)
            sin_squared = (vp + vm)**2 / (vp * vm * determinant)
            gap = sin_squared / (one + (one - sin_squared).sqrt())
            expected_log = float(gap.ln() / two.ln())
            assert np.isclose(star_pair_log2_gap(degree, float(beta)), expected_log,
                              atol=2e-10, rtol=0)


def test_rotated_ground_is_not_vacuum_at_all_orders():
    model = build_model(2, [])
    beta = .5
    data = parents(model, beta)
    rotation = expm(beta * model.k / 2)
    ground = rotation @ data["pilot"]
    rotated = rotation @ data["flat"] @ rotation.T
    assert abs(ground @ rotated @ ground) < 1e-12
    assert ground @ model.number @ ground > 1e-5
    # Even on a commuting graph, rotated F >= c N is false for every c>0.
    assert ground @ (rotated - .5 * model.number) @ ground < -1e-6


def test_canonical_order_change_is_a_public_signed_permutation():
    model = build_model(4, [(0, 1), (0, 3), (1, 2)], [1, -.5, .25, -.75])
    permutation = [2, 0, 3, 1]  # old vertex -> new vertex
    couplings = [0.0] * model.m
    for i, j in enumerate(model.couplings):
        couplings[permutation[i]] = j
    reordered = build_model(model.m, [(permutation[i], permutation[j]) for i, j in model.edges], couplings)
    unitary = np.zeros_like(model.h)
    for y in range(1 << model.m):
        new_label = sum(((y >> i) & 1) << permutation[i] for i in range(model.m))
        inversions = sum((y >> i & 1) * (y >> j & 1)
                         for i, j in model.edges if permutation[i] > permutation[j])
        unitary[new_label, y] = (-1) ** inversions
    assert np.array_equal(unitary @ model.h @ unitary.T, reordered.h)
    left, right = parents(model, .3), parents(reordered, .3)
    for kind in ("raw", "flat"):
        assert np.allclose(unitary @ left[kind] @ unitary.T, right[kind], atol=2e-12)


@pytest.mark.parametrize("flattened", [False, True])
def test_regular_bipartite_leading_gap(flattened):
    model = control_graphs()["K3,3"]
    coefficient = -model.degree + (0 if flattened else 1)
    assert np.isclose(eigh(one_excitation_prediction(model, flattened), eigvals_only=True)[0], coefficient)
    errors = []
    for beta in (.04, .02):
        ev = eigh(parents(model, beta)["flat" if flattened else "raw"], eigvals_only=True)
        errors.append(abs((ev[1] - 1) / beta**2 - coefficient))
    assert errors[1] < .3 * errors[0]  # fixed-graph even spectrum; no uniform remainder claim


def test_commuting_flat_gap_is_one_and_raw_gap_is_cosh_squared():
    model = build_model(3, [], [1, -.5, .25])
    beta = .8
    data = parents(model, beta)
    assert np.isclose(eigh(data["flat"], eigvals_only=True)[1], 1)
    assert np.isclose(eigh(data["raw"], eigvals_only=True)[1], math.cosh(beta / 4)**2)


def test_pilot_coefficients_match_normalized_trace_expansion():
    model = build_model(4, [(0, 1), (1, 2), (0, 3), (2, 3)])
    beta = .5
    data = parents(model, beta)
    coefficients = []
    for label in range(1 << model.m):
        word = np.eye(1 << model.m)
        for i, oi in enumerate(model.operators):
            if label >> i & 1:
                word = word @ oi
        coefficients.append(np.trace(word.T @ data["s"]) / (1 << model.m))
    coefficients = np.array(coefficients)
    assert np.allclose(coefficients, data["s"][:, 0], atol=1e-12)
    partition = np.trace(expm(-beta * model.h)) / (1 << model.m)
    assert np.isclose(coefficients @ coefficients, partition)


@pytest.mark.parametrize("args", [(0, []), (9, []), (3, [(0, 0)]), (2, [(0, 2)]),
                                  (2, [(0, 1), (1, 0)]), (2, [], [1, 2]),
                                  (2, [], [1, float("nan")]), (2, [], [1])])
def test_invalid_dense_inputs(args):
    with pytest.raises(ValueError):
        build_model(*args)


def test_invalid_beta_and_degree():
    with pytest.raises(ValueError):
        parents(build_model(2, [(0, 1)]), -1)
    with pytest.raises(ValueError):
        star_log2_raw_norm(-1, .1)
    with pytest.raises(ValueError):
        star_log2_raw_norm(2, float("inf"))
    with pytest.raises(ValueError):
        parents(build_model(2, []), 100)
