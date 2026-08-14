import pytest

from coset_hidden_involution_binary_decision_reduction import (
    involution_transposition_count,
)
from coset_hidden_involution_pair_polar_holonomy_no_go import (
    audit_pair_polar_holonomy,
    build_pair_polar_holonomy_report,
    embedding_record,
    fixed_point_free_s3_embedding,
    write_pair_polar_holonomy_report,
)


def test_exact_s3_triangle_has_nontrivial_pair_polar_holonomy():
    control = audit_pair_polar_holonomy()
    assert control.nontrivial_holonomy_verified
    assert control.pair_rotation_orders == (3, 3, 3)
    assert control.starting_plus_dimension == 3
    assert control.positive_holonomy_multiplicity == 1
    assert control.negative_holonomy_multiplicity == 2
    assert control.maximum_pair_polar_support_residual < 1e-9
    assert control.loop_starting_space_invariance_residual < 1e-9
    assert control.loop_unitarity_residual < 1e-9
    assert control.maximum_holonomy_eigenvalue_residual < 1e-9
    assert control.loop_distance_from_identity == pytest.approx(2.0)
    assert control.direct_vs_two_edge_path_operator_distance == pytest.approx(
        2.0
    )


@pytest.mark.parametrize("n", (6, 8, 16, 32, 64))
def test_regular_s3_holonomy_embeds_as_fixed_point_free_involutions(n):
    generators = fixed_point_free_s3_embedding(n)
    assert len(generators) == 3
    assert all(
        involution_transposition_count(generator) == n // 2
        for generator in generators
    )

    row = embedding_record(n)
    assert row.embedded_subgroup_order == 6
    assert row.fixed_point_free_generator_count == 3
    assert row.pair_product_orders == (3, 3, 3)
    assert row.one_copy_positive_holonomy_multiplicity == 1
    assert row.one_copy_negative_holonomy_multiplicity == 2
    assert 0.49 <= row.tensor_negative_holonomy_fraction <= 0.51
    assert not row.path_independent_pair_alignment_possible
    assert not row.holonomy_aware_global_transform_ruled_out


def test_fixed_point_free_embedding_rejects_invalid_degree():
    with pytest.raises(ValueError, match="even and at least six"):
        fixed_point_free_s3_embedding(5)
    with pytest.raises(ValueError, match="even and at least six"):
        fixed_point_free_s3_embedding(7)


def test_report_refutes_only_path_independent_pair_alignment(tmp_path):
    report = build_pair_polar_holonomy_report(
        embedding_n_values=(6, 8, 16, 32)
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_nontrivial_triangle_holonomy_proved
    assert report.theorem.all_n_fixed_point_free_embedding_proved
    assert report.theorem.tensor_extensive_holonomy_proved
    assert report.theorem.path_independent_pair_alignment_refuted
    assert not report.theorem.holonomy_aware_global_polar_refuted
    assert not report.theorem.mrs_sieve_separation_proved
    assert report.claim_gate["path_independent_pair_alignment_refuted"]
    assert report.claim_gate["tensor_holonomy_extensive"]
    assert not report.claim_gate["holonomy_resolver_constructed"]
    assert not report.claim_gate["full_orbit_synthesis_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_pair_polar_holonomy_report(
        tmp_path / "pair-polar-holonomy.json",
        embedding_n_values=(6, 8),
    )
    assert payload["status"] == (
        "pair-polar-connection-nonflat-holonomy-aware-global-route-open"
    )
    assert payload["headline_metrics"][
        "path_independent_pair_alignment_count"
    ] == 0
