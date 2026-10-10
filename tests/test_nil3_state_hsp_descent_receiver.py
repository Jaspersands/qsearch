"""Tests for Nil-3 StateHSP central descent receiver and tree dilation barrier."""
from __future__ import annotations

import hashlib
from pathlib import Path
import pytest
import numpy as np

from theorems.nil3_state_hsp_descent_receiver import (
    DERIVATION,
    REPORT,
    Nil3Element,
    commutator_nil3,
    deterministic_phase_lift_trial,
    full_nil3_receiver_simulation,
    invert_nil3,
    multiply_nil3,
    run_all_controls,
    solve_linear_system_f3,
    tree_dilation_complexity_ledger,
    verify_nilpotency_class_3,
)


def test_nil3_group_multiplication_and_inverses():
    n = 2
    # Identity element
    e = Nil3Element(x=(0, 0), y=(0, 0), z=(0, 0), t=0)

    g1 = Nil3Element(x=(1, 2), y=(0, 1), z=(2, 0), t=1)
    g2 = Nil3Element(x=(2, 1), y=(1, 2), z=(0, 1), t=2)

    # e * g = g * e = g
    assert multiply_nil3(e, g1) == g1
    assert multiply_nil3(g1, e) == g1

    # g * g^-1 = e
    inv_g1 = invert_nil3(g1)
    assert multiply_nil3(g1, inv_g1) == e
    assert multiply_nil3(inv_g1, g1) == e

    # Associativity: (g1 * g2) * g3 == g1 * (g2 * g3)
    g3 = Nil3Element(x=(0, 1), y=(2, 2), z=(1, 1), t=1)
    left = multiply_nil3(multiply_nil3(g1, g2), g3)
    right = multiply_nil3(g1, multiply_nil3(g2, g3))
    assert left == right


def test_nilpotency_class_3_series():
    for n in (1, 2, 3):
        res = verify_nilpotency_class_3(n=n)
        assert res["nilpotency_class_is_exact_3"] is True
        assert res["gamma_2_is_pi_A"] is True
        assert res["gamma_3_is_pi_squared_A_center"] is True
        assert res["gamma_4_is_trivial"] is True


def test_deterministic_phase_lift():
    rng = np.random.default_rng(999)
    for n in (2, 3, 4):
        for _ in range(5):
            s2 = tuple(int(v) for v in rng.integers(0, 3, size=n))
            a0 = tuple(int(v) for v in rng.integers(0, 3, size=n))
            lift = deterministic_phase_lift_trial(n, s2, a0)

            assert lift["is_deterministic_success"] is True
            exp_k = sum(a * s for a, s in zip(a0, s2)) % 3
            assert lift["expected_k"] == exp_k
            assert abs(lift["measured_probabilities"][exp_k] - 1.0) < 1e-12


def test_full_nil3_receiver_simulation():
    for seed in (101, 202, 303):
        sim = full_nil3_receiver_simulation(n=3, seed=seed)
        assert sim["full_secret_recovered_identically"] is True
        assert sim["recovered_s0"] == sim["true_secret_s0"]
        assert sim["recovered_s1"] == sim["true_secret_s1"]
        assert sim["recovered_s2"] == sim["true_secret_s2"]
        assert sim["linear_measurements_needed"] >= 3


def test_solve_linear_system_f3():
    # Simple invertible 2x2 system
    rows = [(1, 0), (0, 1)]
    rhs = [2, 1]
    sol = solve_linear_system_f3(rows, rhs, 2)
    assert sol == (2, 1)

    # Invertible 3x3 system
    rows = [(1, 1, 0), (0, 1, 1), (1, 0, 1)]
    rhs = [1, 0, 2]
    sol = solve_linear_system_f3(rows, rhs, 3)
    # Check that rows @ sol == rhs mod 3
    for r, b in zip(rows, rhs):
        assert sum(a * s for a, s in zip(r, sol)) % 3 == b

    # Inconsistent system should raise ValueError
    inconsistent_rows = [(1, 1, 0), (0, 1, 2), (1, 0, 1)]
    inconsistent_rhs = [1, 0, 2]
    with pytest.raises(ValueError, match="Inconsistent linear equations"):
        solve_linear_system_f3(inconsistent_rows, inconsistent_rhs, 3)


def test_tree_dilation_ledger():
    ledger = tree_dilation_complexity_ledger(n_vals=(4, 8), r_vals=(2, 3, 4, 8))
    assert len(ledger) == 8

    for item in ledger:
        n = item["dimension_n"]
        r = item["nilpotency_class_r"]
        W = (n + 1) ** 2
        assert item["window_size_W"] == W

        depth = max(0, r - 2)
        assert item["descent_tree_depth"] == depth
        expected_copies = (n ** 2) * (W ** depth)
        assert item["total_copy_complexity"] == str(expected_copies)
        assert item["log2_total_copy_complexity"] > 0

        if r <= 3:
            assert item["scaling_regime"] == "polynomial"
        elif r == 4:
            assert item["scaling_regime"] == "mild superpolynomial"
        else:
            assert item["scaling_regime"] == "exponential"


def test_run_all_controls_and_report_integrity():
    report = run_all_controls()
    assert report["status"] == "NIL3_STATE_HSP_DESCENT_CERTIFIED"
    assert report["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert report["producer_sha256"] == hashlib.sha256(Path("theorems/nil3_state_hsp_descent_receiver.py").read_bytes()).hexdigest()

    summary = report["summary"]
    assert summary["nil3_state_hsp_solved_in_polynomial_time"] is True
    assert summary["nil3_copy_complexity_is_O_n4"] is True
    assert summary["deterministic_phase_lift_probability_one"] is True
    assert summary["tree_dilation_barrier_proven_for_r_ge_4"] is True
    assert summary["growing_depth_lwe_remains_hard_under_central_descent"] is True
    assert summary["shor_level_speedup_claimed"] is False
