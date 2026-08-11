import math

import pytest

from coset_hidden_involution_support_span_reduction import (
    audit_support_span_control,
    build_hidden_involution_support_span_report,
    support_span_scaling_record,
    support_span_sufficient_copies,
    write_hidden_involution_support_span_report,
)


def test_support_span_sample_count_inverts_rank_union_bound():
    copies = support_span_sufficient_copies(105, 0.1)
    assert copies == math.ceil(math.log2(1050))
    assert 105 / 2**copies <= 0.1
    with pytest.raises(ValueError, match="null_false_positive"):
        support_span_sufficient_copies(10, 1.0)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 1), (3, 1, 2), (3, 1, 3), (4, 2, 2)),
)
def test_support_span_has_perfect_completeness_and_rank_bounded_null_error(
    n, transpositions, copies
):
    row = audit_support_span_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.minimum_alternative_acceptance_probability == pytest.approx(1.0)
    assert row.maximum_alternative_acceptance_residual < 1e-9
    assert (
        row.exact_null_false_positive_probability
        <= row.rank_union_false_positive_upper_bound + 1e-9
    )
    assert row.support_span_rank <= row.sum_of_candidate_support_ranks
    assert row.synthesis_frame_identity_residual < 1e-9
    assert row.equal_prior_support_test_success_probability <= (
        row.equal_prior_helstrom_success_probability + 1e-9
    )


def test_scaling_keeps_sample_theorem_separate_from_range_compiler():
    row = support_span_scaling_record(128)
    assert row.certified_null_false_positive_upper_bound <= 0.1
    assert row.alternative_completeness == 1.0
    assert row.sample_count_polynomial_in_group_register_length
    assert not row.least_positive_frame_eigenvalue_certified
    assert not row.polynomial_range_projector_compiler_known


def test_report_recovers_prior_art_without_promoting_algorithm(tmp_path):
    report = build_hidden_involution_support_span_report(
        finite_specs=((3, 1, 1), (3, 1, 2), (4, 2, 2)),
        scaling_n_values=(16, 32, 64),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.perfect_alternative_completeness_proved
    assert report.theorem.logarithmic_sample_upper_bound_proved
    assert not report.theorem.inverse_polynomial_positive_frame_gap_proved
    assert not report.theorem.polynomial_range_projector_compiler_constructed
    assert not report.claim_gate["sample_complexity_result_new_to_literature"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_hidden_involution_support_span_report(
        tmp_path / "support.json",
        finite_specs=((3, 1, 1), (3, 1, 2)),
        scaling_n_values=(16, 32),
    )
    assert payload["status"] == (
        "published-support-span-test-reduced-to-range-polar-compiler-open"
    )

