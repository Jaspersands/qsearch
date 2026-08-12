import pytest

from dcp_label_incidence_rank_width_no_go import (
    audit_binary_matrix_rank_tail,
    audit_incidence_cut_ranks,
    balanced_ideal_cut_rank_lower_bound,
    build_incidence_rank_width_report,
    gf2_matrix_rank,
    ideal_bipartite_cut_rank,
    incidence_cut_rank,
    incidence_rank_width_scaling_record,
    uniform_submatrix_failure_log2_upper_bound,
    write_incidence_rank_width_report,
)


def test_gf2_rank_and_bipartite_cut_identity_controls():
    assert gf2_matrix_rank((0b001, 0b010, 0b100), 3) == 3
    assert gf2_matrix_rank((0b011, 0b101, 0b110), 3) == 2
    assert ideal_bipartite_cut_rank(5, 7, 2, 3) == 5
    assert ideal_bipartite_cut_rank(5, 7, 5, 0) == 5


def test_cut_rank_is_sum_of_the_two_cross_submatrix_ranks():
    labels = (3, 5, 6)
    assert incidence_cut_rank(labels, 3, 0b111, 0) == 2
    assert incidence_cut_rank(labels, 3, 0, 0b111) == 2
    row = audit_incidence_cut_ranks(3, labels)
    assert row.balanced_cut_count > 0
    assert row.cut_rank_formula_failure_count == 0
    assert row.minimum_balanced_cut_rank >= 0


def test_ideal_balanced_cut_floor_matches_complete_bipartite_formula():
    for equation_count, variable_count in ((8, 8), (8, 12), (12, 8)):
        floor = balanced_ideal_cut_rank_lower_bound(
            equation_count,
            variable_count,
        )
        total = equation_count + variable_count
        for left_size in range((total + 2) // 3, 2 * total // 3 + 1):
            observed = []
            for equation_left in range(equation_count + 1):
                variable_left = left_size - equation_left
                if 0 <= variable_left <= variable_count:
                    observed.append(
                        ideal_bipartite_cut_rank(
                            equation_count,
                            variable_count,
                            equation_left,
                            variable_left,
                        )
                    )
            assert min(observed) >= floor


def test_exact_small_matrix_census_obeys_rank_count_tail():
    rows = [
        audit_binary_matrix_rank_tail(3, 4, 1),
        audit_binary_matrix_rank_tail(4, 4, 2),
    ]
    assert all(row.bound_verified for row in rows)
    assert all(
        row.exact_bad_probability
        <= row.rank_count_probability_upper_bound
        for row in rows
    )
    with pytest.raises(ValueError, match="deficit"):
        audit_binary_matrix_rank_tail(3, 3, 3)


def test_uniform_submatrix_union_beats_all_branch_choices():
    row = incidence_rank_width_scaling_record(512)
    assert row.uniform_submatrix_failure_log2_upper_bound < -0.1 * 512
    assert row.balanced_cut_rank_lower_bound >= 0.45 * 512
    assert row.rank_width_lower_bound == row.balanced_cut_rank_lower_bound
    assert row.treewidth_lower_bound == row.rank_width_lower_bound - 1
    assert row.uniform_linear_rank_width_certified
    assert uniform_submatrix_failure_log2_upper_bound(
        row.modulus_bits,
        row.register_count,
        row.selected_rank_deficit,
    ) == row.uniform_submatrix_failure_log2_upper_bound


def test_scaling_certifies_linear_rank_width_not_rewrite_hardness():
    rows = [
        incidence_rank_width_scaling_record(bits)
        for bits in (512, 1024, 2048, 4096)
    ]
    assert all(row.uniform_linear_rank_width_certified for row in rows)
    assert all(row.rank_width_fraction_of_modulus_bits >= 0.45 for row in rows)
    assert rows[-1].uniform_submatrix_failure_log2_upper_bound < -100_000


def test_report_keeps_auxiliary_rewrites_and_approximation_open(tmp_path):
    report = build_incidence_rank_width_report(
        scaling_modulus_bits=(512, 1024),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.random_incidence_linear_rank_width_proved
    assert report.theorem.arbitrary_branch_ordering_low_width_ruled_out
    assert not report.theorem.auxiliary_graph_rewrites_ruled_out
    assert not report.theorem.approximate_tensor_contraction_ruled_out
    assert not report.theorem.polynomial_subset_sum_solver_ruled_out
    assert not report.claim_gate[
        "natural_incidence_bounded_rank_width_route_alive"
    ]
    assert report.claim_gate["auxiliary_graph_rewrite_route_alive"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_incidence_rank_width_report(
        tmp_path / "incidence-rank-width.json",
        scaling_modulus_bits=(512, 1024),
    )
    assert payload["status"] == (
        "random-label-incidence-all-branch-width-linear"
    )
