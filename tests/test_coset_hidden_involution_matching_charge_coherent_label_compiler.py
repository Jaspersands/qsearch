import itertools
import math

from coset_hidden_involution_matching_charge_coherent_label_compiler import (
    audit_matching_charge_index,
    build_coherent_label_compiler_report,
    coherent_label_scaling_record,
    matching_charge_term_count,
    matching_charge_term_from_index,
    rank_four_subset,
    unrank_four_subset,
    write_coherent_label_compiler_report,
)


def test_four_subset_combinadic_round_trip():
    for size in range(4, 13):
        subsets = tuple(itertools.combinations(range(size), 4))
        assert len(subsets) == math.comb(size, 4)
        for rank, subset in enumerate(subsets):
            assert rank_four_subset(subset, size) == rank
            assert unrank_four_subset(rank, size) == subset


def test_matching_charge_index_is_bijective_and_inverse_closed():
    for half_degree in (4, 5, 6):
        row = audit_matching_charge_index(half_degree)
        assert row.indexed_term_count == matching_charge_term_count(half_degree)
        assert row.distinct_term_count == row.expected_term_count
        assert row.local_orbit_size == 192
        assert row.maximum_moved_point_count <= 6
        assert row.inverse_closed
        assert row.subset_rank_unrank_verified
        assert row.term_index_is_bijective


def test_term_index_embeds_only_a_constant_support_permutation():
    for half_degree in (4, 5, 6):
        total = matching_charge_term_count(half_degree)
        probes = (0, 1, 191, total // 2, total - 1)
        for index in probes:
            permutation = matching_charge_term_from_index(half_degree, index)
            assert len(permutation) == 2 * half_degree
            assert sum(i != value for i, value in enumerate(permutation)) <= 6


def test_coherent_phase_label_query_bound_is_polynomial():
    rows = [coherent_label_scaling_record(value) for value in (11, 16, 32, 64)]
    assert all(row.query_bound_polynomial_in_half_degree for row in rows)
    assert all(row.target_phase_precision > 0 for row in rows)
    assert all(row.good_source_mass_lower_bound > 0 for row in rows)
    assert all(row.standalone_label_distribution_likelihood_blind for row in rows)
    # The proved upper bound scales as m^(9/2) up to fixed logarithmic precision.
    ratios = [
        row.SELECT_query_upper_bound / row.half_degree**4.5 for row in rows
    ]
    assert max(ratios) / min(ratios) < 1.01


def test_report_compiles_access_without_promoting_a_detector():
    report = build_coherent_label_compiler_report()
    theorem = report.theorem
    assert theorem.exact_uniform_orbit_indexing_compiled
    assert theorem.normalization_one_Hermitian_block_encoding_compiled
    assert theorem.coherent_inverse_polynomial_precision_D_label_compiled
    assert theorem.conditional_natural_separated_direction_resolvable
    assert not theorem.hyperoctahedral_subduction_required_for_D_label
    assert not theorem.standalone_D_measurement_is_detector
    assert not theorem.all_copy_target_coupled_use_compiled
    assert not theorem.full_joint_minimum_gap_proved
    assert not theorem.residual_multiplicity_bounded
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_live_coherent_label_report_is_json_serializable(tmp_path):
    output = tmp_path / "coherent-D-label.json"
    payload = write_coherent_label_compiler_report(output)
    assert output.exists()
    assert payload["status"] == (
        "coherent-natural-D-label-compiled-target-recoupling-open"
    )
    assert payload["claim_gate"]["coherent_inverse_polynomial_D_label_compiled"]
    assert payload["claim_gate"]["standalone_D_measurement_likelihood_blind"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
