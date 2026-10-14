"""Actual known-bank access, frozen reuse, pure gauge and gap falsifiers."""
from copy import deepcopy
from itertools import product
import inspect
import json
import math
import subprocess

from flint import fmpq
import numpy as np
import pytest

from theorems.known_preparation_coherent_reflection import (
    IID, REPORT, ROOT, build_report, central_support, correlated_bank_counterexample,
    dense_preparation, exact_iid_control, finite_bank_gap_budget,
    frozen_bank_counterexample, iid_characteristic_statistics,
    preparation_control, reflection_budget, reflection_recipe,
)
from cyclotomic_rescaling_gate import multiply
from native_noisy_phase_input import prepare_inputs
from native_state_hsp_bridge import NativeGroup, ring_words
from ternary_noise_degradation import NoisyLinearRecord


def records(B=2, M=2, digits=2):
    q = 3**digits
    return tuple(NoisyLinearRecord((i % q, (2*i+1) % q), (i*i+3) % q, q, f"reflection-original-{i}") for i in range(2*B*M))


@pytest.mark.parametrize("digits", (1, 2, 16, 64))
def test_actual_recipe_is_same_original_data_and_no_ideal_unknown_inverse(digits):
    raw = records(digits=digits)
    recipe = reflection_recipe(raw, (1, 2), 2, 2)
    actual = prepare_inputs(raw, (1, 2), "1")
    assert tuple(p[1:] for c in recipe["known_phase_numerators"] for p in c) == tuple(r["known_phase_values"] for r in actual.reduction_side_recipes)
    assert recipe["original_classical_record_count"] == 8
    assert recipe["controlled_diagonal_branches_per_preparation_upper"] == 8
    assert recipe["preparation_calls_per_reflection"] == 2
    assert not recipe["secret_or_errors_read_by_preparation"]
    assert not recipe["ideal_unknown_state_inverse_supplied"]
    assert not recipe["new_independent_originals_created_by_reuse"]
    assert "secret" not in inspect.signature(reflection_recipe).parameters
    assert "errors" not in inspect.signature(reflection_recipe).parameters


@pytest.mark.parametrize("bad", ("short", "duplicate", "non_power_two", "zero_sites", "opaque_quantum"))
def test_recipe_rejects_unpaid_or_unimplemented_source_access(bad):
    raw, B, M = records(), 2, 2
    if bad == "short": raw = raw[:-2]
    if bad == "duplicate": raw = (raw[0], raw[0])+raw[2:]
    if bad == "non_power_two": B = 3
    if bad == "zero_sites": M = 0
    if bad == "opaque_quantum": raw = (np.ones(3)/math.sqrt(3),)*8
    with pytest.raises(ValueError): reflection_recipe(raw, (1, 2), B, M)


@pytest.mark.parametrize("B,M", ((1, 3), (2, 1), (2, 2), (4, 2)))
def test_literal_forward_inverse_reflection_preserve_complete_cohort_gauge(B, M):
    recipe = reflection_recipe(records(B, M), (1, 2), B, M)
    U, psi, R, phases = dense_preparation(recipe["known_phase_numerators"], 9)
    assert np.max(abs(U.conj().T@U-np.eye(len(psi)))) < 1e-12
    assert np.max(abs(U.conj().T@psi-np.eye(len(psi))[:, 0])) < 1e-12
    assert np.max(abs(R-(np.eye(len(psi))-2*np.outer(psi, psi.conj())))) < 1e-12
    assert np.max(abs(R@R-np.eye(len(psi)))) < 1e-12
    assert np.max(abs(psi-np.exp(2j*np.pi*np.array(phases)/9)/math.sqrt(len(psi)))) < 1e-12
    # Swapping the inverse layers is a different operation.
    diagonal = np.diag(np.exp(2j*np.pi*np.array(phases)/9))
    fourier_layer = diagonal.conj().T@U
    wrong_inverse = diagonal.conj().T@fourier_layer.conj().T
    assert np.max(abs(wrong_inverse@psi-np.eye(len(psi))[:, 0])) > .01


def test_cohort_global_phase_cannot_be_removed_from_an_indexed_seed():
    _, psi, R, _ = dense_preparation((((0, 1, 2),), ((0, 4, 8),)), 9)
    rephased = psi.copy()
    rephased[3:] *= np.exp(2j*np.pi/3)
    changed = np.eye(6)-2*np.outer(rephased, rephased.conj())
    assert np.linalg.norm(changed-R, 2) > 1
    assert abs(abs(np.vdot(psi, rephased))**2-.25) < 1e-12


