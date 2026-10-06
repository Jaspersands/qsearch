from fractions import Fraction
from itertools import combinations

import numpy as np
import pytest

from dhsp_domain_collision_walk import (
    classical_birthday, coherent_preparation, driver, floquet,
    local_path_certificate, marker_only_certificate, partner_indices, physical_amplification_control,
    qpe_record_control, run_controls, source_table, walk_control,
)


def exact(row):
    return Fraction(int(row["numerator"]), int(row["denominator"]))


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_domain_is_retained_and_hidden_right_symmetry_is_physically_preserved(report):
    assert len(report["native_oracle_pilot_controls"]) == 48
    for r in report["native_oracle_pilot_controls"]:
        assert r["right_hidden_symmetry_commutator_residual"] < 1e-10
        assert r["plus_minus_sector_cross_residual"] < 1e-10
        assert r["partner_sector_return_identity_residual"] < 1e-10
        assert r["full_output_probabilities_normalized"]
        assert r["hidden_reflection_used_only_for_calibration"]
        assert not r["initial_oracle_state_or_support_projector_supplied"]


@pytest.mark.parametrize("family", ["local", "dyadic", "chirp", "chirp_lifted"])
def test_known_driver_is_even_fourier_arithmetic_unitary_not_unknown_eigenbasis(family):
    C, multiplier = driver(16, family, .75)
    assert np.abs(multiplier).max() <= 1+1e-12
    assert multiplier == pytest.approx(multiplier[(-np.arange(16)) % 16])
    assert C.conj().T @ C == pytest.approx(np.eye(32))
    assert C == pytest.approx(driver(16, family, .75)[0])


