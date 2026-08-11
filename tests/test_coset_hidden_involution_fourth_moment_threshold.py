import math

import pytest

from coset_hidden_involution_binary_decision_reduction import (
    involution_conjugacy_class,
)
from coset_hidden_involution_fourth_moment_threshold import (
    UNIVERSAL_FOURTH_MOMENT_BOUND,
    UNIVERSAL_TRACE_DISTANCE_CONSTANT,
    audit_fourth_moment_finite_control,
    audit_involution_class_relations,
    build_hidden_involution_fourth_moment_report,
    covered_identity_pattern_count,
    exact_fourth_moment_from_relations,
    fourth_moment_pattern_polynomials,
    fourth_moment_threshold_scaling_record,
    identity_subword_masks,
    universal_fourth_moment_upper_bound,
    write_hidden_involution_fourth_moment_report,
)


def test_identity_pattern_polynomials_match_explicit_involution_tuples():
    transpositions = involution_conjugacy_class(3, 1)
    first, second = transpositions[:2]
    polynomials = fourth_moment_pattern_polynomials(3)

    all_equal_masks = identity_subword_masks((first,) * 4)
    assert covered_identity_pattern_count(all_equal_masks, 3) == (
        polynomials["all_equal"]
    )

    alternating_masks = identity_subword_masks(
        (first, second, first, second)
    )
    assert 15 not in alternating_masks
    assert covered_identity_pattern_count(alternating_masks, 3) == (
        polynomials["alternating_noncommuting_pairs"]
    )


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 2), (4, 1, 3), (4, 2, 2), (5, 2, 4), (6, 3, 4)),
)
def test_relation_formula_matches_direct_identity_pattern_enumeration(
    n, transpositions, copies
):
    row = audit_fourth_moment_finite_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.relation_formula_pattern_residual < 1e-12
    assert row.interpolation_bound_respected
    if row.dense_matrix_residual is not None:
        assert row.dense_matrix_residual < 1e-9
        assert (
            row.dense_helstrom_trace_distance
            >= row.interpolation_trace_distance_lower_bound - 1e-9
        )


def test_relation_statistics_charge_commutation_triples_and_energy_exactly():
    s4_matching = audit_involution_class_relations(4, 2)
    assert s4_matching.conjugacy_class_size == 3
    assert s4_matching.commuting_class_neighbors_per_element == 3
    assert s4_matching.ordered_triple_identity_count == 6
    assert s4_matching.ordered_four_identity_count == 21
    assert s4_matching.full_relation_without_repeated_pair_count == 0
    assert exact_fourth_moment_from_relations(s4_matching, 2) == pytest.approx(
        49 / 9
    )

    s5_partial = audit_involution_class_relations(5, 2)
    assert s5_partial.conjugacy_class_size == 15
    assert s5_partial.full_relation_without_repeated_pair_count == 240


def test_universal_log_class_threshold_has_constant_fourth_and_l1_bounds():
    for size in (2, 3, 15, 105, 10_000, 10**30):
        copies = math.ceil(math.log2(size))
        fourth = float(universal_fourth_moment_upper_bound(size, copies))
        assert fourth < UNIVERSAL_FOURTH_MOMENT_BOUND

    row = fourth_moment_threshold_scaling_record(128)
    assert row.threshold_copy_count == math.ceil(
        math.log2(row.conjugacy_class_size)
    )
    assert row.threshold_second_moment >= 0.5
    assert row.relation_count_fourth_moment_upper_bound < 55
    assert (
        row.certified_trace_distance_lower_bound
        >= UNIVERSAL_TRACE_DISTANCE_CONSTANT
    )
    assert row.logarithmic_copy_information_sufficiency_proved
    assert not row.polynomial_block_sign_compiler_known


def test_report_promotes_information_threshold_but_not_algorithm_claim(tmp_path):
    report = build_hidden_involution_fourth_moment_report(
        finite_specs=((3, 1, 2), (4, 2, 2), (5, 2, 4)),
        scaling_n_values=(8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.constant_trace_distance_at_log_class_size_proved
    assert report.theorem.theta_log_class_copy_complexity_proved
    assert not report.theorem.efficient_helstrom_compiler_constructed
    assert report.claim_gate["information_theoretic_binary_measurement_exists"]
    assert not report.claim_gate["sample_complexity_result_new_to_literature"]
    assert not report.claim_gate["graph_isomorphism_algorithm_constructed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_hidden_involution_fourth_moment_report(
        tmp_path / "fourth.json",
        finite_specs=((3, 1, 2), (4, 2, 2)),
        scaling_n_values=(8, 16),
    )
    assert payload["status"] == (
        "theta-log-class-information-threshold-proved-compiler-open"
    )
