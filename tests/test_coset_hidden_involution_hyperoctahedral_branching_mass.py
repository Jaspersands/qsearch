import pytest

from coset_hidden_involution_hyperoctahedral_branching_mass import (
    audit_even_branch_dimension_sums,
    branching_multiplicity_scaling_record,
    build_hyperoctahedral_branching_mass_report,
    even_hyperoctahedral_irrep_dimension_sum,
    low_branching_multiplicity_probability_log2_bound,
)


@pytest.mark.parametrize("half_degree", (2, 3, 4, 5, 6, 8))
def test_even_branch_dimension_sums_are_exact(half_degree: int) -> None:
    row = audit_even_branch_dimension_sums(half_degree)
    assert row.symmetric_irrep_dimension_sum == row.symmetric_involution_count
    assert row.even_hyperoctahedral_irrep_dimension_sum == row.even_dimension_convolution_sum
    assert row.even_hyperoctahedral_regular_dimension_sum == row.expected_even_hyperoctahedral_regular_dimension_sum
    assert row.dimension_sum_identities_verified


def test_even_dimension_sum_matches_small_closed_values() -> None:
    assert even_hyperoctahedral_irrep_dimension_sum(2) == 4
    assert even_hyperoctahedral_irrep_dimension_sum(3) == 10
    assert even_hyperoctahedral_irrep_dimension_sum(4) == 44


def test_low_multiplicity_bound_is_monotone_in_threshold() -> None:
    lower = low_branching_multiplicity_probability_log2_bound(16, 4.0)
    higher = low_branching_multiplicity_probability_log2_bound(16, 7.0)
    assert higher - lower == pytest.approx(3.0)


def test_natural_branching_multiplicity_becomes_jointly_huge() -> None:
    rows = [branching_multiplicity_scaling_record(m) for m in (16, 24, 32, 64)]
    assert rows[-1].joint_all_source_high_multiplicity_probability_lower_bound > 0.999999
    assert rows[-1].branching_multiplicity_threshold_log2 > rows[0].branching_multiplicity_threshold_log2
    assert rows[-1].missing_label_commutant_dimension_log2_lower_bound == pytest.approx(
        2 * rows[-1].branching_multiplicity_threshold_log2
    )
    assert all(row.threshold_superpolynomial for row in rows)
    assert all(not row.K_qft_resolves_branching_multiplicity_copy for row in rows)
    assert all(not row.paired_young_graph_recursion_compiled for row in rows)


def test_report_localizes_missing_labels_without_claiming_hardness() -> None:
    report = build_hyperoctahedral_branching_mass_report()
    assert report.headline_metrics["dimension_sum_control_failure_count"] == 0
    assert report.claim_gate["exact_even_branch_joint_law_proved"] is True
    assert report.claim_gate["natural_mass_in_superpolynomial_branching_proved"] is True
    assert report.claim_gate["K_qft_resolves_branching_missing_labels"] is False
    assert report.claim_gate["paired_young_graph_recursion_compiled"] is False
    assert report.claim_gate["source_aware_normalized_subduction_transform_compiled"] is False
    assert report.claim_gate["binary_hidden_involution_detector_constructed"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
