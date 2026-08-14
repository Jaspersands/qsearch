import math
from fractions import Fraction

import pytest

from coset_hidden_involution_source_deflation_no_go import (
    audit_source_deflation_control,
    build_source_deflation_no_go_report,
    full_quantum_chi_square,
    source_chi_square,
    source_deflation_scaling_record,
    source_likelihood_second_moment,
    weighted_conditional_chi_square,
    write_source_deflation_no_go_report,
)


def test_exact_source_and_conditional_chi_square_identities():
    assert source_chi_square(15, 3) == Fraction(16**3 - 15**3, 15**3)
    assert full_quantum_chi_square(15, 3) == Fraction(7, 15)
    assert weighted_conditional_chi_square(15, 3) == (
        full_quantum_chi_square(15, 3) - source_chi_square(15, 3)
    )
    assert source_likelihood_second_moment(15, 3) == (
        1 + source_chi_square(15, 3)
    )
    assert weighted_conditional_chi_square(15, 1) == 0

    with pytest.raises(ValueError, match="positive"):
        source_chi_square(0, 2)
    with pytest.raises(ValueError, match="positive"):
        full_quantum_chi_square(3, 0)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 2), (3, 1, 3), (4, 1, 2), (4, 2, 2)),
)
def test_exact_fourier_blocks_verify_source_law_and_chain_rule(
    n, transpositions, copies
):
    row = audit_source_deflation_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.source_chi_square_residual < 1e-12
    assert row.conditional_chain_rule_residual < 1e-10
    assert row.maximum_block_trace_identity_residual < 1e-10
    assert row.maximum_conditional_state_trace_residual < 1e-10
    assert row.exact_source_total_variation <= (
        row.source_total_variation_chi_square_upper_bound + 1e-12
    )
    assert row.weighted_conditional_chi_square > 0
    assert row.conditional_share_of_full_chi_square > 0


def test_threshold_source_transcript_is_negligible():
    rows = [source_deflation_scaling_record(n) for n in (16, 32, 64, 128)]
    assert all(
        row.copy_count
        == math.ceil(math.log2(4 * row.conjugacy_class_size))
        for row in rows
    )
    assert all(
        row.weak_source_total_variation_upper_bound < 0.01 for row in rows
    )
    assert all(
        not row.source_only_bounded_error_binary_test_possible for row in rows
    )
    assert rows[-1].weak_source_total_variation_upper_bound < rows[0].weak_source_total_variation_upper_bound
    assert all(
        row.conditional_share_of_full_chi_square > 0.999 for row in rows
    )


def test_exceptional_source_deletion_leaves_constant_low_spectrum_mass():
    row = source_deflation_scaling_record(32)
    assert row.typical_alternative_source_mass == 0.75
    assert row.typical_source_frame_trace_times_class_size < 1.0
    assert row.low_spectrum_eigenvalue_times_class_size <= 5.0
    assert (
        row.simultaneous_typical_source_and_low_spectrum_mass_lower_bound
        == 0.5
    )
    assert not row.exceptional_source_deflation_removes_low_spectrum_burden
    assert not row.coherent_within_block_rescaling_ruled_out

    with pytest.raises(ValueError, match="even"):
        source_deflation_scaling_record(15)
    with pytest.raises(ValueError, match="tail_probability"):
        source_deflation_scaling_record(16, tail_probability=0.5)


def test_report_closes_source_deflation_but_preserves_fused_escape(tmp_path):
    report = build_source_deflation_no_go_report(
        finite_specs=((3, 1, 2), (4, 2, 2)),
        scaling_n_values=(16, 32, 64),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_source_chi_square_proved
    assert report.theorem.source_only_threshold_test_refuted
    assert report.theorem.exceptional_source_deflation_refuted
    assert report.theorem.conditional_signal_localization_proved
    assert not report.theorem.coherent_within_block_rescaling_refuted
    assert not report.theorem.arbitrary_circuit_lower_bound_proved
    assert report.claim_gate["conditional_multiplicity_signal_required"]
    assert not report.claim_gate[
        "fused_multiplicity_support_transform_constructed"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_source_deflation_no_go_report(
        tmp_path / "source-deflation.json",
        finite_specs=((3, 1, 2),),
        scaling_n_values=(16, 32),
    )
    assert payload["status"] == (
        "weak-source-deflation-refuted-fused-multiplicity-transform-open"
    )
    assert payload["headline_metrics"]["finite_control_failure_count"] == 0
