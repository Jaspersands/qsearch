"""Projective-code measurements on native DCP: target and baseline admission.

LOCAL DERIVATION / REVIEW PENDING. No new source, accepted algorithm, complete
classical simulation, generic DCP no-go or independently reviewed theorem.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import random

import numpy as np
from flint import nmod_mat
from scipy.linalg import hadamard

from dhsp_codomain_instrument import _integer, rational

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_projective_code_admission.json"


def _source(N, secret, labels):
    _integer(N, "power-of-two source modulus", 8)
    if N & (N-1):
        raise ValueError("source modulus must be a power of two >=8")
    _integer(secret, "canonical source secret", 0)
    if secret >= N or not labels or any(type(k) is not int or not 0 <= k < N for k in labels):
        raise ValueError("canonical secret and public DCP labels required")


def native_pauli_signature(N, secret, labels):
    _source(N, secret, labels)
    signature = []
    for k in labels:
        phase = k*secret % N
        if 2*phase % N == 0:
            signature.append("X")
        elif 4*phase % N == 0:
            signature.append("ZX")
        else:
            signature.append("identity-only")
    return signature


def validate_code(rows):
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("nonempty rectangular binary code required")
    if any(type(x) is not int or x not in (0, 1) for row in rows for x in row):
        raise ValueError("canonical integer binary coefficients required")
    A = nmod_mat(rows, 2)
    h, width = len(rows), len(rows[0])
    if A.rank() != h:
        raise ValueError("full row rank required: cocycle cancellation alone does not preserve targets")
    gram = A*A.transpose()
    if any(int(gram[i, j]) for i in range(h) for j in range(h)):
        raise ValueError("MM^T=0 over F_2 required for a genuine linear representation")
    reduced, rank = A.rref()
    pivots = [next(j for j in range(width) if reduced[i, j]) for i in range(rank)]
    free = [j for j in range(width) if j not in pivots]
    tail = [[int(reduced[i, j]) for j in free] for i in range(h)]
    assert nmod_mat(tail, 2).rank() == h
    return h, width, A, {"systematic_column_order": pivots+free, "systematic_tail": tail,
                         "tail_rank": h, "tail_gram_equals_identity": True,
                         "basis_rows_doubly_even": all(sum(row) % 4 == 0 for row in rows)}


def _words(rows):
    masks = [sum(x << i for i, x in enumerate(row)) for row in rows]
    words = [0]
    for mask in masks:
        words += [w ^ mask for w in words]
    return words


def code_signal_certificate(rows):
    h, width, A, systematic = validate_code(rows)
    if h > 16:
        raise ValueError("expanded exact code moment is capped at dimension16; symbolic Bell bound is separate")
    shortened, kernel = [], Fraction(0)
    for v in _words(rows):
        outside = [j for j in range(width) if not (v >> j & 1)]
        restricted = nmod_mat([[int(A[i, j]) for j in outside] for i in range(h)], 2) if outside else None
        dimension = h-(restricted.rank() if restricted is not None else 0)
        contribution = Fraction(1 << dimension, 1 << v.bit_count())
        kernel += contribution
        shortened.append({"codeword_hex": hex(v), "weight": v.bit_count(),
                          "shortened_dimension": dimension, "exact_contribution": rational(contribution)})
    baseline = Fraction(3, 2)**h
    assert kernel <= baseline
    return {"logical_rows": h, "consumed_native_phase_qubits": width,
            "full_output_bits": 2*h, "code_rows": rows, **systematic,
            "shortened_code_terms": shortened,
            "source_averaged_full_collision_kernel": rational(kernel),
            "source_averaged_centered_chi_squared": rational(kernel-1),
            "matched_logical_row_bell_kernel": rational(baseline),
            "matched_bell_native_qubits": 2*h,
            "matched_output_bit_individual_X_kernel": rational(Fraction(3, 2)**(2*h)),
            "individual_X_native_qubits": 2*h,
            "individual_X_candidate_likelihood_cost": "O(h) scalar cosine factors; this is NOT an efficient secret search",
            "individual_X_baseline_is_full_classical_phase_state_simulator": False,
            "bell_source_signal_upper_satisfied": True,
            "hypothesis_source": "secret order>=4; independent uniform labels; code fixed before these labels",
            "label_adaptive_code_moment_covered": False,
            "unmeasured_logical_qubits": width-2*h,
            "retained_register_source_quantum_collision": rational((1 << (width-2*h))*kernel),
            "untouched_native_source_quantum_collision": str(1 << width),
            "retained_quantum_register_algorithms_covered_by_bell_ceiling": False,
            "full_transcript_or_classical_time_dominance_proved": False,
            "raw_sample_algorithms_excluded": False,
            "higher_moment_or_noise_advantage_excluded": False}


def code_distribution(rows, N, secret, labels):
    _source(N, secret, labels)
    h, width, _, _ = validate_code(rows)
    if width != len(labels) or h > 8:
        raise ValueError("matching labels and bounded logical dimension<=8 required")
    words = _words(rows)
    theta = np.array([2*math.pi*((k*secret) % N)/N for k in labels])
    cosine, sine = np.cos(theta), np.sin(theta)
    coefficients = np.zeros(1 << (2*h), complex)
    for a, u in enumerate(words):
        for b, v in enumerate(words):
            if u & ~v:
                continue
            value = (-1j)**u.bit_count()
            for i in range(width):
                if v >> i & 1:
                    value *= sine[i] if u >> i & 1 else cosine[i]
            coefficients[a | b << h] = value
    assert np.max(abs(coefficients.imag)) < 1e-12
    probabilities = hadamard(len(coefficients)) @ coefficients.real/len(coefficients)
    assert min(probabilities) > -1e-12
    return probabilities, coefficients.real


def _purified_instrument(rows, N, secret, labels):
    h, width, _, _ = validate_code(rows)
    if width > 8 or h > 4:
        raise ValueError("full purified measurement is bounded to8 source qubits and4 logical rows")
    _source(N, secret, labels)
    if len(labels) != width:
        raise ValueError("one native source label per physical qubit required")
    size, control_size = 1 << width, 1 << (2*h)
    words = _words(rows)
    state = np.array([np.exp(2j*math.pi*(secret*sum(k for i, k in enumerate(labels) if x >> i & 1) % N)/N)
                      for x in range(size)])/math.sqrt(size)
    joint = np.empty((control_size, size), complex)
    for a, u in enumerate(words):
        for b, v in enumerate(words):
            # Actual known Pauli action P=Z^u X^v; no secret-dependent gate.
            target = np.arange(size) ^ v
            signs = np.array([(-1)**((u & int(y)).bit_count()) for y in target])
            joint[a | b << h, target] = signs*state/math.sqrt(control_size)
    transformed = hadamard(control_size) @ joint/math.sqrt(control_size)
    return joint, transformed


def physical_control(name, rows, N, secret, labels):
    h, width, _, _ = validate_code(rows)
    expected, coefficients = code_distribution(rows, N, secret, labels)
    joint, transformed = _purified_instrument(rows, N, secret, labels)
    probabilities = np.sum(abs(transformed)**2, axis=1)
    assert np.max(abs(probabilities-expected)) < 1e-12
    return {"code_name": name, "modulus": N, "secret_calibration": secret,
            "native_labels": labels, "certificate": code_signal_certificate(rows),
            "native_pauli_signature": native_pauli_signature(N, secret, labels),
            "full_output_probabilities": probabilities.tolist(),
            "full_pauli_expectations": coefficients.tolist(),
            "maximum_probability_identity_error": float(np.max(abs(probabilities-expected))),
            "joint_state_norm": float(np.sum(abs(joint)**2)),
            "output_norm": float(sum(probabilities)),
            "source_qubits_consumed": width, "postselection_or_cloning_used": False,
            "native_full_oracle_queries_if_states_generated_by_standard_bridge": width,
            "known_two_qubit_clifford_gate_count_upper": 2*sum(map(sum, rows)),
            "known_control_register_hadamard_count": 4*h,
            "identical_state_copy_promise_used": False,
            "paper_same_state_stabilizer_output_claim": False,
            "current_labels_chosen_to_fit_code": False,
            "actual_joint_clifford_measurement_on_independent_native_registers": True}


def residual_countercontrol(rows, N, secret, labels):
    """Same classical law under s/-s, but do NOT erase quantum remainders."""
    _, first = _purified_instrument(rows, N, secret, labels)
    _, other = _purified_instrument(rows, N, (-secret) % N, labels)
    p, q = np.sum(abs(first)**2, axis=1), np.sum(abs(other)**2, axis=1)
    terms = []
    for u, v, a, b in zip(first, other, p, q):
        difference = np.outer(u, u.conj())-np.outer(v, v.conj())
        terms.append(float(sum(abs(np.linalg.eigvalsh(difference)))/2))
    trace_distance = sum(terms)
    input_overlap = math.prod(math.cos(2*math.pi*((k*secret) % N)/N) for k in labels)
    input_trace_distance = math.sqrt(max(0, 1-input_overlap*input_overlap))
    assert trace_distance <= input_trace_distance+1e-12
    joint_purity = float(sum(p*p))
    h, width, _, _ = validate_code(rows)
    return {"code_rows": rows, "modulus": N, "first_secret_calibration": secret,
            "second_secret_calibration": (-secret) % N, "native_labels": labels,
            "classical_full_output_total_variation": float(sum(abs(p-q))/2),
            "classical_and_retained_quantum_output_trace_distance": trace_distance,
            "original_native_input_trace_distance": input_trace_distance,
            "unnormalized_branch_trace_distance_terms": terms,
            "instrument_output_purity": joint_purity,
            "actual_remaining_encoded_qubits": width-2*h,
            "all_ones_in_code": ((1 << width)-1) in _words(rows),
            "all_classical_branches_retained": True, "conditional_normalization_used": False,
            "polynomial_time_full_shift_decoder_supplied": False}


def overlapping_zero_branch(N, secret, labels):
    """Paid branch amplitudes of the six-to-two overlapping CSS instrument."""
    _source(N, secret, labels)
    if len(labels) != 6:
        raise ValueError("six distinct consumed source registers required")
    rows = [[1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1]]
    _, instrument = _purified_instrument(rows, N, secret, labels)
    theta = [2*math.pi*(k*secret % N)/N for k in labels]
    global_phase = np.exp(1j*sum(theta)/2)
    literal, formula = [], []
    for p in (0, 1):
        angles = [(theta[2*j]+(-1)**p*theta[2*j+1])/2 for j in range(3)]
        cosine, sine = math.prod(map(math.cos, angles)), math.prod(map(math.sin, angles))
        for a in (0, 1):
            orbit = []
            for r1 in (0, 1):
                for r2 in (0, 1):
                    r3 = a ^ r1 ^ r2
                    bits = [r1, p ^ r1, r2, p ^ r2, r3, p ^ r3]
                    orbit.append(sum(x << i for i, x in enumerate(bits)))
            literal.append(sum(instrument[0, x] for x in orbit)/2)
            formula.append(global_phase*(cosine+(-1)**a*1j*sine)/4)
    error = float(max(abs(a-b) for a, b in zip(literal, formula)))
    assert error < 1e-12
    probability = float(sum(abs(x)**2 for x in literal))
    assert abs(probability-float(sum(abs(instrument[0])**2))) < 1e-12
    return {"modulus": N, "secret_calibration": secret, "native_labels": labels,
            "branch": "all four measured commuting generator bits zero",
            "unnormalized_logical_amplitudes": [[float(x.real), float(x.imag)] for x in literal],
            "zero_branch_probability": probability, "full_formula_error": error,
            "logical_basis_order": ["p0,a0", "p0,a1", "p1,a0", "p1,a1"],
            "known_clifford_decoding_exists": True,
            "native_source_qubits": 6, "retained_logical_qubits": 2,
            "nonlinear_angle_compiler_is_new_algorithm_claim": False,
            "all_other_measurement_branches_retained_in_parent_countercontrol": True,
            "conditional_success_without_branch_cost_claim": False}


def sq_gate(N, logical_rows, queries, tolerance):
    _source(N, 1, [0])
    _integer(logical_rows, "logical row count")
    _integer(queries, "bounded one-record expectation queries", 0)
    if not isinstance(tolerance, Fraction) or not 0 < tolerance <= 1:
        raise ValueError("exact tolerance in (0,1] required")
    orbits = (N-2)//2
    d = Fraction(3, 2)**logical_rows-1
    affected = d//(tolerance*tolerance)
    success = min(Fraction(1), Fraction(queries*affected+1, orbits))
    return {"modulus": str(N), "order_at_least_four_negation_orbits": str(orbits),
            "logical_rows": logical_rows, "bounded_expectation_queries": queries,
            "absolute_tolerance": rational(tolerance), "matched_bell_centered_norm_upper": rational(d),
            "uniform_orbit_identification_success_upper": rational(success),
            "raw_sample_or_multirecord_inference_covered": False,
            "source_label_adaptive_measurement_covered": False,
            "bound_may_be_vacuous_for_growing_logical_rows": True,
            "classical_computational_hardness_claim": False}


def block_rows(block, dimension):
    return [[int(i//block == row) for i in range(block*dimension)] for row in range(dimension)]


def run_controls():
    codes = [("bell-one", block_rows(2, 1)), ("bell-two", block_rows(2, 2)),
             ("bell-three", block_rows(2, 3)), ("quartic-one", block_rows(4, 1)),
             ("quartic-two", block_rows(4, 2)),
             ("extended-hamming-eight", [[(mask >> i) & 1 for i in range(8)] for mask in (15, 51, 85, 255)])]
    controls = []
    for name, rows in codes:
        # Code fixed before IID label draw. No cherry-picking the source.
        rng = random.Random(43011)
        labels = [rng.randrange(32) for _ in rows[0]]
        for secret in (1, 3):
            controls.append(physical_control(name, rows, 32, secret, labels))
    packet = []
    for secret in range(1, 32, 2):
        packet.append({"secret_calibration": secret,
                       "all_public_label_signature": native_pauli_signature(32, secret, list(range(32)))})
    ledgers = [{"modulus_bits": bits,
                "sq_gate": sq_gate(1 << bits, 4, bits**2, Fraction(1, bits)),
                "doubly_even_quartic_block_kernel": rational(Fraction(9, 8)**4),
                "native_scalar_commutator_label_fraction": rational(Fraction(4, 1 << bits)),
                "odd_secret_single_state_worst_gap_upper": rational(Fraction(20, (1 << bits)**2)),
                "worst_gap_not_a_typical_packet_claim": True} for bits in (8, 16, 32, 64, 128)]
    remainders = [residual_countercontrol(block_rows(2, 2), 32, 1, [1, 5, 7, 11]),
                  residual_countercontrol(block_rows(4, 1), 32, 1, [1, 5, 7, 11])]
    overlapping = [[1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1]]
    for seed in range(43011, 43019):
        rng = random.Random(seed)
        row = residual_countercontrol(overlapping, 32, 1, [rng.randrange(32) for _ in range(6)])
        row["unfiltered_label_seed"] = seed
        remainders.append(row)
    return {"status": "NATIVE_DCP_PROJECTIVE_CODE_TARGET_AND_SIGNAL_AUDIT_LOCAL_REVIEW_PENDING",
            "physical_controls": controls, "odd_secret_signature_controls": packet,
            "retained_quantum_register_countercontrols": remainders,
            "overlapping_native_logical_branch_controls": [overlapping_zero_branch(32, 1, r["native_labels"])
                                                           for r in remainders[2:]],
            "scaling_ledgers": ledgers,
            "same_stabilizer_does_not_imply_same_raw_measurement_distribution": True,
            "claim_gate": {"candidate_accepted": False, "novel_algorithm": False,
                           "full_classical_dequantization": False,
                           "all_label_adaptive_code_search_excluded": False,
                           "all_raw_sample_decoders_excluded": False,
                           "retained_quantum_register_decoders_excluded": False,
                           "generic_DCP_no_go": False, "independent_theorem_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "physical_measurements": len(report["physical_controls"]),
                      "accepted_candidate": False, "raw_statistics_discarded": False}))


if __name__ == "__main__":
    main()
