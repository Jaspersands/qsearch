import pytest

from self_dual_wreath_separating_surface_target_mixing import (
    audit_direct_surface_count,
    audit_nonseparating_surface_target,
    audit_separating_surface_target,
    audit_unconditioned_surface_target,
    run_separating_surface_target_mixing,
    nonseparating_surface_tv_bound,
    separating_surface_tv_bound,
    surface_mixing_scaling_record,
    unconditioned_surface_tv_bound,
)


def test_direct_surface_counts_match_frobenius_character_density() -> None:
    control = audit_direct_surface_count(3, 1, 2)
    assert control.exact_surface_homomorphism_count == control.frobenius_surface_homomorphism_count
    assert control.maximum_direct_to_character_probability_residual < 1e-15
    assert control.direct_frobenius_formula_verified


def test_genus_two_handle_target_recovers_exact_s3_standard_bias() -> None:
    control = audit_separating_surface_target(3, 1, 1)
    assert control.exact_density_probability_sum == "1"
    assert control.exact_odd_density_mass == "0"
    assert control.standard_normalized_character_expectation == pytest.approx(0.5)
    assert control.exact_density_and_bound_verified


def test_surface_tv_bounds_dominate_exact_finite_distributions() -> None:
    for n in range(3, 9):
        for genus in (1, 2, 3):
            row = audit_unconditioned_surface_target(n, genus)
            assert row.exact_total_variation_from_uniform_alternating <= row.total_variation_upper_bound + 1e-12
            assert row.total_variation_upper_bound == pytest.approx(
                unconditioned_surface_tv_bound(n, genus)
            )
        for left, right in ((1, 1), (1, 2), (2, 2)):
            row = audit_separating_surface_target(n, left, right)
            assert row.exact_total_variation_from_uniform_alternating <= row.total_variation_upper_bound + 1e-12
            assert row.total_variation_upper_bound == pytest.approx(
                separating_surface_tv_bound(n, left, right)
            )


def test_genus_one_is_uniform_worst_case_and_bounds_decay() -> None:
    n = 12
    assert unconditioned_surface_tv_bound(n, 3) < unconditioned_surface_tv_bound(n, 2) < unconditioned_surface_tv_bound(n, 1)
    assert separating_surface_tv_bound(n, 2, 2) < separating_surface_tv_bound(n, 1, 2) < separating_surface_tv_bound(n, 1, 1)
    assert nonseparating_surface_tv_bound(n, 4) < nonseparating_surface_tv_bound(n, 3) < nonseparating_surface_tv_bound(n, 2)
    records = [surface_mixing_scaling_record(value) for value in range(8, 31)]
    assert all(
        later.genus_uniform_nonsign_character_upper_bound
        < earlier.genus_uniform_nonsign_character_upper_bound
        for earlier, later in zip(records, records[1:])
    )


def test_nonseparating_simple_curves_mix_to_uniform_symmetric_group() -> None:
    for n in range(3, 9):
        for genus in (2, 3, 4):
            row = audit_nonseparating_surface_target(n, genus)
            assert row.exact_density_probability_sum == "1"
            assert row.exact_total_variation_from_uniform_symmetric <= row.total_variation_upper_bound + 1e-12
            assert row.maximum_nontrivial_normalized_character_expectation <= 2 * row.exact_total_variation_from_uniform_symmetric + 1e-12
            assert row.exact_density_and_bound_verified


def test_report_dequantizes_surface_targets_but_not_all_marked_words() -> None:
    report = run_separating_surface_target_mixing()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["simple_surface_target_class_dequantized"] is True
    assert report.claim_gate["all_simple_surface_target_characters_vanish"] is True
    assert report.claim_gate["all_nonsign_surface_target_characters_vanish"] is True
    assert report.claim_gate["all_pressure_saturating_marked_targets_are_surface_curves"] is False
    assert report.claim_gate["non_surface_target_characters_controlled"] is False
    assert report.claim_gate["natural_component_M4_positive"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
