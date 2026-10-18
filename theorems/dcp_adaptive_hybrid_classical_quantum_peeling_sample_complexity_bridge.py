"""Native witness readout, legal separable competitors and charged erasures.

V1's classical-dominance/sample-complexity claim is RETRACTED: gamma^h
does not specify the Fourier bias of a legal measurement of h phase qubits.
This module executes the public star-CNOT GHZ-basis readout and compares
two explicit single-copy separable protocols. It neither solves DCP nor
bounds all classical/separable/adaptive receivers. Dense laws are finite
calibrations; the exported circuit and realized-label calculation are linear
in the number of selected wires (times the public label dimension).
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
import math

import numpy as np

THEOREM_ID = "dcp_adaptive_hybrid_classical_quantum_peeling_sample_complexity_bridge"
SCHEMA_VERSION = "dcp-adaptive-hybrid-classical-quantum-peeling-sample-complexity-bridge-v2"


def _model(a_matrix, v_vec, t_bits, gamma_0):
    if type(t_bits) is not int or not 1 <= t_bits <= 256:
        raise ValueError("canonical modulus exponent in [1,256] required")
    v = tuple(v_vec)
    A = tuple(tuple(row) for row in a_matrix)
    q = 1 << t_bits
    if (not A or not v or any(type(x) is not int or x not in (0, 1) for x in v)
            or not any(v) or any(len(row) != len(v) for row in A)
            or any(type(x) is not int or not 0 <= x < q for row in A for x in row)):
        raise ValueError("nonempty canonical public labels and nonzero binary witness required")
    gamma = Fraction(gamma_0)
    if not 0 <= gamma <= 1:
        raise ValueError("visibility in [0,1] required")
    return A, v, q, gamma


def native_gate_plan(a_matrix, v_vec, t_bits, gamma_0):
    """No secret, inverse source, synthesized target state or branch table supplied."""
    A, v, q, gamma = _model(a_matrix, v_vec, t_bits, gamma_0)
    support = tuple(i for i, bit in enumerate(v) if bit)
    h = len(support)
    return {"original_public_label_columns": len(v), "selected_original_wires": list(support),
            "source_phase_qubits_consumed_per_packet": h,
            "witness_finding_and_pool_acquisition_cost_not_included": True,
            "target_label": [sum(row[i] for i in support) % q for row in A],
            "local_wire_order": "selected wires in ascending original-index order; target local wire0",
            "gates": [["CX", 0, j] for j in range(1, h)]+[["H", 0]],
            "measure_Z_local_wires": list(range(h)),
            "syndrome_bits": h-1, "realized_label_arithmetic_multiply_adds_upper": len(A)*h,
            "all_syndromes_and_target_outcomes_retained": True,
            "full_exponential_syndrome_table_needed_by_circuit": False,
            "visibility_model": "independent original Z faults",
            "per_wire_visibility_exact": str(gamma), "actual_hardware_execution": False}


def realized_effective_label(a_matrix, v_vec, t_bits, syndrome):
    A, v, q, _ = _model(a_matrix, v_vec, t_bits, 1)
    support = tuple(i for i, bit in enumerate(v) if bit)
    h = len(support)
    if type(syndrome) is not int or not 0 <= syndrome < 1 << (h-1):
        raise ValueError("actual measured canonical syndrome required")
    return tuple((row[support[0]]+sum((1-2*(syndrome >> (j-1) & 1))*row[i]
                                     for j, i in enumerate(support[1:], 1))) % q for row in A)


def erasure_fisher_accounting(acceptance, conditional_visibility, *, target_cosine=Fraction(0)):
    """Exact local information for a COARSENED target-cosine coin experiment.

    This is NOT Fisher information for the discrete DCP secret or an optimal
    decoder bound. The acceptance flag is independent of that cosine.
    """
    p, g, mu = map(Fraction, (acceptance, conditional_visibility, target_cosine))
    if not 0 <= p <= 1 or not 0 <= g <= 1 or not -1 < mu < 1:
        raise ValueError("valid acceptance, visibility and interior target cosine required")
    flagged = p*g*g/(1-g*g*mu*mu)
    forgotten = p*p*g*g/(1-p*p*g*g*mu*mu)
    return {"acceptance_exact": str(p), "conditional_visibility_exact": str(g),
            "target_cosine_exact": str(mu),
            "flagged_local_Fisher_exact": str(flagged),
            "fair_coin_replacement_local_Fisher_exact": str(forgotten),
            "flagged_inverse_local_Fisher_exact": str(1/flagged) if flagged else None,
            "fair_coin_replacement_inverse_local_Fisher_exact": str(1/forgotten) if forgotten else None,
            "at_zero_cosine_flagged_acceptance_penalty": str(1/p) if p else None,
            "at_zero_cosine_fair_coin_acceptance_penalty": str(1/(p*p)) if p else None,
            "discrete_secret_recovery_complexity_or_global_lower_bound": False,
            "unmatched_syndromes_are_deliberately_coarsened_not_proved_useless": True}


def evaluate_matched_branch_accounting(a_matrix, v_vec, t_bits, gamma_0):
    """Enumerate finite support-only syndromes, not an efficient collision counter."""
    A, v, q, gamma = _model(a_matrix, v_vec, t_bits, gamma_0)
    plan = native_gate_plan(A, v, t_bits, gamma)
    h = len(plan["selected_original_wires"])
    if h > 18:
        raise ValueError("UNKNOWN: exponential label-count calibration cap; circuit needs no table")
    target = tuple(plan["target_label"])
    negative = tuple(-x % q for x in target)
    branches = 1 << (h-1)
    hits = sum(realized_effective_label(A, v, t_bits, d) in (target, negative) for d in range(branches))
    p = Fraction(hits, branches)
    return {"gate_plan": plan, "hamming_weight": h,
            "target_w_mod_2t": list(target), "native_syndromes_enumerated": branches,
            "matched_syndromes": hits, "p_match_up_to_sign_exact": str(p),
            "zero_target_is_secret_independent": not any(target),
            "conditional_visibility_exact": str(gamma**h),
            "flagged_vs_forgotten_accounting": erasure_fisher_accounting(p, gamma**h) if any(target) else None,
            "classical_phase_bearing_modular_samples_supplied": False,
            "classical_dominance_established": False,
            "v1_unconditional_sample_complexity_ratio_retracted": True,
            "exhaustive_count_is_calibration_not_circuit_cost": True}


def _packet_density(phases, gamma):
    h, size = len(phases), 1 << len(phases)
    amplitudes = np.array([np.exp(1j*sum((x >> j & 1)*angle for j, angle in enumerate(phases)))
                           for x in range(size)])/math.sqrt(size)
    attenuation = np.array([[float(gamma**((x ^ y).bit_count())) for y in range(size)] for x in range(size)])
    return np.outer(amplitudes, amplitudes.conj())*attenuation


def _pauli_parity(rho, y_mask):
    """Direct product-Pauli matrix on the original input, little-endian wires."""
    size = len(rho)
    operator = np.zeros_like(rho)
    for x in range(size):
        phase = (1j)**y_mask.bit_count()*(-1)**((x & y_mask).bit_count())
        operator[x ^ (size-1), x] = phase
    return float(np.trace(rho@operator).real)


def physical_packet_law(a_matrix, v_vec, t_bits, gamma_0, secret):
    """Execute finite native density/CNOT/Born laws. Secret is calibration-only.

    The exported quantum circuit and the two separable measurement settings
    depend only on the public witness, NEVER on this calibration secret.
    """
    A, v, q, gamma = _model(a_matrix, v_vec, t_bits, gamma_0)
    support = tuple(i for i, bit in enumerate(v) if bit)
    h, s = len(support), tuple(secret)
    if (h > 7 or len(s) != len(A)
            or any(type(x) is not int or not 0 <= x < q for x in s)):
        raise ValueError("UNKNOWN: finite density cap or canonical secret dimension mismatch")
    phases = tuple(2*math.pi*(sum(s[j]*A[j][i] for j in range(len(A))) % q)/q for i in support)
    rho = _packet_density(phases, gamma)
    size = 1 << h
    # Actual CX(0,j) basis permutation, not a guessed conditional phase formula.
    permutation = [((x & 1) | sum(((x >> j & 1) ^ (x & 1)) << j for j in range(1, h))) for x in range(size)]
    transformed = np.zeros_like(rho)
    transformed[np.ix_(permutation, permutation)] = rho
    target = tuple(sum(row[i] for i in support) % q for row in A)
    negative = tuple(-x % q for x in target)
    branch_records = []
    max_error = 0.0
    matched_mass = matched_mean = 0.0
    for d in range(size//2):
        block = transformed[2*d:2*d+2, 2*d:2*d+2]
        mass = float(np.trace(block).real)
        label = realized_effective_label(A, v, t_bits, d)
        phase = 2*math.pi*(sum(a*b for a, b in zip(label, s)) % q)/q
        mean = float(2*block[0, 1].real)
        expected = mass*float(gamma**h)*math.cos(phase)
        max_error = max(max_error, abs(mean-expected), abs(mass-1/(size//2)))
        is_match = label in (target, negative)
        if is_match:
            matched_mass, matched_mean = matched_mass+mass, matched_mean+mean
        branch_records.append({"syndrome": d, "effective_label": list(label), "probability": mass,
                               "joint_X_plus_probability": (mass+mean)/2,
                               "joint_X_minus_probability": (mass-mean)/2,
                               "target_match_up_to_sign": is_match})
    x_product = _pauli_parity(rho, 0)
    even_masks = tuple(y for y in range(size) if y.bit_count() % 2 == 0)
    random_even_pauli = sum((-1)**(y.bit_count()//2)*_pauli_parity(rho, y) for y in even_masks)/len(even_masks)
    all_plus_target = float(gamma**h)*math.cos(sum(phases))
    correct_product_x = float(gamma**h)*math.prod(math.cos(x) for x in phases)
    correct_even_pauli = all_plus_target/(1 << (h-1))
    return {"calibration_secret": list(s), "selected_phases_radians": list(phases),
            "native_density_dimension": size, "native_input_trace": float(np.trace(rho).real),
            "branches": branch_records, "total_Born_probability": sum(b["probability"] for b in branch_records),
            "max_native_branch_law_residual": max_error,
            "independent_X_parity_mean": x_product, "independent_X_product_cosine_formula": correct_product_x,
            "random_even_XY_signed_parity_mean": random_even_pauli,
            "random_even_XY_formula": correct_even_pauli,
            "hypothetical_modular_sample_target_cosine_mean": all_plus_target,
            "matched_flag_probability": matched_mass, "matched_flag_signed_joint_mean": matched_mean,
            "matched_flag_conditional_mean": matched_mean/matched_mass,
            "matched_branch_formula_residual": abs(matched_mean-matched_mass*all_plus_target),
            "separable_protocol_formula_residual": max(abs(x_product-correct_product_x), abs(random_even_pauli-correct_even_pauli)),
            "X_parity_is_target_cosine_counterexample": abs(x_product-all_plus_target) > 1e-12,
            "secret_used_to_choose_circuit_or_measurement": False,
            "native_source_has_independent_Z_faults": True,
            "full_laws_are_exponential_reference_not_decoder": True}


def generate_dcp_adaptive_hybrid_classical_quantum_peeling_sample_complexity_certificate():
    fixtures = (([[1, 1]], [1, 1], 3, Fraction(1), (2,)),
                ([[1, 1, 1]], [1, 1, 1], 3, Fraction(4, 5), (1,)),
                ([[3, 5, 7]], [1, 0, 0], 3, Fraction(4, 5), (3,)),
                ([[1, 1, 1]], [1, 1, 1], 1, Fraction(4, 5), (1,)))
    audits = [{"public_labels": A, "witness": v, "phase_bits": t,
               "accounting": evaluate_matched_branch_accounting(A, v, t, g),
               "native_law": physical_packet_law(A, v, t, g, s)} for A, v, t, g, s in fixtures]
    payload = {"theorem_id": THEOREM_ID, "schema_version": SCHEMA_VERSION,
               "v1_classical_dominance_and_16x_sample_penalty_retracted": True,
               "scope_constraints": {
                   "applies_to": "Specified native GHZ/CNOT readout and two explicit separable measurement protocols",
                   "does_not_claim": "Classical dominance, optimal separable bounds, a DCP decoder, or asymptotic advantage",
                   "classical_modular_phase_samples_are_not_supplied_by_the_input": True,
                   "Fisher_accounting_is_for_a_coarsened_cosine_coin_not_discrete_secret_recovery": True},
               "native_audits": audits,
               "all_checks_passed": (audits[0]["native_law"]["X_parity_is_target_cosine_counterexample"]
                                     and all(x["native_law"]["max_native_branch_law_residual"] < 1e-12
                                             and x["native_law"]["matched_branch_formula_residual"] < 1e-12
                                             and x["native_law"]["separable_protocol_formula_residual"] < 1e-12 for x in audits)),
               "honesty_guardrails": {"accepted_speedup_candidate": False,
                                      "new_active_negative_result_created": False, "novelty_claim": False}}
    payload["certificate_sha256_16"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]
    return payload
