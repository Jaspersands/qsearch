from fractions import Fraction
from itertools import product

from flint import fmpz_mat
import pytest

from native_rlwe_primal_babai import exact_row_profile, nearest_plane
from ternary_pair_collimation import LowProblem, verify_pair
from ternary_pair_lattice import (
    complete_census, congruence_basis, coset_target, decode_shell, embed, deflated_second_witness,
    extract_witness, inverse_embed, lattice_pair, nearest_plane_list,
    prepared_bases, shell_norm, uniform_sweep, word_coordinates,
)


def problem(labels=(1, 7, 11, 18), Q=27):
    return LowProblem((Q,), tuple(((a,), (c,)) for a, c in zip(labels[::2], labels[1::2])), 0)


def test_a2_metric_exactly_matches_native_alphabet_and_integer_gap():
    allowed = {(0, 0), (1, 0), (0, 1)}
    for a, b in product(range(-7, 8), repeat=2):
        z = (a, b); norm = shell_norm(z)
        assert norm == 18*(a*a+a*b+b*b-a-b)+6
        assert inverse_embed(embed(z)) == z
        assert (norm == 6) == (z in allowed)
        if z not in allowed: assert norm >= 24
    for z in product(range(-1, 3), repeat=6):
        word = decode_shell(z)
        assert (word is not None) == (shell_norm(z) == 18)
        if word is None: assert shell_norm(z) >= 36
        else: assert word_coordinates(word) == z


def test_euclidean_center_and_unrestricted_boolean_encodings_are_wrong():
    # Euclidean distance to the barycenter prefers zero; the A2 metric does not.
    euclidean = [sum((Fraction(x)-Fraction(1, 3))**2 for x in z)
                 for z in ((0, 0), (1, 0), (0, 1))]
    assert euclidean == [Fraction(2, 9), Fraction(5, 9), Fraction(5, 9)]
    assert decode_shell((1, 1)) is None
    assert shell_norm((1, 1)) == 24


@pytest.mark.parametrize("labels,Q", [((1, 7, 11, 19), 27), ((3, 6, 2, 9), 27), ((0, 0, 0, 1), 9), ((0, 0), 1), ((3, 6), 9), ((0, 0), 9)])
def test_full_kernel_basis_index_and_bounded_coset_bijection(labels, Q):
    view = problem(labels, Q); geo = congruence_basis(view); A = geo["labels"]
    B = geo["kernel_rows"]; p = geo["pivot"]
    assert abs(int(fmpz_mat(B).det())) == geo["kernel_index"]
    L = fmpz_mat(geo["embedded_rows"])
    assert int((L*L.transpose()).det()) == geo["gram_determinant"]
    assert all(sum(a*x for a, x in zip(A, row)) % Q == 0 for row in B)
    for z in product(range(-1, 2), repeat=len(A)):
        target = sum(a*x for a, x in zip(A, z)) % Q
        z0, T = coset_target(view, (target,), geo)
        l = tuple(a-b for a, b in zip(z, z0)); coeff = list(l)
        rem = l[p]-sum(l[j]*B[j][p] for j in range(len(A)) if j != p)
        assert rem % geo["kernel_index"] == 0; coeff[p] = rem//geo["kernel_index"]
        reconstructed = tuple(sum(coeff[i]*B[i][j] for i in range(len(A))) for j in range(len(A)))
        assert reconstructed == l
        point = tuple(3*x for x in embed(l))
        assert sum((a-b)**2 for a, b in zip(point, T)) == shell_norm(z)
        word, decoded_z, norm = extract_witness(view, (target,), z0, point)
        assert decoded_z == z and norm == shell_norm(z)
        assert word == decode_shell(z)


