from fractions import Fraction
from math import comb

import numpy as np
import pytest

from spectral_source import (
    ceil_log2, controlled_collision, controlled_ideal, finite_qpe,
    phase_probabilities, source_budget, trace_distance,
)


def random_density(d, seed):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    result = x @ x.conj().T
    return result / np.trace(result)


def direct_collision(operator, rho, angle):
    """Independent dilation on control/reference/target/environment."""
    d = len(rho)
    r = len(operator) // (2 * d)
    swap = np.zeros((d*d, d*d))
    for a in range(d):
        for b in range(d):
            swap[b*d+a, a*d+b] = 1
    partial = np.cos(angle) * np.eye(d*d) + 1j * np.sin(angle) * swap
    active = np.kron(np.eye(r), partial)
    unitary = np.block([[np.eye(r*d*d), np.zeros_like(active)],
                       [np.zeros_like(active), active]])
    joint = unitary @ np.kron(operator, rho) @ unitary.conj().T
    return np.trace(joint.reshape(len(operator), d, len(operator), d),
                    axis1=1, axis2=3)


@pytest.mark.parametrize("x,expected", [(1, 0), (2, 1), (3, 2),
                                      (Fraction(9, 4), 2), (2**127+1, 128)])
def test_integer_log_bound(x, expected):
    assert ceil_log2(x) == expected


@pytest.mark.parametrize("gap", [Fraction(1, 2), Fraction(1, 17), Fraction(1, 1000)])
def test_hard_budget_and_global_error(gap):
    plan = source_budget(7, gap, Fraction(1, 100))
    assert plan.phase_grid * gap >= 256
    assert plan.median_repeats % 2 == 1
    assert plan.simulation_bound() <= plan.error / 4
    assert plan.raw_copy_cap == plan.target_cap + plan.program_copy_cap
    assert plan.target_cap == plan.calibration_targets + 7 * plan.attempts_per_output
    assert plan.raw_copy_cap <= (
        16 * plan.time_upper_bound**2 / plan.error
        + plan.target_cap * plan.median_repeats * plan.phase_bits + plan.target_cap
    )
    assert plan.receipt()["gap_verified"] is False
    assert plan.receipt()["physical_protocol_executed"] is False


def test_cost_is_polynomial_in_inverse_gap_not_free():
    plans = [source_budget(2, Fraction(1, n), Fraction(1, 16))
             for n in (16, 32, 64, 128)]
    for a, b in zip(plans, plans[1:]):
        assert 16 < b.raw_copy_cap / a.raw_copy_cap < 25
    assert plans[-1].raw_copy_cap > 10**20


@pytest.mark.parametrize("args", [(0, 1, Fraction(1, 8)),
                                  (True, 1, Fraction(1, 8)),
                                  (1, 0, Fraction(1, 8)),
                                  (1, -1, Fraction(1, 8)),
                                  (1, 2, Fraction(1, 8)), (1, 1, 0), (1, 1, 1)])
def test_invalid_budget(args):
    with pytest.raises(ValueError):
        source_budget(*args)


@pytest.mark.parametrize("angle", [0, 0.031, -0.7, 2.0])
def test_all_complex_matrix_units_against_dilation(angle):
    rho = random_density(2, 91)
    for i in range(8):
        for j in range(8):
            operator = np.zeros((8, 8), dtype=complex)
            operator[i, j] = 1 + 0.3j
            assert np.allclose(controlled_collision(operator, rho, angle),
                               direct_collision(operator, rho, angle), atol=2e-12)


@pytest.mark.parametrize("copies", [8, 32, 128])
def test_entangled_reference_and_global_channel_error(copies):
    rho = random_density(2, 18)
    # A maximally entangled control/reference/target versus extra reference is
    # not needed for the proof, but this non-product fixture checks reference use.
    rng = np.random.default_rng(19)
    vector = rng.normal(size=8) + 1j * rng.normal(size=8)
    vector /= np.linalg.norm(vector)
    original = np.outer(vector, vector.conj())
    output = original.copy()
    time = 0.9
    for _ in range(copies):
        output = controlled_collision(output, rho, time / copies)
    ideal = controlled_ideal(original, rho, time)
    assert trace_distance(output, ideal) <= 2 * time**2 / copies + 1e-12
    assert np.isclose(np.trace(output), 1)
    assert np.linalg.eigvalsh(output).min() > -1e-12


def test_classical_control_destroys_phase_information():
    rho = np.diag([0.8, 0.2])
    plus = np.ones((2, 2)) / 2
    original = np.kron(plus, np.diag([1, 0]))
    dephased = np.kron(np.eye(2) / 2, np.diag([1, 0]))
    ideal = controlled_ideal(original, rho, 0.4)
    assert trace_distance(controlled_collision(dephased, rho, 0.4), ideal) >= 0.49


