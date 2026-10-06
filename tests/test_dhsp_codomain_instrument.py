from fractions import Fraction
from itertools import combinations

import numpy as np
import pytest

from dhsp_codomain_instrument import (
    balanced_histogram, classical_collision_records, index_erasure_range_gate,
    encoded_instrument, general_encoder_scaling_certificate,
    instrument, one_copy_moments, oracle_table, physical_control, probability,
    run_controls, scoped_scaling_certificate, shared_two_copy_control, three_outcomes,
)


def exact(row):
    return Fraction(int(row["numerator"]), int(row["denominator"]))


def matrix(rows):
    return np.array([[float(exact(x)) for x in row] for row in rows])


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_literal_query_uncompute_and_domain_projection_matches_complete_instrument(report):
    assert len(report["physical_controls"]) == 108
    for row in report["physical_controls"]:
        assert row["instrument_residual"] < 1e-12
        assert row["discarded_diagonal_residual"] < 1e-12
        assert row["herald_vector_residual"] < 1e-12
        assert row["minimum_state_eigenvalue"] > -1e-12
        assert row["trace"] == pytest.approx(1)
        assert row["oracle_queries"] == 2
        assert row["all_failure_hash_outputs_retained"]
        assert not row["failed_domain_register_retained"]


@pytest.mark.parametrize("K", [2, 4, 8])
def test_discarding_register_is_not_pure_image_preparation(K):
    row = physical_control(list(range(K)), list(range(K)), K)
    rho = np.array(row["discarded_state"])
    claimed = np.ones((K, K))/K
    distance = np.linalg.norm(rho-claimed, ord="nuc")/2
    assert distance == pytest.approx(1-1/K)
    assert np.trace(rho@rho) == pytest.approx(1/K)


def test_herald_amplitudes_are_counts_not_square_roots():
    p = (Fraction(3, 4), Fraction(1, 4))
    row = physical_control([0, 0, 0, 1], [0, 1], 2)
    H = np.array(row["state"])[:2, :2]
    assert np.diag(H/np.trace(H)) == pytest.approx([9/10, 1/10])
    assert np.trace(H) == pytest.approx(float(sum(x*x for x in p)))
    assert not np.allclose(np.diag(H/np.trace(H)), [3/4, 1/4])


def test_full_computational_tag_hash_records_have_exact_classical_collision_baseline():
    for p in ((1,), (Fraction(3, 4), Fraction(1, 4)), (Fraction(1, 3),)*3):
        sigma = instrument(p)
        assert tuple(sigma[i][i] for i in range(len(sigma))) == classical_collision_records(p)
        assert sum(classical_collision_records(p)) == 1
    # Classical diagonal records do NOT reproduce retained off-diagonal coherence.
    assert instrument((Fraction(1, 2),)*2)[0][1] == Fraction(1, 4)


def test_unconditional_flat_herald_has_no_histogram_signal(report):
    for row in report["physical_controls"]:
        assert row["unconditional_herald_flat"] == pytest.approx(1/row["hash_bins"])
        p = tuple(exact(x) for x in row["histogram"])
        law = three_outcomes(p)
        assert sum(law) == 1 and min(law) >= 0