def test_naive_chirp_parity_invariant_is_an_exact_failure_not_roundoff_signal(report):
    N = 16
    C, multiplier = driver(N, "chirp", .75)
    assert multiplier[:N//2] == pytest.approx(multiplier[N//2:])
    for g in range(2*N):
        for h in range(2*N):
            if g % 2 != h % 2:
                assert abs(C[g, h]) < 1e-12
    rows = [r for r in report["native_oracle_pilot_controls"] if r["driver_family"] == "chirp" and r["hidden_shift_calibration"] % 2]
    assert len(rows) == 6
    for r in rows:
        assert r["exact_zero_from_parity_preserving_driver"]
        assert r["actual_verified_two_register_success"] == 0
        assert r["raw_numeric_verified_success"] < 1e-24
        assert r["square_root_amplified_query_PROXY_not_algorithm_bound"] is None


def test_lifted_chirp_removes_parity_invariant_without_being_a_speedup_claim(report):
    C, multiplier = driver(16, "chirp_lifted", .75)
    assert not np.allclose(multiplier[:8], multiplier[8:])
    assert np.max(np.abs(C[np.arange(32)[:, None] % 2 != np.arange(32)[None, :] % 2])) > 1e-3
    for r in report["native_oracle_pilot_controls"]:
        if r["driver_family"] == "chirp_lifted":
            assert r["actual_verified_two_register_success"] > 0
            assert not r["speedup_claim_allowed"]


def test_predicate_recovers_partner_without_hidden_shift_as_algorithm_input():
    for N in (4, 8):
        pi = [(3*y+1) % N for y in range(N)]
        for s in range(N):
            labels = source_table(N, s, pi)
            partners = partner_indices(N, s)
            for g in range(2*N):
                candidates = [h for h in range(2*N) if h != g and labels[h] == labels[g]]
                assert candidates == [partners[g]]
                b, x = divmod(g, N)
                c, y = divmod(candidates[0], N)
                # g^-1*g'=(1,(-1)^b*(y-x)), derived from known group arithmetic.
                assert b ^ c == 1
                assert ((-1)**b*(y-x)) % N == s


def test_coherent_clocked_seed_copy_matches_full_probability_not_cloning_unknown_state():
    N, Q, s = 4, 2, 1
    pi = [1, 0, 3, 2]
    labels = source_table(N, s, pi)
    U, _, _ = floquet(N, labels, "chirp_lifted")
    zero = np.zeros((Q, Q, 2*N, 2*N), dtype=complex)
    zero[0, 0, 0, 0] = 1
    state = coherent_preparation(zero, U)
    partners = partner_indices(N, s)
    p = sum(float(np.sum(np.abs(state[:, :, g, partners[g]])**2)) for g in range(2*N))
    row = walk_control(N, s, pi, "chirp_lifted", Q)
    assert p == pytest.approx(row["actual_verified_two_register_success"])
    assert np.sum(np.abs(state)**2) == pytest.approx(1)
    assert coherent_preparation(state, U, True) == pytest.approx(zero)


def test_actual_preparation_inverse_and_function_marker_amplification_not_free_reflection(report):
    for r in report["coherent_amplification_controls"]:
        assert r["preparation_inverse_residual"] < 1e-12
        assert r["final_norm"] == pytest.approx(1)
        assert r["executed_success_probabilities"] == pytest.approx(r["rotation_formula_control"], abs=1e-12)
        assert r["predicate_uses_only_function_equality_and_distinct_inputs"]
        assert not r["unknown_support_reflection_used"]
        Q = r["clock_size"]
        assert r["function_evaluations_by_iteration"] == [4*(Q-1)+j*(8*(Q-1)+4)+2 for j in range(r["iterations"]+1)]
        assert r["last_control_cost_exceeds_full_table_classical"]


def test_fresh_independent_preparations_falsify_transfer_of_seeded_walk_obstruction(report):
    for r in report["independent_preparations_amplification_countercontrols"]:
        N, s, Q = r["rotation_order"], r["hidden_shift_calibration"], r["clock_size"]
        row = walk_control(N, s, r["output_permutation"], r["driver_family"], Q)
        assert r["second_domain_preparation"] == "fresh_uniform"
        assert r["initial_success"] == pytest.approx(row["two_independent_preparations_collision_baseline"])
        assert r["initial_success"] >= 1/(2*N)-1e-12
        assert r["executed_success_probabilities"] == pytest.approx(r["rotation_formula_control"], abs=1e-12)
        assert r["preparation_inverse_residual"] < 1e-12
        assert r["final_norm"] == pytest.approx(1)
        if r["driver_family"] == "chirp":
            assert s % 2 == 1
            assert row["actual_verified_two_register_success"] == 0
            assert r["initial_success"] > 0
    for row in report["native_oracle_pilot_controls"]:
        assert row["two_independent_preparations_collision_baseline"] == pytest.approx(1/row["position_collision_support_after_first_walk"])
        assert row["two_independent_preparations_collision_baseline"] < exact(row["classical_birthday_same_eval_budget"]["verified_collision_probability"])
    for r in report["local_driver_scaling_certificates"]:
        assert exact(r["two_independent_preparations_collision_probability_upper"]) == min(Fraction(1), exact(r["maximum_first_walk_position_weight_upper"]))


def test_verified_quantum_signal_is_compared_to_stronger_classical_budget(report):
    for r in report["native_oracle_pilot_controls"]:
        Q = r["clock_size"]
        assert r["preparation_function_evaluations"] == 4*(Q-1)
        assert r["inverse_preparation_function_evaluations"] == 4*(Q-1)
        assert r["grover_iteration_function_evaluations"] == 8*(Q-1)+4
        assert r["unamplified_trial_function_evaluations"] == 4*(Q-1)+2
        assert exact(r["classical_birthday_same_eval_budget"]["verified_collision_probability"]) > r["actual_verified_two_register_success"]
        assert not r["failure_branches_or_energy_postselection_normalized_away"]
        assert r["unknown_success_probability_used_only_for_proxy"]


def test_energy_localization_is_not_two_free_copies_or_exact_eigenstate_measurement():
    r = qpe_record_control()
    assert r["finite_time_kraus_completeness_residual"] < 1e-12
    assert r["all_first_outcome_and_position_mass"] == pytest.approx(1)
    assert r["all_second_outcomes_partner_probability"] >= r["same_energy_record_partner_probability_unconditional"]
    assert not r["exact_eigenstate_or_global_level_spacing_free"]
    row = walk_control(4, 1, list(range(4)), "dyadic", 4)
    assert r["all_second_outcomes_partner_probability"] == pytest.approx(row["actual_verified_two_register_success"])


def test_local_path_gate_is_pointwise_conservative_and_excludes_nonlocal_drivers(report):
    bounds = []
    for r in report["local_driver_scaling_certificates"]:
        n, Q, R = r["modulus_bits"], r["clock_size"], r["dyson_truncation_hops"]
        D, eps = 2 << n, exact(r["operator_tail_upper"])
        assert R == 8*(Q+n)
        assert R+1 > 8*(Q-1)
        assert eps == Fraction(1, 1 << (n+8))
        vol, near = min(D, 4*R+2), min(D, 8*R+4)
        expected_weight = 2*(1+eps)**2*Fraction(vol, D)+2*eps**2
        assert exact(r["maximum_first_walk_position_weight_upper"]) == expected_weight
        bound = min(Fraction(1), near*expected_weight+eps**2)
        assert exact(r["verified_clocked_collision_probability_upper"]) == bound
        j = n*n
        assert exact(r["ideal_amplified_success_upper"]) == min(Fraction(1), (2*j+1)**2*bound)
        assert r["total_function_evaluations_with_final_verification"] == 4*(Q-1)+j*(8*(Q-1)+4)+2
        assert r["uniform_hidden_shift_and_oracle_labeling_not_required"]
        assert not r["dyadic_or_chirp_driver_covered"]
        assert not r["other_full_oracle_algorithms_covered"]
        bounds.append(bound)
    assert bounds == sorted(bounds, reverse=True)
    assert bounds[-1] < Fraction(1, 10**60)


def test_dyson_tail_geometric_bound_is_below_conservative_certificate():
    for n in (2, 4, 8, 32):
        for Q in (1, 2, 4, 16):
            r = local_path_certificate(n, Q)
            a, R = Q-1, r["dyson_truncation_hops"]
            tail = Fraction(3*a, R+1)**(R+1)/(1-Fraction(a, R+2))
            assert tail < Fraction(1, 1 << R)
            assert Fraction(1, 1 << R) <= exact(r["operator_tail_upper"])


def test_classical_birthday_law_is_exact_for_distinct_domains_not_iid_approximation():
    N, r, shift = 8, 2, 3
    pairs = 0
    total = 0
    for A in combinations(range(N), r):
        for B in combinations(range(N), r):
            total += 1
            pairs += bool(set(A) & {(y-shift) % N for y in B})
    assert Fraction(pairs, total) == exact(classical_birthday(N, r)["verified_collision_probability"])
    assert exact(classical_birthday(N, 0)["verified_collision_probability"]) == 0
    assert exact(classical_birthday(N, N)["verified_collision_probability"]) == 1


def test_oracle_free_driver_baseline_is_charged_as_known_search_not_extra_query_advantage():
    row = walk_control(8, 3, list(range(8)), "chirp_lifted", 4, gamma=0, include_arrays=True)
    assert row["preparation_function_evaluations"] == 0
    assert row["grover_iteration_function_evaluations"] == 4
    assert row["actual_verified_two_register_success"] == pytest.approx(row["phase_free_known_driver_partner_baseline"])
    assert row["initial_position_weights"] == pytest.approx([1/16]*16)
    assert row["unamplified_trial_function_evaluations"] == 2


def test_local_compiler_precision_is_not_silently_zero_in_physical_claim(report):
    row = report["local_driver_precision_counterledger"]
    assert exact(row["amplified_success_upper_with_error"]) > Fraction(1, 10**6)
    assert exact(row["assumed_total_composed_trace_error_budget"]) == Fraction(1, 10**6)
    for error in (True, 0.0, -1, Fraction(2)):
        with pytest.raises(ValueError):
            local_path_certificate(8, 4, error)


def test_oracle_free_preparation_mean_success_is_disjoint_marking_not_DHSP_lower_bound(report):
    for r in report["phase_free_all_shift_controls"]:
        assert r["uniform_shift_mean_success"] == pytest.approx(r["known_reflection_mixing_formula"])
        assert sum(r["all_shift_success_probabilities"]) <= 1+1e-12
        assert r["uniform_shift_mean_success"] <= r["upper_from_disjoint_hidden_shift_predicates"]
    for r in report["marker_only_scaling_certificates"]:
        n, j = r["modulus_bits"], r["ordinary_amplification_iterations"]
        assert exact(r["uniform_shift_mean_initial_success_upper"]) == Fraction(1, 1 << n)
        assert exact(r["uniform_shift_mean_amplified_success_upper"]) == min(Fraction(1), Fraction((2*j+1)**2, 1 << n))
        assert r["function_evaluations_with_final_verification"] == 4*j+2
        assert not r["initial_oracle_phases_or_coset_states_covered"]
        assert not r["general_full_oracle_DHSP_lower_bound"]
    assert exact(marker_only_certificate(256, 256**2)["uniform_shift_mean_amplified_success_upper"]) < Fraction(1, 10**60)


def test_shift_predicates_partition_cross_layer_pairs_with_arbitrary_ancilla_state():
    N, D = 8, 16
    rng = np.random.default_rng(41033)
    state = rng.normal(size=(3, D, D))+1j*rng.normal(size=(3, D, D))
    state /= np.linalg.norm(state)
    total = 0
    for s in range(N):
        labels = source_table(N, s, list(reversed(range(N))))
        good = np.array([[a != b and labels[a] == labels[b] for b in range(D)] for a in range(D)])
        total += float(np.sum(np.abs(state[:, good])**2))
    cross = np.array([[a//N != b//N for b in range(D)] for a in range(D)])
    assert total == pytest.approx(float(np.sum(np.abs(state[:, cross])**2)))
    assert total <= 1


def test_localized_pair_preparation_is_possible_but_selected_label_gap_remains_Grover(report):
    for r in report["selected_fibre_preparation_controls"]:
        N, j = r["rotation_order"], r["grover_preparation_iterations"]
        assert r["selected_fibre_mass"] == pytest.approx(r["grover_mass_formula"])
        assert r["two_fresh_preparations_collision_success"] == pytest.approx(r["collision_success_formula"])
        assert r["two_fresh_preparations_collision_success"] > .4
        assert r["two_preparations_function_evaluations_plus_verification"] == 4*j+2
        assert exact(r["minimum_protected_gap_squared"]) == Fraction(1, N)
        for row in r["protected_path_spectral_controls"]:
            assert row["plus_sector_gap"] == pytest.approx(row["known_label_search_gap_formula"])
        endpoint = r["protected_path_spectral_controls"][-1]
        assert endpoint["full_space_gap"] == pytest.approx(0, abs=1e-12)
        assert endpoint["plus_sector_gap"] == pytest.approx(1)
        assert not r["general_DHSP_lower_bound"]


def test_random_conditional_coset_localization_does_not_grant_matched_records(report):
    for r in report["random_coset_record_countercontrols"]:
        N = r["rotation_order"]
        pairs = sum(y == z for y in range(N) for z in range(N))
        unconditional = Fraction(pairs, 2*N*N)
        assert exact(r["actual_unconditional_two_fresh_records_partner_probability"]) == unconditional
        assert exact(r["two_fresh_coset_records_match_probability"]) == Fraction(1, N)
        assert exact(r["incorrect_average_of_conditional_IPRs"]) == N*unconditional
        assert exact(r["position_IPR_after_averaging_independent_records"]) == unconditional
        assert not r["matched_second_record_or_unknown_state_copy_supplied"]


@pytest.mark.parametrize("family,tau", [("hidden_driver", .75), ("local", -1), ("local", 1.1), ("local", True), ("local", float("nan"))])
def test_invalid_or_uncommitted_driver_inputs_rejected(family, tau):
    with pytest.raises(ValueError):
        driver(8, family, tau)


def test_invalid_source_clock_and_phase_inputs_rejected():
    for call in (lambda: source_table(8, 0, [0]*8),
                 lambda: source_table(8, True, list(range(8))),
                 lambda: walk_control(8, 1, list(range(8)), "local", 3),
                 lambda: floquet(8, list(range(16))),
                 lambda: floquet(8, [0]*16, gamma=float("inf")),
                 lambda: local_path_certificate(1, 2)):
        with pytest.raises(ValueError):
            call()


def test_no_candidate_or_speedup_or_generic_no_go_promotion(report):
    assert not any(report["claim_gate"].values())