def test_nonunit_scalar_inputs_are_solved_by_exact_quotient_but_vector_is_not_assumed():
    view = problem((3, 6), 9)
    geo = congruence_basis(view)
    assert geo["common_divisor"] == 3 and geo["kernel_index"] == 3
    assert coset_target(view, (1,), geo) is None
    answer = lattice_pair(view, (1,))
    assert answer["status"] == "DIVISIBILITY_CERTIFIED_EMPTY_TARGET"
    assert not answer["pair"] and answer["cost"]["lll_calls"] == 0
    assert lattice_pair(problem((0, 3), 9), (0,))["pair"]
    assert lattice_pair(problem((0, 0), 9), (0,))["pair"]
    vector = LowProblem((9, 27), (((1, 2), (3, 4)),), 0)
    with pytest.raises(ValueError): congruence_basis(vector)


def test_exact_rectangular_bareiss_profile_and_nearest_plane():
    rows = [[3, -3, 0], [3, 0, -3]]
    profile = exact_row_profile(rows)
    assert profile["leading_gram_determinants"] == [18, 243]
    assert profile["gs_squared"] == [18, Fraction(27, 2)]
    assert profile["mu"][1][0] == Fraction(1, 2)
    for target in product(range(-2, 3), repeat=3):
        result = nearest_plane(rows, target, profile)
        listed = list(nearest_plane_list(rows, target, profile))
        assert tuple(result["point"]) == listed[0]["point"]
        assert tuple(result["basis_coefficients"]) == listed[0]["coefficients"]
        assert len(listed) == 5
        for candidate in listed:
            assert candidate["point"] == tuple(sum(c*r[j] for c, r in zip(candidate["coefficients"], rows)) for j in range(3))


def test_lll_transform_preserves_full_integer_kernel_not_sublattice():
    view = problem(); geo, bases = prepared_bases(view, 83270, 3)
    L = fmpz_mat(geo["embedded_rows"])
    for basis in bases:
        U = fmpz_mat(basis["transform"]); reduced = fmpz_mat(basis["rows"])
        assert U*L == reduced and abs(int(U.det())) == 1
        assert basis["profile"]["leading_gram_determinants"][-1] == geo["gram_determinant"]


def test_all_small_targets_only_accept_two_distinct_exact_original_words():
    view = problem(); prepared = prepared_bases(view, 83270, 2)
    found = 0
    for t in range(27):
        result = lattice_pair(view, (t,), 83270, prepared=prepared, max_decodes=54)
        actual = {w for w in product(range(3), repeat=view.width) if view.value(w) == (t,)}
        assert set(result["witnesses"]).issubset(actual)
        if result["pair"]:
            assert verify_pair(view, (t,), result["pair"]) == result["pair"]; found += 1
        for attempt in result["attempts"]:
            if attempt["word"] is not None: assert int(attempt["exact_original_norm"]) == 12
        assert result["cost"]["preparation_charged_by_caller"]
        assert result["cost"]["candidate_decodes"] <= 54
    assert found >= 1


def test_invalid_norm_and_wrong_coset_cannot_be_promoted_as_witnesses():
    view = problem(); geo = congruence_basis(view); z0, T = coset_target(view, (0,), geo)
    invalid = (1, 1, 0, 0)
    point = tuple(3*x for x in embed(invalid))
    assert extract_witness(view, (0,), z0, point)[0] is None
    wrong = tuple(3*x for x in embed((1, 0, 0, 0)))
    with pytest.raises(ValueError, match="original congruence"): extract_witness(view, (0,), z0, wrong)
    with pytest.raises(ValueError): extract_witness(view, (0,), z0, (0, 1, 2, 0, 0, 0))


def test_caps_and_single_witness_do_not_count_as_pair_coverage():
    view = problem(); answer = lattice_pair(view, (0,), max_decodes=1)
    assert answer["cost"]["candidate_decodes"] == 1
    assert answer["cost"]["rounding_steps"] == 4
    assert not answer["pair"] and len(answer["witnesses"]) <= 1
    assert answer["status"] == "DECODE_CAP_NO_PAIR"
    large = problem(tuple(range(80)), 243)
    answer = lattice_pair(large, (0,))
    assert answer["status"] == "WIDTH_GUARD_NO_PAIR"
    assert answer["cost"]["lll_calls"] == answer["cost"]["candidate_decodes"] == 0
    with pytest.raises(ValueError): lattice_pair(view, (0,), prepared=prepared_bases(problem((1, 2)), 1))


