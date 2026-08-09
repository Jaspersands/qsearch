import math

import pytest

from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_natural_leaf_commutator_trace_profile import (
    exact_leaf_commutator_trace_formula_control,
    independent_leaf_pair_commutator_trace,
    natural_leaf_trace_profile_scaling_record,
    run_natural_leaf_commutator_trace_profile,
)


@pytest.mark.parametrize("n", [3, 4, 5, 6, 7])
def test_carrier_sum_telescopes_to_closed_leaf_trace_formula(n: int) -> None:
    target = max(integer_partitions(n), key=hook_length_dimension)
    row = exact_leaf_commutator_trace_formula_control(n, target)

    assert row.formula_residual.startswith("0/")
    assert row.exact_carrier_trace_formula_verified is True
    assert independent_leaf_pair_commutator_trace(n) == pytest.approx(
        2 * (math.factorial(n) - len(integer_partitions(n))) / math.factorial(n) ** 3
    )


def test_natural_pair_trace_is_exactly_on_q_inverse_two_scale() -> None:
    row = natural_leaf_trace_profile_scaling_record(24)
    q = 1 << row.child_leaf_count_log2

    assert 2 * math.factorial(24) <= q < 4 * math.factorial(24)
    assert row.q_squared_rescaled_pair_commutator_trace == pytest.approx(
        q**2 * row.independent_pair_commutator_trace
    )
    assert 8 < row.q_squared_rescaled_pair_commutator_trace < 32
    assert row.aggregate_balanced_leaf_commutator_trace_lower_bound > 0


def test_balanced_block_variance_proves_density_profile_but_not_component_transfer() -> None:
    row = natural_leaf_trace_profile_scaling_record(16)

    assert row.minimum_shared_random_block_size >= 3
    assert row.minimum_exclusive_random_block_size >= 3
    assert row.relative_L1_error_expectation_upper_bound < 1
    assert row.density_one_balanced_pair_trace_profile_proved is True
    assert row.global_distinct_density_transfer_proved is True
    assert row.canonical_component_trace_transfer_proved is False


def test_concentration_and_balanced_mass_improve_with_n() -> None:
    early = natural_leaf_trace_profile_scaling_record(8)
    late = natural_leaf_trace_profile_scaling_record(32)

    assert late.relative_L1_error_expectation_upper_bound < (
        early.relative_L1_error_expectation_upper_bound
    )
    assert late.balanced_pair_fraction > early.balanced_pair_fraction
    assert late.aggregate_balanced_leaf_commutator_trace_lower_bound > 1


def test_report_keeps_green_normalization_as_the_only_trace_transfer_gate() -> None:
    report = run_natural_leaf_commutator_trace_profile()

    assert report.status == (
        "natural-leaf-trace-scale-and-density-proved-Green-transfer-open"
    )
    assert report.headline_metrics[
        "exact_natural_leaf_pair_trace_formula_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "quenched_density_one_leaf_trace_profile_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "constant_aggregate_uncompressed_leaf_trace_theorem_count"
    ] == 1
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert report.claim_gate[
        "natural_leaf_pair_trace_has_q_inverse_two_scale"
    ] is True
    assert report.claim_gate[
        "natural_aggregate_uncompressed_leaf_trace_constant"
    ] is True
    assert report.claim_gate[
        "natural_Green_ridge_preserves_leaf_pair_trace_scale"
    ] is False
    assert report.claim_gate[
        "natural_independent_plancherel_component_M4_positive"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
