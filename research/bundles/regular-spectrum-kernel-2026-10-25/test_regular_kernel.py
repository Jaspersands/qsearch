import random

import pytest
from sympy import Matrix, eye, zeros

from regular_kernel import (adjoint, column_basis, compatible_neighbor,
                            from_source_pullback, mod, regular_candidates, select_original)
from regular_controls import POLYNOMIAL, acquire_polynomial, arithmetic_source, previous_unknown_control
from pullback import reconstruct_pullbacks
from residual import nullspace, same_space
from residual_controls import OpaqueLabels, lagrangians, space_key
from kernel_output import (action, alternating_form, integral_matrix_test,
                           lift_split, matrix_on_column, product_actions, reconstruct)
from algebra_controls import local_action


@pytest.fixture(scope="module", params=[0, 1, 2])
def arithmetic(request):
    rank = request.param
    source = arithmetic_source(rank)
    public = acquire_polynomial(source)
    assert tuple(public["coefficients"]) == POLYNOMIAL
    got = reconstruct_pullbacks(source.order, source.ell, source.characteristic,
                               source.norms(), source.levels(), source.split, source.observe,
                               max_auxiliary_prime=47)
    assert got.coordinates == source.reference_pullbacks()
    result = from_source_pullback(source.order, got.coordinates[0], public["coefficients"],
                                  source.ell, source.split(source.ell), rng=random.Random(25))
    truth = nullspace(action(source.phi, product_actions(source.split(source.ell))), source.ell)
    return rank, source, got.coordinates[0], result, truth


def test_three_actual_crt_branches(arithmetic):
    rank, source, alpha, result, truth = arithmetic
    assert result.image_ranks == (rank, rank)
    assert len(result.candidates) == (4, 2, 1)[rank]
    assert any(same_space(truth, k, source.ell) for k in result.candidates)
    assert result.exact_source_products_checked
    assert not result.geometric_input_verified


def test_original_source_selects_the_same_kernel(arithmetic):
    _, source, _, result, truth = arithmetic
    labels = OpaqueLabels(truth, source.ell)
    chosen = select_original(result.candidates, source.ell, labels)
    assert same_space(chosen["kernel"], truth, source.ell)
    assert chosen["original_source_calls"] == labels.calls <= 13
    assert not chosen["source_fibers_verified"]


def test_all_listed_planes_pass_independent_hom_module_integrality(arithmetic):
    _, source, alpha, result, _ = arithmetic
    left = Matrix.hstack(*(matrix_on_column(source.order, alpha, eye(8)[:, j]) for j in range(8)))
    for kernel in result.candidates:
        module = reconstruct(source.order, source.split(source.ell), kernel, source.ell).module_numerator
        assert integral_matrix_test(module.inv()*left*module/source.ell)


@pytest.mark.parametrize("ell", [47, 2**127-1])
def test_previous_unknown_primes_give_two_candidates_without_changing_prime(ell):
    alpha, truth, old = previous_unknown_control(ell)
    assert old["status"] == "UNKNOWN"
    result = regular_candidates(alpha, [25, 0, 0, 0, 1], ell, rng=random.Random(25))
    assert result.image_ranks == (0, 0)
    assert len(result.candidates) == 2
    labels = OpaqueLabels(truth, ell)
    out = select_original(result.candidates, ell, labels)
    assert out["original_source_calls"] == 5
    assert same_space(out["kernel"], truth, ell)


def test_complete_rank_zero_census_is_not_just_a_contains_truth_check():
    source = arithmetic_source(0)
    alpha = source.reference_pullbacks()[0]
    lifted = lift_split(source.order, source.split(5), 5)
    matrix = action(alpha, product_actions(lifted))
    out = regular_candidates(matrix, POLYNOMIAL, 5)
    expected = [k for k in lagrangians(5)
                if compatible_neighbor(matrix, k, 5) and compatible_neighbor(adjoint(matrix), k, 5)]
    assert len(expected) == 4
    assert {space_key(k, 5) for k in expected} == {space_key(k, 5) for k in out.candidates}


def test_complete_rank_one_census():
    ell = 7
    matrix = local_action(Matrix([[4, 1], [0, 5]]), ell)
    # alpha/ell has two diagonal blocks with eigenvalues (2,3) and (4,5).
    polynomial = [1]
    for root in (2, 3, 4, 5):
        updated = [0]*(len(polynomial)+1)
        for j, value in enumerate(polynomial):
            updated[j] -= root*value
            updated[j+1] += value
        polynomial = updated
    out = regular_candidates(matrix, polynomial, ell, rng=random.Random(1))
    expected = [k for k in lagrangians(ell)
                if compatible_neighbor(matrix, k, ell) and compatible_neighbor(adjoint(matrix), k, ell)]
    assert len(expected) == 2
    assert {space_key(k, ell) for k in expected} == {space_key(k, ell) for k in out.candidates}
    assert out.residual_polynomial == (6, 5, 1)


