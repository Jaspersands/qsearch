"""Proof-oriented tests for a real copy-only terminal hidden-shift decoder."""
from itertools import product
import inspect
import json
import subprocess

from flint import fmpq
import numpy as np
import pytest

import theorems.ternary_phase_qubit_decoder as receiver
from native_generalized_dihedral_bridge import AdditiveChart, BinaryPhaseSample, project_native_density
from native_state_hsp_bridge import NativeGroup
from native_uniform_descent_receiver import SourceExhausted


def phase_sample(k, secret, ids, visibility=1):
    # Forward ideal phase fixture, never a receiver-side oracle.
    j = sum(a*s for a, s in zip(k, secret)) % 3
    psi = np.array([1, np.exp(2j*np.pi*j/3)])/np.sqrt(2)
    rho = visibility*np.outer(psi, psi.conj())+(1-visibility)*np.eye(2)/2
    return BinaryPhaseSample(tuple(k), (3,)*len(k), rho, tuple(ids))


def test_literal_anti_trine_has_positive_effects_isometry_and_known_qutrit_unitary():
    V = receiver.measurement_isometry()
    assert np.max(abs(V.conj().T@V-np.eye(2))) < 1e-12
    effects = [np.outer(row.conj(), row) for row in V]
    assert np.max(abs(sum(effects)-np.eye(2))) < 1e-12
    assert all(min(np.linalg.eigvalsh(E)) > -1e-12 and abs(np.trace(E)-2/3) < 1e-12 for E in effects)
    F = np.exp(-2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
    U = F@np.diag([1, -1, 1])
    assert np.max(abs(U[:, :2]-V)) < 1e-12
    assert np.max(abs(U.conj().T@U-np.eye(3))) < 1e-12
    for j in range(3):
        sample = phase_sample((1,), (j,), (0,))
        embedded = np.zeros((3, 3), complex)
        embedded[:2, :2] = sample.state
        physical = np.diag(U@embedded@U.conj().T).real
        _, b, record = receiver.anti_trine_measure(sample, np.random.default_rng(3+j))
        assert b != j
        assert np.max(abs(physical-record["actual_probabilities"])) < 1e-12
        assert abs(physical[j]) < 1e-12
        assert np.max(abs(physical[np.arange(3) != j]-.5)) < 1e-12


@pytest.mark.parametrize("n", (1, 2, 3))
def test_every_ideal_exclusion_yields_the_correct_quadratic_equation(n):
    for s, k in product(product(range(3), repeat=n), repeat=2):
        j = sum(a*b for a, b in zip(k, s)) % 3
        lift = tuple(s[i]*s[l] % 3 for i, l in receiver.symmetric_basis(n))+s
        for b in range(3):
            row, rhs = receiver.quadratic_equation(k, b)
            equality = sum(a*v for a, v in zip(row, lift)) % 3 == rhs
            assert equality == (b != j)


def test_actual_native_high_root_order_three_adapter_is_not_a_field_shadow():
    chart, G = AdditiveChart(4), NativeGroup(4)
    label, secret = chart.label((3, 6)), ((5, 2),)
    psi = G.supplied_phase_state(label, secret)
    sample, _ = project_native_density(label, np.outer(psi, psi.conj()), 4, (0,))
    row, axes = receiver.terminal_character_row(sample)
    assert row == (1, 2) and axes == (0, 1)
    terminal_secret = tuple(x % 3 for x in chart.coordinates(secret))
    _, excluded, _ = receiver.anti_trine_measure(sample, np.random.default_rng(1))
    assert excluded != sum(a*b for a, b in zip(row, terminal_secret)) % 3
    bad = BinaryPhaseSample((1, 6), chart.orders, sample.state, (1,))
    with pytest.raises(ValueError, match="order3 character subgroup"):
        receiver.terminal_character_row(bad)


@pytest.mark.parametrize("n", (1, 2, 4, 8, 16))
@pytest.mark.parametrize("zero", (False, True))
def test_actual_original_native_source_recovers_full_terminal_vector_including_zero(n, zero):
    c = receiver.source_control(n, 16000+n, zero_secret=zero)
    r = c["decoder"]
    assert r["recovered_ternary_secret"] == c["truth_fixture_only"]
    assert r["coefficient_rank"] == r["budget"]["lifted_unknown_dimension"]
    assert r["consumed_binary_inputs"] == r["budget"]["binary_copy_cap"]
    assert c["forbidden_outcomes_fixture_only"] == 0
    projected = c["original_projection"]
    assert projected["outputs_accepted"] == r["consumed_binary_inputs"]
    assert sorted(list(r["original_indices"])+projected["rejected_original_indices"]) == list(range(projected["original_inputs_supplied"]))
    assert c["known_native_qutrit_F3_readout_is_a_stronger_baseline_on_this_calibration_source"]
    assert not r["classical_hypotheses_enumerated"] and not r["receiver_takes_hidden_secret"]
    assert not r["new_quantum_speedup_established"]


def test_rank_deficiency_and_shortage_never_guess_or_regenerate_unknown_inputs():
    budget = receiver.decoder_budget(1)
    M = budget["binary_copy_cap"]
    zero_rows = [phase_sample((0,), (1,), (i,)) for i in range(M)]
    r = receiver.receive(receiver.FiniteBinarySource(zero_rows, M), 1, np.random.default_rng(2))
    assert r["status"] == "INSUFFICIENT_INDEPENDENT_QUADRATIC_ROWS" and r["recovered_ternary_secret"] is None
    short = receiver.receive(receiver.FiniteBinarySource(zero_rows[:1], M), 1, np.random.default_rng(2))
    assert short["status"] == "NO_COMPLETE_FINITE_SAMPLE_BATCH" and short["consumed_binary_inputs"] == 1
    assert short["source_exhaustion"]


def test_copy_reuse_is_rejected_even_across_separate_terminal_measurements():
    sample = phase_sample((1,), (2,), (0,))
    source = receiver.FiniteBinarySource([sample, sample], 2)
    source.take()
    with pytest.raises(ValueError, match="no cloning"):
        source.take()


def test_rank_one_lift_is_checked_not_promoted_from_a_unique_linear_solution(monkeypatch):
    M = receiver.decoder_budget(1)["binary_copy_cap"]
    samples = [phase_sample((i % 3,), (1,), (i,)) for i in range(M)]
    monkeypatch.setattr(receiver, "solve_full_rank_f3", lambda *args: (0, 1))
    r = receiver.receive(receiver.FiniteBinarySource(samples, M), 1, np.random.default_rng(4))
    assert r["status"] == "INVALID_RANK_ONE_LIFT" and r["recovered_ternary_secret"] is None


@pytest.mark.parametrize("n", (1, 2, 4, 8, 128, 256))
@pytest.mark.parametrize("bits", (1, 8, 64))
def test_scalable_rank_budget_is_a_conditional_expression_not_a_fitted_curve(n, bits):
    b = receiver.decoder_budget(n, bits)
    D, M = n*(n+1)//2+n, b["binary_copy_cap"]
    assert b["lifted_unknown_dimension"] == D and M == 3*D+2*bits
    exact = fmpq(3**D-1, 2)*fmpq(2, 3)**M
    assert exact < fmpq(1, 2**(bits+1))
    assert not b["source_IID_label_promise_proved_from_data"] and not b["noise_and_hardware_errors_included"]


def test_complete_dual_polynomial_support_escape_census():
    for c in receiver.dual_polynomial_census():
        assert c["dual_polynomials_tested"] == 242
        assert c["source_row_outcomes"] == 18 and c["minimum_nonzero_count"] >= 6
        assert sum(c["nonzero_count_histogram"].values()) == 242


@pytest.mark.parametrize("gamma", ("1", "99/100", "9/10", "0"))
def test_actual_dephased_POVM_and_strict_decoder_noise_ceiling(gamma):
    g = fmpq(gamma)
    for j in range(3):
        sample = phase_sample((1,), (j,), (0,), float(g))
        _, _, r = receiver.anti_trine_measure(sample, np.random.default_rng(1))
        assert abs(r["actual_probabilities"][j]-float((1-g)/3)) < 1e-12
        assert all(abs(r["actual_probabilities"][b]-float((2+g)/6)) < 1e-12 for b in range(3) if b != j)
    c = receiver.strict_decoder_noise_contract(4, gamma)
    assert fmpq(c["this_strict_decoder_correct_recovery_upper"]) == ((2+g)/3)**c["binary_copy_cap"]
    assert not c["all_quantum_receivers_excluded"] and not c["robust_error_correction_implemented"]


@pytest.mark.parametrize("gamma", ("9/10", "0"))
def test_noisy_native_countercontrol_falsifies_equations_instead_of_claiming_robustness(gamma):
    c = receiver.source_control(4, 15100, visibility=gamma)
    assert c["forbidden_outcomes_fixture_only"] > 0
    assert c["decoder"]["status"] == "INCONSISTENT_EXCLUSION_EQUATIONS"
    assert not c["decoder"]["noisy_error_correcting_decoder_supplied"]


@pytest.mark.parametrize("call", (
    lambda: receiver.quadratic_equation((True,), 1),
    lambda: receiver.quadratic_equation((1,), True),
    lambda: receiver.decoder_budget(0),
    lambda: receiver.strict_decoder_noise_contract(1, "-1"),
    lambda: receiver.FiniteBinarySource([], 0),
    lambda: receiver.terminal_character_row(BinaryPhaseSample((0,), (1,), np.eye(2)/2, (0,))),
    lambda: receiver.terminal_character_row(BinaryPhaseSample((1,), (4,), np.eye(2)/2, (0,))),
))
def test_invalid_field_source_and_budget_premises_rejected(call):
    with pytest.raises(ValueError):
        call()


def test_receiver_and_measurement_never_take_unknown_secret_or_value_oracle():
    for f in (receiver.receive, receiver.anti_trine_measure, receiver.quadratic_equation):
        assert "secret" not in inspect.signature(f).parameters
    source = inspect.getsource(receiver.receive)
    assert "product(" not in source and "truth" not in source


def test_independent_source_POVM_rank_and_noise_replay():
    checker = receiver.REPORT.parents[1]/"certificates/ternary_phase_qubit_decoder_crosscheck.js"
    out = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    r = json.loads(out.stdout)
    assert r["status"] == "PASS" and r["ideal_source_recoveries"] == 6
    assert r["dual_polynomials_replayed"] == 2178
    assert not r["new_quantum_speedup_established"]


@pytest.mark.parametrize("mutation", ("born", "outcome", "row", "lift", "rank", "original", "secret", "cap", "census", "noise", "claim"))
def test_checker_rejects_false_exclusions_free_inputs_rank_and_recovery_claims(tmp_path, mutation):
    r = json.loads(receiver.REPORT.read_text())
    c = r["ideal_original_source_controls"][1]
    d = c["decoder"]
    m = d["measurement_records"][0]
    if mutation == "born":
        m["actual_probabilities"][0] += .1
    elif mutation == "outcome":
        m["excluded_value_observed"] = sum(a*s for a, s in zip(m["ternary_character_row"], c["truth_fixture_only"])) % 3
    elif mutation == "row":
        m["ternary_character_row"][0] ^= 1
    elif mutation == "lift":
        d["lifted_solution"][0] ^= 1
    elif mutation == "rank":
        d["coefficient_rank"] -= 1
    elif mutation == "original":
        m["original_indices"] = d["measurement_records"][1]["original_indices"]
    elif mutation == "secret":
        d["recovered_ternary_secret"][0] ^= 1
    elif mutation == "cap":
        d["budget"]["binary_copy_cap"] -= 1
    elif mutation == "census":
        r["complete_dual_polynomial_censuses_dimension2"][0]["minimum_nonzero_count"] -= 1
    elif mutation == "noise":
        r["strict_decoder_noise_contracts"][2]["this_strict_decoder_correct_recovery_upper"] = "1"
    else:
        r["accepted_speedup_candidate"] = True
    target = tmp_path/"forged.json"
    target.write_text(json.dumps(r))
    out = subprocess.run(["node", str(receiver.REPORT.parents[1]/"certificates/ternary_phase_qubit_decoder_crosscheck.js"), str(target)], capture_output=True)
    assert out.returncode != 0
