"""Costed full-secret ternary frequency/fiber receiver reference.

LOCAL DERIVATION / REVIEW PENDING. Public exact DP and bounded coherent replay
are exponential reference machinery, not an efficient new quantum algorithm.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random

import numpy as np
from sympy import Matrix, eye, isprime

from cyclotomic_rescaling_gate import ideal_chart, reduce_element
from dhsp_codomain_instrument import _integer, rational

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/cyclotomic_fiber_receiver.json"


def frequency_matrix(level):
    beta = ideal_chart(level)[1]
    q = 3**((level+1)//2)
    row = [q*x for x in beta]
    if any(x.denominator != 1 for x in row):
        raise AssertionError("integer-secret frequency normalization failed")
    u, v = map(int, row)
    matrix = Matrix([[u, v], [u+v, -u]])
    assert int(matrix.det()) == (-3 if level % 2 else -1)
    return q, matrix


def frequency_coordinates(label, level):
    y = reduce_element(label, level)
    q, matrix = frequency_matrix(level)
    return tuple(int(x) % q for x in matrix*Matrix(y))


def inverse_frequency_coordinates(first, second, level):
    q, matrix = frequency_matrix(level)
    _integer(first, "canonical first frequency", 0)
    _integer(second, "canonical second frequency", 0)
    if first >= q or second >= q:
        raise ValueError("canonical frequency must be below the secret modulus")
    if level % 2:
        delta = (second-2*first) % q
        if delta % 3:
            raise ValueError("odd-level frequencies must satisfy second=2*first mod3")
        u, v = map(int, matrix.row(0))
        companion = Matrix([[u, v], [(v-u)//3, (-u-2*v)//3]])
        assert int(companion.det()) == -1
        y = companion.inv()*Matrix([first, delta//3])
    else:
        y = matrix.inv()*Matrix([first, second])
    return reduce_element(tuple(map(int, y)), level)


def source_bijection_control(level):
    if level > 6:
        raise ValueError("source enumeration is calibration-only, level<=6")
    h0, _, h1 = ideal_chart(level)[0]
    q, matrix = frequency_matrix(level)
    counts = Counter()
    for y in product(range(h0), range(h1)):
        coordinates = frequency_coordinates(y, level)
        assert inverse_frequency_coordinates(*coordinates, level) == y
        counts[coordinates] += 1
    assert len(counts) == 3**level and set(counts.values()) == {1}
    if level % 2:
        expected = {(a, (2*a+3*d) % q) for a in range(q) for d in range(q//3)}
    else:
        expected = set(product(range(q), repeat=2))
    assert set(counts) == expected
    return {"level": level, "integer_secret_modulus": q, "frequency_matrix": [list(map(int, row)) for row in matrix.tolist()],
            "matrix_determinant": int(matrix.det()), "exhaustive_native_label_count": len(counts),
            "every_allowed_frequency_pair_has_exactly_one_native_label": True,
            "even_level_two_frequencies_independently_uniform": level % 2 == 0,
            "odd_level_constraint": "second=2*first mod3; (first,(second-2*first)/3) uniform product",
            "public_frequency_coordinates_reveal_unknown_secret": False}


def general_native_frequency_matrix(prime, modulus_logp):
    _integer(prime, "fixed prime", 2)
    _integer(modulus_logp, "modulus logp")
    if not isprime(prime) or prime > 7 or modulus_logp > 3:
        raise ValueError("general-prime field calibration capped at prime<=7 and logp<=3")
    d, q = prime-1, prime**modulus_logp
    Z = Matrix.hstack(*(eye(d)[:, j+1] if j+1 < d else -Matrix.ones(d, 1) for j in range(d)))
    pi = Z-eye(d)
    level = d*modulus_logp
    beta = Matrix([[d]+[-1]*(d-1)])*pi.inv()**(level-1)/prime
    matrix = Matrix.vstack(*(q*beta*sum((Z**k for k in range(j)), Matrix.zeros(d)) for j in range(1, prime)))
    assert all(x.q == 1 for x in matrix)
    assert abs(int(matrix.det())) == 1
    return q, matrix


def general_source_and_onehot_control(prime, modulus_logp):
    q, matrix = general_native_frequency_matrix(prime, modulus_logp)
    d = prime-1
    rng = random.Random(47051+prime*10+modulus_logp)
    frequencies = [rng.randrange(q) for _ in range(d)]
    label = [int(x) % q for x in matrix.inv()*Matrix(frequencies)]
    assert tuple(int(x) % q for x in matrix*Matrix(label)) == tuple(frequencies)
    secret = q-1
    supplied_binary_product = np.array([np.exp(2j*math.pi*(secret*sum(frequencies[j] for j in range(d)
                                  if word >> j & 1) % q)/q)/math.sqrt(2**d) for word in range(2**d)])
    selected = [0]+[1 << j for j in range(d)]
    probability = float(sum(abs(supplied_binary_product[selected])**2))
    assert abs(probability-prime/2**d) < 4e-12
    native = supplied_binary_product[selected]/math.sqrt(probability)
    expected = np.array([np.exp(2j*math.pi*(secret*f % q)/q)/math.sqrt(prime) for f in [0]+frequencies])
    assert max(abs(native-expected)) < 4e-12
    reverse_probability = float(sum(abs(x)**2 for x in native[:2]))
    reverse_binary = native[:2]/math.sqrt(reverse_probability)
    assert abs(reverse_probability-2/prime) < 4e-12
    assert max(abs(reverse_binary-np.array([1, np.exp(2j*math.pi*(secret*frequencies[0] % q)/q)])/math.sqrt(2))) < 4e-12
    return {"prime": prime, "modulus_logp": modulus_logp, "modulus": q,
            "native_full_ramification_level": d*modulus_logp,
            "power_basis_frequency_matrix": [list(map(int, row)) for row in matrix.tolist()],
            "integer_matrix_determinant": int(matrix.det()),
            "all_nonzero_native_frequencies_are_IID_uniform_Zq": True,
            "integer_secret_calibration": secret, "native_ring_label_coefficients": label,
            "independent_supplied_binary_phase_labels": frequencies,
            "fresh_binary_registers_required": d, "accepted_binary_word_indices": selected,
            "onehot_projection_probability": probability,
            "failed_binary_word_indices": [j for j in range(2**d) if j not in selected],
            "failed_projection_probability": 1-probability,
            "conditional_native_qudit_amplitudes": [[float(x.real), float(x.imag)] for x in native],
            "expected_binary_samples_per_native_qudit": rational(Fraction(d*2**d, prime)),
            "expected_native_qudits_per_binary_sample": rational(Fraction(prime, 2)),
            "expected_native_qudits_yield_per_forward_binary_input": rational(Fraction(prime, d*2**d)),
            "reverse_two_word_projection_probability": reverse_probability,
            "reverse_accepted_native_digits": (0, 1),
            "reverse_conditional_binary_amplitudes": [[float(x.real), float(x.imag)] for x in reverse_binary],
            "reverse_cost_is_not_the_forward_yield": True,
            "forward_then_reverse_expected_binary_cost_per_binary_output": rational(Fraction(d*2**(d-1))),
            "inverse_from_one_native_qudit_or_cloning_granted": False,
            "constant_overhead_requires_fixed_prime": True,
            "known_reduction_conformance_not_novel_algorithm": True}


@dataclass(frozen=True)
class FrequencySource:
    labels: tuple
    level: int
    frequencies: tuple
    modulus: int

    @property
    def dimension(self):
        return len(self.labels[0])

    @property
    def inputs(self):
        return len(self.labels)

    @property
    def group_size(self):
        return self.modulus**self.dimension

    def value(self, word):
        if len(word) != self.inputs or any(type(j) is not int or not 0 <= j < 3 for j in word):
            raise ValueError("one canonical digit per supplied native qutrit required")
        return tuple(sum((row[j-1][l] if j else 0) for row, j in zip(self.frequencies, word)) % self.modulus
                     for l in range(self.dimension))


def native_source(labels, level):
    q, _ = frequency_matrix(level)
    if not labels or not labels[0] or any(len(row) != len(labels[0]) for row in labels):
        raise ValueError("nonempty rectangular native ring-vector labels required")
    labels = tuple(tuple(reduce_element(y, level) for y in row) for row in labels)
    frequencies = []
    for row in labels:
        columns = [frequency_coordinates(y, level) for y in row]
        frequencies.append(tuple(tuple(c[j] for c in columns) for j in range(2)))
    return FrequencySource(labels, level, tuple(frequencies), q)


class ExactFiberIndex:
    """Known suffix counts, rank/unrank and explicit exponential cost ledger."""
    def __init__(self, source):
        if source.group_size > 4096 or source.inputs > 12:
            raise ValueError("exact DP reference capped at4096 group elements and12 qutrits")
        self.source = source
        zero = (0,)*source.dimension
        self.suffix = [{} for _ in range(source.inputs+1)]
        self.suffix[-1] = {zero: 1}
        self.additions = 0
        for i in range(source.inputs-1, -1, -1):
            layer = Counter()
            for tail, count in self.suffix[i+1].items():
                for j in range(3):
                    f = zero if j == 0 else source.frequencies[i][j-1]
                    target = tuple((a+b) % source.modulus for a, b in zip(f, tail))
                    layer[target] += count
                    self.additions += 1
            self.suffix[i] = dict(layer)
        assert sum(self.suffix[0].values()) == 3**source.inputs

    def _count(self, position, target, prefix, digit):
        source = self.source
        f = (0,)*source.dimension if digit == 0 else source.frequencies[position][digit-1]
        rest = tuple((t-p-a) % source.modulus for t, p, a in zip(target, prefix, f))
        return self.suffix[position+1].get(rest, 0), f

    def rank(self, word):
        target = self.source.value(word)
        rank, prefix = 0, (0,)*self.source.dimension
        for i, digit in enumerate(word):
            for lower in range(digit):
                rank += self._count(i, target, prefix, lower)[0]
            f = self._count(i, target, prefix, digit)[1]
            prefix = tuple((p+a) % self.source.modulus for p, a in zip(prefix, f))
        return target, rank

    def unrank(self, target, rank):
        _integer(rank, "canonical within-fiber rank", 0)
        if len(target) != self.source.dimension or any(type(t) is not int or not 0 <= t < self.source.modulus for t in target):
            raise ValueError("canonical public group target required")
        target = tuple(target)
        if rank >= self.suffix[0].get(target, 0):
            raise ValueError("empty fiber or rank outside its exact count")
        prefix, word = (0,)*self.source.dimension, []
        for i in range(self.source.inputs):
            for j in range(3):
                count, f = self._count(i, target, prefix, j)
                if rank >= count:
                    rank -= count
                    continue
                word.append(j)
                prefix = tuple((p+a) % self.source.modulus for p, a in zip(prefix, f))
                break
            else:
                raise AssertionError("suffix count failed to unrank")
        assert rank == 0 and self.source.value(word) == target
        return tuple(word)

    def resources(self):
        return {"suffix_layer_support_sizes": [len(c) for c in self.suffix],
                "exact_count_additions": self.additions,
                "stored_count_entries": sum(len(c) for c in self.suffix),
                "full_group_size": str(self.source.group_size),
                "ternary_word_count": str(3**self.source.inputs),
                "preprocessing_is_polynomial_in_group_size_not_its_log": True,
                "uniform_scalable_receiver_circuit_supplied": False,
                "dense_public_rank_blocks_replayed": True,
                "gate_level_uniform_receiver_compiled": False,
                "free_coherent_table_lookup_or_QRAM_granted": False,
                "counts_ranks_and_range_rotations_are_public_not_secret_dependent": True}


def erase_uniform_rank(vector):
    """Known Householder range erasure; dense verification, not circuit synthesis."""
    if len(vector) == 1:
        return np.array(vector, complex)
    v = np.ones(len(vector))/math.sqrt(len(vector))
    v[0] -= 1
    v /= np.linalg.norm(v)
    return np.array(vector)-2*v*np.vdot(v, vector)


def binary_projection_controls(source, secret):
    controls = []
    for first, second in source.frequencies:
        phases = [0]+[sum(s*f for s, f in zip(secret, frequency)) % source.modulus for frequency in (first, second)]
        native = np.array([np.exp(2j*math.pi*x/source.modulus) for x in phases])/math.sqrt(3)
        probability = float(sum(abs(native[:2])**2))
        assert abs(probability-Fraction(2, 3)) < 4e-12
        binary = native[:2]/math.sqrt(probability)
        controls.append({"known_projector_basis_indices": [0, 1], "binary_phase_label": list(first),
                         "accepted_probability": probability, "failed_probability": float(abs(native[2])**2),
                         "conditional_binary_amplitudes": [[float(x.real), float(x.imag)] for x in binary],
                         "expected_native_qutrits_per_binary_sample": rational(Fraction(3, 2)),
                         "all_projector_outcomes_costed": True,
                         "full_integer_secret_retained": True, "arbitrary_Gaussian_DCP_merge_supplied": False})
    return controls


def receiver_control(labels, level, secret):
    source = native_source(labels, level)
    if source.inputs > 7 or source.group_size > 512:
        raise ValueError("dense quantum replay capped at7 qutrits and512 secret targets")
    if len(secret) != source.dimension or any(type(s) is not int or not 0 <= s < source.modulus for s in secret):
        raise ValueError("full integer-secret calibration required")
    index = ExactFiberIndex(source)
    ranked = {t: np.zeros(count, complex) for t, count in index.suffix[0].items()}
    D, N = 3**source.inputs, source.group_size
    for word in product(range(3), repeat=source.inputs):
        t, rank = index.rank(word)
        assert index.unrank(t, rank) == word
        theta = 2*math.pi*(sum(s*v for s, v in zip(secret, t)) % source.modulus)/source.modulus
        ranked[t][rank] = np.exp(1j*theta)/math.sqrt(D)
    erased = np.zeros((source.modulus,)*source.dimension, complex)
    leakage = 0.0
    for t, vector in ranked.items():
        clean = erase_uniform_rank(vector)
        erased[t] = clean[0]
        leakage += float(sum(abs(clean[1:])**2))
    assert leakage < 3e-25
    probabilities = abs(np.fft.fftn(erased)/math.sqrt(N))**2
    optimal = sum(math.sqrt(count/D) for count in index.suffix[0].values())**2/N
    assert abs(float(probabilities[tuple(secret)])-optimal) < 4e-12
    assert abs(float(probabilities.sum())-1) < 4e-12
    return {"parent_level": level, "native_labels": labels,
            "integer_secret_calibration": secret, "full_secret_modulus": source.modulus,
            "full_integer_secret_group_size": N, "native_qutrits_consumed": source.inputs,
            "public_two_frequency_vectors": source.frequencies,
            "charged_vector_DCP_projection_controls": binary_projection_controls(source, secret),
            "public_fiber_counts": [{"target": list(t), "count": count} for t, count in sorted(index.suffix[0].items())],
            "classical_DP_resources": index.resources(), "all_native_words_ranked_and_unranked": D,
            "rank_register_leakage_probability": leakage,
            "nonzero_rank_outcomes_retained_as_failure": True,
            "erased_target_amplitudes": [[float(x.real), float(x.imag)] for x in erased.ravel()],
            "all_full_secret_Fourier_outcome_probabilities": list(map(float, probabilities.ravel())),
            "actual_full_secret_recovery_probability": float(probabilities[tuple(secret)]),
            "optimal_covariant_measurement_probability": optimal,
            "measure_public_fiber_before_readout_uniform_prior_success": 1/N,
            "unknown_state_preparation_or_inverse_used_by_receiver": False,
            "higher_secret_digits_discarded": False, "exponential_DP_preprocessing_ignored": False,
            "primitive_status": "KNOWN_PUBLIC_DP_REFERENCE_RECEIVER_NOT_NEW_EFFICIENT_ALGORITHM"}


def scaling_ledger(dimension, modulus_log3, slack=4):
    _integer(dimension, "growing vector dimension")
    _integer(modulus_log3, "growing modulus log3")
    _integer(slack, "native packet entropy slack", 0)
    exponent = dimension*modulus_log3
    if exponent > 1024 or slack > 128:
        raise ValueError("decimal exact ledger capped at1024 target trits and128 slack trits")
    N, D = 3**exponent, 3**(exponent+slack)
    return {"vector_dimension": dimension, "modulus_log3": modulus_log3,
            "original_even_CCP_level": 2*modulus_log3,
            "raw_native_qutrits": exponent+slack, "full_secret_target_trits": exponent,
            "ideal_source_mean_PGM_success_lower_bound": rational(Fraction(D, D+N-1)),
            "pairwise_distinct_word_collision_probability": rational(Fraction(1, N)),
            "explicit_DP_worst_case_group_states": str(N),
            "expected_final_DP_count_entries_lower_bound": rational(Fraction(N*D, D+N-1)),
            "source_information_bound_is_new_algorithm": False,
            "classical_or_quantum_optimal_runtime_lower_bound_claimed": False,
            "scope": "IID native even-level frequencies, all full secret digits; DP is only a sufficient reference implementation"}


def run_controls():
    controls = []
    for level, n, m in ((2, 2, 5), (4, 2, 6), (6, 1, 5)):
        for seed in range(47011, 47014):
            rng = random.Random(seed)
            h0, _, h1 = ideal_chart(level)[0]
            labels = [[(rng.randrange(h0), rng.randrange(h1)) for _ in range(n)] for _ in range(m)]
            q = 3**(level//2)
            secret = [(q-1-j) % q for j in range(n)]
            c = receiver_control(labels, level, secret)
            c["unfiltered_native_label_seed"] = seed
            controls.append(c)
    zero = receiver_control([[(0, 0)]]*3, 2, [2])
    return {"status": "FULL_SECRET_TERNARY_FIBER_REFERENCE_VERIFIED_EXPONENTIAL_PREPROCESSING_REVIEW_PENDING",
            "source_bijection_controls": [source_bijection_control(L) for L in range(1, 7)],
            "general_prime_source_and_charged_onehot_controls": [
                general_source_and_onehot_control(p, t) for p in (2, 3, 5, 7) for t in (1, 2, 3)],
            "native_full_secret_receiver_controls": controls, "zero_information_countercontrol": zero,
            "growing_parameter_ledgers": [scaling_ledger(n, t) for n in (8, 16, 32, 64) for t in (4, 8, 16)],
            "claim_gate": {"new_algorithm": False, "candidate_accepted": False, "Shor_level_improvement": False,
                "polynomial_time_fiber_preparation": False, "generic_fiber_receiver_lower_bound": False,
                "general_ring_secret_reduction_verified": False,
                "standard_LWE_attack": False, "independent_human_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "full_secret_receivers": len(report["native_full_secret_receiver_controls"]),
                      "new_algorithm": False, "preprocessing_cost_preserved": True}))


if __name__ == "__main__":
    main()
