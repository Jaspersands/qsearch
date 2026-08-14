import math

import pytest

from self_dual_wreath_alternating_base_orbit_reduction import (
    aggregate_sign_orbit_law,
    audit_alternating_base_orbit_reduction,
    coarse_alternating_plancherel_weights,
    even_word_base_likelihood_array,
    permutation_parity_from_cycle_type,
    run_alternating_base_orbit_reduction,
)


def test_cycle_type_parity_is_exact():
    assert permutation_parity_from_cycle_type((1, 1, 1, 1, 1)) == 0
    assert permutation_parity_from_cycle_type((3, 1, 1)) == 0
    assert permutation_parity_from_cycle_type((2, 1, 1, 1)) == 1
    assert permutation_parity_from_cycle_type((5,)) == 0


def test_coarse_alternating_plancherel_weights_sum_to_one():
    orbits, weights = coarse_alternating_plancherel_weights(5)
    assert len(orbits) == 4
    assert sum(weights.values()) == pytest.approx(1.0)
    trivial = tuple(sorted({(5,), (1, 1, 1, 1, 1)}))
    assert weights[trivial] == pytest.approx(1 / 60)


def test_even_word_likelihood_equals_aggregated_sign_orbit_likelihood():
    for n in range(2, 6):
        orbits, even_likelihood, even_count = even_word_base_likelihood_array(n)
        aggregate_orbits, aggregate_likelihood, _product, _physical = (
            aggregate_sign_orbit_law(n)
        )
        assert orbits == aggregate_orbits
        assert even_count == (math.factorial(n) // 2) ** 3
        assert abs(even_likelihood - aggregate_likelihood).max() < 1e-8


def test_exact_alternating_reduction_and_trivial_tail_hold_through_S5():
    rows = [audit_alternating_base_orbit_reduction(n) for n in range(2, 6)]
    assert all(row.exact_alternating_group_reduction_verified for row in rows)
    assert all(row.maximum_base_likelihood_residual < 1e-8 for row in rows)
    assert all(
        row.coarse_trivial_label_physical_mass
        == pytest.approx(row.exact_coarse_trivial_physical_mass)
        for row in rows
    )


def test_report_keeps_trimmed_mixing_and_classical_gate_open():
    report = run_alternating_base_orbit_reduction()
    assert report.headline_metrics["coarse_alternating_group_reduction_theorem_count"] == 1
    assert report.claim_gate["base_sign_orbit_law_equals_coarse_An_law_proved"]
    assert report.claim_gate["self_conjugate_labels_handled_exactly"]
    assert not report.claim_gate["dimension_trimmed_coarse_An_kl_vanishes_proved"]
    assert not report.claim_gate["dimension_trimmed_coarse_An_signal_survives_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
