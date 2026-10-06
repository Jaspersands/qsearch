from fractions import Fraction
from itertools import product
import math
import random

from flint import arb, ctx
import numpy as np
import pytest

from ternary_covariant_noise import CovariantRecord, phase, simulated_record
from ternary_posterior_dual import (
    _field_countercontrol, canonical_phase, classical_least_trit_gate, likelihood_terms,
    low_degree_gate, necessary_coherence_radius, solve_least_trit, sparse_coherence_gate,
)


def _batch(n, r, M, seed):
    q, rng = 3**r, random.Random(seed)
    secret = tuple(rng.randrange(q) for _ in range(n))
    records = [simulated_record(tuple(rng.randrange(q) for _ in range(n)),
                                tuple(rng.randrange(q) for _ in range(n)), secret, q, rng)[0] for _ in range(M)]
    return records, secret


def _enumerated_posterior(records, target):
    q, n = records[0].modulus, len(records[0].first)
    masses = np.zeros(3)
    for trial in product(range(q), repeat=n):
        likelihood = math.prod(q*q*r.probability(trial) for r in records)
        masses[trial[target] % 3] += likelihood
    return masses/masses.sum()


@pytest.mark.parametrize("q", [3, 9, 27, 3**32])
def test_cyclotomic_reduction_is_exact_and_does_not_allocate_a_dense_root_table(q):
    assert canonical_phase({0: 1, q//3: 1, 2*q//3: 1}, q) == {}
    assert canonical_phase({q-1: 2}, q) == {q//3-1: -2, 2*q//3-1: -2}
    assert canonical_phase({q+1: 7, 1: -7}, q) == {}


@pytest.mark.parametrize("n,r,M", [(1, 1, 4), (1, 2, 6), (2, 2, 6), (1, 4, 6)])
def test_exact_MITM_posterior_matches_all_secret_reference_only_in_bounded_tests(n, r, M):
    records, _ = _batch(n, r, M, 91800+n+r)
    for target in range(n):
        result = solve_least_trit(records, range(M), target)
        p = result["posterior"]
        assert p["status"] == "EXACT_POSTERIOR_WITH_CERTIFIED_BALL_ORDERING"
        expected = _enumerated_posterior(records, target)
        assert np.max(abs(expected-p["posterior_probabilities"])) < 2e-12
        assert result["cost_ledger"]["secret_assignments_enumerated"] is False
        assert result["cost_ledger"]["original_native_qutrits_consumed"] == M
        assert result["cost_ledger"]["raw_assignments_per_half"] == [str(7**(M//2)), str(7**(M-M//2))]
        if p["maximum_a_posteriori_trit"] is not None:
            assert expected[p["maximum_a_posteriori_trit"]] == max(expected)


def test_sparse_record_terms_are_the_true_paired_likelihood_not_independent_marginals():
    q = 9
    record = CovariantRecord((2, 7), (6, 3), (1, 5), q)
    for secret in product(range(q), repeat=2):
        value = sum(weight*phase(e+sum(x*s for x, s in zip(f, secret)), q)/3
                    for f, e, weight in likelihood_terms(record))
        assert abs(value-q*q*record.probability(secret)) < 1e-12
    # At zero errors, product of scalar marginals would give25/9, not3.
    aligned = CovariantRecord((1,), (2,), (0, 0), q)
    assert abs(q*q*aligned.probability((0,))-3) < 1e-12
    assert abs(q*q*aligned.probability((0,))-25/9) > .2


def test_actual_legal_record_has_target_relations_but_exact_phase_cancellation_erases_signal():
    record = CovariantRecord((3,), (6,), (0, 3), 9)
    assert sum(f == (3,) for f, _, _ in likelihood_terms(record)) == 3
    result = solve_least_trit((record,), (11,))
    # The half expansion already cancels both nonzero-frequency buckets.
    assert result["cost_ledger"]["frequency_bucket_joins"] == 1
    assert result["coefficient_numerators"][1:] == [[], []]
    p = result["posterior"]
    assert p["exactly_uniform_least_trit"] and p["maximum_a_posteriori_trit"] is None
    assert p["posterior_probabilities"] == [float(Fraction(1, 3))]*3


def test_full_depth_high_dimension_sparse_control_is_exactly_uniform_not_a_numerical_near_zero():
    records, _ = _batch(4, 32, 8, 87500+4*100+32)
    result = solve_least_trit(records, range(8))
    assert result["posterior"]["exactly_uniform_least_trit"]
    assert result["coefficient_numerators"] == [[["0", "6561"]], [], []]
    assert result["cost_ledger"]["secret_assignments_enumerated"] is False


def test_invalid_zero_likelihood_data_is_detected_exactly_and_never_emits_a_posterior():
    record = CovariantRecord((0,), (0,), (1, 2), 3)
    result = solve_least_trit((record,), (0,))
    assert result["posterior"]["status"] == "ZERO_LIKELIHOOD_DATA_NO_POSTERIOR"
    assert result["posterior"]["posterior_probabilities"] is None


def test_exponential_reference_budget_exhaustion_never_returns_partial_posteriors():
    records, _ = _batch(4, 32, 8, 87500+4*100+32)
    blocked = solve_least_trit(records, range(8), max_half_states=3)
    assert blocked["status"] == "EXACT_REFERENCE_BUDGET_EXHAUSTED_NO_POSTERIOR"
    assert blocked["posterior"] is None
    records, _ = _batch(1, 2, 6, 91801)
    blocked = solve_least_trit(records, range(6), max_join_products=1)
    assert blocked["status"] == "EXACT_REFERENCE_BUDGET_EXHAUSTED_NO_POSTERIOR"
    assert blocked["posterior"] is None


def test_original_ancestor_reuse_and_mixed_sources_are_rejected():
    records, _ = _batch(1, 2, 4, 91801)
    with pytest.raises(ValueError, match="reused ancestors"):
        solve_least_trit(records, (0, 1, 2, 2))
    with pytest.raises(ValueError, match="one modulus"):
        solve_least_trit((records[0], CovariantRecord((1,), (2,), (0, 0), 3)), (0, 1))
    with pytest.raises(ValueError, match="out of range"):
        solve_least_trit(records, range(4), target_coordinate=1)


def test_ball_precision_is_scoped_and_certification_does_not_leak_global_context():
    original = ctx.prec
    records, _ = _batch(1, 2, 6, 91911)
    result = solve_least_trit(records, range(6))
    assert ctx.prec == original
    assert result["posterior"]["precision_bits"] >= 128
    enclosures = [arb(s) for s in result["posterior"]["posterior_probability_enclosures"]]
    assert sum(enclosures, arb(0)).contains(1)
    assert not result["posterior"]["uniform_secret_weak_success_guarantee_proved"]


def test_insufficient_ball_precision_fails_closed_and_bad_precision_is_rejected():
    records = (CovariantRecord((1,), (2,), (0, 0), 9),)*2
    result = solve_least_trit(records, (0, 1), initial_precision=2, maximum_precision=2)
    assert result["posterior"]["status"] == "PRECISION_UNRESOLVED_NO_TRIT_CERTIFICATE"
    assert result["posterior"]["maximum_a_posteriori_trit"] is None
    with pytest.raises(ValueError, match="integer >= 2"):
        solve_least_trit(records, (0, 1), initial_precision=1)


def test_fixed_field_raw_decoder_survives_even_with_large_SQ_dimension_and_matches_exact_posterior():
    result = _field_countercontrol()
    posterior = result["paired_posterior_control"]["posterior"]
    assert result["independent_polynomial_field_decoder"]["secret"] == (2, 0, 1)
    assert posterior["posterior_probabilities"] == [0., 0., 1.]
    assert result["known_easy_counterexample_to_generic_classical_hardness"]
    assert result["paired_posterior_control"]["cost_ledger"]["generic_time_not_polynomial"]


def test_classical_least_trit_bound_needs_more_than_native_entropy_width_but_allows_surplus():
    small, large = classical_least_trit_gate(8, 32, 256), classical_least_trit_gate(8, 32, 768)
    assert not small["necessary_copy_gate_passed"] and large["necessary_copy_gate_passed"]
    assert not small["unmeasured_native_states_or_other_receivers_covered"]
    assert not small["arbitrary_polynomial_surplus_samples_excluded"]


def test_ANOVA_full_degree_recovers_the_raw_record_gate_and_low_degree_really_truncates():
    n, r, M = 2, 4, 16
    full, raw = low_degree_gate(n, r, M, M), classical_least_trit_gate(n, r, M)
    assert full["bounded_low_record_degree_classifier_mean_advantage_squared_upper"] == raw["mean_least_trit_advantage_squared_upper"]
    small = low_degree_gate(n, r, M, 2)
    expected = M*Fraction(2, 3)+math.comb(M, 2)*Fraction(4, 9)
    assert Fraction(small["truncated_centered_likelihood_norm_squared"]) == expected
    assert Fraction(small["bounded_low_record_degree_classifier_mean_advantage_squared_upper"]) < Fraction(full["bounded_low_record_degree_classifier_mean_advantage_squared_upper"])
    assert not small["generic_adaptive_raw_sample_or_all_label_coefficients_covered"]


def test_whole_one_record_native_census_proves_orthogonality_and_trit_mixture_moment():
    q = 9
    table = []
    for a, c, y, z in product(range(q), repeat=4):
        record = CovariantRecord((a,), (c,), (y, z), q)
        table.append([q*q*record.probability((s,))-1 for s in range(q)])
    centered = np.array(table)
    gram = centered.T@centered/len(table)
    assert np.max(abs(gram-np.eye(q)*2/3)) < 1e-12
    by_trit = [centered[:, t::3].mean(axis=1) for t in range(3)]
    unconditional = centered.mean(axis=1)
    for mixture in by_trit:
        assert abs(np.mean((mixture-unconditional)**2)-float(Fraction(4, 3*q))) < 1e-12


def test_full_label_sparse_coherence_bound_screens_final_effects_not_gate_locality():
    minimum = necessary_coherence_radius(8, 32, 4096)["minimum_radius_not_excluded_by_union_gate"]
    assert not sparse_coherence_gate(8, 32, 4096, minimum-1)["necessary_sparse_coherence_gate_passed"]
    assert sparse_coherence_gate(8, 32, 4096, minimum)["necessary_sparse_coherence_gate_passed"]
    gate = sparse_coherence_gate(8, 32, 4096, 2)
    assert not gate["local_gates_sparse_generators_or_shallow_circuits_excluded"]
    assert gate["product_POVMs_generally_have_radius_M_not_one"]


def test_sparse_hamming_observable_has_no_trit_signal_until_a_genuine_frequency_relation():
    # Original q9 native phases, not a root3 substitution. Conditional secret twirl.
    q, M = 9, 3
    words = list(product(range(3), repeat=M)); D = len(words)
    frequencies = np.array([sum(w) % q for w in words])  # each original row a=1,c=2
    rho = []
    for t in range(3):
        matrix = np.zeros((D, D), dtype=complex)
        for h in range(q//3):
            psi = np.exp(2j*np.pi*((frequencies*(t+3*h)) % q)/q)/math.sqrt(D)
            matrix += np.outer(psi, psi.conj())/(q//3)
        rho.append(matrix)
    distance = np.array([[sum(a != b for a, b in zip(x, y)) for y in words] for x in words])
    for t in (1, 2):
        assert np.max(abs((rho[t]-rho[0])[distance <= 1])) < 1e-12
    x, y = words.index((0, 0, 0)), words.index((1, 2, 0))
    assert distance[x, y] == 2 and (frequencies[y]-frequencies[x]) % q == q//3
    observed = [2*matrix[x, y].real for matrix in rho]
    assert np.max(abs(np.array(observed)-np.array([2/D, -1/D, -1/D]))) < 1e-12
