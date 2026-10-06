"""Native line source and a final-field incidence decoder.

LOCAL DERIVATION / REVIEW PENDING. Fixed-field baseline, not a new full-depth
algorithm. Higher-root support exclusions are explicitly NOT a decoder bound.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from fractions import Fraction
from itertools import permutations, product
import json
import math
from pathlib import Path
import random

import numpy as np

from cyclotomic_fiber_receiver import frequency_coordinates, inverse_frequency_coordinates
from cyclotomic_rescaling_gate import ideal_chart, residue
from ternary_carry_packets import compile_packet
from ternary_phase_depth import NativePhaseHierarchy
from ternary_quotient_decoder import Span, monomials

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_incidence_decoder.json"


def _int(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def local_line_matrix(digits):
    if tuple(sorted(digits)) != (0, 1, 2) or any(type(x) is not int for x in digits):
        raise ValueError("one permutation of the three physical digits required")
    j0, j1, j2 = digits
    return ((j1-j0, int(j1 == 2)-int(j0 == 2)),
            (j2-j0, int(j2 == 2)-int(j0 == 2)))


@dataclass(frozen=True)
class NativeLine:
    level: int
    modulus: int
    first: tuple
    second: tuple
    native_output_labels: tuple
    physical_words: tuple
    consumed: int
    initial_syndrome: tuple
    complement: tuple

    def resources(self):
        return {"odd_parent_level": self.level, "even_output_level": self.level-1,
                "retained_phase_modulus": self.modulus,
                "odd_input_qutrits_consumed": self.consumed,
                "qutrits_measured": self.consumed-1,
                "all_syndromes_and_complement_outcomes_kept": True,
                "branch_probability": str(Fraction(1, 3**(self.consumed-1))),
                "frame_selected_using_only_low_labels": True,
                "IID_output_claim_requires_fresh_IID_native_input_batches": True,
                "intermediate_odd_source_acquisition_charged": False,
                "initial_top_secret_digit_retained": False,
                "unknown_preparation_or_inverse_supplied": False,
                "multiple_outputs_from_one_packet_certified_independent": False}


def first_kernel_line(packet, complement=None):
    """Keep first free coordinate; measure all other free coordinates."""
    hierarchy = NativePhaseHierarchy.from_packet(packet)
    complement = (0,)*(packet.retained-1) if complement is None else tuple(complement)
    if len(complement) != packet.retained-1 or any(type(x) is not int or x not in (0, 1, 2) for x in complement):
        raise ValueError("one canonical digit per measured free coordinate required")
    logical = tuple((j, *complement) for j in range(3))
    values = [hierarchy.derivative(z, ()) for z in logical]
    q = hierarchy.retained_modulus
    first, second = (tuple((x-y) % q for x, y in zip(values[j], values[0])) for j in (1, 2))
    labels = tuple(inverse_frequency_coordinates(a, b, packet.level-1) for a, b in zip(first, second))
    return NativeLine(packet.level, q, first, second, labels,
                      tuple(packet.assignment(z) for z in logical), packet.consumed,
                      packet.syndrome, complement)


def sample_native_line(n, level, rng):
    _int(n, "secret dimension", 1)
    _int(level, "odd parent level", 3)
    if level % 2 != 1:
        raise ValueError("odd parent level required")
    h0, _, h1 = ideal_chart(level)[0]
    labels = [[(rng.randrange(h0), rng.randrange(h1)) for _ in range(n)] for _ in range(n+1)]
    packet = compile_packet(labels, level)
    # Original native amplitudes are flat, so every measured coordinate is
    # uniform. This is a source sampler, not postselection on a lucky chart.
    packet = replace(packet, syndrome=tuple(rng.randrange(3) for _ in packet.pivots))
    complement = tuple(rng.randrange(3) for _ in range(packet.retained-1))
    return first_kernel_line(packet, complement)


def measurement_probabilities(first, second, secret, modulus, basis):
    _int(modulus, "phase modulus", 3)
    _int(basis, "canonical MUB basis")
    if not first or basis not in (0, 1, 2) or len(first) != len(second) or len(first) != len(secret):
        raise ValueError("matching phase vectors and canonical MUB basis required")
    if any(type(x) is not int or not 0 <= x < modulus for row in (first, second) for x in row):
        raise ValueError("canonical public phase frequencies required")
    if any(type(s) is not int for s in secret):
        raise ValueError("integer secret calibration required")
    if modulus % 3:
        raise ValueError("phase modulus divisible by3 required")
    a, c = (sum(x*s for x, s in zip(row, secret)) % modulus for row in (first, second))
    state = np.exp(2j*np.pi*np.array([0, a, c])/modulus)/math.sqrt(3)
    transform = np.array([[np.exp(-2j*np.pi*(basis*j*j+o*j)/3)/math.sqrt(3)
                           for j in range(3)] for o in range(3)])
    return tuple(float(abs(x)**2) for x in transform@state)


@dataclass(frozen=True)
class IncidenceSample:
    alpha: tuple
    beta: tuple
    basis: int
    outcome: int
    phase_modulus: int = 3

    def __post_init__(self):
        object.__setattr__(self, "alpha", tuple(self.alpha))
        object.__setattr__(self, "beta", tuple(self.beta))
        if type(self.phase_modulus) is not int or self.phase_modulus != 3:
            raise ValueError("incidence constraints require actual phase modulus3, not a low-digit shadow")
        if not self.alpha or len(self.alpha) != len(self.beta):
            raise ValueError("nonempty equal-length coefficient vectors required")
        if any(type(x) is not int or x not in (0, 1, 2) for x in (*self.alpha, *self.beta, self.basis, self.outcome)):
            raise ValueError("canonical F3 coefficients, basis and outcome required")

    def value(self, trial):
        if len(trial) != len(self.alpha) or any(type(x) is not int or x not in (0, 1, 2) for x in trial):
            raise ValueError("canonical field trial required")
        a = sum(x*y for x, y in zip(self.alpha, trial))-self.outcome
        b = sum(x*y for x, y in zip(self.beta, trial))-self.basis
        return (1-b*b)*a % 3


def field_probabilities(alpha, beta, secret, basis):
    sample = IncidenceSample(alpha, beta, basis, 0)
    if len(secret) != len(sample.alpha) or any(type(s) is not int for s in secret):
        raise ValueError("matching integer secret calibration required")
    if sum(x*s for x, s in zip(beta, secret)) % 3 == basis:
        outcome = sum(x*s for x, s in zip(alpha, secret)) % 3
        return tuple(Fraction(int(j == outcome)) for j in range(3))
    return (Fraction(1, 3),)*3


def field_sample(line, secret, rng):
    if line.modulus != 3:
        raise ValueError("final-field decoder rejects deeper native roots")
    if len(secret) != len(line.first) or any(type(s) is not int for s in secret):
        raise ValueError("secret dimension mismatch")
    alpha = tuple((c-a) % 3 for a, c in zip(line.first, line.second))
    beta = tuple((2*a-c) % 3 for a, c in zip(line.first, line.second))
    basis = rng.randrange(3)
    if sum(x*s for x, s in zip(beta, secret)) % 3 == basis:
        outcome = sum(x*s for x, s in zip(alpha, secret)) % 3
    else:
        outcome = rng.randrange(3)
    return IncidenceSample(alpha, beta, basis, outcome)


def _multiply(left, right):
    out = defaultdict(int)
    for a, u in left.items():
        for b, v in right.items():
            # Canonical polynomial FUNCTIONS on F3: x^3=x, not x^3=0.
            exponent = tuple(t if t < 3 else 1+(t-1) % 2 for t in (x+y for x, y in zip(a, b)))
            out[exponent] = (out[exponent]+u*v) % 3
    return {a: x for a, x in out.items() if x}


def incidence_polynomial(sample):
    n, zero = len(sample.alpha), (0,)*len(sample.alpha)
    A, B = {zero: -sample.outcome % 3}, {zero: -sample.basis % 3}
    for j, (a, b) in enumerate(zip(sample.alpha, sample.beta)):
        unit = tuple(int(k == j) for k in range(n))
        A[unit], B[unit] = a, b
    square = _multiply(B, B)
    factor = {a: -x % 3 for a, x in square.items()}
    factor[zero] = (factor.get(zero, 0)+1) % 3
    return _multiply(factor, A)


def feature_basis(n):
    _int(n, "secret dimension", 1)
    return tuple(a for degree in range(4) for a in monomials(n, degree))


def sample_budget(n, confidence_bits=16):
    _int(n, "secret dimension", 1)
    _int(confidence_bits, "confidence bits", 1)
    D = 1+n+n*(n+1)//2+n*(n-1)+math.comb(n, 3)
    return {"feature_dimension": D, "target_rank": D-1,
            "rank_escape_probability_lower_bound": "2/81",
            "confidence_bits": confidence_bits,
            "sufficient_fresh_IID_samples": 81*(D-1+4*confidence_bits),
            "failure_probability_upper_bound": f"2^-{confidence_bits}",
            "probability_theorem_status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "source_uniformity_and_fresh_batches_required": True}


class IncidenceDecoder:
    def __init__(self, n):
        self.basis = feature_basis(n)
        self.n = n
        self.index = {a: j for j, a in enumerate(self.basis)}
        self.span = Span(len(self.basis))
        self.samples = 0

    def add(self, sample):
        if not isinstance(sample, IncidenceSample) or len(sample.alpha) != self.n:
            raise ValueError("validated field sample of the decoder dimension required")
        vector = np.zeros(len(self.basis), dtype=np.int64)
        for a, x in incidence_polynomial(sample).items():
            vector[self.index[a]] = x
        self.span.add(vector)
        self.samples += 1

    def result(self):
        D, rank = len(self.basis), len(self.span.rows)
        out = {"samples": self.samples, "feature_dimension": D, "rank": rank,
               "secret": None, "feature_vector": None,
               "secret_assignments_enumerated": False, "phase_modulus": 3,
               "complete_parent_secret_recovered": False,
               "speedup_claim_allowed": False, "novelty_claim": False}
        if rank == D:
            return {**out, "status": "INCONSISTENT_FIELD_DATA"}
        if rank != D-1:
            return {**out, "status": "INSUFFICIENT_CONSTRAINT_RANK"}
        free = next(j for j in range(D) if j not in self.span.rows)
        v = np.zeros(D, dtype=np.int64)
        v[free] = 1
        for pivot, row in sorted(self.span.rows.items(), reverse=True):
            v[pivot] = -int(row@v) % 3
        if not v[0]:
            return {**out, "status": "NULLVECTOR_HAS_NO_AFFINE_NORMALIZATION"}
        v = v*int(v[0]) % 3
        secret = tuple(int(v[self.index[tuple(int(k == j) for k in range(self.n))]]) for j in range(self.n))
        features = tuple(math.prod(s**a for s, a in zip(secret, powers)) % 3 for powers in self.basis)
        if features != tuple(map(int, v)):
            return {**out, "status": "NULLVECTOR_IS_NOT_A_SECRET_EVALUATION"}
        return {**out, "status": "FIELD_SECRET_CERTIFIED", "secret": secret,
                "feature_vector": features}


def exact_zero_support(first, second, modulus, basis, outcome):
    _int(modulus, "phase modulus", 3)
    if modulus % 3 or any(type(x) is not int or not 0 <= x < 3 for x in (basis, outcome)):
        raise ValueError("modulus divisible by3 and canonical MUB indices required")
    for value in (first, second):
        if type(value) is not int or not 0 <= value < modulus:
            raise ValueError("canonical root frequency required")
    third = modulus//3
    a = (first-third*(basis+outcome)) % modulus
    c = (second-third*(4*basis+2*outcome)) % modulus
    return {a, c} == {third, 2*third}


def exclusion_ledger(digits, samples=0):
    _int(digits, "root digits", 1)
    _int(samples, "number of measurements")
    q = 3**digits
    return {"phase_modulus": str(q), "root_digits": digits,
            "fixed_MUB_outcome_zero_fraction": str(Fraction(2, q*q)),
            "some_MUB_outcome_zero_fraction": str(Fraction(9, q*q)),
            "measurements": samples,
            "independent_trial_elimination_union_bound": str(min(Fraction(1), Fraction(2*samples, q*q))),
            "independent_trial_survival_law": "(1-2/R^2)^M",
            "true_and_trial_secrets": "s=e1,t=e2; IID native even-level frequency vectors; n>=2",
            "measurement_scope": "fresh single-qutrit quadratic F3 MUB; support-zero constraints only",
            "positive_likelihood_information_ruled_out": False,
            "general_classical_or_quantum_decoder_lower_bound": False}


def low_shadow_countercontrol():
    packet = compile_packet([[(1, 0)]]*3, 5)
    line = first_kernel_line(packet, (0,))
    assert (line.first, line.second) == ((8,), (8,))
    probabilities = measurement_probabilities(line.first, line.second, (1,), 9, 2)
    shadow = IncidenceSample((0,), (2,), 2, 1)
    assert shadow.value((1,)) == 2 and probabilities[1] > .18
    return {"native_labels": packet.labels, "odd_parent_level": 5,
            "initial_syndrome": packet.syndrome, "complement": (0,),
            "native_residual_frequencies": ((0,), line.first, line.second),
            "actual_phase_modulus": 9, "secret": (1,), "MUB_basis": 2,
            "actual_outcome_probabilities": probabilities,
            "formal_quadratic_alpha_beta_mod9": [3, 5],
            "incorrect_field_shadow_alpha_beta": [0, 2],
            "positive_probability_false_constraint_outcome": 1,
            "false_constraint_value_at_true_secret": shadow.value((1,)),
            "total_false_constraint_probability": probabilities[1]+probabilities[2],
            "field_shadow_transfer_admitted": False,
            "deterministic_native_countercontrol_not_IID_frequency_claim": True}


def full_source_control():
    """Entire n1,m2,L3 source; affine measurement branches, not planted data."""
    labels = list(product(range(9), range(3)))
    tables = {y: (0, *frequency_coordinates(y, 3)) for y in labels}
    counts, amplitude_error, born_error, branches = defaultdict(Counter), 0., 0., 0
    for y1, y2 in product(labels, repeat=2):
        packet = compile_packet([[y1], [y2]], 3)
        for syndrome in product(range(3), repeat=len(packet.pivots)):
            packet = replace(packet, syndrome=syndrome)
            for complement in product(range(3), repeat=packet.retained-1):
                line = first_kernel_line(packet, complement)
                stratum = ((residue(y1), residue(y2)), syndrome, complement)
                counts[stratum][(line.first[0], line.second[0])] += 1
                actual = [sum(tables[y][j] for y, j in zip((y1, y2), word)) % 9 for word in line.physical_words]
                original = np.exp(2j*np.pi*8*np.array(actual)/9)/math.sqrt(3)
                expected = np.exp(2j*np.pi*2*np.array([0, line.first[0], line.second[0]])/3)/math.sqrt(3)
                original *= np.exp(-2j*np.pi*8*actual[0]/9)
                amplitude_error = max(amplitude_error, float(max(abs(original-expected))))
                alpha, beta = (line.second[0]-line.first[0]) % 3, (2*line.first[0]-line.second[0]) % 3
                for b in range(3):
                    native = measurement_probabilities(line.first, line.second, (8,), 3, b)
                    field = field_probabilities((alpha,), (beta,), (2,), b)
                    born_error = max(born_error, max(abs(x-float(y)) for x, y in zip(native, field)))
                branches += 1
    assert len(counts) == 27 and all(len(c) == 9 and set(c.values()) == {9} for c in counts.values())
    assert amplitude_error < 1e-12 and born_error < 1e-12
    return {"native_source_batches_enumerated": 729, "physical_input_words": 6561,
            "all_affine_branches_replayed": branches,
            "conditional_low_and_outcome_strata": len(counts),
            "frequency_pairs_per_stratum": 9, "multiplicity_per_pair": 9,
            "all_branches_probability": "1/3", "parent_secret": 8,
            "retained_secret_residue": 2, "maximum_amplitude_error": amplitude_error,
            "maximum_Born_probability_error": born_error,
            "conditional_product_uniformity_checked": True}


def decode_native_control(n, seed):
    rng, decoder = random.Random(seed), IncidenceDecoder(n)
    parent_secret = tuple(8-j % 3 for j in range(n))
    budget = sample_budget(n)
    public_samples = []
    while len(decoder.span.rows) < len(decoder.basis)-1 and decoder.samples < budget["sufficient_fresh_IID_samples"]:
        line = sample_native_line(n, 3, rng)
        sample = field_sample(line, parent_secret, rng)
        decoder.add(sample)
        public_samples.append({"alpha": sample.alpha, "beta": sample.beta,
                               "basis": sample.basis, "outcome": sample.outcome})
    result = decoder.result()
    assert result["status"] == "FIELD_SECRET_CERTIFIED" and result["secret"] == tuple(s % 3 for s in parent_secret)
    return {"dimension": n, "seed": seed, "parent_secret_calibration_only": parent_secret,
            "result": result, "probability_budget": budget,
            "public_measurement_records": public_samples,
            "source_batches": decoder.samples,
            "odd_native_qutrits_consumed": decoder.samples*(n+1),
            "actual_labels_sampled_before_all_measurement_outcomes": True,
            "secret_given_to_classical_decoder": False,
            "odd_source_acquisition_and_high_digit_recursion_supplied": False}


def run_controls():
    matrices = []
    for digits in permutations(range(3)):
        M = local_line_matrix(digits)
        determinant = M[0][0]*M[1][1]-M[0][1]*M[1][0]
        assert abs(determinant) == 1
        matrices.append({"physical_digit_permutation": digits, "integer_matrix": M, "determinant": determinant})
    growing = []
    for level in (3, 5, 7, 9, 19):
        line = sample_native_line(3, level, random.Random(59100+level))
        assert all(frequency_coordinates(y, level-1) == (a, b) for y, a, b in zip(line.native_output_labels, line.first, line.second))
        growing.append({"level": level, "output_first": line.first, "output_second": line.second,
                        "even_native_output_labels": line.native_output_labels, "resources": line.resources()})
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "new_full_depth_algorithm": False,
            "candidate_accepted": False, "speedup_claim_allowed": False,
            "source_law_scope": "one low-defined kernel line; fresh unfiltered IID native batches; arbitrary odd depth",
            "six_unimodular_line_matrices": matrices, "full_native_source_control": full_source_control(),
            "growing_depth_output_controls": growing,
            "final_field_native_decoders": [decode_native_control(n, 59300+n) for n in (1, 2, 4, 8)],
            "higher_root_support_exclusion_ledgers": [exclusion_ledger(r, 1000) for r in (1, 2, 4, 8, 16)],
            "native_low_shadow_countercontrol": low_shadow_countercontrol(),
            "remaining_blockers": ["source cost through all secret digits", "implicit deeper-root likelihood or collective decoder",
                                   "comparison with published quantum sieves", "independent mathematical review"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "new_full_depth_algorithm": False,
                      "field_decoders": len(report["final_field_native_decoders"])}))


if __name__ == "__main__":
    main()
