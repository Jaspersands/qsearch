"""Normalized row access is distinct from a forward evaluator or discarded pointer."""
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest
from flint import fmpq

from theorems import native_word_frame_access as W
from ternary_noise_degradation import NoisyLinearRecord


def fixture(n=1, r=2, B=1, M=3, noisy=False, seed=89001):
    recipe, truth, errors = W.source_fixture(n, r, B, M, noisy, seed)
    src = recipe["source_receipts"]
    raw = tuple(NoisyLinearRecord(tuple(x["label"]), x["value"], x["modulus"], x["source_id"])
                for x in src["original_classical_records"])
    return raw, tuple(src["preparation_random_mask"]), truth, errors


@pytest.mark.parametrize("B,M", ((1, 3), (2, 2), (4, 1)))
def test_compiled_feature_phases_are_actual_signed_original_values(B, M):
    raw, mask, _, _ = fixture(B=B, M=M)
    F = W.finite_frame(raw, mask, B, M)
    for row, beta in zip(F["rows"], F["word_coefficients"]):
        assert row["known_phase"] == sum(b*(r.value+sum(a*m for a, m in zip(r.label, mask)))
                                        for b, r in zip(beta, raw)) % 9
        assert row["frequency"] == tuple(sum(b*r.label[i] for b, r in zip(beta, raw)) % 9
                                         for i in range(len(mask)))
    spec = F["spec"]
    assert spec["original_records_paid_once"] == 2*B*M
    assert spec["cohort_controlled_local_diagonal_gates"] == B*M
    assert not spec["same_as_previous_native_point_seed"]
    assert not spec["secret_or_errors_supplied_to_preparation"]
    assert not spec["normalized_fibre_oracle_supplied"]


def test_frame_singular_values_and_partial_polar_are_the_actual_public_counts():
    raw, mask, _, _ = fixture()
    F = W.finite_frame(raw, mask, 1, 3)
    J, Q, p = F["J"], F["Q"], F["counts"]/27
    assert np.max(abs(J@J.conj().T-np.diag(p))) < 1e-12
    assert np.max(abs(Q@Q.conj().T-np.diag(p > 0))) < 1e-12
    assert np.max(abs(J-np.sqrt(p)[:, None]*Q)) < 1e-12
    expected = sorted(np.sqrt(p[p > 0]), reverse=True)
    actual = np.linalg.svd(J, compute_uv=False)
    assert np.max(abs(actual[:len(expected)]-expected)) < 1e-12


@pytest.mark.parametrize("noisy", (False, True))
def test_complete_reference_dilation_keeps_fibre_orthogonal_failure(noisy):
    raw, mask, _, _ = fixture(noisy=noisy)
    F = W.finite_frame(raw, mask, 1, 3)
    Q, fail, dilation = F["Q"], F["failure"], F["dilation"]
    assert np.max(abs(dilation.conj().T@dilation-np.eye(27))) < 1e-12
    state = F["state"]
    good, bad = Q@state, fail@state
    assert abs(np.vdot(good, good).real+np.vdot(bad, bad).real-1) < 1e-12
    if noisy: assert np.vdot(bad, bad).real > 0.01


def test_multidimensional_transform_is_group_Fourier_not_cyclic_lexicographic_QFT():
    raw, mask, _, _ = fixture(n=2, M=2)
    F = W.finite_frame(raw, mask, 1, 2)
    group = F["group_inverse_Fourier"]
    q, n, N = 9, 2, 81
    assert np.max(abs(group.conj().T@group-np.eye(N))) < 1e-12
    assert abs(group[1, 1]-np.exp(-2j*np.pi/q)/np.sqrt(N)) < 1e-12
    cyclic = np.exp(-2j*np.pi*np.outer(np.arange(N), np.arange(N))/N)/np.sqrt(N)
    assert np.max(abs(group-cyclic)) > 0.1


@pytest.mark.parametrize("noisy", (False, True))
def test_pointer_trace_dephases_all_known_phases_and_outputs_uniform_Fourier(noisy):
    raw, mask, _, _ = fixture(noisy=noisy)
    F = W.finite_frame(raw, mask, 1, 3)
    # Explicit public forward evaluator with retained word pointer, then trace it.
    D, N = F["J"].shape[1], F["J"].shape[0]
    joint = np.zeros((D, N), dtype=complex)
    for x, row in enumerate(F["rows"]):
        joint[x, F["frequencies"].index(row["frequency"])] = F["state"][x]
    reduced = joint.T@joint.conj()
    assert np.max(abs(reduced-np.diag(F["counts"]/D))) < 1e-12
    law = F["group_inverse_Fourier"]@reduced@F["group_inverse_Fourier"].conj().T
    assert np.max(abs(np.diag(law)-1/N)) < 1e-12


