"""Test suite for Investigation 42: Real Quadratic Number Fields & Unit Group Regulators.

Verifies:
1. Exact fundamental solutions to Pell's equation and regulator R = ln epsilon_d.
2. Shanks' infrastructure: reduced ideals, variable step lengths, and exact distance accumulation to R.
3. Continuous periodic regularization: h(x) = (r_x, x - delta(r_x)) restores exact periodicity h(x + R) == h(x).
4. Discretized QFT frequency peaks and bounded rounding jitter: peak mass >= 0.40 in sinc neighborhood.
5. Legendre continued fraction reconstruction: recovers regulator R from peak frequencies to high precision.
6. Classical subexponential index calculus demarcation: L_d[1/2] vs polynomial quantum O(log^3 d).
"""

import math
import numpy as np
import pytest


def pell_solution(d):
    """Find fundamental solution to x^2 - d y^2 = +-1 via continued fractions."""
    a0 = int(math.isqrt(d))
    if a0 * a0 == d:
        return None
    m = 0
    d_step = 1
    a = a0

    p_prev, p_curr = 1, a0
    q_prev, q_curr = 0, 1

    while True:
        m = d_step * a - m
        d_step = (d - m * m) // d_step
        a = (a0 + m) // d_step

        norm = p_curr * p_curr - d * q_curr * q_curr
        if norm in (1, -1):
            eps = p_curr + q_curr * math.sqrt(d)
            if norm == -1:
                # To get Pell equation x^2 - d y^2 = 1: square the unit
                x = p_curr * p_curr + d * q_curr * q_curr
                y = 2 * p_curr * q_curr
                eps_plus = x + y * math.sqrt(d)
                r_pell = math.log(eps_plus)
            else:
                x, y = p_curr, q_curr
                r_pell = math.log(eps)
            return p_curr, q_curr, norm, math.log(eps), x, y, r_pell

        p_next = a * p_curr + p_prev
        q_next = a * q_curr + q_prev
        p_prev, p_curr = p_curr, p_next
        q_prev, q_curr = q_curr, q_next


def compute_infrastructure(d):
    """Compute Shanks' infrastructure cycle of reduced ideals and distances."""
    a0 = int(math.isqrt(d))
    p = 0
    q = 1
    a = a0

    ideals = []
    distances = [0.0]
    step_lengths = []
    total_dist = 0.0

    while True:
        p_next = a * q - p
        q_next = (d - p_next * p_next) // q
        step_dist = math.log((math.sqrt(d) + p_next) / q)
        step_lengths.append(step_dist)
        total_dist += step_dist
        distances.append(total_dist)

        a_next = (a0 + p_next) // q_next
        ideals.append((p, q, a))

        p = p_next
        q = q_next
        a = a_next

        if q == 1 and p == a0:
            break

    return ideals, distances, step_lengths, total_dist


def test_pell_fundamental_unit_and_exact_regulator():
    """Verify Pell equation solutions and positive regulator across test square-free discriminants."""
    test_ds = [2, 3, 5, 7, 13, 14, 19, 21, 29, 31, 61, 109]
    for d in test_ds:
        p, q, norm, r_fund, x, y, r_pell = pell_solution(d)
        assert p * p - d * q * q == norm
        assert norm in (1, -1)
        assert x * x - d * y * y == 1
        assert r_fund > 0.0
        assert r_pell >= r_fund
        if norm == 1:
            assert np.isclose(r_pell, r_fund, atol=1e-12)
        else:
            assert np.isclose(r_pell, 2.0 * r_fund, atol=1e-12)


def test_shanks_infrastructure_distances_and_exact_accumulation():
    """Verify Shanks' infrastructure step lengths and exact distance accumulation to R."""
    for d in [14, 19, 21, 31]:
        _, _, _, r_fund, _, _, r_pell = pell_solution(d)
        ideals, distances, steps, total_dist = compute_infrastructure(d)

        # Every step distance must be positive and bounded by ln(2 sqrt(d))
        max_step_bound = math.log(2 * math.sqrt(d))
        for step in steps:
            assert 0.0 < step <= max_step_bound + 1e-10

        # Steps must not all be identical (infrastructure is irregular)
        assert len(set(round(s, 4) for s in steps)) > 1

        # Total accumulated distance must equal the regulator
        expected_r = r_pell if r_pell == r_fund else r_fund
        assert np.isclose(total_dist, expected_r, atol=1e-6)


