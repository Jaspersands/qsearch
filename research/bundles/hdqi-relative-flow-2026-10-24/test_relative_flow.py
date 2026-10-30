import math

import numpy as np
import pytest
from scipy.linalg import eigh, expm
from scipy.integrate import quad

import relative_flow as r


@pytest.mark.parametrize("edges", ([], [(0, 1)], [(0, 1), (1, 2)], [(0, 1), (0, 2)]))
def test_gram_identity_and_real_time_filter_controls(edges):
    rows = r.dense_control(r.build_model(3, edges, (1, -0.5, 0.25)))
    assert len(rows) == 4
    assert all(row["exact_diagonal_gram_identity"] for row in rows)


def test_neighbor_weight_not_global_mass_or_self_weight():
    model = r.build_model(4, [(0, 1), (0, 2)], (0.25, 0.5, 1, 1))
    assert r.weighted_degree(model) == 1.25


def test_commuting_flow_is_identity_but_tagged_jump_is_not():
    model = r.build_model(3, [], (1, 0.5, 0.25))
    assert np.array_equal(r.liouvillian(model), np.zeros_like(model.h))
    _, _, _, _, _, rho = r.gradient_data(model, 1)
    assert rho == 0.25
    assert np.linalg.norm(r.liouvillian(model, 1)) > 0


def test_seminorm_kernel_cannot_be_silently_ignored():
    with pytest.raises(ValueError, match="seminorm kernel"):
        r.relative_norm(np.eye(2), np.diag([0, 1]))


@pytest.mark.parametrize("t", (0, 0.1, 0.6))
def test_folded_normal_moments_against_integration(t):
    actual = r.folded_normal(t)
    for k in range(3):
        integral = quad(lambda v: 2 * math.sqrt(2 / math.pi) * v**k *
                        math.exp(t * v - 2 * v*v), 0, 12, epsabs=1e-12)[0]
        assert math.isclose(actual[k], integral, rel_tol=1e-11, abs_tol=1e-12)


def test_squared_outer_bound_stops_at_correct_threshold():
    assert r.filter_bounds(0, 0)["outer_mean_square_relative_commutator_bound"] == 0
    assert r.filter_bounds(0.1, 1)["outer_square_bound_available"]
    assert not r.filter_bounds(math.pi / 2, 1)["outer_square_bound_available"]
    assert r.filter_bounds(math.pi / 2, 1)["outer_mean_square_relative_commutator_bound"] is None


def test_outer_square_bound_dominates_actual_folded_exponential_integral():
    beta, rho = 0.1, 1
    a = 2 * beta * math.sqrt(rho)
    mv = r.folded_normal(a)[0]
    integral = quad(lambda s: 4 / math.cosh(2 * math.pi * s) *
                    (r.LCU_NORM * (mv * math.exp(a*s) - 1))**2,
                    0, 20, epsabs=1e-12)[0]
    assert integral <= r.filter_bounds(beta, rho)["outer_mean_square_relative_commutator_bound"]


def test_thermal_dirichlet_counterexample_matches_dense_product():
    m, beta = 4, 0.1
    model = r.build_model(m, [])
    identity = np.eye(1 << m)
    projector = identity.copy()
    for op in model.operators:
        projector = projector @ (identity - op) / 2
    density = expm(-beta * model.h)
    density /= np.trace(density)
    trace_energy = thermal_energy = 0.0
    for z in model.z:
        derivative = (projector - z @ projector @ z) / 2
        square = derivative.T @ derivative
        trace_energy += np.trace(square) / (1 << m)
        thermal_energy += np.trace(density @ square)
    expected = r.product_weight_counterexample(m, beta)
    assert math.isclose(math.log(thermal_energy / trace_energy),
                        expected["log_thermal_over_trace_low_projector_dirichlet_ratio"],
                        abs_tol=1e-12)
    root_density = expm(-beta * model.h / 2) / math.sqrt(np.trace(expm(-beta * model.h)))
    trace_comm = kms_comm = 0.0
    for z in model.z:
        derivative = r.commutator(z, projector)
        trace_comm += np.trace(derivative.T @ derivative) / (1 << m)
        kms_comm += np.trace(root_density @ derivative.T @ root_density @ derivative)
    assert math.isclose(math.log(kms_comm / trace_comm),
                        expected["log_kms_over_trace_low_projector_commutator_ratio"],
                        abs_tol=1e-12)


def test_matching_imaginary_flow_violates_real_time_bound():
    model = r.build_model(4, [(0, 1), (2, 3)])
    ell, grad, _, _, _, _ = r.gradient_data(model)
    values, vectors = eigh(ell)
    v = vectors[:, -1]
    tau = 0.2
    ratio = np.linalg.norm(grad @ expm(tau * ell) @ v) / np.linalg.norm(grad @ v)
    expected = r.matching_imaginary_time_counterexample(2, tau)
    assert math.isclose(math.log(ratio), expected["log_gradient_amplification_on_eigenoperator"],
                        abs_tol=1e-12)
    assert math.log(ratio) > expected["incorrect_real_time_bound_log"]


def test_no_gap_admission_from_small_filter_bound():
    value = r.filter_bounds(0.01, 1)
    assert value["outer_mean_square_relative_commutator_bound"] < 1
    assert value["parent_gap_certified"] is False


@pytest.mark.parametrize("beta,rho", ((-1, 1), (1, -1), (float("nan"), 1)))
def test_invalid_bound_parameters(beta, rho):
    with pytest.raises(ValueError):
        r.filter_bounds(beta, rho)
