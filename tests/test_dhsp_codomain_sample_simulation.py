from fractions import Fraction
from itertools import permutations
from math import comb

import numpy as np
import pytest

from dhsp_codomain_sample_simulation import (
    _cuberoot, channel_choi, empirical_choi, physical_empirical_control,
    predictive_distribution, run_controls, simulation_certificate,
    postselection_counterledger, transcript_control, transcript_probability,
)


def exact(row):
    return Fraction(int(row["numerator"]), int(row["denominator"]))


def matrix(rows):
    return np.array([[float(exact(x)) for x in row] for row in rows])


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_exact_empirical_mean_has_opposite_variance_blocks(report):
    assert len(report["empirical_channel_controls"]) == 12
    for r in report["empirical_channel_controls"]:
        m = r["samples_per_probe"]
        for i, row in enumerate(r["source_choi_F"]):
            for j, f in enumerate(row):
                assert exact(r["empirical_average_choi_H"][i][j])-exact(r["source_choi_H"][i][j]) == exact(f)/m
                assert exact(r["empirical_average_choi_F"][i][j])-exact(f) == -exact(f)/m
        assert r["entangled_reference_allowed"]
        assert not r["source_mean_operator_given_to_simulator"]


def test_channels_are_completely_positive_and_trace_preserving_including_failure(report):
    for r in report["empirical_channel_controls"]:
        d = r["memory_dimension"]
        for prefix in ("source", "empirical_average"):
            H, F = (matrix(r[f"{prefix}_choi_{tag}"]) for tag in ("H", "F"))
            assert np.linalg.eigvalsh(H).min() >= -1e-12
            assert np.linalg.eigvalsh(F).min() >= -1e-12
            assert np.trace(H+F) == pytest.approx(d)
            # Trace OUT and flag; IN remains the identity, not a scalar trace check.
            partial = np.einsum("aiaj->ij", (H+F).reshape(d, d, d, d))
            assert partial == pytest.approx(np.eye(d))


def test_normalized_choi_distance_is_not_silently_called_diamond_distance(report):
    for r in report["empirical_channel_controls"]:
        m = r["samples_per_probe"]
        assert r["maximum_input_trace_distance_numeric_only"] <= 1/m+1e-12
        if r["name"] == "identity_Z_diamond_not_choi":
            assert exact(r["normalized_choi_input_trace_distance"]) == Fraction(1, 2*m)
            assert r["maximum_input_trace_distance_numeric_only"] == pytest.approx(1/m)
        if r["name"] == "global_phase_cancellation":
            assert exact(r["normalized_choi_input_trace_distance"]) == Fraction(1, m)


def test_literal_empirical_projection_covers_complex_gates_and_entangled_input(report):
    assert len(report["physical_empirical_controls"]) == 12
    for r in report["physical_empirical_controls"]:
        assert r["physical_formula_residual"] < 1e-12
        assert r["trace"] == pytest.approx(1)
        assert r["minimum_failure_eigenvalue"] >= -1e-12
        assert r["sample_positions_not_unique_labels"]


def test_empirical_preparation_uses_sample_multiplicity_not_unique_labels():
    Ws = [[[1, 0], [0, 1]], [[1, 0], [0, -1]]]
    H, F = empirical_choi([0, 0, 1], Ws)
    dedup_H, _ = empirical_choi([0, 1], Ws)
    assert H[3][3] == Fraction(1, 9)
    assert dedup_H[3][3] == 0
    assert F[3][3] == Fraction(8, 9)


def test_memory_input_can_attain_error_twice_maximally_entangled_input():
    Ws = [[[1, 0], [0, 1]], [[1, 0], [0, -1]]]
    H, F = channel_choi((Fraction(1, 2),)*2, Ws)
    assert F[3][3] == 1 and F[0][0] == 0
    # Input |1>, not the averaged or reset |0> input, witnesses distance1/m.
    assert H[3][3] == 0
    assert H[0][0] == 1