@pytest.mark.parametrize("B", (1, 2, 4))
def test_reflection_operator_identity_and_K_copies_follow_point_fidelity(B):
    raw = records(B, 2)
    r = reflection_recipe(raw, (1, 2), B, 2)
    _, actual, R, _ = dense_preparation(r["known_phase_numerators"], 9)
    zeros = tuple(tuple((0, 0, 0) for _ in range(2)) for _ in range(B))
    _, ideal, R0, _ = dense_preparation(zeros, 9)
    d2 = 1-abs(np.vdot(ideal, actual))**2
    assert abs(np.linalg.norm(R-R0, 2)**2-4*d2) < 1e-11
    for K in (1, 2, 8): assert 1-(1-d2)**K <= K*d2+1e-12


@pytest.mark.parametrize("q,B,M", ((3, 1, 1), (9, 1, 2), (9, 2, 1), (9, 2, 2)))
def test_exact_full_error_census_matches_actual_coherent_seed_law(q, B, M):
    c = exact_iid_control(q, B, M)
    assert c["mean_fidelity_exact"] == c["formula_fidelity_exact"]
    assert c["error_configurations_checked"] == 2**(2*B*M)
    g = math.cos(2*math.pi/q)
    a, C = (1+2*g)/3, (3+4*g+2*g*g)/9
    predicted = a**(2*M)+(C**M-a**(2*M))/B
    observed = []
    for signs in product((-1, 1), repeat=2*B*M):
        phases = tuple(tuple((0, signs[2*(b*M+j)] % q, signs[2*(b*M+j)+1] % q) for j in range(M)) for b in range(B))
        _, psi, _, _ = dense_preparation(phases, q)
        observed.append(abs(np.vdot(np.ones(len(psi))/math.sqrt(len(psi)), psi))**2)
    assert abs(sum(observed)/len(observed)-predicted) < 1e-12


@pytest.mark.parametrize("g", ("-1", "-1/2", "0", "9/10", "1"))
@pytest.mark.parametrize("B", (1, 4))
def test_characteristic_law_including_negative_and_zero_noise(g, B):
    c = iid_characteristic_statistics(B, 3, g, independence=IID)
    gamma, f = fmpq(g), fmpq(c["mean_seed_fidelity"])
    a, C = (1+2*gamma)/3, (3+4*gamma+2*gamma*gamma)/9
    assert f == a**6+(C**3-a**6)/B
    assert fmpq(c["mean_reflection_operator_error_squared"]) == 4*(1-f)
    assert 0 <= f <= 1


@pytest.mark.parametrize("function,args", ((iid_characteristic_statistics, (2, 3, "9/10")), (reflection_budget, (9, 2, 3, "1", 4))))
def test_IID_is_an_explicit_promise_not_inferred_from_distinct_source_ids(function, args):
    with pytest.raises(ValueError, match="IID"): function(*args, independence="DISTINCT_IDS_ONLY")


@pytest.mark.parametrize("M", (1, 4, 256))
def test_composite_reflection_budget_has_no_cohort_bank_size_multiplier(M):
    budgets = [reflection_budget(3**64, B, M, "1", 100, 4, independence=IID) for B in (2, 4, 2**30)]
    assert len({b["mean_pure_trace_distance_squared_upper"] for b in budgets}) == 1
    assert len({b["averaged_complete_receiver_noise_loss_upper"] for b in budgets}) == 1
    assert len({b["original_classical_records_paid_once"] for b in budgets}) == 3
    tensor = reflection_budget(3**64, 1, M, "1", 100, independence=IID)
    assert fmpq(tensor["mean_pure_trace_distance_squared_upper"]) < fmpq(budgets[0]["mean_pure_trace_distance_squared_upper"])


def test_budget_charges_all_frozen_queries_initial_copies_hardware_and_rounding():
    b = reflection_budget(3**16, 8, 16, "1", 7, 4, independence=IID,
                          preparation_operator_error="1/1000", zero_phase_operator_error="1/2000", source_rounding_loss="1/100",
                          receiver_other_operations_loss="1/500")
    expected = fmpq(2, 1000)+7*fmpq(5, 2000)+fmpq(1, 500)
    assert 0 <= fmpq(b["complete_hardware_loss_upper"])-expected <= fmpq(1, 2**64)
    assert fmpq(b["complete_success_loss_upper"]) == min(fmpq(1), fmpq(b["averaged_complete_receiver_noise_loss_upper"])+fmpq(b["complete_hardware_loss_upper"])+fmpq(1, 100))
    assert not b["averaged_copy_density_bound_used_as_operator_bound"]
    assert not b["arbitrary_diagonal_queries_or_phase_powers_covered"]
    assert b["arbitrary_work_register_allowed_in_hybrid"]


