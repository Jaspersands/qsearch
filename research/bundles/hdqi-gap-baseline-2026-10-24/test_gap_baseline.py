import math

import numpy as np
import pytest
from scipy.linalg import eigh, expm

from gap_baseline import (LCU_NORM, binomial_spectrum, build_model, clipping_plan,
                          control_graphs, filtered_parent, gap_certificate, spectral_control)


@pytest.mark.parametrize("name", ["edge", "cycle4", "weighted-path", "clique5", "commuting-weighted"])
def test_mass_gap_bound(name):
    model = control_graphs()[name]
    mass = sum(j*j for j in model.couplings)
    for beta in (.05, .2, .5):
        bound = gap_certificate(mass, beta)
        parent, _ = filtered_parent(model, beta)
        gap = eigh(parent, eigvals_only=True)[1]
        assert gap + 1e-11 >= bound["gap_lower_bound"]


def test_outside_certificate_is_unknown_not_square_of_negative_number():
    certificate = gap_certificate(10000, .1)
    assert certificate["row_perturbation_bound"] > 1
    assert certificate["status"] == "inconclusive"
    assert certificate["gap_lower_bound"] == 0
    assert gap_certificate(0, 100)["gap_lower_bound"] == 1


def test_subgaussian_mgf_and_vacuum_trace_identity():
    for name in ("edge", "cycle4", "weighted-path", "clique5"):
        model = control_graphs()[name]
        mass = sum(j*j for j in model.couplings)
        for t in (-1, -.2, .3, 1):
            matrix = expm(t * model.h)
            z = np.trace(matrix) / len(matrix)
            assert np.isclose(matrix[0, 0], z, atol=1e-12)
            assert 1 - 1e-12 <= z <= math.prod(math.cosh(t*j) for j in model.couplings) + 1e-12
            assert z <= math.exp(t*t*mass/2) + 1e-12


def test_dependent_paulis_do_not_inherit_moment_bound():
    # ZI, IZ, ZZ multiply to I. The canonical independent-label premise fails.
    h = np.diag([3, -1, -1, -1])
    t = .3
    z = np.trace(expm(t*h)) / 4
    assert z > math.cosh(t)**3
    assert expm(t*h)[0, 0] != z


def test_component_tensorization_of_filtered_parent():
    full = build_model(4, [(0, 1), (2, 3)], [1, -.5, .25, .75])
    first = build_model(2, [(0, 1)], [1, -.5])
    second = build_model(2, [(0, 1)], [.25, .75])
    beta = .3
    f, _ = filtered_parent(full, beta)
    a, _ = filtered_parent(first, beta)
    b, _ = filtered_parent(second, beta)
    assert np.allclose(f, np.kron(np.eye(4), a) + np.kron(b, np.eye(4)), atol=2e-12)
    component_bound = min(gap_certificate(1.25, beta)["gap_lower_bound"],
                          gap_certificate(.625, beta)["gap_lower_bound"])
    assert eigh(f, eigvals_only=True)[1] >= component_bound - 1e-12


def test_clipping_plan_has_actual_clipped_tail_on_easy_commuting_control():
    plan = clipping_plan(64, .1, .1, 64)
    assert plan["cut"] < 64
    assert not plan["clipping_absent_by_norm_bound"]
    energies, weights = binomial_spectrum(64)
    control = spectral_control(energies, weights, .1, plan["cut"])
    assert control["log_weighted_bad_tail"] is not None
    assert control["log_weighted_bad_tail"] <= math.log(plan["weighted_bad_tail_bound"])
    assert control["trace_distance"] <= plan["clipping_trace_distance_budget"]
    assert control["log_success"] / math.log(2) >= plan["log2_success_lower_bound"]
    assert np.isclose(control["log_partition"], 64 * math.log(math.cosh(.1)))


def test_small_unauthorized_cut_is_not_a_good_preparation():
    energies, weights = binomial_spectrum(64)
    good = clipping_plan(64, .1, .1, 64)
    bad = spectral_control(energies, weights, .1, 0)
    assert bad["trace_distance"] > good["clipping_trace_distance_budget"]


def test_dense_clipped_reference_matches_direct_state():
    model = build_model(4, [(0, 1), (1, 2), (2, 3)])
    energies, u = eigh(model.h)
    weights = u[0, :]**2
    beta, cut = .7, .8
    reference = spectral_control(energies, weights, beta, cut)
    vacuum = np.eye(16)[:, 0]
    ideal = expm(-beta*model.h/2) @ vacuum
    ideal /= np.linalg.norm(ideal)
    g = np.minimum(1, np.exp(-beta*(energies+cut)/2))
    actual = u @ (g * (u.T @ vacuum))
    success = np.linalg.norm(actual)**2
    actual /= np.linalg.norm(actual)
    trace = math.sqrt(max(0, 1 - float(ideal @ actual)**2))
    assert np.isclose(reference["trace_distance"], trace, atol=1e-12)
    assert np.isclose(reference["log_success"], math.log(success))


def test_logarithmic_costs_do_not_overflow_or_claim_execution():
    plan = clipping_plan(2**40, math.sqrt(.01/(2**20+1)), .01, 2**40)
    assert plan["log2_amplitude_amplification_scale"] > 10000
    assert plan["quantum_circuit_executed"] is False
    small = clipping_plan(3, .1, .1, 3)
    assert small["clipping_absent_by_norm_bound"]
    assert small["weighted_bad_tail_bound"] == 0


def test_zero_and_polynomial_regime_algebra():
    assert clipping_plan(0, 0, .1, 0)["cut"] == 0
    for mass, beta, epsilon in ((100, .1, .1), (10000, .01, 1e-5), (1000, .02, .01)):
        plan = clipping_plan(mass, beta, epsilon)
        c = beta*beta*mass
        assert beta * plan["cut"] <= 2*c + math.log(64/epsilon**2) + 1e-12
        expected = math.sqrt(5)/2 * LCU_NORM * beta * math.sqrt(mass)
        assert np.isclose(gap_certificate(mass, beta)["row_perturbation_bound"], expected)


def test_inconsistent_norm_sum_is_rejected():
    with pytest.raises(ValueError):
        clipping_plan(100, .1, .1, 1)
    with pytest.raises(ValueError):
        spectral_control([0], [1], float("nan"), 1)


@pytest.mark.parametrize("mass,beta", [(-1, .1), (1, -1), (float("inf"), 0), (1, float("nan"))])
def test_invalid_scalar_inputs(mass, beta):
    with pytest.raises(ValueError):
        gap_certificate(mass, beta)
    with pytest.raises(ValueError):
        clipping_plan(mass, beta, .1)
