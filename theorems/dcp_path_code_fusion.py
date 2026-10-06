"""Exact native DCP path-code instrument and measured-fusion comparator.

LOCAL DERIVATION / REVIEW PENDING. This is a specified measurement, not circuit
search, a novel sieve, a classical state simulator or a polynomial decoder.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import random

import numpy as np

from dcp_projective_code_admission import _source
from dhsp_codomain_instrument import _integer, rational

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_path_code_fusion.json"


def path_rows(pairs):
    _integer(pairs, "number of consumed native pairs", 2)
    return [[int(j in (2*i, 2*i+1, 2*i+2, 2*i+3)) for j in range(2*pairs)]
            for i in range(pairs-1)]


def compiler(pairs):
    _integer(pairs, "number of consumed native pairs", 2)
    cnots = [(2*j, 2*j+1) for j in range(pairs)]
    cnots += [(2*j+1, 2*j+3) for j in range(pairs-2, -1, -1)]
    cnots += [(2*j, 0) for j in range(1, pairs)]
    return {"pairs": pairs, "consumed_native_qubits": 2*pairs,
            "cnots_in_order": [list(g) for g in cnots],
            "hadamards_after_cnots": [2*j for j in range(1, pairs)]+[0],
            "measured_Z_syndrome_qubits": [2*j+1 for j in range(1, pairs)],
            "measured_Fourier_character_qubits": [2*j for j in range(1, pairs)],
            "retained_common_pair_parity_qubit": 1,
            "retained_logical_Fourier_qubit": 0,
            "CNOT_count": 3*pairs-2, "Hadamard_count": pairs,
            "measured_qubits": 2*pairs-2, "retained_qubits": 2,
            "gate_choice_depends_on_secret_or_labels": False,
            "conditional_source_inverse_or_cloning": False}


def _prefix(mask, pairs):
    out = [0]
    for j in range(pairs-1):
        out.append(out[-1] ^ (mask >> j & 1))
    return out


def _apply_h(state, bit):
    blocks = state.reshape(-1, 2, 1 << bit)
    return np.stack((blocks[:, 0]+blocks[:, 1], blocks[:, 0]-blocks[:, 1]), axis=1).reshape(-1)/math.sqrt(2)


def compile_state(state, pairs):
    """Apply only the specified, public CNOT/H network to an arbitrary input."""
    plan = compiler(pairs)
    if pairs > 6 or np.shape(state) != (1 << (2*pairs),):
        raise ValueError("full state-vector verification is capped at six pairs")
    state = np.asarray(state, complex).copy()
    indices = np.arange(len(state))
    for control, target in plan["cnots_in_order"]:
        permutation = indices ^ (((indices >> control) & 1) << target)
        state = state[permutation]
    for bit in plan["hadamards_after_cnots"]:
        state = _apply_h(state, bit)
    return state


def extract_branches(transformed, pairs):
    h = pairs-1
    if pairs > 6 or np.shape(transformed) != (1 << (2*pairs),):
        raise ValueError("matching bounded transformed state required")
    out = np.zeros((1 << (2*h), 2, 2), complex)
    for z in range(1 << h):
        for x in range(1 << h):
            q = _prefix(x, pairs)
            syndrome_index = sum(((z >> j & 1) << (2*j+3))+(q[j+1] << (2*j+2)) for j in range(h))
            for p in (0, 1):
                for t in (0, 1):
                    out[z | x << h, p, t] = transformed[syndrome_index | p << 1 | t]
    return out


def native_input(N, secret, labels):
    _source(N, secret, labels)
    if len(labels) % 2 or not 4 <= len(labels) <= 12:
        raise ValueError("two to six native pairs required for full vector verification")
    D = 1 << len(labels)
    return np.array([np.exp(2j*math.pi*(secret*sum(k for j, k in enumerate(labels) if b >> j & 1) % N)/N)
                     for b in range(D)])/math.sqrt(D)


def logical_formula(N, secret, labels):
    _source(N, secret, labels)
    if len(labels) % 2 or not 4 <= len(labels) <= 12:
        raise ValueError("all-syndrome formula enumeration is capped at six pairs")
    m = len(labels)//2
    theta = [2*math.pi*(k*secret % N)/N for k in labels]
    phase = np.exp(1j*sum(theta)/2)/math.sqrt(1 << m)
    amplitudes = np.zeros((1 << (2*m-2), 2, 2), complex)
    for z in range(1 << (m-1)):
        d = _prefix(z, m)
        for x in range(1 << (m-1)):
            q = _prefix(x, m)
            for p in (0, 1):
                angles = [(theta[2*j]+(-1)**(p ^ d[j])*theta[2*j+1])/2 for j in range(m)]
                for t in (0, 1):
                    value = phase
                    for j, angle in enumerate(angles):
                        value *= -1j*math.sin(angle) if t ^ q[j] else math.cos(angle)
                    amplitudes[z | x << (m-1), p, t] = value
    return amplitudes


def measured_fusion_instrument(N, secret, labels):
    """Measured Kuperberg pair parities, then the same X parity checks.

    Axis p labels CLASSICAL alternatives; concatenating them is not a coherent
    state. Pair branches are unnormalized. The known sum/difference label is used only
    to describe the supplied state, never to implement a secret-dependent gate.
    """
    _source(N, secret, labels)
    m = len(labels)//2
    if len(labels) % 2 or not 2 <= m <= 6:
        raise ValueError("two to six pairs required")
    out = np.zeros((1 << (2*m-2), 2, 2), complex)
    for parity in range(1 << m):
        ps = [(parity >> j) & 1 for j in range(m)]
        z = sum((ps[j] ^ ps[j+1]) << j for j in range(m-1))
        fused_labels = [labels[2*j]+(-1)**ps[j]*labels[2*j+1] for j in range(m)]
        phase = np.exp(2j*math.pi*(secret*sum(labels[2*j+1]*ps[j] for j in range(m)) % N)/N)
        # Each of m measured pair parities has probability 1/2.
        state = np.array([phase*np.exp(2j*math.pi*(secret*sum(k for j, k in enumerate(fused_labels) if r >> j & 1) % N)/N)
                          for r in range(1 << m)])/(1 << m)
        indices = np.arange(len(state))
        for j in range(1, m):
            state = state[indices ^ (((indices >> j) & 1))]
        for j in range(m):
            state = _apply_h(state, j)
        for x in range(1 << (m-1)):
            q = _prefix(x, m)
            index = sum(q[j] << j for j in range(1, m))
            out[z | x << (m-1), ps[0]] = state[[index, index | 1]]
    return out


def _trace_distance(u, v):
    delta = np.outer(u, u.conj())-np.outer(v, v.conj())
    return float(sum(abs(np.linalg.eigvalsh(delta)))/2)


def sign_distances(N, secret, labels):
    first, other = logical_formula(N, secret, labels), logical_formula(N, (-secret) % N, labels)
    coherent = sum(_trace_distance(u.ravel(), v.ravel()) for u, v in zip(first, other))
    measured = sum(_trace_distance(u[p], v[p]) for u, v in zip(first, other) for p in (0, 1))
    theta = [2*math.pi*(k*secret % N)/N for k in labels]
    m = len(labels)//2
    exact_formula = math.prod((abs(math.sin(theta[2*j]+theta[2*j+1]))+
                               abs(math.sin(theta[2*j]-theta[2*j+1])))/2 for j in range(m)) if m % 2 else 0.0
    input_distance = math.sqrt(max(0, 1-math.prod(map(math.cos, theta))**2))
    assert abs(measured-exact_formula) < 2e-12
    assert measured <= coherent+2e-12 <= input_distance+4e-12
    return {"full_coherent_instrument_sign_trace_distance": coherent,
            "measured_pair_fusion_sign_trace_distance": measured,
            "measured_sign_distance_product_formula": exact_formula,
            "original_input_sign_trace_distance": input_distance,
            "sign_erased_for_every_source_when_pair_count_even": m % 2 == 0,
            "surviving_sign_signal_requires_common_parity_coherence": False,
            "classical_full_syndrome_total_variation": float(sum(abs(np.sum(abs(first)**2, axis=(1, 2))-
                                                                         np.sum(abs(other)**2, axis=(1, 2))))/2)}


def linear_label_countercontrol(N, labels):
    """Calibration falsifier of closure under standard known-label DCP states."""
    if len(labels)//2 % 2 != 1:
        raise ValueError("odd pair count required for the flat phase branch")
    ratios, probabilities = [], []
    for s in range(1, N, 2):
        pair = logical_formula(N, s, labels)[0, 0]
        a = np.array([pair[0]+pair[1], pair[0]-pair[1]])/math.sqrt(2)
        probability = float(sum(abs(a)**2))
        if probability > 1e-13:
            assert abs(abs(a[0])-abs(a[1])) < 1e-12
            ratios.append((s, a[1]/a[0]))
            probabilities.append(probability)
    errors = [max(abs(r-np.exp(2j*math.pi*(L*s % N)/N)) for s, r in ratios) for L in range(N)]
    return {"modulus": N, "native_labels": labels, "calibration_only_not_IID_source_evidence": True,
            "branch": "z=0,x=0,measured common parity p=0; logical a basis",
            "nonzero_odd_secret_branches_checked": len(ratios),
            "minimum_over_known_labels_of_worst_secret_ratio_error": float(min(errors)),
            "best_diagnostic_label": int(np.argmin(errors)),
            "minimum_checked_branch_probability": min(probabilities),
            "flat_phase_does_not_imply_standard_DCP_label_closure": bool(min(errors) > 1e-8),
            "arbitrary_nonlinear_decoders_excluded": False}


def scaling_ledger(pairs):
    plan = compiler(pairs)
    K = Fraction(1, 2)+(Fraction(3, 2)**pairs+Fraction(1, 2)**pairs)/4
    return {**plan, "fixed_code_full_classical_kernel": rational(K),
            "all_ones_in_path_code": pairs % 2 == 0,
            "IID_mean_fixed_coherent_syndrome_probability_nonzero_secret": rational(Fraction(1, 1 << (2*pairs-2))),
            "IID_mean_fixed_measured_parity_and_syndrome_probability_nonzero_secret": rational(Fraction(1, 1 << (2*pairs-1))),
            "inverse_mean_branch_yield_not_expected_inverse_instance_probability": str(1 << (2*pairs-1)),
            "full_public_label_measured_fusion_IID_sign_distance_odd_secret": "((2/N)*cot(pi/N))^m" if pairs % 2 else "0",
            "measured_fusion_IID_sign_distance_upper": "(2/pi)^m" if pairs % 2 else "0",
            "measured_fusion_IID_sign_distance_at_N32": ((2/32)/math.tan(math.pi/32))**pairs if pairs % 2 else 0.0,
            "coherent_common_parity_protocol_covered_by_measured_decay": False,
            "per_instance_success_lower_bound": None,
            "label_adaptive_selection_covered_by_IID_mean": False,
            "known_label_sieve_improvement_proved": False}


def run_controls():
    rows = []
    for m, seeds in ((2, range(43011, 43013)), (3, range(43011, 43019)),
                     (4, range(43011, 43013)), (5, range(43011, 43013))):
        for seed in seeds:
            rng = random.Random(seed)
            labels = [rng.randrange(32) for _ in range(2*m)]
            source = native_input(32, 1, labels)
            actual = extract_branches(compile_state(source, m), m)
            formula = logical_formula(32, 1, labels)
            measured = measured_fusion_instrument(32, 1, labels)
            assert np.max(abs(actual-formula)) < 2e-12
            assert np.max(abs(measured-formula)) < 2e-12
            assert abs(sum(abs(actual.ravel())**2)-1) < 2e-12
            z_probs = np.sum(abs(actual.reshape(1 << (m-1), 1 << (m-1), 2, 2))**2, axis=(0, 2, 3))
            assert np.max(abs(z_probs-1/(1 << (m-1)))) < 2e-12
            rows.append({"modulus": 32, "secret_calibration": 1, "native_labels": labels,
                         "unfiltered_label_seed": seed, "pairs": m, "compiler": compiler(m),
                         "all_unnormalized_branch_amplitudes": np.stack((actual.real, actual.imag), axis=-1).tolist(),
                         "maximum_compiler_formula_error": float(np.max(abs(actual-formula))),
                         "maximum_measured_fusion_formula_error": float(np.max(abs(measured-formula))),
                         "all_syndrome_probabilities": np.sum(abs(actual)**2, axis=(1, 2)).tolist(),
                         "all_Z_syndrome_marginals": z_probs.tolist(),
                         "full_output_norm": float(sum(abs(actual.ravel())**2)),
                         "all_branches_charged": True, **sign_distances(32, 1, labels)})
    return {"status": "PATH_CODE_EQUALS_DEFERRED_PAIR_FUSION_LOCAL_REVIEW_PENDING",
            "native_controls": rows,
            "measured_comparator_common_parity_is_classical": True,
            "measured_branch_vectors_must_not_be_coherently_concatenated": True,
            "linear_label_countercontrol": linear_label_countercontrol(32, [1, 2, 3, 5, 7, 11]),
            "scaling_ledgers": [scaling_ledger(m) for m in (2, 3, 5, 9, 17, 33, 65, 129)],
            "claim_gate": {"novel_primitive": False, "new_algorithm": False,
                           "candidate_accepted": False, "polynomial_DCP_decoder": False,
                           "all_coherent_protocol_advantages_excluded": False,
                           "full_classical_dequantization": False, "independent_theorem_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "native_controls": len(report["native_controls"]),
                      "new_algorithm": False, "all_syndromes_retained": True}))


if __name__ == "__main__":
    main()
