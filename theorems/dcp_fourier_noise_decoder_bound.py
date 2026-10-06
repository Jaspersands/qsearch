"""Collision strong converse for measured Boolean-envelope Fourier sources.

LOCAL DERIVATION / REVIEW PENDING. This bounds a classical-observation secret
decoder, NOT arbitrary collective quantum operations or subset-sum algorithms.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from dcp_bell_inference_kernel import exact
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/dcp_fourier_noise_decoder_bound.json"


def collision_decoder_certificate(secret_count, modulus, collision_multipliers):
    for value, name in ((secret_count, "secret count"), (modulus, "modulus")):
        _positive_integer(value, name)
    if modulus < 2:
        raise ValueError("nontrivial observation alphabet required")
    multipliers = tuple(Fraction(k) for k in collision_multipliers)
    if not multipliers or any(not 1 <= k <= modulus for k in multipliers):
        raise ValueError("nonempty valid q*sum(P_i^2) bounds required")
    squared = min(Fraction(1), math.prod(multipliers) / secret_count)
    return {
        "status": "LOCAL_CLASSICAL_OBSERVATION_STRONG_CONVERSE_REVIEW_PENDING",
        "uniform_secret_count": secret_count,
        "observation_modulus": modulus,
        "independent_observations": len(multipliers),
        "mean_correct_secret_probability_squared_upper_bound": exact(squared),
        "holds_for_every_fixed_public_linear_matrix_independent_of_secret": True,
        "unbounded_computation_or_quantum_processing_of_classical_input_allowed": True,
        "random_secret_uniform_and_coordinate_noise_independent_required": True,
        "source_noise_distribution_may_depend_on_secret_or_labels": False,
        "heralds_or_abstentions_count_as_unsuccessful": True,
        "decoder_receiving_coherent_noise_purification_is_bounded": False,
        "all_collective_quantum_subset_sum_algorithms_ruled_out": False,
        "candidate_record_accepted": False,
        "speedup_claim_allowed": False,
    }


def boolean_envelope_native_certificate(dimension, modulus_bits, columns):
    for value, name in ((dimension, "dimension"), (modulus_bits, "modulus bits"), (columns, "columns")):
        _positive_integer(value, name)
    if modulus_bits < 2:
        raise ValueError("unit-gap two-point envelope requires q>=4 here")
    entropy_bits = dimension * modulus_bits
    # (3/2)^5 < 2^3; square-root bound costs another factor of two.
    exponent = max(0, (5 * entropy_bits - 3 * columns) // 10)
    return {
        "dimension": dimension, "modulus_bits": modulus_bits, "columns": columns,
        "uniform_secret_entropy_bits": entropy_bits,
        "source": "b=A^T*s+e moduloq; e distributed as the full coordinate DFT intensity of ANY normalized secret-independent amplitude envelope on {0,1}^m",
        "arbitrary_entangled_amplitudes_and_correlated_Fourier_noise_allowed": True,
        "envelope_may_depend_on_public_matrix_A": True,
        "envelope_may_depend_on_unknown_secret": False,
        "full_block_collision_multiplier_upper_bound": "(3/2)^m",
        "product_coordinate_collision_multiplier_upper_bound": exact(Fraction(3, 2)),
        "mean_correct_secret_probability_upper_bound": "min(1,sqrt((3/2)^m / 2^(nL)))",
        "conservative_correct_probability_dyadic_exponent": exponent,
        "minimum_columns_before_this_collision_obstruction_becomes_vacuous": "m>=nL/log2(3/2); necessary for this bound to be vacuous, not sufficient for decoding",
        "unlimited_runtime_removes_this_information_obstruction": False,
        "all_classical_observation_decoders_bounded": True,
        "general_quantum_or_native_DCP_decoder_bounded": False,
        "A_adaptive_subgroup_covariant_measurements_are_bounded": False,
        "near_entropy_width_binary_error_decoder_import_justified": False,
        "independent_mathematical_review_complete": False,
        "candidate_record_accepted": False, "speedup_claim_allowed": False,
    }


def boolean_block_collision_certificate(modulus, columns):
    for value, name in ((modulus, "modulus"), (columns, "Boolean envelope width")):
        _positive_integer(value, name)
    if modulus < 3:
        raise ValueError("q>=3: the order-two Fourier alphabet is an exception")
    return {
        "status": "LOCAL_BOOLEAN_BLOCK_L4_TENSOR_BOUND_REVIEW_PENDING",
        "modulus": modulus, "Boolean_width": columns,
        "ambient_translation_group": "Z_q^m, not merely the native A^T*Z_q^n subgroup",
        "normalized_envelope_support": "physical unit-gap {0,1}^m",
        "q_to_m_times_Fourier_intensity_collision_upper_bound": exact(Fraction(3, 2)**columns),
        "arbitrary_complex_entangled_or_label_dependent_amplitudes_allowed": True,
        "coordinate_noise_independence_required": False,
        "product_balanced_amplitudes_attain_bound": True,
        "generic_subgroup_covariant_quantum_measurement_ruled_out": False,
        "proof": "Split the multiaffine Fourier polynomial as a+w*b. Average fourth moment over w; apply Cauchy and induction to the mixed term. X^2+Y^2+4XY<=(3/2)*(X+Y)^2.",
        "candidate_record_accepted": False, "speedup_claim_allowed": False,
    }


def _boolean_block_controls():
    records = []
    rng = np.random.default_rng(9105)
    for q, m in ((3, 2), (3, 4), (4, 4), (8, 3), (4, 6)):
        words = list(itertools.product(range(2), repeat=m))
        N = len(words)
        random = rng.normal(size=N) + 1j*rng.normal(size=N)
        random /= np.linalg.norm(random)
        ghz = np.zeros(N, dtype=complex)
        ghz[0], ghz[-1] = 1/math.sqrt(2), 1j/math.sqrt(2)
        for name, amplitude in (("product_balanced", np.ones(N)/math.sqrt(N)),
                                ("GHZ_entangled", ghz), ("random_complex_entangled", random)):
            polynomial = {}
            for x, fx in zip(words, amplitude):
                for y, fy in zip(words, amplitude):
                    z = tuple(a+b for a, b in zip(x, y))
                    polynomial[z] = polynomial.get(z, 0j) + fx*fy
            additive_energy = float(sum(abs(v)**2 for v in polynomial.values()))
            embedded = np.zeros((q,)*m, dtype=complex)
            for x, fx in zip(words, amplitude):
                embedded[x] = fx
            probabilities = np.abs(np.fft.fftn(embedded, norm="ortho"))**2
            collision = q**m * float(np.sum(probabilities**2))
            upper = (3/2)**m
            assert abs(collision-additive_energy) < 1e-9
            assert collision <= upper + 1e-9
            if name == "product_balanced":
                assert abs(collision-upper) < 1e-9
            records.append({"modulus": q, "Boolean_width": m, "amplitude_family": name,
                            "Boolean_amplitudes": [{"real": float(complex(v).real), "imag": float(complex(v).imag)} for v in amplitude],
                            "q_to_m_times_Fourier_intensity_collision": collision,
                            "independent_coefficient_additive_energy": additive_energy,
                            "tensor_bound": upper,
                            "finite_control_is_an_efficient_native_measurement": False})
    return records


def _subgroup_measurement_countercontrols():
    records = []
    for L in (2, 3, 4):
        q = 1 << L
        labels = [1 << j for j in range(L)]
        targets = [sum(a*(x >> j & 1) for j, a in enumerate(labels)) for x in range(q)]
        assert targets == list(range(q))
        minimum = 1.0
        for secret in range(q):
            state = np.exp(2j*np.pi*secret*np.asarray(targets)/q)/math.sqrt(q)
            output = np.fft.fft(state, norm="ortho")
            correct = float(abs(output[secret])**2)
            assert abs(correct-1) < 1e-10
            minimum = min(minimum, correct)
        records.append({"modulus_bits": L, "modulus": q, "labels": labels, "phase_registers": L,
                        "Boolean_sum_is_bijective": True,
                        "actual_coherent_QFT_correct_probability_every_secret": minimum,
                        "measured_full_coordinate_Fourier_noise_decoder_bound": math.sqrt((3/4)**L),
                        "IID_native_literal_label_pattern_probability_dyadic_exponent": L*L,
                        "scalable_native_label_selector_or_quantum_algorithm_supplied": False,
                        "control_is_a_candidate": False})
    return records


def fourier_noise_distribution(modulus, coefficients=(1 / math.sqrt(2), -1 / math.sqrt(2))):
    _positive_integer(modulus, "modulus")
    if modulus < 3 or len(coefficients) != 2:
        raise ValueError("q>=3 and two coefficients required")
    coefficients = np.asarray(coefficients, dtype=complex)
    if not np.all(np.isfinite(coefficients)) or abs(float(np.vdot(coefficients, coefficients).real) - 1) > 1e-10:
        raise ValueError("finite normalized envelope required")
    values = coefficients[0] + coefficients[1] * np.exp(-2j * np.pi * np.arange(modulus) / modulus)
    return np.abs(values) ** 2 / modulus


def _optimal_classical_decoder_control(A, q, probabilities):
    n, m = len(A), len(A[0])
    assert len(probabilities) == m
    secrets = list(itertools.product(range(q), repeat=n))
    success = 0.0
    for b in itertools.product(range(q), repeat=m):
        likelihoods = [math.prod(probabilities[i][(b[i] - sum(A[j][i] * s[j] for j in range(n))) % q]
                                for i in range(m)) for s in secrets]
        success += max(likelihoods) / len(secrets)
    kappa = [q * float(np.dot(p, p)) for p in probabilities]
    bound = min(1, math.sqrt(math.prod(kappa) / len(secrets)))
    assert success <= bound + 1e-10
    return {"dimension": n, "modulus": q, "labels": A, "samples": m,
            "coordinate_noise_probabilities": [p.tolist() for p in probabilities],
            "coordinate_collision_multipliers": kappa,
            "actual_exhaustive_optimal_classical_correct_probability": success,
            "collision_correct_probability_upper_bound": bound,
            "bounded_exhaustive_control_is_an_efficient_native_solver": False}


def run_controls():
    envelopes = []
    coefficients = ((1 / math.sqrt(2), -1 / math.sqrt(2)),
                    (math.sqrt(3) / 2, 0.5j), (1, 0))
    for q in (3, 4, 8, 16, 64):
        for c in coefficients:
            p = fourier_noise_distribution(q, c)
            kappa = q * float(np.dot(p, p))
            expected = 1 + 2 * abs(c[0] * c[1]) ** 2
            assert abs(kappa - expected) < 1e-10 and kappa <= 1.5 + 1e-10
            envelopes.append({"modulus": q, "probabilities": p.tolist(),
                              "coefficients": [{"real": float(complex(z).real), "imag": float(complex(z).imag)} for z in c],
                              "collision_multiplier": kappa, "formula_collision_multiplier": expected,
                              "Shannon_information_per_sample_bits": math.log2(q) + sum(float(v) * math.log2(float(v)) for v in p if v > 1e-20)})
    controls = []
    for A, q in ((((1,),), 4), (((1, 3),), 4), (((0, 0),), 4),
                 (((1, 2, 3),), 4), (((1, 0), (0, 1)), 4), (((1, 2),), 3)):
        probabilities = [fourier_noise_distribution(q, coefficients[i % 2]) for i in range(len(A[0]))]
        controls.append(_optimal_classical_decoder_control(A, q, probabilities))
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "complete_envelope_collision_controls": envelopes,
            "entangled_Boolean_block_controls": _boolean_block_controls(),
            "Boolean_block_collision_certificate": boolean_block_collision_certificate(8, 16),
            "native_subgroup_measurement_scope_countercontrols": _subgroup_measurement_countercontrols(),
            "exhaustive_optimal_classical_decoder_controls": controls,
            "native_near_entropy_width_ledgers": [boolean_envelope_native_certificate(n, 4*n+1, n*(4*n+1)+16) for n in (8, 16, 32)],
            "claim_gate": {"measured_Fourier_noise_classical_decoder_shortcut_falsified_at_near_entropy_width": True,
                           "correlating_secret_independent_Boolean_envelope_amplitudes_evades_converse": False,
                           "A_adaptive_subgroup_covariant_quantum_measurement_ruled_out": False,
                           "native_collective_quantum_source_bridge_supplied": False,
                           "all_quantum_subset_sum_algorithms_ruled_out": False,
                           "novelty_claim": False, "speedup_claim_allowed": False, "candidate_record_accepted": False},
            "dependency_sha256": {str(Path(__file__).relative_to(ROOT)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"],
                      "native_correct_probability_dyadic_exponents": [r["conservative_correct_probability_dyadic_exponent"] for r in report["native_near_entropy_width_ledgers"]]}, indent=2))


if __name__ == "__main__":
    main()
