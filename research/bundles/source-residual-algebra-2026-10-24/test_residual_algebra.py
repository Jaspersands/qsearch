import random
from itertools import product

import pytest
from sympy import Matrix, eye, zeros

from residual_algebra import (
    adjoint, analyze_rank_one, analyze_source_pullbacks, column_basis,
    compatible_neighbor, inverse_mod, mod, nullspace,
    select_with_original_hiding_function,
)
from residual import same_space
from residual_controls import OpaqueLabels, lagrangians, space_key
from controls import frobenius_relation_fixture, word_fixture, unit
from algebra_controls import local_action, quartic_fixture
from pullback import extract_kernel, reconstruct_pullbacks
from kernel_output import (
    action, alternating_form, integral_matrix_test, lift_split, matrix_on_column,
    matrix_multiply, product_actions, reconstruct,
)
from scalar_cancellation import TrialBudgetExceeded


@pytest.mark.parametrize("beta,count", [
    (Matrix([[1, 0], [0, 2]]), 2),
    (Matrix([[1, 1], [0, 1]]), 1),
    (Matrix([[0, 2], [1, 0]]), 0),
    (3 * eye(2), 6),
])
def test_complete_lagrangian_census(beta, count):
    a, ell = local_action(beta, 5), 5
    out = analyze_rank_one([a], ell, rng=random.Random(24))
    actual = [k for k in lagrangians(ell)
              if compatible_neighbor(a, k, ell) and compatible_neighbor(adjoint(a), k, ell)]
    assert len(actual) == out.candidate_count == count
    if count <= 2:
        assert {space_key(k, ell) for k in actual} == {space_key(k, ell) for k in out.candidates}
    assert not out.geometric_input_verified


def test_noncommuting_residual_maps_reduce_two_candidates_to_one():
    maps = [local_action(Matrix([[1, 0], [0, 2]]), 5),
            local_action(Matrix([[1, 1], [0, 2]]), 5)]
    assert analyze_rank_one(maps[:1], 5, rng=random.Random(1)).candidate_count == 2
    out = analyze_rank_one(maps, 5, rng=random.Random(1))
    assert out.candidate_count == 1
    assert all(compatible_neighbor(a, out.candidates[0], 5) for a in maps)


def test_incompatible_common_lines_return_empty_not_hardness():
    maps = [local_action(Matrix([[1, 0], [0, 2]]), 5),
            local_action(Matrix([[1, 1], [1, 1]]), 5)]
    out = analyze_rank_one(maps, 5, rng=random.Random(2))
    assert out.candidate_count == 0
    assert out.status == "INCONSISTENT_WITH_INPUT_PROMISE"


@pytest.mark.parametrize("kind,count", [("two", 2), ("one", 1), ("scalar", 12)])
def test_actual_crt_then_general_residual_with_independent_module_check(kind, count):
    source = quartic_fixture(kind)
    got = reconstruct_pullbacks(source.order, source.ell, source.characteristic,
                               source.norms(), source.levels(), source.split,
                               source.observe, max_auxiliary_prime=47)
    assert got.coordinates == source.reference_pullbacks()
    old = extract_kernel(source.order, 11, source.split(11), got.coordinates)
    assert old.rank_history == (1, 1)
    out = analyze_source_pullbacks(source.order, got.coordinates, 11, source.split(11),
                                  rng=random.Random(24))
    assert out.candidate_count == count
    assert out.exact_source_products_checked and not out.geometric_input_verified
    alpha = got.coordinates[0]
    left = Matrix.hstack(*(matrix_on_column(source.order, alpha, eye(8)[:, i]) for i in range(8)))
    completions = [k for k in lagrangians(11)
                   if column_basis(k.row_join(out.image_basis), 11).cols == 2]
    assert len(completions) == 12
    allowed = []
    for kernel in completions:
        data = reconstruct(source.order, source.split(11), kernel, 11)
        module = data.module_numerator
        if integral_matrix_test(module.inv() * left * module / 11):
            allowed.append(kernel)
    assert len(allowed) == count
    if count <= 2:
        assert {space_key(k, 11) for k in allowed} == {space_key(k, 11) for k in out.candidates}
    truth = nullspace(action(source.phi, product_actions(source.split(11))), 11)
    assert any(same_space(k, truth, 11) for k in allowed)
    # The strict controls have minimal polynomial degree four, excluding
    # every scalar-shifted version of the old quadratic Frobenius case.
    if kind in ("two", "one"):
        powers = [unit(source.order)]
        for _ in range(3):
            powers.append(matrix_multiply(source.order, powers[-1], source.gammas[0]))
        assert Matrix.hstack(*powers).rank() == 4
    if count == 1:
        assert same_space(out.candidates[0], truth, 11)
    if count == 2:
        labels = OpaqueLabels(truth, 11)
        choice = select_with_original_hiding_function(out.candidates, 11, labels)
        assert labels.calls == 2 and same_space(choice.kernel, truth, 11)


