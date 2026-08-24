from __future__ import annotations

import json
import math

from self_dual_wreath_branch_character_sector_resolved_whitening_no_go import (
    audit_sector_resolved_whitening,
    natural_whitening_no_go_scaling,
    run_sector_resolved_whitening_no_go,
    write_sector_resolved_whitening_no_go_report,
)


SINGLE = (((3,), (2, 1)),)
THRESHOLD = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_sector_fourier_inversion_reconstructs_all_correct_blocks() -> None:
    control = audit_sector_resolved_whitening("threshold", THRESHOLD)
    assert control.whitened_reconstruction_residual < 1e-9
    assert control.matched_reconstruction_residual < 1e-9
    assert control.correction_reconstruction_residual < 1e-9
    assert math.isclose(
        control.direct_whitened_correct_success,
        control.reconstructed_whitened_correct_success,
    )


def test_each_sector_correction_is_bounded_by_its_polar_distance_mass() -> None:
    control = audit_sector_resolved_whitening("single", SINGLE)
    assert control.exact_sector_resolved_whitening_no_go_verified
    for sector in control.sector_controls:
        assert sector.central_raw_bound_residual < 1e-9
        assert sector.correction_below_polar_distance_contribution
        assert sector.correction_bound_residual < 1e-9


def test_coherent_sector_sum_costs_only_partition_count() -> None:
    control = audit_sector_resolved_whitening("threshold", THRESHOLD)
    assert control.correction_below_partition_times_distance
    assert control.direct_correction_success <= (
        control.partition_times_polar_distance_bound + 1e-9
    )
    assert control.polar_distance_below_gram_residual
    assert control.polar_distance_parseval_residual < 1e-9
    assert control.polar_gram_parseval_residual < 1e-9


def test_pointwise_whitened_success_bound_uses_overlap_and_partition_weighted_R() -> None:
    control = audit_sector_resolved_whitening("single", SINGLE)
    assert control.matched_success_below_overlap
    assert control.whitened_success_bound_verified
    assert control.direct_whitened_correct_success <= (
        control.partition_times_gram_success_bound + 1e-9
    )


def test_natural_whitened_success_vanishes_at_three_log_group_copy_scale() -> None:
    row = natural_whitening_no_go_scaling(512)
    assert row.log2_partition_weighted_correction_upper_bound < -800
    assert row.expected_whitened_success_upper_bound < 1e-20
    assert row.global_distinct_conditioning_probability_tends_to_one
    assert row.conditioned_expected_whitened_success_tends_to_zero
    assert row.source_typical_whitened_success_tends_to_zero


def test_report_terminates_branch_polar_decoder_without_rejecting_physical_pgm() -> None:
    report = run_sector_resolved_whitening_no_go()
    assert report.theorem.theorem_verified
    assert report.claim_gate["low_sector_coherent_alignment_escape_closed"]
    assert report.claim_gate["global_raw_concentration_escape_closed"]
    assert report.claim_gate[
        "natural_branch_polar_whitened_decoder_success_vanishes"
    ]
    assert report.claim_gate["branch_polar_whitened_decoder_rejected"]
    assert not report.claim_gate["actual_physical_pgm_rejected"]
    assert not report.claim_gate["alternate_multiplicity_whitening_rejected"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_no_go_artifact(tmp_path) -> None:
    path = tmp_path / "sector-whitening-no-go.json"
    payload = write_sector_resolved_whitening_no_go_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"]["global_branch_polar_whitening_no_go_count"] == 1
