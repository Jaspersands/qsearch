import pytest

from coset_hidden_involution_incidence_walk_boundary import (
    audit_incidence_walk,
    build_incidence_walk_report,
    incidence_matrix,
    incidence_walk_scaling_record,
    write_incidence_walk_report,
)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 1), (3, 1, 2), (4, 2, 1)),
)
def test_exact_biregular_linear_incidence_model(n, transpositions, copies):
    control = audit_incidence_walk(n, transpositions, copies)
    assert control.exact_incidence_model_verified
    assert control.minimum_source_column_degree == 2**copies
    assert control.maximum_source_column_degree == 2**copies
    assert control.minimum_physical_row_degree == control.candidate_count
    assert control.maximum_physical_row_degree == control.candidate_count
    assert control.maximum_distinct_candidate_column_intersection == 1
    assert control.maximum_same_candidate_distinct_column_intersection == 0
    assert control.source_gram_formula_residual < 1e-9
    assert control.physical_cayley_formula_residual < 1e-9
    assert control.discriminant_top_singular_value == pytest.approx(1.0)
    assert control.source_gram_top_eigenvalue == pytest.approx(
        control.candidate_count
    )
    assert control.normalized_source_gram_variance == pytest.approx(
        control.predicted_normalized_source_gram_variance
    )


def test_incidence_shape_matches_physical_and_source_counts():
    incidence, candidates = incidence_matrix(3, 1, 2)
    assert incidence.shape == (36, 27)
    assert len(candidates) == 27
    with pytest.raises(ValueError, match="positive"):
        incidence_matrix(3, 1, 0)


def test_walk_normalization_preserves_sqrt_candidate_barrier():
    rows = [
        incidence_walk_scaling_record(m) for m in (3, 4, 8, 16, 32, 64)
    ]
    assert all(row.retained_alternative_mass == 29 / 32 for row in rows)
    assert all(row.generic_polar_superpolynomial for row in rows)
    assert all(row.local_neighbor_oracle_available for row in rows)
    assert all(not row.structured_fourier_row_escape_ruled_out for row in rows)
    assert all(
        row.generic_bounded_polar_degree_lower_order == "Omega(sqrt(M))"
        for row in rows
    )
    assert rows[-1].retained_walk_singular_upper < rows[0].retained_walk_singular_lower

    with pytest.raises(ValueError, match="at least two"):
        incidence_walk_scaling_record(1)


def test_report_keeps_natural_index_erasure_and_structured_escape_open(tmp_path):
    report = build_incidence_walk_report(
        finite_specs=((3, 1, 1), (3, 1, 2)),
        scaling_half_degrees=(3, 4, 8, 16),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_incidence_normal_form_proved
    assert report.theorem.normalized_local_walk_access_constructed
    assert report.theorem.generic_incidence_qsvt_sqrt_M_obstruction_proved
    assert not report.theorem.black_box_index_erasure_reduction_proved
    assert not report.theorem.structured_fourier_row_transform_ruled_out
    assert not report.theorem.full_orbit_synthesis_polar_compiled
    assert report.claim_gate["generic_local_walk_sqrt_M_obstruction_proved"]
    assert not report.claim_gate["natural_problem_index_erasure_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_incidence_walk_report(
        tmp_path / "incidence-walk.json",
        finite_specs=((3, 1, 1),),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "incidence-walk-sqrt-M-obstruction-structured-row-transform-open"
    )
    assert payload["headline_metrics"][
        "black_box_index_erasure_reduction_count"
    ] == 0