@pytest.mark.parametrize("shift", [0, 1, 3, 5])
def test_prime_square_chart_changes_preserve_all_candidates(shift):
    source = quartic_fixture("two")
    split = source.split(11)
    base = analyze_source_pullbacks(source.order, source.reference_pullbacks(), 11, split,
                                   rng=random.Random(1))
    changed = analyze_source_pullbacks(
        source.order, source.reference_pullbacks(), 11, split,
        split_squared=lift_split(source.order, split, 11,
                                 idempotent_lift_shift=shift * Matrix([1, 2, 3, 4])),
        rng=random.Random(1))
    assert {space_key(k, 11) for k in base.candidates} == {space_key(k, 11) for k in changed.candidates}


@pytest.mark.parametrize("seed", range(5))
def test_symplectic_coordinate_changes(seed):
    rng, ell, change = random.Random(seed), 7, eye(4)
    form = alternating_form(2)
    for _ in range(3):
        v = Matrix([rng.randrange(ell) for _ in range(4)])
        change = mod((eye(4) + v * v.T * form) * change, ell * ell)
    a = local_action(Matrix([[1, 1], [0, 2]]), ell)
    base = analyze_rank_one([a], ell, rng=random.Random(3))
    changed = analyze_rank_one([inverse_mod(change, ell * ell) * a * change], ell,
                               rng=random.Random(3))
    expected = {space_key(inverse_mod(change, ell) * k, ell) for k in base.candidates}
    assert {space_key(k, ell) for k in changed.candidates} == expected


def test_old_frobenius_case_is_retained_not_the_only_case():
    source = frobenius_relation_fixture(1)
    out = analyze_source_pullbacks(source.order, source.reference_pullbacks(), 11, source.split(11),
                                  rng=random.Random(5))
    assert out.candidate_count == 2


def test_large_prime_no_enumeration_and_scalar_count_is_symbolic():
    ell = 2**127 - 1
    out = analyze_rank_one([local_action(Matrix([[1, 0], [0, 2]]), ell)], ell,
                          rng=random.Random(7))
    assert out.candidate_count == 2
    scalar = analyze_rank_one([local_action(eye(2), ell)], ell)
    assert scalar.candidate_count == ell + 1 and scalar.candidates == ()


def test_single_digit_does_not_determine_residual():
    matrices = [local_action(b, 5) for b in (eye(2), Matrix([[1, 0], [0, 2]]),
                                           Matrix([[1, 1], [0, 1]]))]
    assert len({tuple(mod(a, 5)) for a in matrices}) == 1
    assert [analyze_rank_one([a], 5, rng=random.Random(8)).candidate_count for a in matrices] == [6, 2, 1]


def test_word_completion_must_not_be_silently_skipped():
    source = word_fixture()
    split = lift_split(source.order, source.split(5), 5)
    a = action(source.reference_pullbacks()[0], product_actions(split))
    with pytest.raises(ValueError, match="not stabilized"):
        analyze_rank_one([a], 5)


def test_adjoint_information_is_not_optional():
    a = zeros(4)
    a[0, 2] = 1
    assert column_basis(a, 5).cols == 1
    assert column_basis(a.row_join(adjoint(a)), 5).cols == 2
    with pytest.raises(ValueError, match="rank-zero or rank-two"):
        analyze_rank_one([a], 5)


@pytest.mark.parametrize("matrix", [zeros(4), eye(4), zeros(3)])
def test_invalid_rank_or_shape_rejected(matrix):
    with pytest.raises(ValueError):
        analyze_rank_one([matrix], 5)


def test_root_cap_is_abort_not_empty_candidate_list():
    class Ones:
        def randrange(self, start, stop):
            return 1
    with pytest.raises(TrialBudgetExceeded):
        analyze_rank_one([local_action(Matrix([[1, 0], [0, 2]]), 5)], 5,
                         rng=Ones(), root_attempt_cap=1)


def test_all_two_by_two_residual_operators_over_f3():
    counts = set()
    planes = list(lagrangians(3))
    for entries in product(range(3), repeat=4):
        a = local_action(Matrix(2, 2, entries), 3)
        out = analyze_rank_one([a], 3, rng=random.Random(42))
        actual = [k for k in planes if compatible_neighbor(a, k, 3)]
        assert len(actual) == out.candidate_count
        counts.add(out.candidate_count)
        if out.candidate_count <= 2:
            assert {space_key(k, 3) for k in actual} == {space_key(k, 3) for k in out.candidates}
    assert counts == {0, 1, 2, 4}


def test_arbitrary_higher_digits_do_not_change_local_compatibility():
    a = local_action(Matrix([[1, 1], [0, 2]]), 5)
    changed = a + 25 * Matrix(4, 4, range(16))
    first = analyze_rank_one([a], 5, rng=random.Random(1))
    second = analyze_rank_one([changed], 5, rng=random.Random(1))
    assert {space_key(k, 5) for k in first.candidates} == {space_key(k, 5) for k in second.candidates}
