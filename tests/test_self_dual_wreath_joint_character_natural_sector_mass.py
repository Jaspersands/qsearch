from __future__ import annotations

from fractions import Fraction

from self_dual_wreath_joint_character_natural_sector_mass import (
    annealed_tensor_target_law,
    audit_collision_conditioning,
    audit_fixed_source_sector_law,
    natural_sector_mass_scaling_record,
    orientation_averaged_target_law,
    partition_number,
    run_joint_character_natural_sector_mass,
)
from self_dual_wreath_plancherel_recoupling_stationarity import (
    plancherel_weights,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_fixed_source_D_trace_is_exact_dimension_weighted_orientation_law() -> None:
    law = orientation_averaged_target_law(THRESHOLD_LABELS)
    assert law == {
        (3,): Fraction(3, 16),
        (2, 1): Fraction(5, 8),
        (1, 1, 1): Fraction(3, 16),
    }
    control = audit_fixed_source_sector_law(
        3,
        THRESHOLD_LABELS,
        control_id="threshold",
    )
    assert control.exact_source_sector_law_verified
    assert control.maximum_projection_gram_trace_residual < 1e-9


def test_annealed_joint_target_law_is_exactly_plancherel_for_every_copy_control() -> None:
    for n, factor_count in ((2, 1), (3, 1), (3, 2), (4, 2), (5, 2)):
        assert annealed_tensor_target_law(n, factor_count) == plancherel_weights(n)


def test_collision_free_conditioning_obeys_target_tv_contraction() -> None:
    n4 = audit_collision_conditioning(4, 2)
    assert n4.exact_collision_free_probability == "89/1536"
    assert n4.target_total_variation_from_plancherel == "1/24"
    assert n4.target_tv_below_source_tv
    assert n4.exact_conditioning_contraction_verified

    n5 = audit_collision_conditioning(5, 2)
    assert n5.target_tv_below_source_tv
    assert n5.exact_conditioning_contraction_verified


def test_partition_count_tail_threshold_is_exact_and_fast() -> None:
    assert [partition_number(n) for n in (0, 1, 4, 8, 16, 32)] == [
        1,
        1,
        5,
        22,
        231,
        8349,
    ]
    record = natural_sector_mass_scaling_record(32)
    assert record.partition_count_decimal == "8349"
    assert record.low_dimension_threshold_log2 > 45
    assert record.unconditioned_low_dimension_mass_upper_bound == 1 / 8349
    assert record.high_dimension_natural_sector_mass_tends_to_one


def test_high_mass_canonical_normalization_is_superpolynomial() -> None:
    record = natural_sector_mass_scaling_record(512)
    assert record.low_dimension_threshold_log2 > 1800
    assert record.minimum_high_mass_canonical_normalization_log2 > 900
    assert record.minimum_high_mass_generic_analysis_degree_log2_lower_bound > 900
    assert not record.low_dimension_only_inverse_polynomial_decoder_possible
    assert not record.high_dimension_sector_information_proved
    assert not record.direct_structured_polar_ruled_out


def test_report_separates_natural_mass_from_hidden_information() -> None:
    report = run_joint_character_natural_sector_mass()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["joint_target_sector_law_identified"]
    assert report.claim_gate["annealed_joint_target_law_is_exact_plancherel"]
    assert report.claim_gate[
        "collision_free_conditioned_target_law_is_asymptotically_plancherel"
    ]
    assert report.claim_gate["natural_target_sector_mass_is_high_dimensional"]
    assert report.claim_gate[
        "canonical_sqrt_d_nu_normalization_hits_one_minus_o_one_mass"
    ]
    assert not report.claim_gate[
        "low_dimension_sectors_support_inverse_polynomial_mass_decoder"
    ]
    assert not report.claim_gate[
        "high_dimension_sectors_carry_extensive_hidden_information_proved"
    ]
    assert not report.claim_gate["direct_structured_polar_compiled"]
    assert not report.claim_gate["direct_structured_polar_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
