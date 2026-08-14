from __future__ import annotations

import pytest

from self_dual_wreath_plancherel_marginal_compatibility_no_go import (
    expected_plancherel_pair_l1,
    normalized_row_spectrum,
    row_spectrum_l1,
    run_plancherel_marginal_compatibility_no_go,
    write_plancherel_marginal_compatibility_no_go_report,
)


def test_row_spectrum_distance_equals_normalized_diagram_difference() -> None:
    left = (4, 2)
    right = (3, 2, 1)

    assert normalized_row_spectrum(left) == pytest.approx((2 / 3, 1 / 3))
    assert row_spectrum_l1(left, right) == pytest.approx(1 / 3)


def test_exact_law_pair_distance_decreases_across_scaling_controls() -> None:
    values = [expected_plancherel_pair_l1(n) for n in (4, 8, 12, 20, 30)]

    assert values == sorted(values, reverse=True)
    assert values[0] == pytest.approx(0.39236111111111105)
    assert values[-1] == pytest.approx(0.2259002115222829)


def test_report_closes_constant_gap_not_shrinking_gap_or_true_norm(tmp_path) -> None:
    report = run_plancherel_marginal_compatibility_no_go()

    assert report.claim_gate["physical_six_spectra_approach_compatibility_proved"]
    assert not report.claim_gate[
        "constant_incompatibility_gap_on_positive_physical_mass_possible"
    ]
    assert not report.claim_gate["marginal_distance_rate_proved"]
    assert not report.claim_gate["typical_recoupling_norm_lower_bound_proved"]
    assert not report.claim_gate["typical_recoupling_contraction_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "marginal-compatibility.json"
    payload = write_plancherel_marginal_compatibility_no_go_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
