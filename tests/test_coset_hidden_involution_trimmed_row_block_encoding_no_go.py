import math

from coset_hidden_involution_trimmed_row_block_encoding_no_go import (
    audit_edge_state_block_encoding,
    build_trimmed_row_block_encoding_report,
    trimmed_row_normalization_scaling_record,
    write_trimmed_row_block_encoding_report,
)


def test_normalized_edge_isometries_give_exact_discriminant():
    for degree, transpositions, copies in ((3, 1, 1), (3, 1, 2), (4, 2, 1)):
        row = audit_edge_state_block_encoding(degree, transpositions, copies)
        assert row.coherent_edge_states_block_encode_A_not_Z
        assert row.edge_count == row.physical_row_count * row.physical_row_degree
        assert row.edge_count == row.source_column_count * row.source_column_degree
        assert row.maximum_row_isometry_residual < 1e-12
        assert row.maximum_column_isometry_residual < 1e-12
        assert row.discriminant_overlap_residual < 1e-12


def test_discriminant_gram_is_Z_over_candidate_count():
    rows = [
        audit_edge_state_block_encoding(*spec)
        for spec in ((3, 1, 1), (3, 1, 2), (4, 2, 1))
    ]
    assert all(row.normalized_gram_identity_residual < 1e-12 for row in rows)
    assert all(
        row.unnormalized_likelihood_scale_ratio == row.candidate_count
        for row in rows
    )


def test_natural_singular_scale_retains_square_root_candidate_cost():
    rows = [
        trimmed_row_normalization_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    assert all(row.coherent_row_state_preparation_polynomial for row in rows)
    assert all(row.pairwise_kernel_evaluation_polynomial for row in rows)
    assert all(
        not row.canonicalizer_or_QFT_changes_candidate_normalization
        for row in rows
    )
    assert all(not row.unnormalized_Z_fast_forward_compiled for row in rows)
    assert all(
        math.isclose(
            row.generic_polar_query_log2_lower_order,
            row.row_degree_log2 / 2,
        )
        for row in rows
    )
    assert all(
        right.generic_polar_query_log2_lower_order
        > left.generic_polar_query_log2_lower_order
        for left, right in zip(rows, rows[1:])
    )


def test_report_closes_generic_kernel_linear_algebra_without_overclaim():
    report = build_trimmed_row_block_encoding_report()
    theorem = report.theorem
    assert theorem.theorem_verified
    assert theorem.exact_edge_state_block_encoding_proved
    assert theorem.trimmed_row_kernel_block_encoding_is_A_proved
    assert not theorem.canonicalization_or_QFT_removes_M_normalization
    assert not theorem.generic_kernel_quantum_linear_algebra_is_polynomial
    assert not theorem.direct_analytically_normalized_transform_ruled_out
    assert not theorem.unnormalized_Z_fast_forward_compiled
    assert not theorem.speedup_claim_allowed


def test_claim_gate_keeps_only_direct_analytic_transform_open():
    report = build_trimmed_row_block_encoding_report()
    assert report.claim_gate["coherent_trimmed_row_access_compiled"]
    assert report.claim_gate[
        "coherent_trimmed_row_access_block_encodes_A_equals_Z_over_M"
    ]
    assert not report.claim_gate["canonicalizer_or_G_QFT_improves_normalization"]
    assert not report.claim_gate["generic_kernel_SVT_is_polynomial"]
    assert not report.claim_gate["direct_analytically_normalized_transform_ruled_out"]


def test_live_block_encoding_report_is_json_serializable(tmp_path):
    output = tmp_path / "trimmed-row-block-encoding.json"
    payload = write_trimmed_row_block_encoding_report(output)
    assert output.exists()
    assert payload["status"] == (
        "trimmed-row-coherent-access-retains-Z-over-M-normalization"
    )
    assert not payload["claim_gate"]["speedup_claim_allowed"]
