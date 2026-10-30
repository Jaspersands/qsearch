from fractions import Fraction as F
import inspect
from itertools import permutations

import pytest

from diagonal_source import (apply_matrix, coarsen_histogram, colored_points,
    lift_affine, sample_source, sampling_plan)
from run_audit import nonnormal_sample_control, tv_after_action


@pytest.mark.parametrize("rank,gap,eta", [(1, F(1), F(1, 8)), (3, F(3, 4), F(1, 8)),
                                        (128, F(1, 32), F(1, 1024))])
def test_sample_schedule_is_exact_and_covers_union_bound(rank, gap, eta):
    plan = sampling_plan(rank, gap, eta)
    assert 2*plan["sample_count"]*plan["frequency_error"]**2 >= plan["logarithm_upper"]
    assert 2**plan["logarithm_upper"] >= 2*rank/eta
    assert plan["trace_norm_loss_upper"] == gap/8
    assert not plan["group_backend_executed"] and not plan["quantum_speedup_claim"]


def test_confidence_cost_is_logarithmic_not_inverse_probability():
    loose = sampling_plan(10, F(1, 4), F(1, 8))
    tight = sampling_plan(10, F(1, 4), F(1, 2**80))
    assert loose["frequency_error"] == tight["frequency_error"]
    assert tight["sample_count"] < 20*loose["sample_count"]


def test_equal_weights_survive_unequal_counts():
    plan = sampling_plan(2, F(1), F(1, 8))
    result = coarsen_histogram({(0,): 4999, (1,): 5001}, 2, plan["frequency_error"])
    assert result["color_count"] == 1
    assert result["rows"][0]["value"] == result["rows"][1]["value"]
    empirical = {(0,): F(4999, 10000), (1,): F(5001, 10000)}
    assert tv_after_action(empirical, lambda x: (1-x[0],)) > 0


def test_all_permutations_agree_with_true_weighted_stabilizer():
    values = (F(1, 4), F(1, 4), F(1, 4), F(1, 8), F(1, 8), F(0))
    truth = {(i,): value for i, value in enumerate(values) if value}
    counts = {(0,): 25001, (1,): 24999, (2,): 25000, (3,): 12501, (4,): 12499}
    plan = sampling_plan(5, F(1, 8), F(1, 16))
    result = coarsen_histogram(counts, 5, plan["frequency_error"])
    coarse = {tuple(row["point"]): row["value"] for row in result["rows"]}
    assert sum(truth[x]-coarse.get(x, 0) for x in truth) <= plan["trace_norm_loss_upper"]
    for perm in permutations(range(6)):
        action = lambda x: (perm[x[0]],)
        assert (tv_after_action(truth, action) == 0) == (tv_after_action(coarse, action) == 0)


def test_chain_not_only_same_bin_or_pairwise_complete_linkage():
    result = coarsen_histogram({(i,): 16+2*i for i in range(5)}, 5, F(1, 100))
    assert result["color_count"] == 1
    assert {row["value"] for row in result["rows"]} == {F(15, 100)}
    assert 1-sum(row["value"] for row in result["rows"]) <= result["trace_norm_loss_upper"]


def test_zero_component_discards_observed_and_unseen_tiny_weights():
    result = coarsen_histogram({(0,): 1, (1,): 4999, (2,): 5000}, 4, F(1, 1000))
    assert result["discarded_observed_labels"] == [[0]]
    assert {tuple(row["point"]) for row in result["rows"]} == {(1,), (2,)}


def test_false_orbit_gap_can_still_give_a_wrong_subgroup():
    tiny = F(1, 2**200)
    truth = {(0,): F(1, 2)-tiny, (1,): F(1, 2)+tiny}
    plan = sampling_plan(2, F(1, 2), F(1, 8))
    result = coarsen_histogram({(0,): 1, (1,): 1}, 2, plan["frequency_error"])
    coarse = {tuple(row["point"]): row["value"] for row in result["rows"]}
    swap = lambda x: (1-x[0],)
    assert tv_after_action(truth, swap) == 2*tiny < plan["orbit_gap"]
    assert tv_after_action(coarse, swap) == 0


