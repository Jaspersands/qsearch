"""Source-conditional membership, null independence and non-free projection."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from theorems import native_word_span_decision as W
from native_word_frame_access import finite_frame
from native_full_root_slice import source_data
from ternary_noise_degradation import NoisyLinearRecord


@pytest.mark.parametrize("n,r,M", ((1, 1, 3), (1, 2, 4), (2, 1, 3)))
def test_actual_ideal_source_has_exact_membership_without_balance(n, r, M):
    c = W.finite_control(n, r, M, False, 99101)
    assert c["exact_span_acceptance_root_polynomial"] == ("1",)
    assert c["diagnostic_span_acceptance_probability"] == pytest.approx(1)
    assert Fraction(c["exact_uniform_raw_value_null_acceptance"]) == Fraction(c["span_rank"], 3**M)
    assert not c["dense_reference_is_an_efficient_decision_algorithm"]


def test_zero_labels_missing_all_other_frequencies_do_not_break_membership_or_null_trace():
    raw = tuple(NoisyLinearRecord((0,), 0, 9, f"zero-label-{j}") for j in range(4))
    c = W.finite_record_control(raw, (0,), (7,), (0,)*4)
    assert c["span_rank"] == 1 and c["actual_fibre_counts"][0] == 9
    assert c["exact_span_acceptance_root_polynomial"] == ("1",)
    assert c["exact_uniform_raw_value_null_acceptance"] == "1/9"
    # This is an assumption countercontrol, not a cryptographically hard family.


def test_injective_finite_map_has_identity_projection_and_no_decision_advantage():
    raw = (NoisyLinearRecord((1,), 4, 9, "injective-a"), NoisyLinearRecord((4,), 7, 9, "injective-c"))
    c = W.finite_record_control(raw, (0,), (4,), (0, 0))
    assert c["span_rank"] == c["word_dimension"] == 3
    assert c["exact_uniform_raw_value_null_acceptance"] == "1"
    assert W.decision_ledger(1, 2, 1, 0, effect_error="0")["decision_advantage_lower_IF_effect_and_source_promises_hold"] == "0"


def test_IID_uniform_original_values_average_to_identity_not_a_balanced_fibre_premise():
    labels = ((1,), (1,), (0,), (1,))
    density = np.zeros((9, 9), dtype=complex)
    probabilities = []
    projector = None
    for b in product(range(3), repeat=4):
        raw = tuple(NoisyLinearRecord(a, t, 3, f"iid-{j}") for j, (a, t) in enumerate(zip(labels, b)))
        f = finite_frame(raw, (0,), 1, 2)
        projector = f["fibre_projector"]
        psi = f["state"]
        density += np.outer(psi, psi.conj())/81
        probabilities.append(float(np.vdot(psi, projector@psi).real))
    assert np.max(abs(density-np.eye(9)/9)) < 1e-12
    assert np.mean(probabilities) == pytest.approx(np.trace(projector).real/9)


def test_uniform_marginals_are_not_enough_for_null_bound():
    c = W.null_independence_countercontrol()
    assert c["exact_correlated_null_mean_span_acceptance"] == "1"
    assert c["exact_IID_null_mean_span_acceptance"] == "1/3"
    assert c["each_raw_value_marginal_uniform"] and not c["raw_values_jointly_IID"]
    for b in c["complete_equal_weight_original_banks"]:
        assert b["exact_span_acceptance_root_polynomial"] == ("1",)


def test_adaptive_mask_changes_null_density_but_not_full_span_acceptance():
    density = np.zeros((9, 9), dtype=complex)
    acceptance = []
    for values in product(range(3), repeat=4):
        raw = tuple(NoisyLinearRecord((1,), t, 3, f"adaptive-mask-{j}") for j, t in enumerate(values))
        mask = ((-2*values[0]+values[1]) % 3,)
        unmasked, masked = finite_frame(raw, (0,), 1, 2), finite_frame(raw, mask, 1, 2)
        p = float(np.vdot(masked["state"], masked["fibre_projector"]@masked["state"]).real)
        q = float(np.vdot(unmasked["state"], unmasked["fibre_projector"]@unmasked["state"]).real)
        assert p == pytest.approx(q)
        acceptance.append(p);density += np.outer(masked["state"], masked["state"].conj())/81
    assert np.max(abs(density-np.eye(9)/9)) > .05
    assert np.mean(acceptance) == pytest.approx(1/3)
    assert not W.decision_ledger(1, 2, 4, 0)["identity_null_density_after_data_adaptive_mask_claimed"]


def test_span_is_label_only_but_input_state_uses_actual_original_values():
    raw, mask, _, _ = source_data(1, 2, 3, False, 99103)
    changed = (replace(raw[0], value=(raw[0].value+1) % 9), *raw[1:])
    f, g = finite_frame(raw, mask, 1, 3), finite_frame(changed, mask, 1, 3)
    assert np.array_equal(f["fibre_projector"], g["fibre_projector"])
    assert W.span_coefficients(f) != W.span_coefficients(g)
    assert np.max(abs(f["state"]-g["state"])) > .01


def test_frozen_correlated_nonzero_mean_errors_obey_squared_not_sqrt_rejection_bound():
    q, secret, labels, errors = 27, 5, ((1,), (7,), (4,), (11,)), (1, 1, 2, 2)
    raw = tuple(NoisyLinearRecord(a, (a[0]*secret+e) % q, q, f"correlated-{j}") for j, (a, e) in enumerate(zip(labels, errors)))
    c = W.finite_record_control(raw, (0,), (secret,), errors)
    assert 1-c["diagnostic_span_acceptance_probability"] <= float(Fraction(c["pathwise_span_rejection_upper"]))+1e-12
    second = Fraction(str(W.word_error_second_moment(errors, 1, 2)))
    assert Fraction(c["pathwise_span_rejection_upper"]) == min(1, 40*second/q**2)
    l = W.decision_ledger(1, 3, 2, 4)
    assert l["source_span_rejection_upper"] == str(Fraction(80*2*4, q*q))
    assert not l["original_noise_independence_or_label_independence_required_for_moment_bound"]


def test_balanced_condition_one_comparison_is_not_the_span_effect():
    raw = (NoisyLinearRecord((1,), 1, 3, "balanced-a"), NoisyLinearRecord((1,), 1, 3, "balanced-c"),
           NoisyLinearRecord((1,), 1, 3, "balanced-b"), NoisyLinearRecord((1,), 1, 3, "balanced-d"))
    f = finite_frame(raw, (0,), 1, 2)
    assert tuple(f["counts"]) == (3, 3, 3)
    assert np.max(abs(f["J"].conj().T@f["J"]-f["fibre_projector"]/3)) < 1e-12
    psi = f["state"]
    assert np.vdot(psi, f["fibre_projector"]@psi).real == pytest.approx(1)
    assert np.vdot(psi, f["J"].conj().T@f["J"]@psi).real == pytest.approx(1/3)
    l = W.normalization_countercontrol(128, 128)
    assert l["supported_condition_number"] == "1"
    assert l["hypothetical_raw_comparison_positive_eigenvalue"]["exponent"] == -128**2
    assert not l["efficient_group_twirl_or_label_forward_map_supplies_span_projection"]


def test_effect_accuracy_and_each_input_preparation_loss_are_both_charged():
    a = W.decision_ledger(2, 3, 10, "1/4", effect_error="1/16", preparation_trace_error="1/64")
    expected = 1-Fraction(80*10, 4*27**2)-Fraction(1, 81)-Fraction(1, 8)-Fraction(1, 32)
    assert Fraction(a["decision_advantage_lower_IF_effect_and_source_promises_hold"]) == max(0, expected)
    b = W.decision_ledger(2, 3, 10, 0, "1/16", "1")
    assert b["decision_advantage_lower_IF_effect_and_source_promises_hold"] == "0"
    assert a["uniform_operator_norm_approximation_is_sufficient_not_necessary"]
    assert not a["span_projection_proved_easier_than_coherent_row_preparation"]


@pytest.mark.parametrize("n", (8, 32, 64, 128))
def test_quadratic_bank_conditional_gap_survives_but_no_algorithm_is_supplied(n):
    q, M, alpha = 3**n, n*n+12, Fraction(1, n**3)
    l = W.decision_ledger(n, n, M, q*q*alpha*alpha/3+Fraction(1, 2), preparation_trace_error="1/64")
    assert Fraction(l["decision_advantage_lower_IF_effect_and_source_promises_hold"]) > Fraction(4, 5)
    assert l["uniform_null_acceptance_upper_without_balance"] == str(Fraction(1, 3**12))
    assert not l["balanced_fibres_or_full_frequency_coverage_assumed"]
    assert not l["source_noise_and_gate_precision_promises_established"]
    assert not l["efficient_span_effect_supplied"]


@pytest.mark.parametrize("n,expected_h", ((1, 2), (2, 2), (6, 3), (7, 4), (32, 6)))
def test_width_changing_route_uses_exact_declared_smoothing_function(n, expected_h):
    l = W.prime_power_route(n, max(n, 8), Fraction(1, max(2, n)**3), 2*(n*n+12))
    assert l["smoothing_function_value"] == expected_h
    assert Fraction(l["search_continuous_D_alpha_width"])*expected_h**2 == Fraction(l["decision_continuous_D_alpha_width"])
    assert l["polynomial_expansion_of_disjoint_original_samples_is_required"]
    assert not l["same_width_search_recovery_claimed"]
    assert not l["fixed_existing_source_bank_suffices_proved"]


def test_necessary_hard_source_guard_is_separate_from_search_to_decision_guards():
    a, b = W.prime_power_route(8, 8, "1/512", 152), W.prime_power_route(32, 32, "1/32768", 2072)
    assert a["selected_prime_power_theorem_parameter_guards"]
    assert not a["search_alpha_q_at_least_2_sqrt_n"]
    assert b["selected_prime_power_theorem_parameter_guards"] and b["search_alpha_q_at_least_2_sqrt_n"]
    assert not b["worst_case_lattice_reduction_compatibility_established"]
    assert not W.prime_power_route(8, 1, "1/512", 152)["selected_prime_power_theorem_parameter_guards"]


def test_round_then_widen_is_only_a_coupling_not_exact_source_replacement():
    l = W.prime_power_route(32, 32, "1/32768", 2072)
    beta2 = Fraction(l["fresh_auxiliary_Gaussian_width_squared"])
    assert Fraction(l["rounded_search_input_then_fresh_Gaussian_widening_TV_squared_upper"]) == Fraction(11*2072, 28*3**64)/beta2
    assert not l["rounding_then_widening_claimed_exact"]
    assert l["fresh_Gaussian_auxiliary_noise_is_not_a_fresh_original_sample"]
    assert not l["full_source_adapter_or_published_reduction_implemented"]


@pytest.mark.parametrize("q", (1, 6, 9.0, True, 3**8))
def test_finite_polynomial_rejects_wrong_ring_or_unpaid_allocation(q):
    with pytest.raises(ValueError): W.root_polynomial([], q)


@pytest.mark.parametrize("moment,eps,delta", ((-1, 0, 0), (True, 0, 0), (0, .01, 0), (0, "2", 0), (0, 0, "-1/2")))
def test_scientific_ledgers_reject_inexact_or_invalid_promises(moment, eps, delta):
    with pytest.raises(ValueError): W.decision_ledger(2, 2, 7, moment, eps, delta)


def test_large_dense_reference_refuses_to_stand_in_for_scalable_projection():
    raw, mask, truth, errors = source_data(1, 16, 6, False, 99106)
    with pytest.raises(ValueError, match="finite cap"):
        W.finite_record_control(raw, mask, truth, errors)


def test_false_truth_receipts_are_rejected_before_reference_probability():
    raw, mask, truth, errors = source_data(1, 2, 3, False, 99107)
    with pytest.raises(ValueError, match="truth-only source"):
        W.finite_record_control(raw, mask, truth, (1,)*len(errors))


def node_verify(report):
    return subprocess.run(["node", "-e",
        "const C=require('./research/certificates/native_word_span_decision_crosscheck.js');"
        "C.verify(JSON.parse(require('fs').readFileSync(0,'utf8')));"],
        input=json.dumps(report), text=True, cwd=W.ROOT, capture_output=True)


def test_independent_certificate_replays_live_words_and_conditional_ledgers():
    p = json.loads(W.REPORT.read_text())
    result = node_verify(p)
    assert result.returncode == 0, result.stderr
    assert not p["accepted_speedup_candidate"] and not p["new_active_negative_result_created"]


@pytest.mark.parametrize("kind", ("phase", "polynomial", "null", "gap", "width", "guards", "TV", "free-effect", "dependent-null", "source-hash"))
def test_independent_checker_rejects_tampered_scientific_claims(kind):
    p = deepcopy(json.loads(W.REPORT.read_text()))
    c, d, w = p["actual_original_data_controls"][0], p["scaling_decision_route_ledgers"][0]["decision"], p["scaling_decision_route_ledgers"][0]["width_changing_search_route"]
    if kind == "phase": c["actual_word_rows"][0]["known_phase"] = (c["actual_word_rows"][0]["known_phase"]+1) % 3
    elif kind == "polynomial": c["exact_span_acceptance_root_polynomial"] = ["0"]
    elif kind == "null": c["exact_uniform_raw_value_null_acceptance"] = "0"
    elif kind == "gap": d["decision_advantage_lower_IF_effect_and_source_promises_hold"] = "1"
    elif kind == "width": w["search_to_decision_width_multiplier"] = 1
    elif kind == "guards": w["search_alpha_q_at_least_2_sqrt_n"] = True
    elif kind == "TV": w["rounded_search_input_then_fresh_Gaussian_widening_TV_squared_upper"] = "0"
    elif kind == "free-effect": d["efficient_span_effect_supplied"] = True
    elif kind == "dependent-null": p["null_independence_countercontrol"]["raw_values_jointly_IID"] = True
    else: p["producer_sha256"] = "0"*64
    result = node_verify(p)
    assert result.returncode != 0


def test_exact_root_polynomial_has_canonical_field_reduction():
    for q in (3, 9, 27):
        c = [Fraction(0)]*q;c[0] = c[q//3] = c[2*q//3] = Fraction(1)
        assert W.root_polynomial(c, q) == ()
        c[0] += Fraction(1, 2)
        assert W.root_polynomial(c, q) == ("1/2",)
