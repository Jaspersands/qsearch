from coset_hidden_involution_commuting_square_recoupling_boundary import (
    audit_group_square,
    audit_incidence_identity,
    build_commuting_square_recoupling_report,
    connection_cell_dimension,
    natural_connection_cell_scaling_record,
    odd_hyperoctahedral_branching_coefficient,
)


def test_group_factorization_square_is_symmetric():
    for half_degree in (2, 3):
        control = audit_group_square(half_degree)
        assert control.intersection_verified
        assert control.product_factorization_verified
        assert control.symmetric_commuting_square_verified
        assert control.equal_horizontal_index == 2 * half_degree


def test_odd_branching_restricts_through_one_box_removal():
    assert odd_hyperoctahedral_branching_coefficient(
        (3,),
        ((1,), ()),
    ) == 1
    assert odd_hyperoctahedral_branching_coefficient(
        (2, 1),
        ((1,), ()),
    ) == 1


def test_connection_cell_incidence_identity_is_exact():
    for half_degree in (2, 3, 4, 5):
        control = audit_incidence_identity(half_degree)
        assert control.equation_failure_count == 0
        assert control.horizontal_symmetric_branching_multiplicity_free
        assert control.horizontal_wreath_branching_multiplicity_free
        assert control.incidence_identity_verified


def test_representative_connection_cell_has_equal_path_dimensions():
    left, right = connection_cell_dimension(
        (6, 3, 1),
        ((3, 1), ()),
    )
    assert left == right
    assert left > 0


def test_natural_cells_inherit_superpolynomial_vertical_edges():
    record = natural_connection_cell_scaling_record(24)
    assert record.shape_adjacency_count_polynomial
    assert record.vertical_edge_dimension_superpolynomial
    assert (
        record.inherited_connection_cell_dimension_log2_lower_bound
        == record.natural_vertical_multiplicity_threshold_log2
    )
    assert not record.abstract_connection_is_polynomial_cell_compiler


def test_report_does_not_promote_abstract_connection_to_compiler():
    report = build_commuting_square_recoupling_report()
    assert report.theorem.all_rank_symmetric_commuting_square_proved
    assert report.theorem.exact_incidence_identity_proved
    assert report.theorem.abstract_unitary_connection_exists
    assert not report.theorem.polynomial_size_connection_cells_proved
    assert not report.theorem.vertical_multiplicity_factorization_compiled
    assert not report.theorem.source_aware_subduction_transform_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
