from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_recoupling_channel_flatness_boundary import (
    audit_complete_s6_channel_information,
    channel_information_from_recoupling,
    run_recoupling_channel_flatness_boundary,
    write_recoupling_channel_flatness_boundary_report,
)


def test_flat_unitary_has_independent_channel_labels() -> None:
    matrix = np.asarray([[1, 1], [1, -1]], dtype=float) / np.sqrt(2)
    row = channel_information_from_recoupling(
        (2,), matrix, ((2,), (1, 1))
    )

    assert row.exact_channel_flatness
    assert row.total_variation_from_channel_independence == pytest.approx(0.0)
    assert row.mutual_information_bits == pytest.approx(0.0)
    assert row.minimum_positive_likelihood_ratio == pytest.approx(1.0)
    assert row.maximum_likelihood_ratio == pytest.approx(1.0)


def test_complete_s6_controls_contain_nonhaar_and_forbidden_channels() -> None:
    rows = audit_complete_s6_channel_information()

    assert len(rows) == 5
    assert all(row.maximum_marginal_residual < 1e-10 for row in rows)
    assert sum(row.nontrivial_channel_correlation for row in rows) == 4
    assert sum(
        row.product_mass_on_physically_forbidden_channels > 1e-10
        for row in rows
    ) == 2
    selected = next(row for row in rows if row.final_partition == (3, 3))
    assert selected.total_variation_from_channel_independence == pytest.approx(1 / 8)
    assert selected.product_mass_on_physically_forbidden_channels == pytest.approx(1 / 16)
    assert selected.maximum_likelihood_ratio == pytest.approx(16 / 9)
    assert selected.mutual_information_bits == pytest.approx(0.15642516416475646)


def test_report_keeps_asymptotic_and_coherent_claims_open(tmp_path) -> None:
    report = run_recoupling_channel_flatness_boundary()

    assert report.claim_gate["channel_information_identity_proved"]
    assert report.claim_gate["exact_channel_flatness_falsified_at_s6"]
    assert not report.claim_gate[
        "source_weighted_mutual_information_vanishes_proved"
    ]
    assert not report.claim_gate[
        "source_weighted_mutual_information_survives_proved"
    ]
    assert not report.claim_gate["nonhaar_outlier_transform_compiled"]
    assert not report.claim_gate["classical_baseline_separated"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "channel-flatness.json"
    payload = write_recoupling_channel_flatness_boundary_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
