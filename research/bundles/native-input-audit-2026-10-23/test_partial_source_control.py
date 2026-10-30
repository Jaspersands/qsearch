from partial_source_control import (anti_isometry_columns_three, partial_source_control,
                                    stabilizes_padded_graph)


def test_all_padded_gluings_have_exactly_the_same_stabilizer():
    result = partial_source_control()
    assert result["distinct_lagrangian_gluings"] == 24
    assert result["symplectic_group_elements_checked"] == 51840
    assert result["shared_stabilizer_size"] == 54
    assert result["stabilizer_disagreement_count"] == 0
    assert result["no_go_for_all_quantum_algorithms"] is False


def test_nontrivial_known_factor_action_does_not_stabilize_any_gluing():
    columns = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    assert not any(stabilizes_padded_graph(columns, f) for f in anti_isometry_columns_three())


def test_padding_line_scaling_preserves_every_gluing():
    columns = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 2, 0), (0, 0, 0, 2))
    assert all(stabilizes_padded_graph(columns, f) for f in anti_isometry_columns_three())
