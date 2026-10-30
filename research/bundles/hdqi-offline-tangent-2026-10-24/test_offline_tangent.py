from fractions import Fraction as F
from itertools import product

import numpy as np
import pytest
from scipy.linalg import expm, qr

import offline_tangent as t


def random_state(size, seed):
    rng = np.random.default_rng(seed)
    state = rng.normal(size=size) + 1j * rng.normal(size=size)
    return state / np.linalg.norm(state)


@pytest.mark.parametrize("seed", range(12))
def test_complex_uhlmann_identity_and_covariance(seed):
    psi = random_state(16, seed)
    rho = t.reduced_operator(np.outer(psi, psi.conj()), (0, 1), 4)
    observable = t.pauli("ZIII")
    out = t.polar_tangent(rho, t.pauli("ZI"))
    lifted = np.kron(out.generator, np.eye(4))
    desired = observable @ psi - np.vdot(psi, observable @ psi).real * psi
    actual_loss = np.linalg.norm(desired - lifted @ psi)**2
    p = np.trace(rho[:2, :2]).real
    assert np.isclose(actual_loss, 4 * p * (1 - p) - 4 * out.off_diagonal_trace_norm**2)
    assert np.isclose(actual_loss, out.loss)
    assert actual_loss <= 2 * t.far_covariance(psi, observable, (0, 1), 4) + 1e-12
    assert np.allclose(lifted.conj().T, -lifted)
    assert np.linalg.norm(out.generator, 2) <= 1 + 1e-12


@pytest.mark.parametrize("p", [0, 1e-24, .01, .5, .99, 1])
def test_no_population_or_density_spectral_gap_needed(p):
    u = random_state(4, 90)
    v = random_state(4, 91)
    psi = np.concatenate((np.sqrt(p) * u, np.sqrt(1 - p) * v))
    rho = np.outer(psi, psi.conj())
    out = t.polar_tangent(rho, t.pauli("ZII"))
    target = t.pauli("ZII") @ psi - (2 * p - 1) * psi
    assert np.linalg.norm(out.generator @ psi - target) < 1e-12
    assert np.isfinite(out.generator).all()


def test_far_single_site_covariances_miss_joint_obstruction():
    bell_plus = np.array([1, 0, 0, 1]) / np.sqrt(2)
    bell_minus = np.array([1, 0, 0, -1]) / np.sqrt(2)
    psi = np.concatenate((bell_plus, bell_minus)) / np.sqrt(2)
    observable = t.pauli("ZII")
    for far_word in ("IXI", "IYI", "IZI", "IIX", "IIY", "IIZ"):
        assert abs(np.vdot(psi, observable @ t.pauli(far_word) @ psi)) < 1e-12
    assert np.isclose(t.far_covariance(psi, observable, (0,), 3), 1)
    rho = t.reduced_operator(np.outer(psi, psi.conj()), (0,), 3)
    assert np.isclose(t.polar_tangent(rho, t.pauli("Z")).loss, 1)


@pytest.mark.parametrize("seed", range(8))
def test_robustness_is_objective_not_polar_operator_continuity(seed):
    psi = random_state(16, seed + 40)
    rho = t.reduced_operator(np.outer(psi, psi.conj()), (0, 1), 4)
    noise = random_state(4, seed + 80)
    noisy = .997 * rho + .003 * np.outer(noise, noise.conj())
    observable = t.pauli("ZI")
    original = t.polar_tangent(rho, observable)
    approximate = t.polar_tangent(noisy, observable)
    tau = t.trace_norm(noisy - rho)
    loss = t.tangent_loss(rho, observable, approximate.generator)
    assert loss <= original.loss + 10 * tau + 1e-12
    eta = t.far_covariance(psi, t.pauli("ZIII"), (0, 1), 4)
    assert loss <= 2 * eta + 10 * tau + 1e-12


def test_polar_discontinuity_does_not_break_bounded_loss():
    rows = []
    for sign in (-1, 1):
        rho = np.eye(4) / 4
        rho[0, 2] = rho[2, 0] = .2
        rho[1, 3] = rho[3, 1] = sign * 1e-12
        rows.append((rho, t.polar_tangent(rho, t.pauli("ZI"))))
    assert np.linalg.norm(rows[0][1].generator - rows[1][1].generator, 2) > .79
    assert t.trace_norm(rows[0][0] - rows[1][0]) < 5e-12
    assert abs(t.tangent_loss(rows[0][0], t.pauli("ZI"), rows[1][1].generator)
               - rows[0][1].loss) < 1e-10


def test_psd_projection_and_pauli_precision_budget():
    psi = random_state(8, 31)
    rho = np.outer(psi, psi.conj())
    alpha = 1e-4
    calls = []
    def expectation(word):
        calls.append(word)
        return np.trace(rho @ t.pauli(word)).real + alpha * (-1)**word.count("X")
    estimated = t.reconstruct_marginal(3, expectation)
    assert len(calls) == 4**3 - 1
    assert t.trace_norm(estimated - rho) <= 8 * alpha + 1e-12
    assert np.linalg.eigvalsh(estimated)[0] >= -1e-12
    assert np.isclose(np.trace(estimated), 1)


def test_projection_is_not_naive_clipping():
    raw = np.diag([1.3, .1, -.4])
    assert np.allclose(t.project_density(raw), np.diag([1., 0, 0]))