@pytest.mark.parametrize("N", [4, 8, 16])
def test_oracle_table_really_hides_right_cosets_and_index_two_images(N):
    pi = [(3*x+1) % N for x in range(N)]
    for s in range(N):
        f = lambda b, x: pi[(x-b*s) % N]
        for b in range(2):
            for x in range(N):
                assert f(b, x) == f(b ^ 1, (x+(-1)**b*s) % N)
        for epsilon in (0, 1):
            table = oracle_table(N, s, pi, epsilon)
            assert len(set(table)) == (N//2 if epsilon == s % 2 else N)
            if epsilon == s % 2:
                assert set(table) == set(pi[::2])
            assert all(table.count(v) == (2 if epsilon == s % 2 else 1) for v in set(table))


@pytest.mark.parametrize("N,K", [(4, 2), (8, 2), (8, 4)])
def test_hypergeometric_covariance_and_full_one_copy_distance_by_literal_subset_average(N, K):
    ps = [balanced_histogram(N, K, S) for S in combinations(range(N), N//2)]
    mean = sum(np.array(instrument(p), dtype=float) for p in ps)/len(ps)
    wrong = np.array(instrument((Fraction(1, K),)*K), dtype=float)
    delta = one_copy_moments(N, K)["one_copy_averaged_trace_distance"]
    assert np.linalg.norm(mean-wrong, ord="nuc")/2 == pytest.approx(float(delta))
    assert sum(sum((x-Fraction(1, K))**2 for x in p) for p in ps)/len(ps) == delta


def test_shared_nuisance_falsifies_naive_one_copy_tensor_averaging(report):
    row = next(r for r in report["shared_nuisance_controls"] if r["rotation_order"] == 8)
    assert exact(row["second_moment"]) == Fraction(1, 28)
    assert exact(row["fourth_moment"]) == Fraction(1, 280)
    assert exact(row["fixed_measurement_absolute_difference"]) == Fraction(11, 70)
    assert exact(row["twice_averaged_one_copy_distance"]) == Fraction(1, 7)
    assert row["naive_averaged_one_copy_hybrid_falsified"]
    assert row["shared_is_not_resampled"]
    assert not row["measurement_depends_on_hidden_permutation"]
    assert not row["algorithm_or_scaling_evidence"]


def test_explicit_two_copy_witness_is_valid_projector_not_optimal_classifier_advice():
    row = shared_two_copy_control(8)
    E = np.zeros((16, 16))
    v = np.zeros(16)
    v[0], v[5] = 1/np.sqrt(2), -1/np.sqrt(2)
    E += np.outer(v, v)
    for i in (3, 12, 15):
        E[i, i] = 1
    assert np.allclose(E@E, E)
    shared, wrong = matrix(row["shared_two_copy_state"]), matrix(row["wrong_two_copy_state"])
    assert np.trace(E@(shared-wrong)) == pytest.approx(-11/70)
    for rho in (shared, wrong, matrix(row["fresh_resampled_two_copy_state"])):
        assert np.trace(rho) == pytest.approx(1)
        assert np.linalg.eigvalsh(rho).min() >= -1e-12


def test_pointwise_hybrid_coefficient_covers_both_quantum_tag_blocks():
    K, N = 4, 8
    u = (Fraction(1, K),)*K
    for S in combinations(range(N), N//2):
        p = balanced_histogram(N, K, S)
        distance = np.linalg.norm(np.array(instrument(p), dtype=float)-np.array(instrument(u), dtype=float), ord="nuc")/2
        assert distance <= (2+np.sqrt(K)/2)*np.linalg.norm(np.array(p, dtype=float)-1/K)+1e-12


def test_growing_ledgers_are_scoped_source_means_not_general_oracle_hardness(report):
    previous = Fraction(1)
    for row in report["native_scaling_ledgers"]:
        n, K, T, R = (row[k] for k in ("modulus_bits", "hash_bins", "instrument_probes", "predeclared_balanced_hash_menu_size"))
        delta = Fraction(K-1, K*((1 << n)-1))
        C = exact(row["pointwise_distance_coefficient_upper"])
        sq = exact(row["shared_oracle_quantum_hybrid_squared_bound"])
        ideal = exact(row["ideal_quantum_trace_distance_upper"])
        assert sq == T*T*C*C*R*delta
        assert ideal*ideal >= min(Fraction(1), sq)
        assert ideal <= previous
        previous = ideal
        assert row["oracle_queries"] == 2*T
        assert row["arbitrary_quantum_postprocessing_retained_hashes_allowed"]
        assert not row["coherent_hash_selection_or_retained_domain_covered"]
        assert not row["other_full_oracle_algorithms_covered"]
        assert not row["independent_nuisance_resampling_assumed"]
    assert previous < Fraction(1, 10**25)


def test_precision_error_is_paid_and_full_range_hash_bound_may_be_vacuous(report):
    row = report["precision_floor_counterledger"]
    assert exact(row["quantum_trace_distance_upper_with_error"]) > Fraction(1, 10**6)
    assert exact(row["total_composed_trace_error_budget"]) == Fraction(1, 10**6)
    assert exact(scoped_scaling_certificate(8, 256, 1, 1)["ideal_quantum_trace_distance_upper"]) == 1
    assert exact(scoped_scaling_certificate(8, 1, 100, 10)["ideal_quantum_trace_distance_upper"]) == 0


def test_source_mean_does_not_erase_easy_or_zero_signal_structured_permutations(report):
    rows = [r for r in report["physical_controls"] if r["rotation_order"] == 16 and r["hash_bins"] == 2 and r["shift"] == r["subgroup_parity"] == 0]
    excesses = [three_outcomes(tuple(exact(x) for x in r["histogram"]))[2] for r in rows]
    assert set(excesses) == {Fraction(0), Fraction(1, 2)}
    assert Fraction(1, 2) > one_copy_moments(16, 2)["mean_squared_deviation"]


def test_index_erasure_gate_preserves_large_range_and_primitive_only_scope():
    assert not index_erasure_range_gate(8, 8)["large_range_numeric_premise_met"]
    assert index_erasure_range_gate(8, 4096)["large_range_numeric_premise_met"]
    assert index_erasure_range_gate(4, 128, Fraction(1, 2))["large_range_numeric_premise_met"]
    assert not index_erasure_range_gate(8, 4096)["general_dhsp_lower_bound_licensed"]
    assert not index_erasure_range_gate(8, 4096)["surjective_permutation_dhsp_transfer_licensed"]


@pytest.mark.parametrize("p", [[], [0, 0], [True], [0.5, 0.5], [Fraction(-1), 2]])
def test_invalid_exact_probabilities_rejected(p):
    with pytest.raises(ValueError):
        probability(p)


@pytest.mark.parametrize("args", [(0, 2, 1, 1), (3, 3, 1, 1), (3, 16, 1, 1), (3, 2, -1, 1), (3, 2, 1, 0), (True, 2, 1, 1)])
def test_invalid_scaling_source_rejected(args):
    with pytest.raises(ValueError):
        scoped_scaling_certificate(*args)


@pytest.mark.parametrize("error", [-1, Fraction(2), 0.0, True])
def test_inexact_or_invalid_error_budgets_rejected(error):
    with pytest.raises(ValueError):
        scoped_scaling_certificate(8, 2, 1, 1, error)


def test_invalid_oracle_hash_and_index_erasure_inputs_rejected():
    for call in (lambda: oracle_table(8, 0, [0]*8, 0),
                 lambda: oracle_table(8, 0, list(range(8)), True),
                 lambda: physical_control([2], [0, 1], 2),
                 lambda: physical_control([0], [2], 2),
                 lambda: physical_control([0], [0], 65),
                 lambda: shared_two_copy_control(512),
                 lambda: index_erasure_range_gate(8, 7),
                 lambda: index_erasure_range_gate(8, 4096, 0)):
        with pytest.raises(ValueError):
            call()


def test_no_candidate_or_speedup_promotion(report):
    assert not any(report["claim_gate"].values())


def test_coherent_hash_selection_and_complex_encoders_obey_full_output_variance_gate(report):
    controls = report["general_encoder_controls"]
    assert [r["retained_encoder_dimension"] for r in controls] == [4, 2, 8]
    for r in controls:
        N, d = r["rotation_order"], r["retained_encoder_dimension"]
        assert r["averaged_instrument_formula_residual"] < 1e-12
        assert r["mean_complete_instrument_distance"] <= (2+np.sqrt(d)/2)/np.sqrt(N-1)
        assert r["mean_vector_variance"] <= 1/(N-1)
        assert r["mean_density_frobenius_variance"] <= 1/(N-1)
    assert controls[2]["one_copy_averaged_distance"] == pytest.approx(1/8)


def test_general_encoder_scope_counts_dimension_not_qubits(report):
    for r in report["general_encoder_scaling_ledgers"]:
        assert r["coherent_hash_selector_inside_fresh_known_encoder_covered"]
        assert not r["polynomial_qubits_implies_polynomial_hilbert_dimension"]
        assert not r["coherent_cross_call_or_domain_retaining_oracle_access_covered"]
    assert exact(general_encoder_scaling_certificate(128, 2**128, 1, 1)["shared_oracle_distance_dyadic_upper"]) == 1
    assert exact(general_encoder_scaling_certificate(128, 128**2, 128**2, 128)["shared_oracle_distance_dyadic_upper"]) < Fraction(1, 10**9)


def test_encoder_validation_does_not_silently_normalize_or_duplicate_source_rows():
    for vectors, S in (([[1, 1], [1, 0]], [0]), ([[1, 0], [0, 1]], [0, 0]),
                       ([[1, 0], [0, np.nan]], [0]), ([[1, 0], [0, 1]], [True])):
        with pytest.raises(ValueError):
            encoded_instrument(vectors, S)