def test_complete_source_census_includes_empty_singleton_and_nonunit_labels():
    census = complete_census()
    assert census["uniform_target_instances"] == 729
    assert census["truth_pairs"] == 25
    assert census["divisibility_certified_empty_targets"] == 56
    assert census["found_pairs"] == 25
    beta = Fraction(census["uniform_pair_coverage_exact"])
    assert census["exact_source_average_informative_acceptance"] == str(4*beta)
    assert Fraction(census["exact_source_average_raw_least_trit_success"]) == Fraction(1, 3)+4*beta/3
    assert any(x["fiber_size"] == 0 for x in census["all_cases"])
    assert any(x["fiber_size"] == 1 for x in census["all_cases"])
    assert census["decode_work_uniform_average"] != census["decode_work_Born_average"]


def test_uniform_sweep_is_reproducible_not_planted_and_keeps_failures():
    a = uniform_sweep((4, 8), trials=3, seed=71, max_decodes=4)
    b = uniform_sweep((4, 8), trials=3, seed=71, max_decodes=4)
    for x, y in zip(a["trials"], b["trials"]):
        assert {k: v for k, v in x.items() if not k.startswith("wall_")} == {k: v for k, v in y.items() if not k.startswith("wall_")}
        assert x["cost"]["candidate_decodes"] <= 4
        assert x["cost"]["lll_calls"] == 2
    assert len(a["trials"]) == 6
    assert a["IID_fresh_labels_and_independent_uniform_target_each_trial"]
    assert not a["planted_or_conditioned_nonempty_targets"]
    assert a["no_confidence_or_polynomial_coverage_claim"]


def test_deflation_searches_changed_native_digits_not_unrestricted_boolean_coordinates():
    view = problem()
    first = (0, 2); target = view.value(first)
    result = deflated_second_witness(view, target, first)
    assert result["pair"] == (first, (2, 1))
    assert result["cost"]["slice_calls"] <= 2*view.width
    assert result["cost"]["lll_calls"] <= result["cost"]["slice_calls"]
    assert not result["cost"]["pointwise_solver_guarantee_supplied"]
    singleton = deflated_second_witness(view, (0,), (0, 0))
    assert not singleton["pair"]
    assert singleton["cost"]["slice_calls"] == 4
    with pytest.raises(ValueError): deflated_second_witness(view, (1,), first)


@pytest.mark.parametrize("labels", [(0, 3), (3, 3), (0, 0), (1, 2)])
def test_deflation_terminal_complete_original_digit_solver(labels):
    view = problem(labels, 9)
    for word in product(range(3), repeat=1):
        result = deflated_second_witness(view, view.value(word), word)
        count = sum(view.value(w) == view.value(word) for w in product(range(3), repeat=1))
        assert bool(result["pair"]) == (count >= 2)
        if result["pair"]: verify_pair(view, view.value(word), result["pair"])
        assert result["cost"]["lll_calls"] == result["cost"]["candidate_decodes"] == 0


@pytest.mark.parametrize("call", [lambda: embed((True, 0)), lambda: shell_norm((False, 1)),
    lambda: inverse_embed((1, 0, 0)), lambda: word_coordinates((3,)),
    lambda: lattice_pair(problem(), (0,), seed=True), lambda: lattice_pair(problem(), (0,), max_decodes=0),
    lambda: lattice_pair(problem(), (0,), perturbations=-1), lambda: prepared_bases(problem(), basis_count=0)])
def test_invalid_inputs_rejected(call):
    with pytest.raises(ValueError): call()
