"""Noise guarantees, literal mixed-state instruments and scoped falsifiers."""
from itertools import product
import json
import subprocess

from flint import fmpq
import numpy as np
import pytest

from theorems.native_descent_noise_composition import (
    REPORT, RECEIVER_REPORT, adaptive_error_budget, compose_even_noisy_input,
    contrast_contract, dephased_fixture, fixed_transcript_noise_loss, measured_density_branch,
    fixed_symmetric_noise_loss, fixed_tree_mean_contrast, lineage_offset_counts, symmetric_error_kernel,
)
from native_uniform_descent_receiver import merge_branch, resource_contract
from nil3_state_hsp_descent_receiver import SuppliedPhaseSample
from native_state_hsp_bridge import NativeGroup
from cyclotomic_rescaling_gate import residue
from ternary_cyclic_extractor import apply_cycle_basis


@pytest.mark.parametrize("level", (2, 3, 4))
@pytest.mark.parametrize("size", (2, 3, 4))
@pytest.mark.parametrize("visibilities", (("1", "1", "1", "1"), ("9/10", "3/5", "1/2", "2/3"), ("0", "1/5", "1", "1")))
def test_literal_mixed_SUM_instrument_has_product_contrast_in_every_branch(level, size, visibilities):
    G, secret = NativeGroup(level), ((5, 2),)
    labels = [(i+1, 2*i) for i in range(size-1)]
    labels.append((-sum(map(residue, labels)), 0))
    samples = [SuppliedPhaseSample((a,), G.supplied_phase_state((a,), secret), level) for a in labels]
    matrices = [dephased_fixture(s.state, v) for s, v in zip(samples, visibilities)]
    joint = np.ones((1, 1), complex)
    for rho in matrices:
        joint = np.kron(joint, rho)
    U = np.column_stack([apply_cycle_basis(v, (1,)*size) for v in np.eye(3**size)])
    literal = U@joint@U.conj().T
    tensor = literal.reshape((3,)*(2*size))
    visibility = float(np.prod([float(fmpq(v)) for v in visibilities[:size]]))
    total = 0.
    for tail in product(range(3), repeat=size-1):
        rho, probability = measured_density_branch(matrices, tail)
        child, _ = merge_branch(samples, tail)
        expected = visibility*np.outer(child.state, child.state.conj())+(1-visibility)*np.eye(3)/3
        projected = tensor[(slice(None),)+tail+(slice(None),)+tail]
        p = float(np.trace(projected).real)
        assert np.max(abs(projected/p-rho)) < 1e-12
        assert np.max(abs(rho-expected)) < 1e-12
        assert abs(probability-p) < 1e-12
        assert abs(p-3**(1-size)) < 1e-12
        total += p
    assert abs(total-1) < 1e-12


