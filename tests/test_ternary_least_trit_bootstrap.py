from collections import Counter
from fractions import Fraction
from itertools import product
import math
import random

import numpy as np
import pytest

from ternary_incidence_decoder import IncidenceSample
from ternary_least_trit_bootstrap import (
    NativeTransform, WeakLearnerContract, WeakVote, amplitude_control,
    bootstrap_ledger, close_known_prefix_control, least_trit_copy_gate,
    least_trit_reference, plurality, primitive_only_transfer,
    source_uniformity_ledger, symmetrized_error_law, transformed_secret_for_calibration,
)


@pytest.mark.parametrize("n,r,d", [(1, 2, 0), (2, 3, 1), (3, 8, 5), (4, 32, 31)])
def test_prefix_and_random_self_reduction_are_exact_original_native_amplitudes(n, r, d):
    rng, q = random.Random(91000+n+r), 3**r
    s = tuple(rng.randrange(q) for _ in range(n))
    prefix = tuple(x % 3**d for x in s)
    a, c = (tuple(rng.randrange(q) for _ in range(n)) for _ in range(2))
    u = tuple(rng.randrange(3**(r-d)) for _ in range(n))
    for target in range(n):
        for sign in (-1, 1):
            t = NativeTransform(a, c, r, prefix, d, u, target, sign)
            control = amplitude_control(t, s)
            assert control["maximum_amplitude_error"] < 2e-12
            truth = transformed_secret_for_calibration(t, s)[0] % 3
            assert t.pullback(truth) == ((s[target]-prefix[target])//3**d) % 3
            assert not control["prefix_correctness_checked_using_unknown_secret"]
            assert not control["unknown_secret_passed_to_learner"]
            assert set(t.learner_view()) == {"first", "second", "native_even_level", "modulus"}


def test_wrong_prefix_is_not_silently_given_a_lower_source_promise():
    transform = NativeTransform((1,), (2,), 2, (1,), 1, (0,), 0, 1)
    assert not transform.recipe()["wrong_prefix_source_promise"]
    with pytest.raises(ValueError, match="wrong prefix"):
        transformed_secret_for_calibration(transform, (3,))
    # The actual corrected original state has phase chi9(2), not any root3 phase.
    residual = (3-transform.known_phase_guess[0]) % 9
    assert residual % 3 != 0


def test_complete_small_source_frequency_lifts_are_uniform_after_prefix_correction():
    counts = Counter()
    for a, c in product(range(9), repeat=2):
        t = NativeTransform((a,), (c,), 2, (2,), 1, (1,), 0, -1)
        counts[t.learner_frequencies] += 1
    assert len(counts) == 9 and set(counts.values()) == {9}
    ledger = source_uniformity_ledger(1, 2, 1)
    assert ledger["exact_preimages_per_lower_pair"] == "9"
    assert not ledger["reducing_measured_covariant_records_gives_this_source"]


def test_every_fixed_secret_randomizes_to_uniform_transformed_secret_independently_of_sign():
    # All secrets, including zero/nonprimitive. Labels and shifts transform separately.
    q, n = 9, 2
    for s in ((0, 0), (3, 6), (2, 8)):
        for coordinate in range(n):
            distributions = []
            for sign in (-1, 1):
                counts = Counter()
                for shift in product(range(q), repeat=n):
                    t = NativeTransform((1, 2), (3, 4), 2, (0, 0), 0, shift, coordinate, sign)
                    counts[transformed_secret_for_calibration(t, s)] += 1
                assert len(counts) == q**n and set(counts.values()) == {1}
                distributions.append(counts)
            assert distributions[0] == distributions[1]


def test_sign_symmetry_repairs_adversarial_wrong_class_bias_without_an_assumed_decoder():
    original = (Fraction(2, 5), Fraction(3, 5), Fraction(0))
    assert original[1] > original[0]
    result = symmetrized_error_law(original)
    assert result == (Fraction(2, 5), Fraction(3, 10), Fraction(3, 10))
    # Deliberately secret-dependent predictor, only a distribution identity control.
    for s in range(9):
        errors = Counter()
        for sign, shift in product((-1, 1), range(9)):
            t = NativeTransform((1,), (2,), 2, (0,), 0, (shift,), 0, sign)
            target = transformed_secret_for_calibration(t, (s,))[0] % 3
            full_target = transformed_secret_for_calibration(t, (s,))[0]
            prediction = target if full_target % 5 < 2 else (target+1) % 3
            errors[(t.pullback(prediction)-s) % 3] += 1
        assert errors[1] == errors[2]
        assert errors[0] > errors[1]


def test_primitive_only_contract_is_rejected_and_transfer_can_lose_all_advantage():
    with pytest.raises(ValueError, match="primitive-only"):
        WeakLearnerContract(Fraction(1, 15), 10, secret_distribution="uniform_primitive_secrets")
    control = primitive_only_transfer(1, Fraction(2, 5))
    assert Fraction(control["uniform_all_secret_success_lower_bound"]) == Fraction(4, 15) < Fraction(1, 3)
    with pytest.raises(ValueError, match="chosen labels"):
        WeakLearnerContract(Fraction(1, 10), 10, source_distribution="chosen_labels")


@pytest.mark.parametrize("n,r,eps,k", [(1, 1, Fraction(1, 10), 8), (8, 32, Fraction(1, 256), 16),
                                        (32, 128, Fraction(1, 10), 32)])
def test_amplification_ledger_charges_fresh_states_and_proves_conservative_failure_bound(n, r, eps, k):
    B = n*r
    ledger = bootstrap_ledger(n, r, WeakLearnerContract(eps, B), k)
    R = ledger["repetitions_per_coordinate_digit"]
    exponent = Fraction(9*R, 8)*eps**2
    assert float(exponent) >= math.log(2*n*r)+k*math.log(2)
    assert ledger["total_fresh_original_native_qutrits"] == n*r*R*B
    assert not ledger["full_native_recovery_implemented"] and not ledger["weak_learner_implemented"]


def test_plurality_is_only_an_empirical_output_and_reused_batches_fail_closed():
    votes = [WeakVote(2, 1, -1, 2, frozenset({0, 1})),
             WeakVote(2, 0, 1, 2, frozenset({2, 3})),
             WeakVote(2, 1, 1, 0, frozenset({4, 5}))]
    result = plurality(votes)
    assert result["counts"] == [0, 1, 2] and result["trit"] == 2
    assert result["original_native_records_charged"] == 6
    assert not result["success_probability_certified_from_votes_alone"]
    with pytest.raises(ValueError, match="shared original"):
        plurality((votes[0], votes[0]))
    assert plurality((votes[0], votes[2]))["trit"] is None


@pytest.mark.parametrize("n,r", [(1, 8), (2, 16), (4, 32)])
def test_native_high_root_top_digit_closes_only_given_an_external_correct_prefix(n, r):
    c = close_known_prefix_control(n, r, 86400+n)
    q = 3**r
    secret = tuple(map(int, c["calibration_secret_only"]))
    prefix = tuple(map(int, c["externally_given_correct_prefix"]))
    assert c["recovered_top_trit"] == tuple((s-u)//(q//3) for s, u in zip(secret, prefix))
    assert not c["prefix_discovered_by_this_control"] and not c["original_full_secret_discovery"]
    assert not c["decoder_received_unknown_secret"]
    assert c["original_fresh_native_qutrits_consumed"] == len(c["raw_public_records"])
    assert c["maximum_native_amplitude_error"] < 2e-12
    for row in c["raw_public_records"]:
        assert IncidenceSample(row["alpha"], row["beta"], row["basis"], row["outcome"]).value(c["recovered_top_trit"]) == 0


def test_information_reference_matches_native_secret_twirl_and_matching_primal_dual_certificates():
    # Small dense proof check of the formula, not a receiver implementation.
    q, M = 9, 3
    rows = [((1,), (3,)), ((2,), (8,)), ((4,), (1,))]
    report = least_trit_reference(rows, 2)
    words = list(product(range(3), repeat=M))
    f = np.array([sum(rows[i][j-1][0] if j else 0 for i, j in enumerate(w)) % q for w in words])
    states = []
    for t in range(3):
        rho = np.zeros((3**M, 3**M), dtype=complex)
        for h in range(q//3):
            psi = np.exp(2j*np.pi*((f*(t+3*h)) % q)/q)/math.sqrt(3**M)
            rho += np.outer(psi, psi.conj())/(q//3)
        states.append(rho)
    success, dual_trace = 0., 0.
    for fiber in report["nuisance_fibers"]:
        indices = [i for i in range(3**M) if f[i] % 3 == fiber["key"][0]]
        by_k = [[i for i in indices if f[i]//3 == k] for k in range(3)]
        active = [k for k in range(3) if by_k[k]]
        columns = np.zeros((3**M, len(active)), dtype=complex)
        for j, k in enumerate(active):
            columns[by_k[k], j] = 1/math.sqrt(len(by_k[k]))
        roots = np.sqrt([len(by_k[k]) for k in active])
        dual = columns@np.diag(roots*sum(roots)/(3*3**M))@columns.conj().T
        dual_trace += np.trace(dual).real
        for t in range(3):
            v = columns@np.exp(2j*np.pi*np.array(active)*t/3)/math.sqrt(3)
            success += (v.conj()@states[t]@v).real/3
            block = states[t][np.ix_(indices, indices)]/3
            assert np.min(np.linalg.eigvalsh(dual[np.ix_(indices, indices)]-block)) > -1e-12
    assert abs(success-report["optimal_uniform_secret_least_trit_success"]) < 1e-12
    assert abs(success-dual_trace) < 1e-12
    assert not report["efficient_fiber_preparation_or_inverse_granted"]


@pytest.mark.parametrize("q,r,M", [(3, 1, 1), (9, 2, 1), (9, 2, 2)])
def test_all_small_label_sources_optimal_average_respects_arbitrary_collective_copy_gate(q, r, M):
    cases = product(range(q), repeat=2*M)
    total, count = 0., 0
    for case in cases:
        rows = [((case[2*i],), (case[2*i+1],)) for i in range(M)]
        total += least_trit_reference(rows, r)["optimal_uniform_secret_least_trit_success"]
        count += 1
    squared = Fraction(least_trit_copy_gate(1, r, M)["mean_advantage_squared_upper_bound"])
    assert total/count-Fraction(1, 3) <= math.sqrt(float(squared))+1e-12


def test_full_label_copy_gate_is_not_a_low_label_no_go_or_a_polynomial_sample_obstruction():
    small = least_trit_copy_gate(8, 32, 128)
    enough = least_trit_copy_gate(8, 32, 256)
    assert not small["necessary_copy_gate_passed"] and enough["necessary_copy_gate_passed"]
    assert not small["arbitrary_polynomial_copy_receivers_excluded"]
    assert "ANY full-label" in small["receiver_scope"]
    with pytest.raises(ValueError, match="violates the full-label native copy gate"):
        bootstrap_ledger(8, 32, WeakLearnerContract(Fraction(1, 10), 128))


@pytest.mark.parametrize("n,r", [(1, 2), (2, 1)])
def test_exact_small_native_label_census_proves_the_Frobenius_moment_not_just_final_bound(n, r):
    q, D = 3**r, 3
    moment, cases = 0., 0
    secrets = list(product(range(q), repeat=n))
    for labels in product(range(q), repeat=2*n):
        F = np.array([(0,)*n, labels[:n], labels[n:]])
        rho_t = [np.zeros((D, D), dtype=complex) for _ in range(3)]
        for secret in secrets:
            psi = np.exp(2j*np.pi*((F@np.array(secret)) % q)/q)/math.sqrt(D)
            rho_t[secret[0] % 3] += np.outer(psi, psi.conj())/(q**n//3)
        rho_bar = sum(rho_t)/3
        moment += sum(float(np.linalg.norm(rho-rho_bar, "fro")**2) for rho in rho_t)/3
        cases += 1
    assert abs(moment/cases-float(Fraction(2, q**n)*(1-Fraction(1, D)))) < 1e-12


@pytest.mark.parametrize("kwargs", [{"sign": 0}, {"known_digits": 2}, {"target_coordinate": 1},
                                     {"prefix": (3,)}, {"original_first": (True,)}])
def test_bad_source_transforms_fail_closed(kwargs):
    parameters = dict(original_first=(1,), original_second=(2,), original_digits=2,
                      prefix=(2,), known_digits=1, shift=(0,), target_coordinate=0, sign=1)
    parameters.update(kwargs)
    with pytest.raises(ValueError):
        NativeTransform(**parameters)
