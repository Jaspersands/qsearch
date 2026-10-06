from collections import Counter
from fractions import Fraction
from itertools import product

import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_cyclic_extractor import random_even_source
from ternary_pair_collimation import (
    LowProblem, apply_recipe, apply_syndrome_tape, capped_runtime_transfer,
    exhaustive_one_input_census, low_problem, mitm_pair, pair_recipe,
    physical_control, pointed_unit_minor, solver_contract, syndrome_recipe,
    verify_pair,
)


def source(pairs, level=6):
    return native_source([[inverse_frequency_coordinates(a, c, level) for a, c in row] for row in pairs], level)


def test_low_solver_view_removes_target_high_trit_but_keeps_all_other_secret_coordinates():
    original = source([[(5, 22), (16, 25)], [(7, 26), (21, 1)]])
    view = low_problem(original, 1)
    assert view.moduli == (27, 9)
    assert view.frequencies == (((5, 7), (22, 7)), ((7, 3), (26, 1)))
    assert view.group_size == original.group_size//3
    assert not hasattr(view, "secret") and not hasattr(view, "original_full_target_frequency")
    shifted = source([[(5, 4), (25, 7)], [(7, 8), (3, 19)]])
    # Other-coordinate changes are visible; target high changes alone are not.
    assert low_problem(shifted, 1).frequencies != view.frequencies
    only_high = source([[(5, 22), (25, 7)], [(7, 26), (3, 19)]])
    assert low_problem(only_high, 1) == view


def test_solver_view_is_deeply_immutable_and_accepts_only_original_canonical_frequencies():
    data = [[[[1], [2]]]][0]
    view = LowProblem([9], data, 0); data[0][0][0] = 8
    assert view.frequencies == (((1,), (2,)),)
    with pytest.raises(ValueError): LowProblem((9,), (((True,), (1,)),), 0)
    with pytest.raises(ValueError): LowProblem((2,), (((0,), (1,)),), 0)
    with pytest.raises(ValueError): LowProblem((9,), (((0,), (1,)),), True)


@pytest.mark.parametrize("n,r,j", [(1, 2, 0), (2, 2, 0), (2, 2, 1), (3, 1, 2)])
def test_ordinary_mitm_finds_two_witnesses_iff_the_actual_native_target_has_them(n, r, j):
    native = random_even_source(n, 2*r, 3, 92381+n+r+j); view = low_problem(native, j)
    fibers = Counter(view.value(w) for w in product(range(3), repeat=3))
    for target in product(*(range(q) for q in view.moduli)):
        result = mitm_pair(view, target)
        assert bool(result["pair"]) == (fibers[target] >= 2)
        if result["pair"]: assert verify_pair(view, target, result["pair"]) == result["pair"]
        assert result["cost"]["left_words_enumerated"] == 3
        assert result["cost"]["right_words_enumerated"] <= 9
        assert result["cost"]["retained_left_words"] <= 3
        assert result["cost"]["uses_only_LowProblem"]
        assert not result["cost"]["polynomial_witness_finder"]


def test_two_retained_left_words_per_residue_are_sufficient_not_all_witness_lists():
    view = LowProblem((9,), (((0,), (0,)),)*4, 0)
    result = mitm_pair(view, (0,))
    assert result["pair"] and result["cost"]["retained_left_words"] == 2
    assert len(set(result["pair"])) == 2


def test_exponential_half_budget_aborts_without_partial_or_unverified_success():
    view = low_problem(random_even_source(1, 64, 30, 92432))
    result = mitm_pair(view, (0,), max_half_words=100_000)
    assert result["status"] == "BUDGET_EXHAUSTED_NO_PARTIAL_PAIR"
    assert not result["pair"]
    assert result["cost"]["raw_half_assignments"] == (str(3**15), str(3**15))
    assert result["cost"]["left_words_enumerated"] == result["cost"]["right_words_enumerated"] == 0