def test_exact_posterior_depends_on_all_distinct_correct_samples_not_on_resampling(report):
    for r in report["exact_posterior_controls"]:
        N, c = r["rotation_order"], len(r["forced"])
        law = tuple(exact(x) for x in r["predictive_law"])
        assert sum(law) == 1
        assert exact(r["distance_to_uniform"]) == Fraction(c, N)
        if c:
            assert law[0] == Fraction(2, N)
    assert transcript_control(4, 2, "zero")["exact_total_variation"] == {"numerator": "1", "denominator": "4"}
    # Resampling the subset for every sample would instead give IID uniform labels.
    assert predictive_distribution(4, [0])[0] > Fraction(1, 4)


def policy_choice(name, prefix):
    if name == "zero":
        return 0
    if name == "alternating":
        return len(prefix) % 2
    if name == "last_label_parity":
        return prefix[-1] % 2 if prefix else 0
    return int(len(set(prefix)) < len(prefix))


def test_recursive_adaptive_laws_equal_direct_shared_subset_marginal(report):
    for r in report["adaptive_shared_subset_controls"]:
        N, Q, name = r["rotation_order"], r["label_only_queries"], r["policy"]
        totals = [Fraction(0), Fraction(0)]
        TV = Fraction(0)
        for row in r["records"]:
            labels = row["labels"]
            for h in (0, 1):
                correct = [labels[t] for t in range(Q) if policy_choice(name, labels[:t]) == h]
                c = len(set(correct))
                marginal = Fraction(comb(N-c, N//2-c), comb(N, N//2)) if c <= N//2 else Fraction(0)
                direct = marginal*Fraction(2, N)**len(correct)*Fraction(1, N)**(Q-len(correct))
                assert direct == exact(row["probabilities"][h])
                totals[h] += direct
            TV += abs(exact(row["probabilities"][0])-exact(row["probabilities"][1]))/2
        assert totals == [1, 1]
        assert TV == exact(r["exact_total_variation"])
        assert TV <= min(Fraction(1), Fraction(Q*(Q-1), 2*N))
        assert not r["domain_indices_available_to_decoder"]


def test_dimension_free_scaling_gate_and_all_simulator_queries_are_charged(report):
    bounds = []
    for r in report["dimension_free_scaling_ledgers"]:
        N, T, m = 1 << r["modulus_bits"], r["instrument_calls"], int(r["samples_per_empirical_call"])
        Q = T*m
        assert int(r["total_classical_label_samples"]) == Q
        assert r["empirical_list_size_is_power_of_two"]
        assert exact(r["simulation_error_per_hypothesis"]) == Fraction(T, m)
        data = min(Fraction(1), Fraction(Q*(Q-1), 2*N))
        assert exact(r["simulated_label_transcript_distance_upper"]) == data
        distance = min(Fraction(1), Fraction(2*T, m)+data)
        assert exact(r["ideal_original_instrument_parity_distance_upper"]) == distance
        assert exact(r["binary_parity_success_upper_with_error"]) == (1+distance)/2
        assert r["arbitrary_memory_dimension_and_entangled_reference_allowed"]
        assert r["initial_memory_secret_independent_required_for_parity_gate"]
        assert not r["other_oracle_queries_retained_domain_or_coherent_subgroup_choices_covered"]
        bounds.append(distance)
    assert bounds == sorted(bounds, reverse=True)
    assert bounds[-1] < Fraction(1, 10**18)


def test_polynomial_accuracy_simulation_is_quantum_processing_not_free_classical_decoder(report):
    r = report["polynomial_accuracy_simulator_ledger"]
    assert exact(r["simulation_error_per_hypothesis"]) < Fraction(1, 10**6)
    assert r["classical_query_quantum_processing_not_classical_computation"]
    assert r["simulator_samples_not_free_algorithm_resources"]
    assert not r["conditional_herald_accuracy_certified"]
    assert int(r["total_classical_label_samples"]) > 10**12


def test_precision_budget_paid_and_zero_call_gate_exact(report):
    r = report["precision_floor_counterledger"]
    assert exact(r["original_instrument_distance_upper_with_error"]) > Fraction(1, 10**6)
    zero = simulation_certificate(8, 0)
    assert exact(zero["ideal_original_instrument_parity_distance_upper"]) == 0
    assert exact(zero["binary_parity_success_upper_with_error"]) == Fraction(1, 2)


def test_targeted_domain_queries_break_any_attempted_general_oracle_transfer(report):
    for pi in permutations(range(4)):
        for s in (0, 1):
            assert (pi[0] == pi[(-s) % 4]) == (s == 0)
    assert report["chosen_query_scope_countercontrol"]["classical_success"] == {"numerator": "1", "denominator": "1"}
    assert not report["claim_gate"]["general_dhsp_oracle_lower_bound"]


def test_adaptive_subgroups_preserve_entangled_memory_all_flags_and_shared_source(report):
    for r in report["adaptive_entangled_memory_controls"]:
        m = r["samples_per_call"]
        assert r["entangled_reference_retained"] and r["all_flags_and_memory_retained"]
        assert r["source_is_not_resampled"]
        assert not r["unknown_mean_operator_used_by_physical_simulator"]
        assert r["shared_resampled_maximum_frobenius_difference"] > 1e-3
        for key in ("source_states_by_parity", "simulated_states_by_parity", "fresh_resampled_states_by_parity"):
            for rows in r[key]:
                state = np.array(rows)
                assert np.trace(state) == pytest.approx(1)
                assert np.linalg.eigvalsh(state).min() > -1e-12
        assert max(r["simulation_distances_by_parity"]) <= 2/m
        assert abs(r["source_parity_trace_distance"]-r["simulated_parity_trace_distance"]) <= sum(r["simulation_distances_by_parity"])


def test_unconditional_simulation_is_not_free_conditional_index_erasure(report):
    r = report["postselection_counterledger"]
    assert exact(r["unconditional_complete_output_trace_distance"]) < Fraction(1, 10**9)
    assert exact(r["empirical_heralded_pure_target_overlap"]) < Fraction(1, 2**90)
    assert exact(r["empirical_average_full_label_herald"]) > 2**90*exact(r["true_full_label_herald"])
    assert not r["efficient_conditional_pure_image_preparation_claim_allowed"]
    for n, m in ((3, 2), (4, 4), (8, 8)):
        row = postselection_counterledger(n, m)
        M = 1 << (n-1)
        accepted = (1-Fraction(1, m))*np.ones((M, M))/M**2+np.eye(M)/(m*M)
        u = np.ones(M)/np.sqrt(M)
        overlap = u@accepted@u/np.trace(accepted)
        assert overlap == pytest.approx(float(exact(row["empirical_heralded_pure_target_overlap"])))


@pytest.mark.parametrize("n", [0, 1, 2, 7, 8, 9, 10**6, 2**256])
def test_integer_cuberoot_does_not_use_float_scaling(n):
    root = _cuberoot(n)
    assert root**3 <= n < (root+1)**3


@pytest.mark.parametrize("args", [(0, 1), (3, -1), (True, 1), (3, 1, 0), (3, 1, True)])
def test_invalid_scaling_inputs_rejected(args):
    with pytest.raises(ValueError):
        simulation_certificate(*args)


@pytest.mark.parametrize("error", [-1, Fraction(2), 0.0, True])
def test_invalid_error_budget_rejected(error):
    with pytest.raises(ValueError):
        simulation_certificate(8, 1, 4, error)


def test_operator_probability_and_sample_validation():
    for call in (lambda: channel_choi((1,), [[[1, 0], [0, 2]]]),
                 lambda: channel_choi((Fraction(1, 2),)*2, [[[1]]]),
                 lambda: empirical_choi([], [[[1]]]),
                 lambda: empirical_choi([True], [[[1]]]),
                 lambda: empirical_choi([1], [[[1]]]),
                 lambda: physical_empirical_control([[[2]]], [0]),
                 lambda: predictive_distribution(8, [0, 0]),
                 lambda: predictive_distribution(8, [0, 1, 2, 3, 4]),
                 lambda: transcript_probability(4, 0, [0], "secret_policy")):
        with pytest.raises(ValueError):
            call()


def test_no_candidate_or_algorithm_promotion(report):
    assert not any(report["claim_gate"].values())