def test_correlated_program_invalidates_fresh_copy_channel():
    # Program and target have the same marginals as an IID input but are |00>
    # or |11> together. Both are SWAP eigenvectors, producing a false phase.
    angle = 0.6
    plus = np.ones((2, 2)) / 2
    correlated = np.diag([0.5, 0, 0, 0.5])
    joint = np.kron(plus, correlated)
    swap = np.array([[1, 0, 0, 0], [0, 0, 1, 0],
                     [0, 1, 0, 0], [0, 0, 0, 1]])
    active = np.cos(angle) * np.eye(4) + 1j * np.sin(angle) * swap
    unitary = np.block([[np.eye(4), np.zeros((4, 4))],
                       [np.zeros((4, 4)), active]])
    joint = unitary @ joint @ unitary.conj().T
    correlated_out = np.trace(joint.reshape(4, 2, 4, 2), axis1=1, axis2=3)
    iid_out = controlled_collision(np.kron(plus, np.eye(2)/2), np.eye(2)/2, angle)
    assert trace_distance(correlated_out, iid_out) > 0.1


@pytest.mark.parametrize("value", [0, 0.0001, 0.13, 0.49, 0.9999, 1])
def test_single_qpe_tail(value):
    gap = 0.125
    grid = 2048
    estimates = np.clip(4 * np.arange(grid) / grid - 1, 0, 1)
    probabilities = phase_probabilities(value, grid)
    bad = np.abs(estimates - value) > gap / 8 + 1e-12
    assert probabilities[bad].sum() < 0.25


def test_ideal_qpe_joint_instrument_not_only_distribution():
    rho = random_density(3, 281)
    values, vectors = np.linalg.eigh(rho)
    outcomes = finite_qpe(rho, 16)
    for y, actual in enumerate(outcomes):
        expected = sum(value * phase_probabilities(value, 16)[y]
                       * np.outer(vectors[:, j], vectors[:, j].conj())
                       for j, value in enumerate(values))
        assert np.allclose(actual, expected, atol=1e-12)
    assert np.allclose(sum(outcomes), rho, atol=1e-12)


def test_real_collision_qpe_converges_on_complete_instrument():
    rho = random_density(2, 282)
    ideal = finite_qpe(rho, 8)
    distances = []
    for base in (32, 128):
        counts = [base * (1 << j) for j in range(3)]
        actual = finite_qpe(rho, 8, counts)
        distance = sum(trace_distance(a, b) for a, b in zip(actual, ideal))
        bound = sum(2 * (np.pi * (1 << j) / 2)**2 / n
                    for j, n in enumerate(counts))
        assert distance <= bound
        assert abs(sum(np.trace(x) for x in actual) - 1) < 2e-11
        distances.append(distance)
    assert distances[1] < distances[0] / 3


def test_unobserved_filter_cannot_purify():
    rho = np.diag([0.7, 0.2, 0.1])
    outcomes = finite_qpe(rho, 16)
    top = np.diag([1, 0, 0])
    selected = sum(outcomes[y] for y in range(16) if 4*y/16 - 1 > 0.45)
    success = float(np.trace(selected).real)
    assert 0 < success < 1
    assert trace_distance(selected / success, top) < trace_distance(rho, top)
    assert np.allclose(sum(outcomes), rho)


def test_degenerate_top_does_not_choose_unknown_pure_state():
    rho = np.diag([0.4, 0.4, 0.2])
    outcomes = finite_qpe(rho, 16)
    selected = sum(outcomes[y] for y in range(16) if 4*y/16 - 1 > 0.3)
    selected /= np.trace(selected)
    assert np.isclose(selected[0, 0], selected[1, 1])
    assert trace_distance(selected, np.diag([1, 0, 0])) >= 0.5


def test_median_on_fresh_targets_is_the_wrong_algorithm():
    # Spectrum (.4,.3,.3): fresh targets each time turn the median into a
    # population quantile, not a sharper measurement of one eigenvalue.
    def top_median_probability(repeats):
        return sum(comb(repeats, k) * 0.4**k * 0.6**(repeats-k)
                   for k in range(repeats//2+1, repeats+1))
    assert top_median_probability(101) < top_median_probability(11) < 0.4


@pytest.mark.parametrize("gap", [Fraction(1, 2), Fraction(1, 7), Fraction(1, 100)])
def test_threshold_intervals_separate_all_good_estimates(gap):
    top = (1 + gap) / 2
    other = top - gap
    for v in (top-gap/8, top+gap/8):
        threshold = v-gap/2
        assert top-gap/8 > threshold
        assert other+gap/8 < threshold


@pytest.mark.parametrize("rho", [np.eye(2), np.diag([1.1, -0.1]),
                                 np.array([[1, 1], [0, 0]])])
def test_invalid_program(rho):
    with pytest.raises(ValueError):
        controlled_collision(np.eye(4)/4, rho, 0.1)