def test_second_word_layer_can_recover_the_whole_kernel():
    ell = 5
    a, b, d = Matrix([[1, 0], [1, 2]]), Matrix.diag(1, 0), Matrix.diag(3, 4)
    standard = (ell*a).row_join(b).col_join(zeros(2).row_join(ell*d))
    permutation = eye(4)[:, [0, 2, 1, 3]]
    alpha = permutation.T*standard*permutation
    # The target neighbor action is triangular with eigenvalues 1,2,3,4.
    out = regular_candidates(alpha, [24, -50, 35, -10, 1], ell)
    assert out.image_ranks == (1, 2)
    assert len(out.candidates) == 1
    assert same_space(out.candidates[0], eye(4)[:, [0, 2]], ell)


@pytest.mark.parametrize("ell", [3, 47, 2**127-1])
def test_common_field_product_frobenius_cannot_pass_the_regular_gate(ell):
    # For an isogeny E^2 -> B defined over the same F_q, chi_B=chi_E^2.
    # q=5, trace=0 gives (T^2+5)^2, not the smaller-field T^4+25 example.
    out = regular_candidates(ell*eye(4), [25, 0, 10, 0, 1], ell)
    assert out.status == "NOT_REGULAR_USE_EXISTING_GENERAL_GATES"


def test_repeated_spectrum_is_not_promoted_or_called_hard():
    ell = 7
    out = regular_candidates(ell*eye(4), [1, -4, 6, -4, 1], ell)
    assert out.status == "NOT_REGULAR_USE_EXISTING_GENERAL_GATES"
    assert out.candidates == () and out.image_ranks == ()


def test_scalar_residual_contradicts_regular_characteristic_polynomial():
    with pytest.raises(ValueError, match="spectrum"):
        regular_candidates(local_action(4*eye(2), 7), [1, 0, 0, 0, 1], 7)


def test_wrong_characteristic_polynomial_is_rejected_in_zero_branch():
    with pytest.raises(ValueError, match="different characteristic"):
        regular_candidates(7*eye(4), [1, 0, 0, 0, 1], 7)


def test_no_invariant_lagrangian_is_inconsistent_not_hard():
    ell = 3
    beta = Matrix.diag(Matrix([[0, 1], [1, 2]]), Matrix([[0, 1], [1, 1]]))
    out = regular_candidates(ell*beta, [25, 0, 0, 0, 1], ell)
    assert not out.candidates
    assert out.status == "INCONSISTENT_WITH_GEOMETRIC_PROMISE"


def test_constant_invalid_labels_are_not_treated_as_a_selection():
    alpha, _, _ = previous_unknown_control(47)
    out = regular_candidates(alpha, [25, 0, 0, 0, 1], 47)
    with pytest.raises(ValueError, match="exactly one"):
        select_original(out.candidates, 47, lambda _: 0)


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_changed_public_symplectic_charts_do_not_change_the_list(seed):
    ell, rng, frame = 5, random.Random(seed), eye(4)
    form = alternating_form(2)
    for _ in range(3):
        v = Matrix([rng.randrange(ell) for _ in range(4)])
        frame = frame*(eye(4)+v*v.T*form)
    source = arithmetic_source(0)
    lifted = lift_split(source.order, source.split(ell), ell)
    alpha = action(source.reference_pullbacks()[0], product_actions(lifted))
    base = regular_candidates(alpha, POLYNOMIAL, ell)
    changed = regular_candidates(frame.inv()*alpha*frame, POLYNOMIAL, ell)
    assert {space_key(frame*k, ell) for k in changed.candidates} == {
        space_key(k, ell) for k in base.candidates}


@pytest.mark.parametrize("ell,coefficients,matrix", [(2, [1, 0, 0, 0, 1], eye(4)),
    (9, [1, 0, 0, 0, 1], eye(4)), (7, [1, 0, 1], eye(4)),
    (7, [1, 0, 0, 0, 1], eye(3))])
def test_bad_shapes_and_fields_rejected(ell, coefficients, matrix):
    with pytest.raises(ValueError):
        regular_candidates(matrix, coefficients, ell)
