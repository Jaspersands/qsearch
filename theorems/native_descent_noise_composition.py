"""Adaptive error accounting and exact phase-contrast loss for native descent.

The dephasing family is an explicit falsifier of automatic noise robustness,
not a Gaussian-source identification or a universal receiver impossibility.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from flint import fmpq
import numpy as np

from native_uniform_descent_receiver import REPORT as RECEIVER_REPORT, resource_contract
from native_noisy_phase_input import quantum_input_bound
from ternary_certified_noise_sampler import rational
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_DESCENT_NOISE_COMPOSITION.md"
REPORT = ROOT/"research/reductions/native_descent_noise_composition.json"


def unit_interval(value, name):
    value = rational(value, name)
    if not 0 <= value <= 1:
        raise ValueError(name+" must lie in[0,1]")
    return value


def adaptive_error_budget(dimension, level, per_original_trace, per_gate=0, per_measurement=0, overhead=8):
    contract = resource_contract(dimension, level, overhead)
    C, K = int(contract["original_copy_upper"]), contract["fresh_digit_samples_per_level"]
    delta = unit_interval(per_original_trace, "per original trace-distance promise")
    gate = unit_interval(per_gate, "per implemented unitary operator error")
    measurement = unit_interval(per_measurement, "per instrument half-diamond error")
    SUM = (level-1)*C
    digit_gates = (2*level-1)*K  # K Fourier gates at every level; K corrections above level1.
    measured = SUM+level*K
    source_loss = min(fmpq(1), C*delta)
    gate_loss = min(fmpq(1), (SUM+digit_gates)*gate)
    measurement_loss = min(fmpq(1), measured*measurement)
    total = min(fmpq(1), source_loss+gate_loss+measurement_loss)
    rank = rational(contract["ideal_IID_rank_failure_upper"], "ideal rank loss")
    return {"resource_contract": contract, "original_copy_cap": str(C),
            "per_original_trace_promise": str(delta), "known_SUM_gate_upper": str(SUM),
            "known_digit_gate_upper": str(digit_gates), "measurement_upper": str(measured),
            "per_unitary_operator_error_promise": str(gate), "per_measurement_half_diamond_promise": str(measurement),
            "original_source_loss_upper": str(source_loss), "gate_loss_upper": str(gate_loss),
            "measurement_loss_upper": str(measurement_loss), "total_implementation_loss_upper": str(total),
            "ideal_rank_failure_upper": str(rank), "full_correct_recovery_lower": str(max(fmpq(0), 1-rank-total)),
            "promises_established_from_sample_values": False, "marginal_bounds_cover_correlated_sources": False,
            "actual_success_predicted_by_vacuous_upper": False, "universal_noise_lower_bound": False}


def compose_even_noisy_input(dimension, root_exponent, normalized_second_moment):
    integer(root_exponent, "positive root exponent", 1)
    second = rational(normalized_second_moment, "V/q^2 source moment promise")
    if second < 0:
        raise ValueError("nonnegative source moment promise required")
    level, q = 2*root_exponent, 3**root_exponent
    C = int(resource_contract(dimension, level)["original_copy_upper"])
    native = quantum_input_bound(q, C, second*q*q)
    # This existing native-input theorem is an averaged density bound under
    # independent symmetric errors, not a bound for individual pure noises.
    per_copy = min(fmpq(1), 20*second+rational(native["gate_budget"]["per_state_preparation_trace_error_upper"], "preparation error"))
    composed = adaptive_error_budget(dimension, level, per_copy)
    return {"dimension": dimension, "root_exponent": root_exponent, "native_even_level": level,
            "normalized_integer_error_second_moment": str(second), "classical_original_records_upper": str(2*C),
            "native_input_bound": native, "receiver_budget": composed,
            "scope": "independent classical-pair preparation with an unknown integer-embedded secret",
            "source_rounding_loss_included": False, "growing_depth_noise_robustness_established": False,
            "classical_original_data_hardness_established": False}


def measured_density_branch(densities, outcomes):
    densities, outcomes = tuple(densities), tuple(outcomes)
    if not densities or len(outcomes) != len(densities)-1 or any(type(v) is not int or v not in (0, 1, 2) for v in outcomes):
        raise ValueError("nonempty density block and every measured complement required")
    matrices = []
    for rho in densities:
        rho = np.asarray(rho, complex)
        if (rho.shape != (3, 3) or not np.all(np.isfinite(rho)) or
                np.max(abs(rho-rho.conj().T)) > 1e-12 or abs(np.trace(rho)-1) > 1e-12 or
                min(np.linalg.eigvalsh(rho)) < -1e-12):
            raise ValueError("normalized positive supplied qutrit density required")
        matrices.append(rho)
    result = np.ones((3, 3), complex)
    for rho, v in zip(matrices, (0,)+outcomes):
        order = [(t+v) % 3 for t in range(3)]
        result *= rho[np.ix_(order, order)]
        scale = float(np.max(abs(result)))
        if scale == 0:
            raise ValueError("zero-probability density branch")
        result /= scale
    norm = float(np.trace(result).real)
    if norm <= 0:
        raise ValueError("zero-probability density branch")
    # Probability is diagnostic; retained density is rescaled against underflow.
    probability = sum(float(np.prod([rho[(t+v) % 3, (t+v) % 3].real for rho, v in zip(matrices, (0,)+outcomes)])) for t in range(3))
    return result/norm, probability


def dephased_fixture(state, visibility):
    visibility = unit_interval(visibility, "phase visibility")
    state = np.asarray(state, complex)
    if state.shape != (3,) or abs(np.vdot(state, state)-1) > 1e-12:
        raise ValueError("normalized phase fixture required")
    if np.max(abs(abs(state)**2-1/3)) > 1e-12:
        raise ValueError("uniform computational moduli required for this phase-dephasing family")
    v = float(visibility)
    return v*np.outer(state, state.conj())+(1-v)*np.eye(3)/3


def contrast_contract(original_ancestors, per_original_dephasing):
    integer(original_ancestors, "paid positive ancestry", 1)
    eta = unit_interval(per_original_dephasing, "per original dephasing")
    B = original_ancestors
    lower, upper = max(fmpq(0), 1-B*eta), (fmpq(0) if eta == 1 else 1/(1+B*eta))
    return {"original_ancestors": str(B), "per_original_dephasing": str(eta),
            "per_original_trace_distance_exact": str(2*eta/3),
            "retained_visibility_exact_compact": {"base": str(1-eta), "exponent": str(B)},
            "retained_visibility_lower": str(lower), "retained_visibility_upper": str(upper),
            "correct_character_probability_upper": str((1+2*upper)/3),
            "correct_character_advantage_above_chance_upper": str(2*upper/3),
            "bound_applies_to_this_measured_compression": True, "all_receivers_excluded": False,
            "Gaussian_noise_identified_with_dephasing": False}


def fixed_transcript_noise_loss(result, per_original_dephasing):
    eta = unit_interval(per_original_dephasing, "per original dephasing")
    if result["status"] != "IDEAL_NATIVE_REFERENCE_SECRET_DECODED":
        raise ValueError("complete full-rank ideal reference transcript required")
    counts = Counter(len(ids) for stage in result["completed_digit_stages"] for ids in stage["digit_measurement_original_lineages"])
    probability = fmpq(1)
    factors = []
    for B, count in sorted(counts.items()):
        v = (1-eta)**B
        p = (1+2*v)/3
        probability *= p**count
        factors.append({"original_ancestors": B, "measured_packets": count, "visibility_exact": str(v), "correct_character_probability_exact": str(p)})
    return {"per_original_dephasing": str(eta), "packet_ancestry_factors": factors,
            "conditional_all_correct_readouts_exact": str(probability),
            "conditional_readout_failure_exact": str(1-probability),
            "conditioning": "this complete public ideal-source selector/branch transcript with full rank",
            "noisy_receiver_executed": False, "error_correcting_decoder_supplied": False,
            "fresh_lower_prefix_guessed": False, "new_quantum_speedup_established": False}


def symmetric_error_kernel(characteristic):
    gamma = unit_interval(characteristic, "nonnegative symmetric-error characteristic")
    g = float(gamma)
    return np.array([[1, g, g], [g, 1, g*g], [g, g*g, 1]])


def lineage_offset_counts(result):
    if result["status"] != "IDEAL_NATIVE_REFERENCE_SECRET_DECODED":
        raise ValueError("complete ideal reference transcript required")
    level = result["resource_contract"]["level"]
    counts = {(level, (i,)): (1, 0, 0) for i in range(result["original_inputs_supplied"])}
    for stream in result["descent_streams"]:
        records = stream["complete_output_records"]
        if records is None:
            raise ValueError("complete physical merge trace required, not a preview")
        for branch in records:
            out, root_ids = [0, 0, 0], []
            inputs = branch["input_original_lineages"]
            if len(branch["measured_complement"]) != len(inputs)-1:
                raise ValueError("every measured offset required")
            for ids, v in zip(inputs, (0,)+tuple(branch["measured_complement"])):
                if type(v) is not int or v not in (0, 1, 2):
                    raise ValueError("canonical measured offsets required")
                parent = counts[(stream["parent_level"], tuple(ids))]
                for t, count in enumerate(parent):
                    out[(t+v) % 3] += count
                root_ids.extend(ids)
            if len(set(root_ids)) != len(root_ids) or tuple(sorted(root_ids)) != tuple(branch["original_source_indices"]):
                raise ValueError("paid disjoint lineage must match actual output ancestors")
            counts[(stream["child_level"], tuple(branch["original_source_indices"]))] = tuple(out)
    return [(stage["level"], tuple(ids), counts[(stage["level"], tuple(ids))])
            for stage in result["completed_digit_stages"] for ids in stage["digit_measurement_original_lineages"]]


def fixed_symmetric_noise_loss(result, characteristic):
    gamma = unit_interval(characteristic, "nonnegative symmetric-error characteristic")
    probability, factors = fmpq(1), []
    for level, ids, counts in lineage_offset_counts(result):
        B = len(ids)
        if sum(counts) != B:
            raise ArithmeticError("offset counts do not cover all original errors")
        # Pair (t,u) has omitted index m and exceptional factor gamma^2
        # precisely for original offset -m. The unordered sum needs no ordering.
        contrasts = tuple(gamma**(B+c) for c in counts)
        p = fmpq(1, 3)+fmpq(2, 9)*sum(contrasts)
        probability *= p
        factors.append({"level": level, "original_lineage": ids, "original_offset_counts_mod3": counts,
                        "unordered_offdiagonal_contrasts_exact": tuple(map(str, contrasts)),
                        "correct_character_probability_exact": str(p)})
    return {"symmetric_error_characteristic": str(gamma), "original_kernel": "[[1,gamma,gamma],[gamma,1,gamma^2],[gamma,gamma^2,1]]",
            "packet_factors": factors, "conditional_all_correct_readouts_exact": str(probability),
            "original_error_characteristic_is_a_source_promise": True,
            "conditioning": "full-rank fixed public source/selector/offset transcript",
            "noisy_receiver_executed": False, "Gaussian_density_identified_from_moment": False,
            "error_correcting_decoder_supplied": False, "new_quantum_speedup_established": False}


def fixed_tree_mean_contrast(original_ancestors, characteristic):
    integer(original_ancestors, "fixed tree positive ancestry", 1)
    gamma = unit_interval(characteristic, "nonnegative symmetric-error characteristic")
    return {"original_ancestors": original_ancestors, "characteristic": str(gamma),
            "uniform_offset_mean_visibility_exact": str((gamma*(2+gamma)/3)**original_ancestors),
            "scope": "fixed unfiltered disjoint common-index tree; not an adaptively selected tree posterior",
            "adaptive_tree_average_law_proved": False}


def build_report():
    receiver = json.loads(RECEIVER_REPORT.read_text())
    if receiver["status"] != "NATIVE_SOURCE_PRESERVING_DESCENT_AND_REFERENCE_RECOVERY_REVIEW_PENDING":
        raise ValueError("corrected source-driven receiver artifact required")
    transcript_controls = [{"dimension": c["dimension"], "level": c["level"],
                            "conditional_noise_losses": [fixed_transcript_noise_loss(c["result"], eta) for eta in ("0", "1/1000", "1/100", "1/10")]}
                           for c in receiver["source_driven_receiver_controls"]]
    return {"status": "SCOPED_NATIVE_DESCENT_NOISE_COMPOSITION_EXTERNAL_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "receiver_artifact_sha256": hashlib.sha256(RECEIVER_REPORT.read_bytes()).hexdigest(),
            "even_input_compositions": ([compose_even_noisy_input(4, 1, 0), compose_even_noisy_input(4, 1, fmpq(1, 4**10))]+
                                        [compose_even_noisy_input(n, r, fmpq(1, n**6)) for n, r in ((4, 1), (8, 2), (8, 8), (32, 32), (128, 128))]),
            "dephasing_exposure_contracts": [contrast_contract(B, fmpq(1, n**6)) for n in (8, 32, 128) for B in (n, n*n, n**4, n**(2*n))],
            "source_transcript_controls": transcript_controls,
            "symmetric_error_transcript_controls": [{"dimension": c["dimension"], "level": c["level"],
                                                       "conditional_noise_losses": [fixed_symmetric_noise_loss(c["result"], g) for g in ("9/10", "99/100", "999/1000")]}
                                                      for c in receiver["source_driven_receiver_controls"]],
            "fixed_tree_mean_controls": [fixed_tree_mean_contrast(B, "999/1000") for B in (1, 4, 16, 64)],
            "growing_depth_robust_receiver_supplied": False, "noise_proves_universal_impossibility": False,
            "dephasing_is_the_Gaussian_source": False, "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "source_compositions": len(report["even_input_compositions"]),
                      "dephasing_exposures": len(report["dephasing_exposure_contracts"]),
                      "transcript_controls": len(report["source_transcript_controls"]),
                      "positive_recovery_lower_bounds": sum(r["receiver_budget"]["full_correct_recovery_lower"] != "0" for r in report["even_input_compositions"]),
                      "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()
