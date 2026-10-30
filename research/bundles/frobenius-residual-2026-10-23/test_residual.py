import random

import pytest
from sympy import Matrix, eye, zeros

from residual import (
    analyze_local_matrix, analyze_pullback, column_basis, compatible_neighbor,
    lift_split, matrix_multiply, matrix_star, mod, nullspace, same_space,
    select_with_original_hiding_function,
)
from residual_controls import (
    OpaqueLabels, incompatible_inert_pullback, inert_stable_fixture,
    lagrangians, space_key, split_frobenius_fixture, unit,
)
from controls import frobenius_relation_fixture
from kernel_output import (
    action, integral_matrix_test, matrix_on_column, odd_maximal_split,
    product_actions, reconstruct,
)


def analyze(source, **kwargs):
    return analyze_pullback(source.order, source.reference_pullbacks()[0], source.ell,
                            source.characteristic, source.split(source.ell),
                            rng=random.Random(721), **kwargs)


@pytest.mark.parametrize("rank,count", [(0, 8), (1, 2), (2, 1)])
def test_all_split_ranks_match_complete_prime_square_census(rank, count):
    source = split_frobenius_fixture(rank)
    result = analyze(source)
    assert result.image_rank == rank
    assert result.candidate_count == count
    assert result.exact_source_relations_checked
    assert not result.geometric_input_verified
    splitting = source.split(5)
    lifted = lift_split(source.order, splitting, 5)
    a = action(source.reference_pullbacks()[0], product_actions(lifted))
    accepted = [k for k in lagrangians(5) if compatible_neighbor(a, k, 5)]
    assert len(accepted) == count
    if rank:
        assert {space_key(k, 5) for k in result.candidates} == {space_key(k, 5) for k in accepted}
    truth = nullspace(action(source.phi, product_actions(splitting)), 5)
    assert any(same_space(truth, k, 5) for k in accepted)


def test_inert_rank_zero_count_is_ell_plus_one_not_all_lagrangians():
    source = inert_stable_fixture()
    result = analyze(source)
    assert result.image_rank == 0
    assert result.splitting_type == "nonsplit"
    assert result.candidate_count == 6
    lifted = lift_split(source.order, source.split(5), 5)
    a = action(source.reference_pullbacks()[0], product_actions(lifted))
    assert sum(compatible_neighbor(a, k, 5) for k in lagrangians(5)) == 6


def test_true_integral_frobenius_relation_does_not_certify_a_global_weak_source():
    order, a = incompatible_inert_pullback()
    result = analyze_pullback(order, a, 5, 7, odd_maximal_split(7, 5))
    assert result.image_rank == 1
    assert result.status == "INCONSISTENT_WITH_INPUT_PROMISE"
    assert result.candidate_count == 0
    assert result.exact_source_relations_checked
    assert not result.geometric_input_verified
    lifted = lift_split(order, odd_maximal_split(7, 5), 5)
    matrix = action(a, product_actions(lifted))
    assert not any(compatible_neighbor(matrix, k, 5) for k in lagrangians(5))


def test_both_candidates_pass_independent_quaternion_hom_module_condition():
    source = frobenius_relation_fixture(1)
    result = analyze(source)
    a = source.reference_pullbacks()[0]
    left = Matrix.hstack(*(matrix_on_column(source.order, a, eye(8)[:, i]) for i in range(8)))
    splitting = source.split(11)
    # Check every completion of the returned line, not only the two positives.
    completions = [k for k in lagrangians(11)
                   if column_basis(k.row_join(result.image_basis), 11).cols == 2]
    assert len(completions) == 12
    successes = []
    for k in completions:
        data = reconstruct(source.order, splitting, k, 11)
        j = data.module_numerator
        preserves = integral_matrix_test(j.inv() * left * j / 11)
        if preserves:
            successes.append(space_key(k, 11))
    assert set(successes) == {space_key(k, 11) for k in result.candidates}
    assert len(successes) == 2


@pytest.mark.parametrize("index", [0, 1])
def test_two_original_oracle_queries_select_each_possible_kernel(index):
    source = frobenius_relation_fixture(1)
    result = analyze(source)
    oracle = OpaqueLabels(result.candidates[index], 11)
    selected = select_with_original_hiding_function(result.candidates, 11, oracle)
    assert selected.selected_index == index
    assert same_space(selected.kernel, result.candidates[index], 11)
    assert selected.original_label_queries == oracle.calls == 2
    assert not selected.source_hsp_promise_verified


