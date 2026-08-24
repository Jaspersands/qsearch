from __future__ import annotations

import math

import numpy as np

from self_dual_wreath_branch_character_raw_concentration_central_fourier_bridge import (
    audit_central_raw_concentration,
    central_compressed_isotypic_block,
    natural_bulk_concentration_scaling,
    run_central_raw_concentration_bridge,
)


SINGLE = (((3,), (2, 1)),)
THRESHOLD = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def _sector(control, partition):
    return next(row for row in control.sector_controls if row.partition == partition)


def test_central_compressions_are_positive_contractions() -> None:
    for target in ((3,), (2, 1), (1, 1, 1)):
        block = central_compressed_isotypic_block(target, THRESHOLD)
        eigenvalues = np.linalg.eigvalsh(block)
        assert eigenvalues[0] >= -1e-9
        assert eigenvalues[-1] <= 1 + 1e-9


def test_actual_right_multiplier_gram_uses_central_compression() -> None:
    control = audit_central_raw_concentration("threshold", THRESHOLD)
    assert control.exact_central_fourier_bridge_verified
    assert control.maximum_multiplier_gram_identity_residual < 1e-9
    assert control.global_concentration_residual < 1e-9


def test_noncentral_orientation_block_substitution_is_rejected() -> None:
    control = audit_central_raw_concentration("single", SINGLE)
    standard = _sector(control, (2, 1))
    assert not standard.naive_noncentral_F_substitution_valid
    assert standard.naive_noncentral_F_gram_residual > 0.1
    assert control.naive_noncentral_F_failure_count >= 1


def test_native_sector_law_equals_central_trace_law() -> None:
    control = audit_central_raw_concentration("threshold", THRESHOLD)
    assert math.isclose(control.native_sector_probability_sum, 1.0)
    assert control.maximum_trace_bridge_residual < 1e-9
    assert control.maximum_native_sector_probability_residual < 1e-9
    assert math.isclose(_sector(control, (3,)).native_sector_probability, 3 / 16)
    assert math.isclose(_sector(control, (2, 1)).native_sector_probability, 5 / 8)
    assert math.isclose(
        _sector(control, (1, 1, 1)).native_sector_probability,
        3 / 16,
    )


def test_dimension_weighted_sector_concentrations_are_exact() -> None:
    single = audit_central_raw_concentration("single", SINGLE)
    assert math.isclose(single.raw_convolution_concentration, 3.0)
    assert math.isclose(_sector(single, (3,)).raw_sector_concentration, 3.0)
    assert math.isclose(_sector(single, (2, 1)).raw_sector_concentration, 0.75)

    threshold = audit_central_raw_concentration("threshold", THRESHOLD)
    assert math.isclose(threshold.raw_convolution_concentration, 1.5)
    assert math.isclose(
        _sector(threshold, (2, 1)).raw_sector_concentration,
        1.125,
    )


def test_natural_high_dimensional_bulk_cannot_supply_whitening_rescue() -> None:
    row = natural_bulk_concentration_scaling(512)
    assert row.natural_high_dimension_sector_mass_tends_to_one
    assert row.high_sector_whitening_correction_tends_to_zero
    assert row.log2_high_sector_whitening_correction_upper_bound < -100
    assert not row.low_sector_coherent_alignment_bounded
    assert not row.full_branch_polar_decoder_no_go_proved


def test_report_localizes_without_overclaiming_decoder_no_go() -> None:
    report = run_central_raw_concentration_bridge()
    assert report.theorem.theorem_verified
    assert report.claim_gate["raw_convolution_central_fourier_block_identified"]
    assert report.claim_gate["noncentral_orientation_block_substitution_rejected"]
    assert report.claim_gate["native_raw_sector_mass_matches_joint_D_nu_mass"]
    assert not report.claim_gate["high_dimensional_bulk_can_rescue_branch_polar_whitening"]
    assert not report.claim_gate["low_dimensional_coherent_alignment_bounded"]
    assert not report.claim_gate["full_branch_polar_decoder_rejected"]
    assert not report.claim_gate["actual_physical_pgm_rejected"]
    assert not report.claim_gate["speedup_claim_allowed"]