def test_ideal_receiver_formula_and_comparison_postselection_have_different_normalization():
    raw, mask, truth, _ = fixture()
    F = W.finite_frame(raw, mask, 1, 3)
    D, N = F["J"].shape[1], F["J"].shape[0]
    target = F["frequencies"].index(tuple(truth))
    good = F["group_inverse_Fourier"]@F["Q"]@F["state"]
    raw_good = F["group_inverse_Fourier"]@F["J"]@F["state"]
    ideal = sum(np.sqrt(F["counts"]))**2/(D*N)
    assert abs(abs(good[target])**2-ideal) < 1e-12
    assert abs(abs(raw_good[target])**2-1/N) < 1e-12
    assert ideal > 1/N
    interval = W.ideal_success_interval(tuple(int(x) for x in F["counts"]), D, N)
    assert float(Fraction(interval["lower"]))-1e-12 <= ideal <= float(Fraction(interval["upper"]))+1e-12


@pytest.mark.parametrize("B,M", ((1, 1), (1, 3), (2, 2), (4, 1)))
def test_exact_word_second_moment_identity_needs_no_independence_or_centring(B, M):
    errors = tuple(((-1)**j)*(j+1) for j in range(2*B*M))
    values = []
    for b in range(B):
        for word in product(range(3), repeat=M):
            values.append(sum((errors[2*(b*M+j)], errors[2*(b*M+j)+1]-errors[2*(b*M+j)],
                               -errors[2*(b*M+j)+1])[t] for j, t in enumerate(word))**2)
    exact = fmpq(sum(values), len(values))
    assert exact == W.word_error_second_moment(errors, B, M)
    assert exact <= fmpq(sum(e*e for e in errors), B)


def test_frozen_correlated_nonzero_mean_errors_still_obey_pathwise_pure_distance_bound():
    q, errors, labels = 27, (2, 2, 2, 2), ((1,), (7,), (4,), (11,))
    raw = tuple(NoisyLinearRecord(a, (a[0]*5+e) % q, q, f"correlated-{j}") for j, (a, e) in enumerate(zip(labels, errors)))
    F = W.finite_frame(raw, (0,), 1, 2)
    ideal = np.array([np.exp(2j*np.pi*row["frequency"][0]*5/q) for row in F["rows"]])/3
    distance2 = 1-abs(np.vdot(ideal, F["state"]))**2
    exact_second = W.word_error_second_moment(errors, 1, 2)
    assert distance2 <= float(40*exact_second/(q*q))+1e-12
    L = W.noise_ledger(2, q, 4)
    assert not L["original_independence_or_zero_mean_required"]
    assert not L["errors_independent_of_public_labels_required"]


def test_noise_ledger_has_exact_enclosed_bound_not_a_lower_bound_on_actual_error():
    L = W.noise_ledger(5, 81, "3/2", bits=100)
    x = Fraction(80*5*3, 2*81**2)
    assert Fraction(L["mean_pure_trace_distance_squared_upper"]) == x
    a = Fraction(L["mean_unconditional_measurement_loss_bound_lower_enclosure"])
    b = Fraction(L["mean_unconditional_measurement_loss_upper"])
    assert a*a <= x <= b*b and b-a <= Fraction(1, 2**100)
    assert L["bound_is_on_complete_good_and_failure_measurement"]
    assert not L["ideal_fibre_coverage_or_success_proved_by_moments"]
    assert not L["generic_physical_gate_errors_included"]


@pytest.mark.parametrize("n", (8, 32, 64, 128))
def test_balanced_symbolic_scale_has_condition_one_but_exponential_absolute_cost(n):
    C = W.balanced_scale(n, n)
    assert C["supported_condition_number_squared"] == "1"
    assert fmpq(C["comparison_singular_value_squared"]) == fmpq(1, 3**(n*n))
    assert fmpq(C["normalization_multiplier_squared"]) == 3**(n*n)
    assert not C["actual_random_native_family_is_proved_balanced"]
    assert not C["polynomial_clean_row_implementation_supplied"]
    assert not C["all_decoders_have_this_normalization_cost"]


def test_scalable_preparation_contract_does_not_materialize_exponential_words():
    raw, mask, _, _ = fixture(r=64, M=6)
    C = W.preparation_contract(raw, mask, 1, 6)
    assert C["frequency_coordinate_trits"] == 64
    assert C["original_records_paid_once"] == 12
    assert not C["all_word_table_required_for_indexed_preparation"]
    with pytest.raises(ValueError, match="finite cap"):
        W.finite_frame(raw, mask, 1, 6)


@pytest.mark.parametrize("counts,D,N", (((1, 1), 3, 2), ((-1, 4), 3, 2), ((1.0, 2), 3, 2), ((3,), 3, 2)))
def test_invalid_ideal_fibre_count_promises_rejected(counts, D, N):
    with pytest.raises(ValueError): W.ideal_success_interval(counts, D, N)