@pytest.mark.parametrize("first,second", [((0,), (2,)), ((1, 2), (2, 1)), ((0, 1, 2), (0, 2, 1)), ((2, 2, 2), (1, 0, 1))])
def test_pair_compression_is_full_basis_reversible_and_erases_no_endpoint_tag(first, second):
    recipe = pair_recipe(first, second); width = len(first)
    outputs = {apply_recipe(w, recipe) for w in product(range(3), repeat=width)}
    assert len(outputs) == 3**width
    assert apply_recipe(first, recipe) == (0,)*width
    assert apply_recipe(second, recipe) == tuple(int(i == recipe["pivot"]) for i in range(width))
    assert recipe["projector"]["do_not_measure_which_endpoint"]
    assert not recipe["unknown_state_preparation_inverse_cloning_or_fiber_counter_required"]
    assert not recipe["identically_labeled_unknown_copies_required"]


def test_syndrome_tape_is_reversible_on_all_ancilla_values_not_an_inverse_function_oracle():
    view = low_problem(random_even_source(2, 4, 2, 92424), 1)
    recipe = syndrome_recipe(view)
    assert recipe["clean_syndrome_qutrits"] == 3
    for w in product(range(3), repeat=2):
        for ancilla in product(*(range(q) for q in view.moduli)):
            output = apply_syndrome_tape(view, w, ancilla)
            assert output == tuple((a+b) % q for a, b, q in zip(ancilla, view.value(w), view.moduli))
            assert apply_syndrome_tape(view, w, output, inverse=True) == ancilla
    assert recipe["original_phase_register_retained_while_solver_runs"]
    assert recipe["solver_runs_in_separate_workspace_not_controlled_by_unknown_word"]


@pytest.mark.parametrize("s", list(range(27)))
def test_actual_full_root_pair_and_qutrit_fourier_measurement_work_for_every_original_secret(s):
    native = source([[(9, 18)]])
    control = physical_control(native, 0, (s,))
    assert control["original_modulus"] == "27"
    assert control["informative_acceptance"] == "2/3"
    assert control["all_rejections_and_projection_failures"] == "1/3"
    assert control["unconditional_correct_including_uniform_failure_guess"] == "5/9"
    assert control["calibration_full_root_phase_amplitude_error"] < 1e-12
    record = control["all_nonempty_syndrome_branches"][0]
    assert record["inverse_F3_probabilities"][s % 3] == pytest.approx(2/3)
    assert sorted(record["inverse_F3_probabilities"]) == pytest.approx([1/6, 1/6, 2/3])


def test_high_zero_pair_is_rejected_without_switching_to_a_favorable_high_selected_pair():
    native = source([[(0, 9)]])
    control = physical_control(native, 0, (17,))
    assert control["informative_acceptance"] == "0"
    assert control["unconditional_correct_including_uniform_failure_guess"] == "1/3"
    branch = control["all_nonempty_syndrome_branches"][0]
    assert branch["solver"]["pair"] == ((0,), (1,))
    assert branch["target_trit_multiplier"] == 0
    assert "ZERO_TARGET_TRIT_MULTIPLIER" in branch["rejection"]
    # A different pair is informative, but selecting it is a different policy.
    assert native.value((2,))[0] == 9


def test_multidimensional_pair_isolates_only_the_requested_unknown_secret_coordinate():
    native = random_even_source(2, 6, 4, 76223)
    for secret in ((7, 8), (2, 8), (1, 11), (0, 20)):
        control = physical_control(native, 1, secret)
        assert control["informative_acceptance"] == "8/27"
        for branch in control["all_nonempty_syndrome_branches"]:
            if "recipe" in branch:
                assert branch["relative_full_frequency"][0] == 0
                delta = branch["target_trit_multiplier"]
                assert branch["inverse_F3_probabilities"][delta*secret[1] % 3] == pytest.approx(2/3)


@pytest.mark.parametrize("width", [1, 2, 3])
def test_every_native_simplex_word_triple_has_an_integer_unit_minor(width):
    words = list(product(range(3), repeat=width))
    for base, u, v in product(words, repeat=3):
        if len({base, u, v}) == 3:
            witness = pointed_unit_minor(base, u, v); a, b = witness["columns"]; A, B = witness["rows"]
            assert A[a]*B[b]-A[b]*B[a] == witness["integer_determinant"]
            assert abs(witness["integer_determinant"]) == 1


