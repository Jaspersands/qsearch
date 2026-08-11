import math
from fractions import Fraction

import pytest

from coset_hidden_involution_query_separation_boundary import (
    DEFAULT_TARGET_BAYES_ADVANTAGE,
    audit_classical_query_control,
    build_hidden_involution_query_separation_report,
    hidden_candidates_exposed_by_queries,
    minimum_classical_queries_for_bayes_advantage,
    minimum_quantum_copies_from_chi_square,
    query_separation_scaling_record,
    write_hidden_involution_query_separation_report,
)
from coset_hidden_involution_binary_decision_reduction import (
    involution_conjugacy_class,
)


def test_query_pairs_expose_at_most_one_promised_hidden_element_each():
    conjugacy_class = involution_conjugacy_class(4, 2)
    identity = tuple(range(4))
    queries = (identity, *conjugacy_class[:2])
    exposed = hidden_candidates_exposed_by_queries(queries, conjugacy_class)
    assert len(exposed) <= math.comb(len(queries), 2)
    assert set(exposed).issubset(set(conjugacy_class))
    with pytest.raises(ValueError, match="distinct"):
        hidden_candidates_exposed_by_queries(
            (identity, identity), conjugacy_class
        )


@pytest.mark.parametrize(
    ("n", "transpositions", "queries"),
    ((3, 1, 2), (3, 1, 3), (4, 1, 4), (4, 2, 3), (5, 2, 6)),
)
def test_finite_collision_probability_obeys_adaptive_pair_boundary(
    n, transpositions, queries
):
    row = audit_classical_query_control(n, transpositions, queries)
    assert row.exact_collision_candidate_identity_verified
    assert row.pair_bound_verified
    assert (
        row.exact_uniform_hidden_collision_probability
        <= row.pair_union_upper_bound + 1e-12
    )
    assert row.exposed_hidden_involution_count <= row.queried_pair_count


def test_exact_classical_and_quantum_query_lower_bound_inversions():
    size = 10_000
    advantage = Fraction(1, 100)
    classical = minimum_classical_queries_for_bayes_advantage(size, advantage)
    assert classical * (classical - 1) >= 4 * advantage * size
    assert (classical - 1) * (classical - 2) < 4 * advantage * size

    quantum = minimum_quantum_copies_from_chi_square(size, advantage)
    assert 2**quantum >= 1 + 16 * advantage * advantage * size
    assert 2 ** (quantum - 1) < 1 + 16 * advantage * advantage * size


def test_fixed_point_free_scaling_certifies_query_but_not_time_separation():
    row = query_separation_scaling_record(32)
    assert row.target_equal_prior_bayes_advantage == pytest.approx(
        float(DEFAULT_TARGET_BAYES_ADVANTAGE)
    )
    assert row.quantum_threshold_query_count == math.ceil(
        row.log2_conjugacy_class_size
    )
    assert row.classical_randomized_query_lower_bound > (
        row.quantum_threshold_query_count
    )
    assert row.exponential_query_separation_certified
    assert not row.polynomial_time_quantum_measurement_known
    assert not row.natural_input_reduction_known


def test_report_keeps_oracle_query_gap_below_speedup_gate(tmp_path):
    report = build_hidden_involution_query_separation_report(
        finite_specs=((3, 1, 2), (4, 2, 3), (5, 2, 6)),
        scaling_n_values=(16, 32, 64),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.adaptive_classical_coupling_proved
    assert report.theorem.exponential_query_separation_proved
    assert report.theorem.quantum_log_class_query_upper_bound_proved
    assert not report.theorem.arbitrary_coherent_quantum_query_lower_bound_proved
    assert not report.theorem.polynomial_time_quantum_algorithm_constructed
    assert report.claim_gate["exponential_oracle_query_separation_proved"]
    assert not report.claim_gate["oracle_query_separation_new_to_literature"]
    assert not report.claim_gate["natural_graph_or_code_input_reduction_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_hidden_involution_query_separation_report(
        tmp_path / "query.json",
        finite_specs=((3, 1, 2), (4, 2, 3)),
        scaling_n_values=(16, 32),
    )
    assert payload["status"] == (
        "exponential-hidden-involution-query-separation-compiler-open"
    )