def test_colors_and_setwise_semantics_are_essential():
    result = coarsen_histogram({(0,): 3, (1,): 2, (2,): 1}, 3, F(1, 1000))
    points = set(colored_points(result))
    translation = lift_affine(((1,),), (1,), result["color_count"], 3)
    assert {apply_matrix(translation, x, 3) for x in points} != points
    assert {(x+1) % 3 for x in range(3)} == set(range(3))  # Uncolored support is wrong.
    equal = coarsen_histogram({(0,): 1000, (1,): 1001, (2,): 999}, 3, F(1, 100))
    equal_points = set(colored_points(equal))
    translation = lift_affine(((1,),), (1,), equal["color_count"], 3)
    assert {apply_matrix(translation, x, 3) for x in equal_points} == equal_points
    assert all(apply_matrix(translation, x, 3) != x for x in equal_points)


def test_affine_lift_at_127_bit_prime_uses_no_basis_enumeration():
    p = 2**127-1
    x = (p-2, p-3, 1, 0, 1)
    lifted = lift_affine(((1, p-1), (0, 1)), (7, 11), 2, p)
    assert apply_matrix(lifted, x, p) == (8, 8, 1, 0, 1)


def test_sample_only_nonnormal_control_preserves_entire_subgroup():
    result = nonnormal_sample_control()
    assert result["sample_calls"] == result["planned_samples"] == 196608
    assert result["minimum_true_weight_reference_only"] == F(1, 2**200)
    assert result["unequal_heavy_weight_difference_reference_only"] == F(1, 2**179)
    assert result["uniform_frequency_event_verified_in_reference"]
    assert result["coarsening_trace_norm_loss"] <= result["trace_norm_loss_bound"]
    assert result["hidden_order"] == 5 and result["normal_core_order"] == 1
    assert result["same_original_rounded_encoded_subgroup"]
    assert result["minimum_outside_tv"] >= F(3, 4)
    assert not result["source_stage_group_backend_executed"]


def test_short_sample_budget_fails_before_calls():
    def forbidden():
        raise AssertionError("source must not be queried")
    with pytest.raises(ValueError, match="budget"):
        sample_source(forbidden, rank_cap=1, orbit_gap=F(1), failure_probability=F(1, 8),
                      dimension=1, field_prime=3, sample_budget=1)


def test_sampling_stage_never_accepts_probability_table_or_support():
    parameters = inspect.signature(sample_source).parameters
    assert not any(x in parameters for x in ["probabilities", "support", "spectrum", "density_matrix"])


@pytest.mark.parametrize("rank,gap,eta", [(0, F(1), F(1)), (True, F(1), F(1)),
                                         (2, .5, F(1)), (2, F(1), 0)])
def test_bad_schedules_rejected(rank, gap, eta):
    with pytest.raises(ValueError):
        sampling_plan(rank, gap, eta)


@pytest.mark.parametrize("counts", [{}, {(0,): 0}, {(0,): True}, {(0,): 1, (1, 0): 1},
                                    {(0,): 1, (1,): 1, (2,): 1}])
def test_invalid_histograms_rejected(counts):
    with pytest.raises(ValueError):
        coarsen_histogram(counts, 2, F(1, 100))


def test_observed_support_violation_and_bad_labels_abort():
    for source in [iter([(0,), (1,)]), iter([(3,)])]:
        with pytest.raises(ValueError):
            sample_source(lambda: next(source), rank_cap=1, orbit_gap=F(1),
                failure_probability=F(1, 8), dimension=1, field_prime=3, sample_budget=2048)


@pytest.mark.parametrize("matrix,offset,colors,p", [(((1, 0),), (1,), 1, 3),
    (((1,),), (3,), 1, 3), (((1.,),), (0,), 1, 3), (((1,),), (0,), -1, 3)])
def test_bad_affine_instances_rejected(matrix, offset, colors, p):
    with pytest.raises(ValueError):
        lift_affine(matrix, offset, colors, p)


def test_non_diagonal_pure_state_is_not_a_sparse_diagonal_source():
    # Measuring |+> erases coherence and changes its conjugation symmetries.
    import numpy as np
    pure = np.ones((2, 2))/2
    diagonal = np.eye(2)/2
    z = np.diag([1, -1])
    assert not np.allclose(z@pure@z, pure)
    assert np.array_equal(z@diagonal@z, diagonal)
    assert np.linalg.matrix_rank(pure) == 1 and np.linalg.matrix_rank(diagonal) == 2
