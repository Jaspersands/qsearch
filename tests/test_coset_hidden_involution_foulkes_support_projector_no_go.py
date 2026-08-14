import pytest

from coset_hidden_involution_foulkes_support_projector_no_go import (
    build_foulkes_support_projector_report,
    foulkes_projector_condition_record,
    write_foulkes_support_projector_report,
)


@pytest.mark.parametrize("block_count", (4, 8, 16, 32, 64, 128))
def test_explicit_two_row_twirl_eigenvalue_is_exponentially_small(block_count):
    row = foulkes_projector_condition_record(block_count)
    assert row.selected_partition == (2 * block_count + 1, block_count - 1)
    assert not row.selected_partition_has_even_rows
    assert 1 <= row.exact_invariant_multiplicity <= block_count
    assert int(row.exact_irrep_dimension_decimal) >= int(
        row.dimension_elementary_lower_bound_decimal
    )
    assert row.exponential_conditioning_witness_verified
    assert row.direct_partition_label_bypass_available
    assert not row.higher_row_structured_bypass_ruled_out


def test_condition_ratio_and_markov_degree_grow_exponentially():
    rows = [foulkes_projector_condition_record(a) for a in (8, 16, 32, 64)]
    assert all(
        right.support_condition_ratio_log2 > left.support_condition_ratio_log2
        for left, right in zip(rows, rows[1:])
    )
    assert rows[-1].markov_degree_lower_bound_log2 > 40
    with pytest.raises(ValueError, match="even"):
        foulkes_projector_condition_record(5)


def test_report_refutes_only_generic_twirl_threshold(tmp_path):
    report = build_foulkes_support_projector_report(block_counts=(4, 8, 16, 32))
    assert report.theorem.theorem_verified
    assert report.theorem.exact_twirl_spectrum_proved
    assert report.theorem.exponential_generic_threshold_degree_proved
    assert report.theorem.full_foulkes_support_projector_via_generic_qsvt_refuted
    assert report.theorem.direct_two_row_label_bypass_available
    assert not report.theorem.higher_row_structured_projector_ruled_out
    assert not report.theorem.residual_frame_norm_bounded
    assert report.claim_gate["generic_foulkes_support_qsvt_refuted"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_foulkes_support_projector_report(
        tmp_path / "foulkes-projector.json",
        block_counts=(4, 8, 16),
    )
    assert payload["status"] == (
        "generic-foulkes-support-qsvt-no-go-structured-projector-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