def test_zero_noise_and_no_queries_zero_loss_vacuous_large_noise_is_not_success():
    b = reflection_budget(9, 4, 2, "0", 100, 3, independence=IID)
    assert b["complete_success_loss_upper"] == "0"
    b = reflection_budget(9, 4, 2, "1000000", 0, 0, independence=IID)
    assert b["complete_success_loss_upper"] == "0"
    b = reflection_budget(9, 4, 2, "1000000", 1, independence=IID)
    assert b["complete_success_loss_upper"] == "1" and not b["bound_is_nonvacuous"]


@pytest.mark.parametrize("kwargs", ({"moment":"-1"}, {"reflections":-1}, {"initial_copies":True}, {"bits":0}, {"preparation_operator_error":"2"}, {"source_rounding_loss":"-1"}, {"receiver_other_operations_loss":"2"}))
def test_invalid_error_or_query_promises_are_rejected(kwargs):
    args = dict(q=9, cohorts=2, sites=3, moment="1", reflections=4, independence=IID)
    args.update(kwargs)
    with pytest.raises(ValueError): reflection_budget(**args)


def test_frozen_bank_reuse_falsifies_averaged_copy_budget_with_certified_gap():
    c = frozen_bank_counterexample()
    lo, _ = map(fmpq, c["actual_minus_probability_box"])
    _, hi = map(fmpq, c["copy_trace_distance_box"])
    assert lo > c["reflections_of_noisy_bank"]*hi
    assert c["analytic_minus_probability"] > .99
    assert c["invalid_T_times_copy_budget"] < .04
    assert c["falsifier_is_certified_by_rational_boxes"] and not c["candidate_algorithm"]


def test_correlated_source_falsifies_IID_moment_bound_without_universal_no_go():
    c = correlated_bank_counterexample()
    assert fmpq(c["certified_mean_trace_distance_squared_box"][0]) > fmpq(c["misapplied_IID_budget"]["mean_pure_trace_distance_squared_upper"])
    assert c["actual_mean_trace_distance_squared"] > c["misapplied_IID_moment_upper"]
    assert c["falsifier_is_certified_by_rational_boxes"]
    assert not c["source_independence_promise_satisfied"] and not c["universal_noise_no_go"]


@pytest.mark.parametrize("B,M", ((1, 3), (2, 1), (2, 2), (4, 2)))
def test_center_witnesses_act_on_actual_tensor_seed_not_field_shadow(B, M):
    c = preparation_control(B, M, 81000+B*100+M)
    r, support = c["recipe"], c["central_support"]
    G = NativeGroup(4, 3)
    _, psi, _, _ = dense_preparation(r["known_phase_numerators"], 9)
    for key in ("nonzero_extra_vector_stabilizer_witness", "nonzero_extra_ray_stabilizer_witness"):
        u = support[key]
        if u is None: continue
        z = tuple(multiply(support["central_generator"], (x, 0), 4) for x in u)
        assert any(x != (0, 0) for x in z)
        transformed = []
        for b, cohort in enumerate(r["public_native_labels"]):
            A = np.ones((1, 1), complex)
            for label in cohort: A = np.kron(A, G.induced_action(label, (z, 0)))
            transformed.extend(A@psi[b*3**M:(b+1)*3**M])
        transformed = np.array(transformed)
        if "vector" in key: assert np.max(abs(transformed-psi)) < 1e-12
        else: assert abs(abs(np.vdot(psi, transformed))**2-1) < 1e-12
    if B == 1:
        assert support["ray_stabilizer_central_rank"] == 0
        assert support["vector_kernel_order"]["exponent"] >= 2
    assert not support["full_hidden_subgroup_or_gap_established"]