def test_report_retains_missing_circuit_and_all_noisy_failure_mass():
    p = json.loads(W.REPORT.read_text())
    assert not p["accepted_speedup_candidate"]
    assert not p["efficient_normalized_fibre_circuit_supplied"]
    assert not p["general_quantum_decoder_lower_bound_proved"]
    for c in p["bounded_reference_controls"]:
        assert abs(c["reference_good_mass"]+c["reference_failure_mass"]-1) < 1e-10
        assert c["reference_correct_and_good_probability"] <= c["reference_good_mass"]+1e-10
        assert not c["finite_float_laws_are_exact_certificates"]
    assert any(c["reference_failure_mass"] > .1 for c in p["bounded_reference_controls"])


@pytest.mark.parametrize("n,B,M", ((1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1)))
def test_complete_small_label_populations_have_exact_collision_law_and_receiver_bound(n, B, M):
    # Enumerate actual paired labels only, not guessed random occupancy statistics.
    q, D, N = 3, B*3**M, 3**n
    collision, ideal_lower, families = fmpq(0), fmpq(0), 0
    for flat in product(range(q), repeat=2*B*M*n):
        labels = tuple(tuple(flat[j*n:(j+1)*n]) for j in range(2*B*M))
        raw = tuple(NoisyLinearRecord(a, 0, q, f"population-{j}") for j, a in enumerate(labels))
        family = W.public_family(raw, B, M)
        counts = {x: 0 for x in product(range(q), repeat=n)}
        for b in range(B):
            for word in product(range(3), repeat=M): counts[family.frequency(b, word)] += 1
        collision += fmpq(sum(x*x for x in counts.values()), D*D)
        ideal_lower += fmpq(W.ideal_success_interval(tuple(counts.values()), D, N)["lower"])
        families += 1
    assert collision/families == fmpq(1, N)+fmpq(N-1, N*D)
    L = W.random_label_receiver_ledger(n, 1, B, M, 0)
    assert ideal_lower/families+fmpq(1, 2**90) >= fmpq(L["ideal_ensemble_receiver_success_lower"])
    assert L["normalized_fibre_circuit_is_an_explicit_missing_assumption"]
    assert not L["per_dataset_success_or_exact_balance_guaranteed"]


def test_ensemble_noise_loss_scales_down_without_per_instance_or_circuit_claims():
    last = fmpq(0)
    for n in (8, 32, 64, 128):
        q, M = 3**n, n*n+24
        L = W.random_label_receiver_ledger(n, n, 1, M, fmpq(q*q, 3*n**6)+fmpq(1, 2))
        assert fmpq(L["ideal_ensemble_receiver_failure_upper"]) < fmpq(1, 3**24)
        current = fmpq(L["noisy_complete_ensemble_receiver_success_lower"])
        assert current > last
        assert not L["efficient_receiver_constructed"] and not L["accepted_speedup_candidate"]
        assert not L["original_errors_independent_of_labels_required"]
        last = current
    assert last > fmpq(999, 1000)


def test_independent_checker_replays_report():
    checker = W.ROOT/"research/certificates/native_word_frame_crosscheck.js"
    p = subprocess.run(["node", str(checker)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


@pytest.mark.parametrize("mutation", ("counts", "phase", "noise", "garbage", "candidate", "scale", "law", "ensemble", "source_law", "ideal_interval"))
def test_independent_checker_rejects_false_scope_and_wrong_laws(mutation, tmp_path):
    p = json.loads(W.REPORT.read_text()); c = p["bounded_reference_controls"][0]
    if mutation == "counts": c["fibre_counts"][0] += 1
    if mutation == "phase": c["word_rows"][0]["known_phase"] = (c["word_rows"][0]["known_phase"]+1) % 3
    if mutation == "noise": p["scalable_conditional_access_ledgers"][0]["noise"]["mean_pure_trace_distance_squared_upper"] = "0"
    if mutation == "garbage": p["bounded_reference_controls"][3]["reference_failure_mass"] = 0
    if mutation == "candidate": p["accepted_speedup_candidate"] = True
    if mutation == "scale": p["scalable_conditional_access_ledgers"][0]["hypothetical_balanced_access"]["normalization_multiplier_squared"] = "1"
    if mutation == "law": c["pointer_discarded_Fourier_probabilities"][0] = 1
    if mutation == "ensemble": p["scalable_conditional_access_ledgers"][0]["random_label_reference"]["noisy_complete_ensemble_receiver_success_lower"] = "1"
    if mutation == "source_law": p["scalable_conditional_access_ledgers"][0]["random_label_reference"]["source_population_promises_established_by_small_artifacts"] = True
    if mutation == "ideal_interval": c["ideal_clean_receiver_success_interval"]["lower"] = "0"
    target = tmp_path/"forged.json"; target.write_text(json.dumps(p))
    checker = W.ROOT/"research/certificates/native_word_frame_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(target)], capture_output=True, text=True)
    assert result.returncode != 0, mutation
