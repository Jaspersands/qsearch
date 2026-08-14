from __future__ import annotations

import pytest

from self_dual_wreath_recoupling_haar_gap_reduction import (
    audit_complete_s6_haar_gap,
    complex_haar_expected_chi_square,
    four_label_variance,
    orthogonal_haar_expected_chi_square,
    physical_haar_gap_scaling_record,
    run_recoupling_haar_gap_reduction,
    write_recoupling_haar_gap_reduction_report,
)


def test_haar_channel_chi_formulas() -> None:
    assert orthogonal_haar_expected_chi_square(4, 3, 3) == pytest.approx(4 / 9)
    assert complex_haar_expected_chi_square(4, 3, 3) == pytest.approx(4 / 15)
    assert orthogonal_haar_expected_chi_square(8, 1, 4) == 0.0


def test_four_label_variance_decays() -> None:
    values = [four_label_variance(n) for n in (8, 12, 16, 20)]

    assert values == sorted(values, reverse=True)
    assert values[-1] < 3e-5


def test_complete_s6_chi_is_below_orthogonal_haar_mean() -> None:
    rows = audit_complete_s6_haar_gap()

    assert len(rows) == 5
    assert all(
        row.observed_chi_square
        <= row.orthogonal_haar_expected_chi_square + 1e-10
        for row in rows
    )
    selected = next(row for row in rows if row.final_partition == (3, 3))
    assert selected.orthogonal_haar_expected_chi_square == pytest.approx(4 / 9)
    assert selected.observed_to_orthogonal_haar_ratio < 0.37


def test_physical_scaling_has_factorial_haar_gap() -> None:
    row = physical_haar_gap_scaling_record(30)

    assert row.good_physical_mass_lower_bound > 0.86
    assert row.multiplicity_lower_bound_log2 > 70
    assert row.orthogonal_haar_chi_square_upper_log2 < -118
    assert row.inverse_haar_chi_square_lower_log2 > 118


def test_report_keeps_actual_enhancement_and_algorithm_open(tmp_path) -> None:
    report = run_recoupling_haar_gap_reduction()

    assert report.claim_gate[
        "physical_final_multiplicity_factorial_lower_bound_proved"
    ]
    assert report.claim_gate["haar_channel_chi_factorially_small_proved"]
    assert report.claim_gate[
        "subfactorial_enhancement_would_force_label_independence_proved"
    ]
    assert not report.claim_gate[
        "natural_recoupling_subfactorial_enhancement_proved"
    ]
    assert not report.claim_gate[
        "factorially_enhanced_outlier_family_constructed"
    ]
    assert not report.claim_gate["coherent_phase_route_dequantized"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "haar-gap.json"
    payload = write_recoupling_haar_gap_reduction_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