def test_patch_order_and_partial_trace_duality():
    psi = random_state(16, 192)
    pure = np.outer(psi, psi.conj())
    for keep in ((3, 0), (2,), (1, 0, 3), (3, 2, 1, 0)):
        local = t.pauli("Y" + "Z" * (len(keep) - 1))
        marginal = t.reduced_operator(pure, keep, 4)
        full = t.lift_operator(local, keep, 4)
        assert np.isclose(np.trace(marginal @ local), np.vdot(psi, full @ psi))


def test_involution_basis_covariance():
    psi = random_state(8, 100)
    rho = t.reduced_operator(np.outer(psi, psi.conj()), (0, 1), 3)
    rng = np.random.default_rng(121)
    unitary, _ = qr(rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)))
    observable = unitary @ t.pauli("ZI") @ unitary.conj().T
    out = t.polar_tangent(unitary @ rho @ unitary.conj().T, observable)
    expected = unitary @ t.polar_tangent(rho, t.pauli("ZI")).generator @ unitary.conj().T
    assert np.allclose(out.generator, expected)


def tfd_fixture():
    initial = np.eye(4).reshape(-1) / 2
    terms = [(1., "XIII"), (-.7, "ZXII")]
    return terms, initial


def test_full_patch_endpoint_controls_have_no_tangent_error():
    terms, initial = tfd_fixture()
    rows = [t.dense_schedule_control(terms, initial, .4, steps, [(0, 1, 2, 3)] * 2)
            for steps in (8, 16, 32)]
    assert all(row["max_tangent_residual"] < 1e-12 for row in rows)
    assert all(row["vector_error"] <= row["total_bound"] for row in rows)
    assert rows[1]["vector_error"] < .6 * rows[0]["vector_error"]
    assert rows[2]["vector_error"] < .6 * rows[1]["vector_error"]
    assert all(row["uses_dense_exact_target_access"] and not row["quantum_executed"] for row in rows)


def test_restricted_patch_is_not_certified_by_smaller_time_steps():
    terms, initial = tfd_fixture()
    row = t.dense_schedule_control(terms, initial, .8, 32, [(0, 2), (0, 1, 2, 3)])
    assert row["max_tangent_residual"] > .01
    assert row["max_far_covariance"] > .001
    assert row["vector_error"] < row["total_bound"]


@pytest.mark.parametrize("edge", [False, True])
def test_all_paired_paulis_have_correct_signed_pullback(edge):
    edges = [(0, 1)] if edge else []
    h = .7 * t.pauli("XI") - .4 * t.pauli("ZX" if edge else "IX")
    s = expm(-.31 * h / 2)
    pilot = s[:, 0] / np.linalg.norm(s[:, 0])
    tfd = s.reshape(-1) / np.linalg.norm(s)
    for letters in product("IXYZ", repeat=4):
        word = "".join(letters)
        pulled = t.tfd_pauli_pullback(2, edges, word)
        actual = np.vdot(tfd, t.pauli(word) @ tfd)
        expected = 0 if pulled is None else pulled[0] * np.vdot(pilot, t.pauli(pulled[1]) @ pilot)
        assert np.isclose(actual, expected, atol=1e-12)


def test_symbolic_pullback_scales_without_density_table():
    vertices = 128
    pulled = t.tfd_pauli_pullback(vertices, [(i, i + 1) for i in range(vertices - 1)],
                                  "X" + "I" * (2 * vertices - 1))
    assert pulled == (1, "X" + "I" * (vertices - 1))


@pytest.mark.parametrize("patch", [1, 20, 256])
def test_charged_plan_has_no_free_target_access(patch):
    plan = t.endpoint_plan(128, F(1, 8), 128, F(1, 100), patch)
    assert F(plan["vector_error_budget"]) <= F(1, 100)
    assert plan["pauli_estimates"] == 128 * plan["steps"] * (4**patch - 1)
    assert F(plan["pauli_additive_error"]) * 2**patch == F(plan["marginal_trace_error"])
    assert not plan["exact_target_marginals_granted"]
    assert not plan["production_observable_estimator_implemented"]
    assert not plan["correlation_promise_verified"]


def test_ball_bill_exposes_nonuniform_degree_cost():
    path = t.ball_ledger(10**6, 2, 8)
    expander_bound = t.ball_ledger(10**6, 16, 8)
    assert path["ball_vertices_bound"] == 17
    assert expander_bound["ball_vertices_bound"] == 10**6
    assert expander_bound["pauli_count_log2_bound"] == 4 * 10**6


@pytest.mark.parametrize("bad", [np.diag([1.2, -.2]), np.eye(2), np.array([[1., 1], [0, 0]]),
                                 np.array([[float("nan"), 0], [0, 1]])])
def test_invalid_density_rejected(bad):
    with pytest.raises(ValueError):
        t.polar_tangent(bad, t.pauli("Z"))


def test_invalid_access_and_dimension_rejected():
    with pytest.raises(ValueError):
        t.polar_tangent(np.eye(2) / 2, np.eye(2))
    with pytest.raises(ValueError):
        t.reconstruct_marginal(6, lambda word: 0)
    with pytest.raises(ValueError):
        t.tfd_pauli_pullback(2, [(0, 1), (1, 0)], "IIII")
    with pytest.raises(ValueError):
        t.endpoint_plan(2, 1, 2, 0, 2)
    with pytest.raises(ValueError):
        t.dense_schedule_control([(1., "XZ")], np.array([1, 0, 0, 0]), .1, 2, [(0,)])
    with pytest.raises(ValueError):
        t.dense_schedule_control([(1., "X")], np.array([1, 0]), 21, 2, [(0,)])