def test_actual_reference_kernel_is_selected_without_reading_phi_in_controller():
    source = frobenius_relation_fixture(1)
    result = analyze(source)
    truth = nullspace(action(source.phi, product_actions(source.split(11))), 11)
    oracle = OpaqueLabels(truth, 11)
    selected = select_with_original_hiding_function(result.candidates, 11, oracle)
    assert same_space(selected.kernel, truth, 11)
    assert oracle.calls == 2


@pytest.mark.parametrize("shift", [0, 1, 3])
def test_compatible_prime_square_splitting_changes_do_not_change_candidates(shift):
    source = frobenius_relation_fixture(1)
    splitting = source.split(11)
    lifted = lift_split(source.order, splitting, 11, idempotent_lift_shift=shift * Matrix([1, 2, 3, 4]))
    result = analyze(source, split_squared=lifted)
    reference = analyze(source)
    assert {space_key(k, 11) for k in result.candidates} == {space_key(k, 11) for k in reference.candidates}


def test_large_prime_local_control_does_not_enumerate_ell():
    ell, p = 2**127 - 1, 7
    fast = Matrix([[0, ell * ell], [-p, 0]])
    slow = ell * Matrix([[0, 1], [-p, 0]])
    a = Matrix.diag(fast, slow)
    assert a * a == -p * ell * ell * eye(4)
    result = analyze_local_matrix(a, ell, p, rng=random.Random(918))
    assert result.image_rank == 1
    assert result.candidate_count == 2
    assert not result.exact_source_relations_checked
    assert result.root_draws <= 128
    assert all(compatible_neighbor(a, k, ell) for k in result.candidates)


def test_zero_rank_large_field_is_symbolic_not_materialized():
    ell, p = 2**127 - 1, 7
    a = ell * Matrix.diag(Matrix([[0, 1], [-p, 0]]), Matrix([[0, 1], [-p, 0]]))
    result = analyze_local_matrix(a, ell, p)
    assert result.status == "STABLE_LAGRANGIAN_RESIDUAL"
    assert result.candidate_count == ell + 3
    assert result.candidates == ()


def test_root_sampling_cap_is_an_explicit_abort():
    from scalar_cancellation import TrialBudgetExceeded

    class AlwaysSquare:
        def randrange(self, start, stop):
            return 1

    source = frobenius_relation_fixture(1)
    with pytest.raises(TrialBudgetExceeded):
        analyze_pullback(source.order, source.reference_pullbacks()[0], 11, 7,
                         source.split(11), rng=AlwaysSquare(), root_attempt_cap=3)


def test_self_adjoint_positive_square_map_is_not_mislabeled_as_skew_frobenius():
    source = frobenius_relation_fixture(1)
    j = Matrix([-1, 0, 2, 0])
    gamma = Matrix.vstack(zeros(4, 1), j, -j, zeros(4, 1))
    assert matrix_star(source.order, gamma) == gamma
    assert matrix_multiply(source.order, gamma, gamma) == 7 * unit(source.order)
    a = matrix_multiply(source.order, matrix_multiply(source.order, matrix_star(source.order, source.phi), gamma), source.phi)
    with pytest.raises(ValueError, match="skew-adjoint"):
        analyze_pullback(source.order, a, 11, 7, source.split(11))


def test_wrong_exact_square_relation_rejected():
    source = frobenius_relation_fixture(1)
    with pytest.raises(ValueError, match="exact source"):
        analyze_pullback(source.order, 2 * source.reference_pullbacks()[0], 11, 7, source.split(11))


def test_selection_rejects_duplicate_or_invalid_candidates():
    source = frobenius_relation_fixture(1)
    result = analyze(source)
    oracle = OpaqueLabels(result.candidates[0], 11)
    with pytest.raises(ValueError, match="distinct"):
        select_with_original_hiding_function((result.candidates[0], result.candidates[0]), 11, oracle)
    with pytest.raises(ValueError, match="exactly two"):
        select_with_original_hiding_function((), 11, oracle)
    assert oracle.calls == 0