@pytest.mark.parametrize("eta", ("0", "1/100", "1/5", "1"))
def test_dephasing_trace_distance_is_exact_and_character_readout_loses_contrast(eta):
    psi = NativeGroup(3).supplied_phase_state(((1, 2),), ((5, 1),))
    v = 1-fmpq(eta)
    rho = dephased_fixture(psi, v)
    trace = np.sum(abs(np.linalg.eigvalsh(rho-np.outer(psi, psi.conj()))))/2
    assert abs(trace-float(2*fmpq(eta)/3)) < 1e-12
    corrected = np.diag(np.conj(psi)*np.sqrt(3))@rho@np.diag(psi*np.sqrt(3))
    F = np.exp(-2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
    p = np.diag(F@corrected@F.conj().T).real
    assert np.max(abs(p-np.array([float((1+2*v)/3), float((1-v)/3), float((1-v)/3)]))) < 1e-12


@pytest.mark.parametrize("gamma", ("0", "1/2", "9/10", "1"))
@pytest.mark.parametrize("B", (1, 2, 3, 4))
def test_symmetric_error_kernel_transports_original_offsets_not_fresh_level_noise(gamma, B):
    g, kernel = fmpq(gamma), symmetric_error_kernel(gamma)
    accumulated = fmpq(0)
    probabilities = []
    for tail in product(range(3), repeat=B-1):
        offsets = (0,)+tail
        rho, p = measured_density_branch([kernel/3]*B, tail)
        counts = [offsets.count(t) for t in range(3)]
        expected = np.ones((3, 3))/3
        for t in range(3):
            for u in range(3):
                if t != u:
                    omitted = 3-t-u
                    expected[t, u] = float(g**(B+counts[(-omitted) % 3]))/3
        assert np.max(abs(rho-expected)) < 1e-12
        assert abs(p-3**(1-B)) < 1e-12
        contrasts = [g**(B+c) for c in counts]
        correct = fmpq(1, 3)+fmpq(2, 9)*sum(contrasts)
        F = np.exp(-2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
        assert abs((F@rho@F.conj().T)[0, 0].real-float(correct)) < 1e-12
        probabilities.append(correct)
        accumulated += sum(contrasts)/3
    average = accumulated/3**(B-1)
    assert str(average) == fixed_tree_mean_contrast(B, gamma)["uniform_offset_mean_visibility_exact"]
    if g == fmpq(1, 2) and B > 1:
        assert len(set(probabilities)) > 1  # Uniform branches can have different contrast.


@pytest.mark.parametrize("index", range(5))
def test_complete_lineage_offsets_cover_original_errors_and_exact_symmetric_loss(index):
    result = json.loads(RECEIVER_REPORT.read_text())["source_driven_receiver_controls"][index]["result"]
    packets = lineage_offset_counts(result)
    assert all(sum(counts) == len(ids) for _, ids, counts in packets)
    good = fixed_symmetric_noise_loss(result, "1")
    assert good["conditional_all_correct_readouts_exact"] == "1"
    bad = fixed_symmetric_noise_loss(result, "0")
    assert bad["conditional_all_correct_readouts_exact"] == str(fmpq(1, 3**len(packets)))
    assert not bad["Gaussian_density_identified_from_moment"]


@pytest.mark.parametrize("B", (1, 2, 30, 1000))
@pytest.mark.parametrize("eta", ("0", "1/1000", "1/10", "1"))
def test_exact_contrast_bounds_are_valid_not_a_gaussian_identification(B, eta):
    r = contrast_contract(B, eta)
    exact = (1-fmpq(eta))**B
    assert fmpq(r["retained_visibility_lower"]) <= exact <= fmpq(r["retained_visibility_upper"])
    assert r["retained_visibility_exact_compact"] == {"base": str(1-fmpq(eta)), "exponent": str(B)}
    assert not r["all_receivers_excluded"] and not r["Gaussian_noise_identified_with_dephasing"]


def test_large_exposure_is_compact_and_rejects_automatic_robustness():
    n = 128
    r = contrast_contract(n**(2*n), fmpq(1, n**6))
    assert fmpq(r["correct_character_advantage_above_chance_upper"]) < fmpq(1, 10**100)
    assert r["per_original_trace_distance_exact"] == str(fmpq(2, 3*n**6))


@pytest.mark.parametrize("n,L", ((1, 1), (4, 2), (8, 4), (8, 16)))
def test_adaptive_error_charges_original_cap_and_all_gate_types(n, L):
    c = resource_contract(n, L)
    C, K = int(c["original_copy_upper"]), n+8
    delta, gate, measurement = fmpq(1, 100*C), fmpq(1, 100*C*L), fmpq(1, 100*C*L)
    r = adaptive_error_budget(n, L, delta, gate, measurement)
    total = C*delta+((L-1)*C+(2*L-1)*K)*gate+((L-1)*C+L*K)*measurement
    assert fmpq(r["total_implementation_loss_upper"]) == min(fmpq(1), total)
    assert fmpq(r["full_correct_recovery_lower"]) == max(fmpq(0), 1-fmpq(c["ideal_IID_rank_failure_upper"])-total)
    assert not r["marginal_bounds_cover_correlated_sources"] and not r["universal_noise_lower_bound"]


def test_vacuous_guarantee_is_not_predicted_failure_and_zero_noise_can_pass():
    bad = compose_even_noisy_input(8, 8, fmpq(1, 8**6))
    assert bad["receiver_budget"]["full_correct_recovery_lower"] == "0"
    assert not bad["receiver_budget"]["actual_success_predicted_by_vacuous_upper"]
    good = compose_even_noisy_input(4, 1, 0)
    assert fmpq(good["receiver_budget"]["full_correct_recovery_lower"]) > fmpq(99, 100)
    assert int(good["classical_original_records_upper"]) == 2*int(good["receiver_budget"]["original_copy_cap"])
    assert not good["source_rounding_loss_included"]


@pytest.mark.parametrize("index", range(5))
def test_fixed_transcript_failure_is_exact_conditioned_and_monotone(index):
    result = json.loads(RECEIVER_REPORT.read_text())["source_driven_receiver_controls"][index]["result"]
    zero = fixed_transcript_noise_loss(result, 0)
    assert zero["conditional_all_correct_readouts_exact"] == "1"
    previous = fmpq(1)
    for eta in ("1/1000", "1/100", "1/10", "1"):
        r = fixed_transcript_noise_loss(result, eta)
        expected = fmpq(1)
        for stage in result["completed_digit_stages"]:
            for ids in stage["digit_measurement_original_lineages"]:
                expected *= (1+2*(1-fmpq(eta))**len(ids))/3
        assert fmpq(r["conditional_all_correct_readouts_exact"]) == expected <= previous
        assert not r["noisy_receiver_executed"] and not r["error_correcting_decoder_supplied"]
        previous = expected
    assert expected == fmpq(1, 3**sum(len(s["measured_outcomes"]) for s in result["completed_digit_stages"]))


@pytest.mark.parametrize("call", (
    lambda: contrast_contract(0, 0),
    lambda: contrast_contract(1, "-1/10"),
    lambda: adaptive_error_budget(1, 2, "3/2"),
    lambda: compose_even_noisy_input(1, 2, "-1"),
    lambda: measured_density_branch([np.eye(3)], ()),
    lambda: measured_density_branch([np.diag([-1, 1, 1])], ()),
    lambda: measured_density_branch([np.eye(3)/3, np.eye(3)/3], (True,)),
    lambda: dephased_fixture(np.array([1, 0, 0]), 1),
))
def test_invalid_noise_and_state_promises_rejected(call):
    with pytest.raises(ValueError):
        call()


def test_independent_exact_noise_composition_replay():
    checker = REPORT.parents[1]/"certificates/native_descent_noise_crosscheck.js"
    out = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    r = json.loads(out.stdout)
    assert r["status"] == "PASS" and r["transcript_noise_controls"] == 20
    assert r["symmetric_error_controls"] == 15
    assert not r["universal_impossibility_established"]


@pytest.mark.parametrize("mutation", ("delta", "cap", "gate", "ancestry", "visibility", "probability", "exposure", "claim", "offset", "symmetric_probability"))
def test_checker_rejects_uncharged_errors_and_false_robustness(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    b = r["even_input_compositions"][2]["receiver_budget"]
    f = r["source_transcript_controls"][1]["conditional_noise_losses"][1]
    if mutation == "delta":
        b["per_original_trace_promise"] = "0"
    elif mutation == "cap":
        b["original_copy_cap"] = "1"
    elif mutation == "gate":
        b["known_SUM_gate_upper"] = "0"
    elif mutation == "ancestry":
        f["packet_ancestry_factors"][0]["original_ancestors"] += 1
    elif mutation == "visibility":
        f["packet_ancestry_factors"][0]["visibility_exact"] = "1"
    elif mutation == "probability":
        f["conditional_all_correct_readouts_exact"] = "1"
    elif mutation == "exposure":
        r["dephasing_exposure_contracts"][3]["retained_visibility_upper"] = "1"
    elif mutation == "offset":
        r["symmetric_error_transcript_controls"][0]["conditional_noise_losses"][0]["packet_factors"][0]["original_offset_counts_mod3"][0] += 1
    elif mutation == "symmetric_probability":
        r["symmetric_error_transcript_controls"][0]["conditional_noise_losses"][0]["conditional_all_correct_readouts_exact"] = "1"
    else:
        r["noise_proves_universal_impossibility"] = True
    target = tmp_path/"forged.json"
    target.write_text(json.dumps(r))
    out = subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_descent_noise_crosscheck.js"), str(target)], capture_output=True)
    assert out.returncode != 0