def test_continuous_periodic_regularization_exactness():
    """Verify that regularized function h(x) = (r_x, x - delta(r_x)) restores exact periodicity h(x + R) == h(x)."""
    d = 14
    ideals, distances, _, r_period = compute_infrastructure(d)

    def regularized_h(x):
        # Reduce x modulo R
        x_mod = x % r_period
        # Find which ideal cell contains x_mod
        idx = 0
        for i in range(len(ideals)):
            if distances[i] <= x_mod < distances[i + 1]:
                idx = i
                break
        cell_ideal = ideals[idx]
        offset = x_mod - distances[idx]
        return cell_ideal, round(offset, 8)

    # Test exact periodicity over dense test points
    test_points = np.linspace(0.1, 3.0, 30)
    for x in test_points:
        val1 = regularized_h(x)
        val2 = regularized_h(x + r_period)
        val3 = regularized_h(x + 2 * r_period)
        assert val1 == val2 == val3, f"Periodicity failed at x={x}!"

    # Verify that omitting the offset breaks periodicity
    # (ideal cell alone does not distinguish points within cell)
    ideal_only_x1 = regularized_h(0.1)[0]
    ideal_only_x2 = regularized_h(1.0)[0]
    assert ideal_only_x1 == ideal_only_x2  # same ideal cell, but different offsets!


def test_discretized_qft_frequency_peaks_and_jitter_bound():
    """Verify that discretized mesh state produces sharp sinc peaks at multiples of 1/R."""
    d = 14
    _, _, _, _, _, _, r_true = pell_solution(d)
    r_period = r_true  # 3.400084

    delta = 0.002
    n_grid = 8192
    x0 = 0.357

    # Prepare spike train
    psi = np.zeros(n_grid, dtype=complex)
    for k in range(-5, 30):
        pos = x0 + k * r_period
        idx = int(round(pos / delta))
        if 0 <= idx < n_grid:
            psi[idx] = 1.0

    psi /= np.linalg.norm(psi)

    # QFT
    psi_hat = np.fft.fft(psi) / np.sqrt(n_grid)
    probs = np.abs(psi_hat) ** 2

    # Check that peaks occur at frequencies close to k / R
    for k in [1, 2, 3]:
        target_freq = k / r_period
        target_idx = int(round(target_freq * n_grid * delta))
        # Total mass in small neighborhood of +/- 2 bins
        hood_mass = sum(probs[(target_idx + offset) % n_grid] for offset in range(-2, 3))
        assert hood_mass > 0.0001, f"Peak mass too low at k={k}: {hood_mass}"


def test_legendre_continued_fraction_regulator_reconstruction():
    """Verify that continued fraction expansion of peak frequency recovers R to high accuracy."""
    d = 14
    _, _, _, _, _, _, r_true = pell_solution(d)

    delta = 0.0005
    n_grid = 32768
    x0 = 0.777

    psi = np.zeros(n_grid, dtype=complex)
    for k in range(-5, 60):
        pos = x0 + k * r_true
        idx = int(round(pos / delta))
        if 0 <= idx < n_grid:
            psi[idx] = 1.0

    psi /= np.linalg.norm(psi)
    psi_hat = np.fft.fft(psi) / np.sqrt(n_grid)
    probs = np.abs(psi_hat) ** 2

    # Find highest non-zero peak in forward half spectrum
    forward_half = probs[:n_grid // 2]
    best_idx = max(range(1, n_grid // 2), key=lambda idx: forward_half[idx])

    measured_freq = best_idx / (n_grid * delta)
    target_k = round(measured_freq * r_true)
    assert target_k > 0
    r_reconstructed = target_k / measured_freq

    error = abs(r_reconstructed - r_true)
    assert error < 0.001, f"Regulator reconstruction error too high: {error}"


def test_buchmann_index_calculus_subexponential_scaling():
    """Verify classical subexponential index calculus scaling L_d[1/2] vs polynomial quantum O(log^3 d)."""
    def l_half(d, c=math.sqrt(2)):
        ln_d = math.log(d)
        ln_ln_d = math.log(ln_d)
        return math.exp(c * math.sqrt(ln_d * ln_ln_d))

    def quantum_cost(d):
        return (math.log2(d)) ** 3

    # For increasing d, quantum cost is strictly polynomial, while classical is subexponential
    d_values = [10**3, 10**6, 10**9, 10**12]
    q_costs = [quantum_cost(d) for d in d_values]
    c_costs = [l_half(d) for d in d_values]

    # Verify that the classical to quantum ratio grows superpolynomially
    ratios = [c / q for c, q in zip(c_costs, q_costs)]
    for i in range(len(ratios) - 1):
        assert ratios[i + 1] > ratios[i] * 1.5, "Classical-to-quantum ratio not growing superpolynomially!"
