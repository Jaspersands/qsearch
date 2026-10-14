"""Original-frequency full-root witnesses, exact ring search and honest source models."""
from dataclasses import replace
from fractions import Fraction
from itertools import combinations, product
import json
import subprocess

import pytest
from flint import fmpq, nmod_mat

from theorems import native_full_root_slice as F
from native_choice_mitm import solve_choices
from native_carry_diagonal_slice import disjoint_kernel_slice, normalize
from native_prefix_carry_lift import compile_carry
from native_short_preimage_reduction import PublicWordFamily, verify_receipt


def family(q=27, k=8):
    pairs = (((1, 0), (0, 0)), ((0, 1), (0, 0)))+(((1, 1), (1, 0)),)*k
    return PublicWordFamily(q, 2, 1, k+2, (pairs,))


def problem(q=27, k=8, target=(7, 8)):
    raw = compile_carry(family(q, k), 0, target)
    return F.full_root_problem(disjoint_kernel_slice(normalize(raw)))


@pytest.mark.parametrize("q,k", ((9, 0), (9, 8), (27, 8), (3**16, 12), (3**64, 8)))
def test_original_all_root_frequency_agrees_everywhere_on_small_slices(q, k):
    P = problem(q, k);raw = P.slice.normalized.raw
    for z in product(range(3), repeat=len(P.choices)):
        actual = raw.family.frequency(raw.cohort, raw.word(P.slice.free(z)))
        assert P.frequency(z) == actual
        residual = tuple((a-b) % q for a, b in zip(actual, raw.target))
        assert all(x % 3 == 0 for x in residual)
        remaining = tuple((sum(col[v][i] for col, v in zip(P.choices, z))-P.remaining_target[i]) % P.modulus
                          for i in range(raw.family.dimension))
        assert remaining == tuple(x//3 for x in residual)


@pytest.mark.parametrize("q", (9, 27, 3**64))
def test_paired_choices_have_actual_source_correlation_not_independent_ring_values(q):
    P = problem(q)
    for column, a_sum in zip(P.choices, P.record()["active_block_original_a_sums"]):
        assert tuple((x+y) % P.modulus for x, y in zip(column[1], column[2])) == tuple(-a % P.modulus for a in a_sum)
    assert not P.record()["independent_ring_choice_distribution_assumed"]


def test_original_word_pair_frequency_lifts_are_uniform_at_composite_remaining_root():
    q, pairs = 27, (((1,), (0,)),)*3
    base = PublicWordFamily(q, 1, 1, 3, (pairs,))
    raw = compile_carry(base, 0, (7,));S = disjoint_kernel_slice(normalize(raw))
    words = [raw.word(S.free((z,))) for z in range(3)]
    for a, b in combinations(range(3), 2):
        site = next(j for j in range(3) if words[a][j] != words[b][j])
        counts = {}
        for h1, h2 in product(range(9), repeat=2):
            changed = list(pairs);changed[site] = ((1+3*h1,), (3*h2,))
            f = PublicWordFamily(q, 1, 1, 3, (tuple(changed),))
            pair = tuple(((f.frequency(0, w)[0]-7) % q)//3 for w in (words[a], words[b]))
            counts[pair] = counts.get(pair, 0)+1
        assert len(counts) == 81 and set(counts.values()) == {1}


@pytest.mark.parametrize("q", (3, 9, 27, 3**64))
def test_ring_mitm_matches_exhaustive_vector_search_without_a_field_inverse(q):
    choices = (((0, 0), (1, 2 % q), (q-1, 1)), ((0, 0), (2 % q, 1), (1, q-1)),
               ((0, 0), (1, 1), (q-1, q-1)))
    for target in ((0, 0), (1, 2 % q), (q-1, 0)):
        solutions = [z for z in product(range(3), repeat=3)
                     if tuple(sum(c[v][i] for c, v in zip(choices, z)) % q for i in range(2)) == target]
        result = solve_choices(choices, target, q)
        if solutions: assert result["parameters"] in solutions
        else: assert result["status"] == "COMPLETE_CHOICE_SEARCH_NO_SOLUTION"
        assert result["cost"]["residue_bits"] == q.bit_length()
        assert result["cost"]["left_payload_bits_upper"] == str(3*(2*q.bit_length()+2))


@pytest.mark.parametrize("bad", ("target", "dimension", "choices", "zero_choice", "modulus", "cap", "bool"))
def test_ring_engine_rejects_invalid_or_unaccounted_inputs(bad):
    args = {"choices": (((0,), (1,), (2,)),), "target": (1,), "modulus": 9}
    if bad == "target": args["target"] = (9,)
    if bad == "dimension": args["target"] = ()
    if bad == "choices": args["choices"] = (((0,), (1,)),)
    if bad == "zero_choice": args["choices"] = (((1,), (1,), (2,)),)
    if bad == "modulus": args["modulus"] = 8
    if bad == "cap": args["max_evaluations"] = 0
    if bad == "bool": args["target"] = (True,)
    with pytest.raises(ValueError): solve_choices(**args)


def test_ring_engine_caps_before_enumeration_and_handles_zero_parameters():
    choices = (((0,), (1,), (2,)),)*6
    result = solve_choices(choices, (0,), 9, max_entries=1)
    assert result["status"] == "SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION" and result["assignments_evaluated"] == 0
    assert solve_choices((), (0,), 9)["parameters"] == ()
    assert solve_choices((), (1,), 9)["status"] == "COMPLETE_CHOICE_SEARCH_NO_SOLUTION"


@pytest.mark.parametrize("q,k", ((9, 8), (27, 12), (3**64, 8)))
def test_whole_root_solver_matches_exact_slice_existence(q, k):
    P = problem(q, k)
    solutions = [z for z in product(range(3), repeat=len(P.choices)) if P.frequency(z) == P.slice.normalized.raw.target]
    result = F.search(P)
    if solutions:
        assert result["parameters"] in solutions
        assert result["whole_root_target_matched"] and result["actual_frequency"] == P.slice.normalized.raw.target
    else:
        assert result["status"] == "COMPLETE_SEARCH_NO_FULL_ROOT_SOLUTION_ON_THIS_SLICE"
        assert not result["absence_of_other_original_preimages_inferred"]


def test_forged_remaining_problem_cannot_promote_a_mod9_word_to_full_root():
    P = problem(27, target=(16, 8))
    shifted = replace(P, remaining_target=(0, 0), choices=(((0, 0),)*3,)*len(P.choices))
    assert P.frequency((0,)*len(P.choices)) != P.slice.normalized.raw.target
    with pytest.raises(ArithmeticError, match="entire-root"): F.search(shifted)


def test_helper_returns_actual_bound_receipts_and_rejects_family_swap():
    raw, _, _, _ = F.source_data(2, 3, 20, False, 93002)
    f = F.public_family(raw, 1, 20);helper = F.FullRootSliceHelper(f)
    receipt = helper(f, (9, 0));assert receipt is not None
    verify_receipt(f, (9, 0), receipt)
    changed = family(27)
    with pytest.raises(ValueError, match="different"): helper(changed, (9, 0))
    assert helper.cost()["public_label_elements_per_query"] == 80
    assert not helper.cost()["polynomial_classical_helper_supplied"]


def test_helper_cap_and_rank_failures_are_preserved_with_reasons():
    raw, _, _, _ = F.source_data(2, 3, 20, False, 93002)
    f = F.public_family(raw, 1, 20);helper = F.FullRootSliceHelper(f, max_evaluations=1)
    assert helper(f, (9, 0)) is None
    assert helper.calls[0]["status"] == "SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION"
    rankless = PublicWordFamily(27, 1, 1, 2, ((((1,), (2,)), ((1,), (2,))),))
    helper = F.FullRootSliceHelper(rankless)
    assert helper(rankless, (1,)) is None
    assert helper.calls[0]["status"] == "LOW_PREFIX_RANK_UNSUPPORTED_NOT_NO_PREIMAGES"


def test_full_helper_reconstructs_original_noisy_data_without_secret_access():
    c = F.reconstruction_control(2, 6, 44, True, 93004)
    assert c["matches_truth_fixture"]
    assert c["result"]["original_secret"] == c["truth_fixture_only"]["original_secret"]
    assert c["result"]["helper_calls"] == 12
    assert all(call["whole_root_target_matched"] for call in c["helper_cost"]["calls"])
    assert not c["secret_or_errors_used_by_helper_or_decoder"]
    assert not c["noise_correctness_inferred_from_small_outputs"]


def test_same_labels_and_different_responses_do_not_change_helper_receipts():
    raw, _, _, _ = F.source_data(2, 3, 20, False, 93002)
    f = F.public_family(raw, 1, 20)
    changed = tuple(replace(s, value=(s.value+1) % s.modulus) for s in raw)
    other = F.public_family(changed, 1, 20)
    assert f == other
    assert F.FullRootSliceHelper(f)(f, (9, 0)) == F.FullRootSliceHelper(other)(other, (9, 0))


def test_label_correlated_bias_is_not_repaired_using_the_true_secret():
    raw, mask, truth, _ = F.source_data(2, 3, 20, False, 93002)
    changed = tuple(replace(s, value=(s.value+s.label[0]) % s.modulus) for s in raw)
    f = F.public_family(changed, 1, 20)
    result = F.recover_with_helper(changed, mask, 1, 20, F.FullRootSliceHelper(f))
    original = tuple((a-b) % 27 for a, b in zip(truth, mask))
    assert result["original_secret"] == ((original[0]+1) % 27, original[1])
    assert result["original_secret"] != original
    assert result["correctness_requires_the_stated_noise_bound"]


def test_actual_uniform_low_slope_rank_failure_obeys_projective_hyperplane_bound():
    for n, M in ((1, 1), (1, 2), (2, 2)):
        failures = total = 0
        for flat in product(range(3), repeat=n*M):
            matrix = [list(flat[i*M:(i+1)*M]) for i in range(n)]
            failures += int(nmod_mat(matrix, 3).rank()) < n
            total += 1
        assert Fraction(failures, total) <= Fraction(3**n-1, 2*3**M)


@pytest.mark.parametrize("n,r,t", ((1, 3, 1), (2, 3, 3), (8, 8, 9), (128, 128, 126)))
def test_whole_root_entropy_and_moment_ledger_are_not_first_carry_statistics(n, r, t):
    L = F.root_moments(n, r, max(t, n*n), t);E = n*(r-1)
    assert L["mean_whole_root_solution_count"] == {"base": 3, "exponent": t-E}
    assert not L["derived_choices_assumed_independent"]
    assert not L["statistics_construct_a_polynomial_solver_or_coherent_row"]
    if abs(t-E) <= 512:
        mu = Fraction(3**max(0,t-E), 3**max(0,E-t))
        assert Fraction(L["solution_existence_lower_if_short"]) == mu/(mu+1)
    else: assert L["solution_existence_lower_if_short"] is None


@pytest.mark.parametrize("n", (8, 32, 64, 128))
def test_larger_bank_guarantees_entropy_but_charges_exponential_runtime_and_noise(n):
    T = F.bank_tradeoff(n, n)
    assert T["sites"] == (n+1)*T["guaranteed_slice_parameters"]+n
    assert T["guaranteed_slice_parameters"] == n*(n-1)+T["entropy_surplus"]
    assert Fraction(T["whole_batch_helper_failure_upper_if_complete_search"]) <= Fraction(1, 3**6)
    assert Fraction(T["whole_batch_helper_failure_upper_if_complete_search"]) == Fraction(T["conditional_batch_absence_probability_upper_if_complete_search"])+Fraction(T["rank_failure_upper_used_in_budget"])
    assert T["meet_in_middle_left_assignment_trits"]+T["meet_in_middle_right_assignment_trits"] == T["guaranteed_slice_parameters"]
    assert not T["live_caps_proved_sufficient_for_scalable_search"]
    assert not T["statistical_or_noise_feasibility_is_polynomial_runtime"]
    noise = T["original_secret_noise_ledger_if_complete_helper"]
    assert noise["original_classical_record_count"] == 2*T["sites"]
    assert noise["original_error_independence_and_zero_mean_required"]


def test_growing_bank_noise_ledger_can_be_vacuous_and_does_not_hide_it():
    a, b = F.bank_tradeoff(8, 8), F.bank_tradeoff(128, 128)
    assert a["original_secret_noise_ledger_if_complete_helper"]["full_recovery_lower_if_helper_is_supplied"] == "0"
    assert fmpq(b["original_secret_noise_ledger_if_complete_helper"]["full_recovery_lower_if_helper_is_supplied"]) > fmpq(4, 5)


def test_live_report_keeps_empty_slices_and_true_full_original_reconstructions():
    p = json.loads(F.REPORT.read_text())
    assert all(c["solver"]["status"] == "COMPLETE_SEARCH_NO_FULL_ROOT_SOLUTION_ON_THIS_SLICE" for c in p["whole_root_slice_controls"][:4])
    assert p["whole_root_slice_controls"][-1]["solver"]["whole_root_target_matched"]
    assert all(c["matches_truth_fixture"] for c in p["original_data_reconstruction_controls"])
    assert not p["polynomial_full_root_preimage_helper_or_uniform_coherent_row_supplied"]


def test_independent_checker_replays_original_roots_searches_and_decoders():
    checker = F.ROOT/"research/certificates/native_full_root_slice_crosscheck.js"
    p = subprocess.run(["node", str(checker)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


@pytest.mark.parametrize("mutation", ("choice", "division", "correlation", "witness", "recovery", "cap", "population", "noise", "scope"))
def test_independent_checker_rejects_false_whole_root_or_noise_claims(mutation, tmp_path):
    p = json.loads(F.REPORT.read_text());c = p["whole_root_slice_controls"][-1]
    if mutation == "choice": c["whole_root_problem"]["remaining_choices"][0][1][0] = (c["whole_root_problem"]["remaining_choices"][0][1][0]+1) % 9
    if mutation == "division": c["whole_root_problem"]["remaining_modulus"] = "27"
    if mutation == "correlation": c["whole_root_problem"]["independent_ring_choice_distribution_assumed"] = True
    if mutation == "witness": c["solver"]["native_word"][0] = (c["solver"]["native_word"][0]+1) % 3
    if mutation == "recovery": p["original_data_reconstruction_controls"][0]["result"]["original_secret"][0] = (p["original_data_reconstruction_controls"][0]["result"]["original_secret"][0]+1) % 27
    if mutation == "cap": c["solver"]["cost"]["left_payload_bits_upper"] = "0"
    if mutation == "population": p["quadratic_bank_whole_root_ledgers"][0]["mean_whole_root_solution_count"]["exponent"] = 0
    if mutation == "noise": p["larger_bank_tradeoffs"][0]["original_secret_noise_ledger_if_complete_helper"]["full_recovery_lower_if_helper_is_supplied"] = "1"
    if mutation == "scope": p["polynomial_full_root_preimage_helper_or_uniform_coherent_row_supplied"] = True
    target = tmp_path/"forged.json";target.write_text(json.dumps(p))
    checker = F.ROOT/"research/certificates/native_full_root_slice_crosscheck.js"
    proc = subprocess.run(["node", str(checker), str(target)], capture_output=True, text=True)
    assert proc.returncode != 0, mutation
