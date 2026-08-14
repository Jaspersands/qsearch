from __future__ import annotations

import math
from fractions import Fraction

import pytest

from self_dual_wreath_physical_recoupling_tetrahedral_synergy import (
    audit_fusion_face_synergy,
    run_physical_recoupling_tetrahedral_synergy,
    tetrahedral_synergy_scaling_record,
    write_physical_recoupling_tetrahedral_synergy_report,
)


def test_fusion_face_has_exact_pair_marginals_and_chi_square() -> None:
    for n in range(3, 7):
        row = audit_fusion_face_synergy(n)
        assert row.exact_face_probability_sum == "1"
        assert row.maximum_exact_pair_marginal_residual == "0"
        assert row.exact_chi_square_identity_verified
        assert row.exact_pairwise_independence_verified
        assert row.face_total_variation <= row.face_total_variation_upper_bound + 1e-12
        assert row.face_mutual_information_bits <= (
            row.face_mutual_information_upper_bound_bits + 1e-12
        )


def test_face_information_bounds_decay() -> None:
    rows = [tetrahedral_synergy_scaling_record(n) for n in (8, 12, 20, 30)]

    assert [row.face_total_variation_upper_bound for row in rows] == sorted(
        (row.face_total_variation_upper_bound for row in rows), reverse=True
    )
    assert rows[-1].face_mutual_information_upper_bound_bits < 0.004
    assert all(row.pairwise_mutual_information_bits == 0.0 for row in rows)


def test_s3_face_information_is_nonzero_but_bounded() -> None:
    row = audit_fusion_face_synergy(3)

    assert row.face_total_variation > 0
    assert row.face_mutual_information_bits > 0
    assert row.face_total_variation_upper_bound == pytest.approx(
        math.sqrt(float(Fraction(row.exact_reciprocal_class_variance))) / 2
    )


def test_report_isolates_global_synergy_and_coherent_phase(tmp_path) -> None:
    report = run_physical_recoupling_tetrahedral_synergy()

    assert report.claim_gate["all_physical_edge_pairs_independent_proved"]
    assert report.claim_gate[
        "all_four_fusion_face_dependencies_vanish_proved"
    ]
    assert not report.claim_gate["full_six_label_product_law_proved"]
    assert not report.claim_gate[
        "source_conditioned_channel_information_vanishes_proved"
    ]
    assert not report.claim_gate[
        "coherent_multiplicity_phase_signal_absent_proved"
    ]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "tetrahedral-synergy.json"
    payload = write_physical_recoupling_tetrahedral_synergy_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["independent_label_pair_count"] == 15
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
