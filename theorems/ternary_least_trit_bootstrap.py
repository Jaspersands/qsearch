"""Source-exact conditional least-trit bootstrap and native copy gate.

LOCAL DERIVATIONS / REVIEW PENDING. The higher-root weak learner is MISSING.
Recipes and conditional reductions are not an implemented full decoder.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_incidence_decoder import IncidenceDecoder, IncidenceSample, sample_budget

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_least_trit_bootstrap.json"


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _vector(values, modulus, name, dimension=None):
    values = tuple(values)
    if not values or (dimension is not None and len(values) != dimension):
        raise ValueError(f"{name}: nonempty matching vector required")
    if any(type(x) is not int or not 0 <= x < modulus for x in values):
        raise ValueError(f"{name}: canonical residues required")
    return values


def _dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def _root(numerator, denominator):
    return np.exp(2j*math.pi*(numerator % denominator)/denominator)


@dataclass(frozen=True)
class NativeTransform:
    original_first: tuple
    original_second: tuple
    original_digits: int
    prefix: tuple
    known_digits: int
    shift: tuple
    target_coordinate: int
    sign: int

    def __post_init__(self):
        r = _integer(self.original_digits, "original digits", 1)
        d = _integer(self.known_digits, "known prefix digits")
        if d >= r:
            raise ValueError("at least one unknown digit must remain")
        q, Q = 3**r, 3**(r-d)
        a = _vector(self.original_first, q, "first frequency")
        for field, modulus in (("original_second", q), ("prefix", 3**d), ("shift", Q)):
            object.__setattr__(self, field, _vector(getattr(self, field), modulus, field, len(a)))
        object.__setattr__(self, "original_first", a)
        _integer(self.target_coordinate, "target coordinate")
        if self.target_coordinate >= len(a) or type(self.sign) is not int or self.sign not in (-1, 1):
            raise ValueError("valid target coordinate and scalar sign +/-1 required")

    @property
    def modulus(self):
        return 3**self.original_digits

    @property
    def lower_modulus(self):
        return 3**(self.original_digits-self.known_digits)

    @property
    def permutation(self):
        p = list(range(len(self.original_first)))
        p[0], p[self.target_coordinate] = p[self.target_coordinate], p[0]
        return tuple(p)

    @property
    def known_phase_guess(self):
        return tuple(u+3**self.known_digits*v for u, v in zip(self.prefix, self.shift))

    @property
    def phase_numerators(self):
        return tuple(-_dot(row, self.known_phase_guess) % self.modulus
                     for row in (self.original_first, self.original_second))

    @property
    def learner_frequencies(self):
        return tuple(tuple(self.sign*row[j] % self.lower_modulus for j in self.permutation)
                     for row in (self.original_first, self.original_second))

    def learner_view(self):
        # Only the transformed source is passed to the learner. Revealing the
        # shift, sign or pre-transform labels would change its promised input.
        return {"first": self.learner_frequencies[0], "second": self.learner_frequencies[1],
                "native_even_level": 2*(self.original_digits-self.known_digits),
                "modulus": self.lower_modulus}

    def pullback(self, predicted_trit):
        _integer(predicted_trit, "predicted least trit")
        if predicted_trit > 2:
            raise ValueError("predicted least trit must be canonical")
        return (self.shift[self.target_coordinate]+self.sign*predicted_trit) % 3

    def recipe(self):
        return {"operation": "known diagonal phases on the original supplied qutrit",
                "original_native_even_level": 2*self.original_digits,
                "original_digits": self.original_digits,
                "diagonal_phase_numerators": (0, *self.phase_numerators),
                "phase_denominator": str(self.modulus),
                "original_first": self.original_first, "original_second": self.original_second,
                "assumed_correct_prefix": self.prefix, "known_prefix_digits": self.known_digits,
                "public_random_shift": self.shift, "target_coordinate": self.target_coordinate,
                "public_random_sign": self.sign, "permutation": self.permutation,
                "learner_view": self.learner_view(),
                "prefix_correctness_checked_using_unknown_secret": False,
                "wrong_prefix_source_promise": False, "fresh_original_state_required": True,
                "labels_selected_or_postselected": False, "all_outcomes_kept": True,
                "state_cloning_or_unknown_inverse_required": False,
                "public_modular_dot_products": 2,
                "phase_precision_and_original_source_acquisition_must_be_charged": True}


def transformed_secret_for_calibration(transform, secret):
    """Simulation assertion, never an input or subroutine of a decoder."""
    secret = _vector(secret, transform.modulus, "calibration secret", len(transform.prefix))
    scale = 3**transform.known_digits
    if any(s % scale != u for s, u in zip(secret, transform.prefix)):
        raise ValueError("wrong prefix: lower native-source promise is invalid")
    residual = tuple((s-u)//scale for s, u in zip(secret, transform.prefix))
    return tuple(transform.sign*(residual[j]-transform.shift[j]) % transform.lower_modulus
                 for j in transform.permutation)


def amplitude_control(transform, secret):
    target = transformed_secret_for_calibration(transform, secret)
    original = np.array([1, *(_root(_dot(row, secret), transform.modulus)
                             for row in (transform.original_first, transform.original_second))])/math.sqrt(3)
    diagonal = np.array([1, *(_root(x, transform.modulus) for x in transform.phase_numerators)])
    expected = np.array([1, *(_root(_dot(row, target), transform.lower_modulus)
                             for row in transform.learner_frequencies)])/math.sqrt(3)
    error = float(np.max(abs(original*diagonal-expected)))
    if error > 2e-12:
        raise AssertionError("native prefix/randomization amplitude identity failed")
    labels = [inverse_frequency_coordinates(a, c, 2*(transform.original_digits-transform.known_digits))
              for a, c in zip(*transform.learner_frequencies)]
    source = native_source([labels], 2*(transform.original_digits-transform.known_digits))
    if source.frequencies[0] != transform.learner_frequencies:
        raise AssertionError("lower native ring chart disagrees")
    original_labels = [inverse_frequency_coordinates(a, c, 2*transform.original_digits)
                       for a, c in zip(transform.original_first, transform.original_second)]
    original_source = native_source([original_labels], 2*transform.original_digits)
    if original_source.frequencies[0] != (transform.original_first, transform.original_second):
        raise AssertionError("original native ring chart disagrees")
    return {**transform.recipe(), "calibration_secret_only": secret,
            "original_native_ring_labels": original_labels,
            "transformed_secret_calibration_only": target, "lower_native_ring_labels": labels,
            "maximum_amplitude_error": error, "unknown_secret_passed_to_learner": False}


def source_uniformity_ledger(n, digits, known_digits):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1)
    _integer(known_digits, "known digits")
    if known_digits >= digits:
        raise ValueError("unknown native root must remain")
    return {"dimension": n, "original_modulus": str(3**digits),
            "lower_modulus": str(3**(digits-known_digits)),
            "original_frequency_pairs": str(3**(2*n*digits)),
            "lower_frequency_pairs": str(3**(2*n*(digits-known_digits))),
            "exact_preimages_per_lower_pair": str(3**(2*n*known_digits)),
            "independent_uniform_frequency_rows_preserved": True,
            "source_uniformity_is_conditional_on_correct_prefix": True,
            "adaptive_prefix_needs_fresh_original_batches": True,
            "reducing_measured_covariant_records_gives_this_source": False}


def symmetrized_error_law(errors):
    errors = tuple(Fraction(x) for x in errors)
    if len(errors) != 3 or any(x < 0 for x in errors) or sum(errors) != 1:
        raise ValueError("three exact error probabilities summing to one required")
    return (errors[0], (errors[1]+errors[2])/2, (errors[1]+errors[2])/2)


@dataclass(frozen=True)
class WeakLearnerContract:
    advantage: Fraction
    native_qutrits_per_call: int
    secret_distribution: str = "uniform_all_secrets"
    source_distribution: str = "fresh_IID_native_even_random_labels"

    def __post_init__(self):
        if not isinstance(self.advantage, Fraction) or not 0 < self.advantage <= Fraction(2, 3):
            raise ValueError("exact rational advantage in (0,2/3] required")
        _integer(self.native_qutrits_per_call, "native copies per weak call", 1)
        if self.secret_distribution != "uniform_all_secrets":
            raise ValueError("primitive-only success is not the required uniform-all-secret guarantee")
        if self.source_distribution != "fresh_IID_native_even_random_labels":
            raise ValueError("chosen labels or reused batches do not satisfy the native weak-source contract")


def primitive_only_transfer(n, primitive_success):
    _integer(n, "dimension", 1)
    p = Fraction(primitive_success)
    if not 0 <= p <= 1:
        raise ValueError("success probability must lie in [0,1]")
    # No guarantee on nonprimitive secrets: do not silently assign chance success.
    return {"primitive_fraction": str(1-Fraction(1, 3**n)),
            "uniform_all_secret_success_lower_bound": str((1-Fraction(1, 3**n))*p),
            "nonprimitive_success_assumed": "0", "primitive_guarantee_is_sufficient_automatically": False}


def bootstrap_ledger(n, digits, contract, confidence_bits=16):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1)
    _integer(confidence_bits, "confidence bits", 1)
    if not isinstance(contract, WeakLearnerContract):
        raise ValueError("validated conditional weak-learner contract required")
    copy_gate = least_trit_copy_gate(n, digits, contract.native_qutrits_per_call, contract.advantage)
    if not copy_gate["necessary_copy_gate_passed"]:
        raise ValueError("weak-learner advantage violates the full-label native copy gate")
    coordinates = n*digits
    log_union = (2*coordinates-1).bit_length()
    # exp(-9R eps^2/8) per competing trit; this conservative exact integer
    # uses ln(2)<1 rather than rounding a floating logarithm in the proof.
    R = math.ceil(Fraction(8*(log_union+confidence_bits), 9)/contract.advantage**2)
    weak_calls = coordinates*R
    return {"dimension": n, "root_digits": digits, "advantage_assumption": str(contract.advantage),
            "native_qutrits_per_weak_call_assumption": contract.native_qutrits_per_call,
            "repetitions_per_coordinate_digit": R, "coordinate_digit_decisions": coordinates,
            "total_fresh_weak_calls": weak_calls,
            "total_fresh_original_native_qutrits": weak_calls*contract.native_qutrits_per_call,
            "correct_vs_each_wrong_expected_margin": str(3*contract.advantage/2),
            "per_competitor_Hoeffding_bound": "exp(-9*R*epsilon^2/8)",
            "first_error_union_bound": "2*n*r*exp(-9*R*epsilon^2/8)",
            "sufficient_complete_recovery_failure_bound": f"2^-{confidence_bits}",
            "fresh_independent_batches_for_every_weak_call": True,
            "known_prefix_validity_conditioned_on_no_previous_digit_error": True,
            "guarantee_required_at_every_lower_native_root": True,
            "weak_copy_budget_is_a_maximum_not_an_uncharged_conditional_expectation": True,
            "necessary_full_label_native_copy_gate_passed": True,
            "public_phase_rotations_upper_bound": 2*weak_calls*contract.native_qutrits_per_call,
            "gate_approximation_error_must_be_added_to_failure_budget": True,
            "weak_learner_implemented": False, "full_native_recovery_implemented": False,
            "polynomial_reduction_only_if_weak_learner_cost_and_inverse_advantage_are_polynomial": True,
            "status": "CONDITIONAL_REDUCTION_REVIEW_PENDING_NOT_AN_ACCEPTED_CANDIDATE"}


@dataclass(frozen=True)
class WeakVote:
    target_coordinate: int
    shift_trit: int
    sign: int
    prediction: int
    original_record_ids: frozenset

    def __post_init__(self):
        _integer(self.target_coordinate, "coordinate")
        for name in ("shift_trit", "prediction"):
            if type(getattr(self, name)) is not int or getattr(self, name) not in (0, 1, 2):
                raise ValueError("canonical trit required")
        if type(self.sign) is not int or self.sign not in (-1, 1):
            raise ValueError("scalar sign +/-1 required")
        ids = frozenset(self.original_record_ids)
        if not ids or any(type(x) is not int or x < 0 for x in ids):
            raise ValueError("nonempty original fresh record IDs required")
        object.__setattr__(self, "original_record_ids", ids)

    @property
    def pulled_trit(self):
        return (self.shift_trit+self.sign*self.prediction) % 3


def plurality(votes):
    votes = tuple(votes)
    if not votes or any(not isinstance(v, WeakVote) for v in votes):
        raise ValueError("validated votes required")
    ids, counts = set(), [0, 0, 0]
    for vote in votes:
        if vote.target_coordinate != votes[0].target_coordinate:
            raise ValueError("votes must address one coordinate")
        if ids.intersection(vote.original_record_ids):
            raise ValueError("fresh amplification forbids shared original ancestors")
        ids.update(vote.original_record_ids)
        counts[vote.pulled_trit] += 1
    best = [j for j in range(3) if counts[j] == max(counts)]
    return {"counts": counts, "trit": best[0] if len(best) == 1 else None,
            "status": "EMPIRICAL_PLURALITY" if len(best) == 1 else "TIED_NO_OUTPUT",
            "original_native_records_charged": len(ids),
            "success_probability_certified_from_votes_alone": False,
            "weak_learner_implemented": False}


def least_trit_copy_gate(n, digits, copies, desired_advantage=Fraction(1, 10)):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1)
    _integer(copies, "native copies")
    eps = Fraction(desired_advantage)
    if not 0 < eps <= Fraction(2, 3):
        raise ValueError("advantage in (0,2/3] required")
    squared = Fraction(3**copies-1, 2*3**(n*digits))
    return {"dimension": n, "root_digits": digits, "native_copies": copies,
            "mean_advantage_squared_upper_bound": str(squared),
            "mean_success_upper_bound": "min(1, 1/3 + sqrt((3^M-1)/(2*q^n)))",
            "desired_advantage": str(eps), "necessary_copy_gate_passed": squared >= eps**2,
            "necessary_copy_condition": "3^M >= 1 + 2*q^n*epsilon^2",
            "receiver_scope": "ANY full-label-controlled collective POVM, uniform ALL native secrets",
            "per_fixed_source_or_secret_bound": False,
            "arbitrary_polynomial_copy_receivers_excluded": False,
            "sample_bound_does_not_prove_computational_hardness": True,
            "status": "LOCAL_DERIVATION_REVIEW_PENDING"}


def least_trit_reference(frequencies, digits):
    """Exponential information-only optimum; not a implementable fiber receiver."""
    _integer(digits, "digits", 1)
    frequencies = tuple(frequencies)
    if not frequencies or len(frequencies) > 8:
        raise ValueError("reference enumeration requires 1..8 native qutrits")
    q = 3**digits
    n = len(frequencies[0][0])
    rows = []
    for pair in frequencies:
        if len(pair) != 2:
            raise ValueError("two public native frequency rows per qutrit required")
        rows.append(tuple(_vector(row, q, "frequency", n) for row in pair))
    counts = defaultdict(Counter)
    for word in product(range(3), repeat=len(rows)):
        f = tuple(sum(rows[i][j-1][k] if j else 0 for i, j in enumerate(word)) % q for k in range(n))
        key = (f[0] % (q//3), *f[1:])
        counts[key][f[0]//(q//3)] += 1
    success = sum(sum(math.sqrt(c.get(k, 0)) for k in range(3))**2 for c in counts.values())/(3*3**len(rows))
    return {"dimension": n, "digits": digits, "frequency_pairs": rows,
            "words_enumerated": 3**len(rows), "nuisance_fiber_count": len(counts),
            "optimal_uniform_secret_least_trit_success": success,
            "nuisance_fibers": [{"key": key, "counts_by_trit_character": [c.get(k, 0) for k in range(3)]}
                                for key, c in sorted(counts.items())],
            "reference_only_exponential_word_enumeration": True,
            "efficient_fiber_preparation_or_inverse_granted": False,
            "native_weak_learner_implemented": False}


def close_known_prefix_control(n, digits, seed):
    """Actual field decoder given a correct external prefix; no full-depth search."""
    _integer(n, "dimension", 1); _integer(digits, "digits", 2)
    rng, q = random.Random(seed), 3**digits
    secret = tuple(rng.randrange(q) for _ in range(n))
    prefix = tuple(s % (q//3) for s in secret)
    decoder, records, max_error = IncidenceDecoder(n), [], 0.
    budget = sample_budget(n)["sufficient_fresh_IID_samples"]
    while len(decoder.span.rows) < len(decoder.basis)-1 and decoder.samples < budget:
        a, c = (tuple(rng.randrange(q) for _ in range(n)) for _ in range(2))
        t = NativeTransform(a, c, digits, prefix, digits-1, (0,)*n, 0, 1)
        view = t.learner_view()
        state = np.array([1, *(_root(_dot(row, secret)+phase, q)
                              for row, phase in zip((a, c), t.phase_numerators))])/math.sqrt(3)
        choice = rng.randrange(3)
        transform = np.array([[_root(-choice*j*j-o*j, 3)/math.sqrt(3) for j in range(3)]
                              for o in range(3)])
        probabilities = abs(transform@state)**2
        pick, outcome = rng.random(), 2
        for o, cumulative in enumerate(np.cumsum(probabilities)):
            if pick < cumulative:
                outcome = o; break
        alpha = tuple((v-u) % 3 for u, v in zip(view["first"], view["second"]))
        beta = tuple((2*u-v) % 3 for u, v in zip(view["first"], view["second"]))
        sample = IncidenceSample(alpha, beta, choice, outcome)
        decoder.add(sample)
        target = tuple((s-u)//(q//3) for s, u in zip(secret, prefix))
        exact = np.array([1, *(_root(_dot(row, target), 3) for row in t.learner_frequencies)])/math.sqrt(3)
        max_error = max(max_error, float(np.max(abs(state-exact))))
        records.append({"original_first": a, "original_second": c,
                        "phase_numerators": [str(x) for x in t.phase_numerators],
                        "lower_first": view["first"], "lower_second": view["second"],
                        "basis": choice, "outcome": outcome, "probabilities": probabilities.tolist(),
                        "alpha": alpha, "beta": beta})
    result = decoder.result()
    assert result["status"] == "FIELD_SECRET_CERTIFIED" and result["secret"] == target
    return {"dimension": n, "original_digits": digits, "original_modulus": str(q), "seed": seed,
            "calibration_secret_only": [str(s) for s in secret],
            "externally_given_correct_prefix": [str(u) for u in prefix],
            "recovered_top_trit": result["secret"], "decoder_result": result,
            "original_fresh_native_qutrits_consumed": len(records),
            "maximum_native_amplitude_error": max_error, "raw_public_records": records,
            "decoder_received_unknown_secret": False, "prefix_discovered_by_this_control": False,
            "original_full_secret_discovery": False, "higher_root_weak_learner_implemented": False}


def build_report():
    controls = []
    for n, r, d in ((1, 2, 0), (2, 3, 1), (3, 8, 5)):
        q, rng = 3**r, random.Random(86200+n+r)
        secret = tuple(rng.randrange(q) for _ in range(n))
        prefix = tuple(s % 3**d for s in secret)
        a, c = (tuple(rng.randrange(q) for _ in range(n)) for _ in range(2))
        shift = tuple(rng.randrange(3**(r-d)) for _ in range(n))
        for target in range(n):
            for sign in (-1, 1):
                controls.append(amplitude_control(NativeTransform(a, c, r, prefix, d, shift, target, sign), secret))
    references = []
    for n, r, M in ((1, 4, 2), (1, 4, 4), (1, 4, 6), (2, 3, 6), (2, 3, 8)):
        rng = random.Random(86300+n*100+r*10+M)
        rows = [(tuple(rng.randrange(3**r) for _ in range(n)), tuple(rng.randrange(3**r) for _ in range(n)))
                for _ in range(M)]
        references.append(least_trit_reference(rows, r))
    return {"status": "LOCAL_DERIVATIONS_REVIEW_PENDING_WEAK_LEARNER_MISSING",
            "source": "fresh IID even-native qutrits, two uniform Z_(3^r)^n labels, all uniform secrets",
            "native_prefix_and_randomization_controls": controls,
            "exact_source_uniformity": [source_uniformity_ledger(n, r, d) for n, r, d in ((1, 2, 1), (4, 16, 8), (32, 128, 127))],
            "biased_error_countercontrol": {"unamplifiable_unsymmetrized_error_law": ["2/5", "3/5", "0"],
                                            "symmetrized_error_law": list(map(str, symmetrized_error_law((Fraction(2, 5), Fraction(3, 5), 0))))},
            "primitive_only_countercontrol": primitive_only_transfer(1, Fraction(2, 5)),
            "conditional_reduction_ledgers": [bootstrap_ledger(n, r, WeakLearnerContract(Fraction(1, 10), n*r))
                                              for n, r in ((2, 8), (8, 32), (32, 128))],
            "arbitrary_collective_least_trit_copy_gates": [least_trit_copy_gate(n, r, M)
                                                         for n, r, M in ((2, 8, 8), (2, 8, 16), (8, 32, 128), (8, 32, 256))],
            "least_trit_information_only_references": references,
            "actual_known_prefix_field_closures": [close_known_prefix_control(n, r, 86400+n)
                                                   for n, r in ((1, 8), (2, 16), (4, 32))],
            "remaining_obligations": ["independent review of native source correction and amplification",
                                       "construct a higher-root full-label least-trit learner with inverse-polynomial advantage",
                                       "charge original native-source acquisition and aggregate phase synthesis error",
                                       "no free nuisance-fiber preparation, erasure, inverse or exhaustive-secret estimator",
                                       "retain original batches and compare raw-sample joint classical inference"],
            "higher_root_weak_learner_implemented": False, "full_native_secret_search_implemented": False,
            "accepted_candidate": False, "novelty_or_quantum_speedup_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
        print(json.dumps({"report": str(REPORT), "higher_root_weak_learner_implemented": False,
                          "known_prefix_field_closures": len(report["actual_known_prefix_field_closures"])}))
    else:
        print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