def test_complete_original_source_law_confirms_four_beta_transfer_and_single_witness_failure():
    census = exhaustive_one_input_census()
    assert census["uniform_target_pair_success_beta"] == "25/729"
    assert census["informative_acceptance_exact"] == "100/729"
    assert census["raw_least_trit_success_exact"] == "829/2187"
    assert census["fiber_size_instance_counts"] == {0: 512, 1: 192, 2: 24, 3: 1}
    assert census["natural_two_element_mass_exact"] == "16/81"
    assert census["verified_pair_high_lifts"] == 225
    assert census["informative_pair_high_lifts"] == 150
    assert census["singleton_only_single_witness_uniform_success"] == "64/243"
    assert census["singleton_only_two_witness_success"] == "0"


@pytest.mark.parametrize("n,r,acceptance,success", [(1, 1, "4/9", "13/27"),
                                                   (1, 2, "28/81", "109/243"), (2, 1, "28/81", "109/243")])
def test_boundary_roots_have_constant_receivers_but_do_not_use_the_underfull_four_beta_formula(n, r, acceptance, success):
    census = exhaustive_one_input_census(n, r)
    assert census["informative_acceptance_exact"] == acceptance
    assert census["raw_least_trit_success_exact"] == success
    beta = Fraction(census["uniform_target_pair_success_beta"])
    H = census["nuisance_group_size"]
    assert Fraction(acceptance) == Fraction(4*H, 9)*beta
    assert H <= 3
    if n == 2:
        native = source([[(1, 2), (0, 0)]], 2)
        assert physical_control(native, 0, (8, 19))["unconditional_correct_including_uniform_failure_guess"] == "5/9"


@pytest.mark.parametrize("n,r", [(1, 3), (1, 16), (1, 32), (8, 32), (32, 128)])
def test_conditional_polynomial_solver_contract_charges_native_input_and_exponential_reference_costs(n, r):
    contract = solver_contract(n, r); M = n*r-2; H = 3**(n*r-1)
    mass = Fraction(2, 9)-Fraction(2, H*H)
    assert Fraction(contract["natural_mass_of_exactly_two_word_fibers_lower"]) == mass
    assert Fraction(contract["source_mean_least_trit_advantage_lower"]) == Fraction(4, 3)*Fraction(contract["uniform_target_pair_success_beta_lower"])
    assert Fraction(contract["expected_binary_phase_inputs_if_fresh_IID_vector_phases_available"]) == Fraction(8*M, 3)
    assert contract["MITM_raw_half_assignment_bounds"] == (str(3**(M//2)), str(3**(M-M//2)))
    assert not contract["pointwise_solver_guarantee_is_supplied"]
    assert not contract["polynomial_full_depth_algorithm"]
    assert not contract["cyclic_DHSP_natural_source_reduction_for_n_greater_than_one_supplied"]


def test_variable_runtime_needs_uniform_target_cap_not_unweighted_born_average_assumption():
    contract = capped_runtime_transfer(100, Fraction(1, 100))
    assert contract["pointwise_runtime_cap"] == "20000"
    assert contract["informative_native_acceptance_after_cap_lower"] == "1/50"
    assert contract["raw_native_least_trit_advantage_after_cap_lower"] == "1/150"
    assert not contract["unweighted_runtime_equals_physical_Born_runtime"]
    assert not contract["assumed_runtime_and_coverage_estimates_certified"]


def test_false_pairs_bad_targets_and_underfull_parameter_fail_closed():
    view = LowProblem((9,), (((1,), (2,)),), 0)
    with pytest.raises(ValueError, match="distinct"): verify_pair(view, (0,), ((0,), (0,)))
    with pytest.raises(ValueError, match="measured nuisance"): verify_pair(view, (0,), ((0,), (1,)))
    with pytest.raises(ValueError): verify_pair(view, (0,), ((0,),))
    with pytest.raises(ValueError): mitm_pair(view, (9,))
    with pytest.raises(ValueError): mitm_pair(view, (0,), max_half_words=0)
    with pytest.raises(ValueError): pair_recipe((True,), (1,))
    with pytest.raises(ValueError): pointed_unit_minor((0,), (0,), (1,))
    with pytest.raises(ValueError): solver_contract(1, 2)
    with pytest.raises(ValueError): solver_contract(1, 3, 0)
    with pytest.raises(ValueError): capped_runtime_transfer(0, Fraction(1, 2))
    with pytest.raises(ValueError): capped_runtime_transfer(100, Fraction(1, 4))