@pytest.mark.parametrize("n,L,M", ((1, 2, 1), (8, 16, 64), (128, 256, 16384), (1024, 2048, 1)))
def test_finite_bank_gap_is_costed_conditional_not_observed_or_a_decoder(n, L, M):
    c = finite_bank_gap_budget(n, L, M)
    B, threshold = int(c["Hadamard_cohort_count"]), fmpq(c["conservative_cohort_threshold"])
    assert B >= threshold > B//2 and B & (B-1) == 0
    assert int(c["original_classical_records_required"]) == 2*B*M
    assert c["group_order_compact"] == {"base":3, "exponent":n*L+1}
    assert c["ideal_absolute_overlap_gap_lower"] == "1/2"
    assert not c["observed_bank_has_been_certified"]
    assert not c["efficient_subgroup_decoder_supplied"]
    assert not c["gap_guarantee_includes_noise"]
    assert c["native_backend_within_current_level_cap"] == (L <= 512)
    assert not c["resource_profile_is_an_executed_bank"]


def test_cohort_overlap_mean_really_is_original_StateHSP_mean_not_a_pure_gap_assumption():
    G, secret = NativeGroup(2), ((2, 1),)
    labels = ring_words(2)
    H = set(G.hidden_elements(secret))
    for b, t in product(labels, range(3)):
        g = ((b,), t)
        overlaps = [np.vdot(G.supplied_phase_state((a,), secret), G.induced_action((a,), g)@G.supplied_phase_state((a,), secret)) for a in labels]
        for M in (1, 2, 3): assert abs((sum(overlaps)/len(overlaps))**M-int(g in H)) < 1e-12


@pytest.mark.parametrize("L", (2, 4, 16, 128, 3, 5, 17, 127))
def test_integer_secret_promise_changes_whether_public_slice_removes_central_false_positives(L):
    # The source factory has even level: do not apply an unfiltered full-ring
    # centre-mass ceiling to its publicly promised integer-secret slice.
    G = NativeGroup(L)
    q = 3**((L+1)//2)
    secret = ((17 % q, 0),)
    H = set(G.hidden_elements(secret))
    h = G.hidden_elements(secret)[1]
    support = central_support([[[(0, 0)]]], L)
    z = support["central_generator"]
    assert h[0][0][1] == 0
    for u in (1, 2):
        shifted = G.compose(h, ((multiply(z, (u, 0), L),), 0))
        assert shifted not in H and shifted[1] == 1
        passes_public_integer_slice = shifted[0][0][1] == 0
        assert passes_public_integer_slice == (L % 2 == 1)


@pytest.fixture(scope="module")
def live_report(): return json.loads(REPORT.read_text())


def test_live_report_independently_replays_exact_quantum_composites_and_all_ledgers(live_report):
    checker = ROOT/"research/certificates/known_preparation_coherent_reflection_crosscheck.js"
    completed = subprocess.run(["node", str(checker)], text=True, capture_output=True, timeout=120)
    assert completed.returncode == 0, completed.stderr
    out = json.loads(completed.stdout)
    assert out["status"] == "PASS" and out["exact_preparation_dimensions"] == [27, 6, 18, 36]
    assert out["falsifiers"] == 2 and not out["accepted_speedup_candidate"]
    assert live_report["producer_sha256"] == build_report()["producer_sha256"]


@pytest.mark.parametrize("forgery", ("promotion", "secret_phase", "cohort_gauge", "unpaid_queries", "unpaid_bank", "bad_gap"))
def test_independent_checker_rejects_forged_scope_and_resource_certificates(live_report, tmp_path, forgery):
    report = deepcopy(live_report)
    export = "run"
    if forgery == "promotion": report["accepted_speedup_candidate"] = True
    if forgery == "secret_phase": report["preparation_controls"][0]["recipe"]["known_phase_numerators"][0][0][1] = 0
    if forgery == "cohort_gauge": report["preparation_controls"][0]["seed_basis_phase_numerators"][0] = 1
    if forgery == "unpaid_queries":
        report = report["scalable_reflection_budgets"][0]["budget"]
        report["reflection_query_cap"] = "0"; export = "budget"
    if forgery == "unpaid_bank":
        report = report["conditional_bank_gap_budgets"][0]
        report["original_classical_records_required"] = "1"; export = "gap"
    if forgery == "bad_gap":
        report = report["conditional_bank_gap_budgets"][0]
        report["ideal_absolute_overlap_gap_lower"] = "1"; export = "gap"
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(report))
    script = "const fs=require('fs'); const C=require(process.argv[1]); C[process.argv[3]](JSON.parse(fs.readFileSync(process.argv[2],'utf8')));"
    completed = subprocess.run(["node", "-e", script, str(ROOT/"research/certificates/known_preparation_coherent_reflection_crosscheck.js"), str(file), export], text=True, capture_output=True, timeout=120)
    assert completed.returncode != 0
