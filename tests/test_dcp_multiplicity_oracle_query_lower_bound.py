import pytest
import numpy as np

from dcp_multiplicity_oracle_query_lower_bound import (
    audit_multiplicity_search_encoding,
    bit_flip_oracle,
    equality_flags,
    multiplicity_query_scaling_record,
    run_multiplicity_oracle_query_lower_bound,
)


def test_equality_flags_add_exactly_one_known_preimage() -> None:
    assert equality_flags((0, 0, 0, 0)) == (1, 0, 0, 0, 0)
    assert equality_flags((0, 1, 0, 0)) == (1, 0, 1, 0, 0)


def test_bit_flip_equality_oracle_is_unitary() -> None:
    oracle = bit_flip_oracle((1, 0, 1, 0))
    assert oracle.T @ oracle == pytest.approx(np.eye(oracle.shape[0]))


@pytest.mark.parametrize("marked", [1, 2, 4])
def test_search_embedding_is_singleton_versus_one_plus_marked(
    marked: int,
) -> None:
    control = audit_multiplicity_search_encoding(16, marked)
    assert control.zero_case_fiber_multiplicity == 1
    assert control.marked_case_fiber_multiplicity == 1 + marked
    assert control.known_preimage_preserved
    assert control.one_query_search_to_equality_reduction
    assert control.reduction_verified


def test_singleton_doubleton_scaling_is_exponential() -> None:
    row = multiplicity_query_scaling_record(
        512,
        extra_marked_count=1,
        polynomial_query_benchmark_power=8,
    )
    assert row.query_lower_bound_log2_without_constant == pytest.approx(256)
    assert row.black_box_query_lower_bound_superpolynomial


def test_report_leaves_arithmetic_structure_open() -> None:
    report = run_multiplicity_oracle_query_lower_bound()
    assert report.headline_metrics["finite_search_encoding_failure_count"] == 0
    assert report.theorem.singleton_doubleton_black_box_lower_bound_proved
    assert not report.theorem.arithmetic_subset_sum_structure_ruled_out
    assert not report.claim_gate["generic_collision_walk_route_open"]
    assert report.claim_gate["source_aware_arithmetic_collision_route_open"]
    assert not report.claim_gate["speedup_claim_allowed"]
