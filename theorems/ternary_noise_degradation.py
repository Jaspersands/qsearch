"""Conditional noisy-linear-to-native classical transcript reduction.

Certified public noise, explicit TV/copy accounting and source-law obligations.
No quantum-state preparation or efficient native decoder is provided.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import random

from flint import fmpq

from ternary_certified_noise_sampler import certified_sample_noise, rational, sampler_failure_bound
from ternary_covariant_noise import CovariantRecord, root_digits
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_NOISE_DEGRADATION.md"
REPORT = ROOT / "research/reductions/ternary_noise_degradation.json"


def degradation_bound(q, records, second_moment, max_bits=64, max_proposals=128):
    root_digits(q)
    integer(records, "positive complete paired record count", 1)
    V = rational(second_moment, "source second-moment bound")
    if V < 0:
        raise ValueError("nonnegative public error moment bound required")
    per_record = min(fmpq(1), 80*V/(3*q*q))
    abort = sampler_failure_bound(max_bits, max_proposals)
    total = min(fmpq(1), records*(per_record+abort))
    return {"source_integer_second_moment_upper": str(V),
            "per_record_ideal_noise_TV_upper": str(per_record),
            "per_record_sampler_abort_probability_upper": str(abort),
            "complete_transcript_success_loss_upper": str(total),
            "bound_is_nonvacuous": total < 1,
            "input_classical_samples_required": 2*records, "output_paired_records": records,
            "native_unknown_quantum_states_prepared": 0,
            "assumptions": ["same unknown secret", "IID uniform full-root labels",
                            "independent symmetric source errors", "public true second-moment bound",
                            "independent ideal random bits", "fixed decoder and charged sample count"],
            "input_assumptions_inferred_from_observed_values": False,
            "unconditional_hardness_or_speedup": False,
            "conditioning_on_sampler_success_erases_loss": False}


def round_observation_interval(q, lower, upper):
    root_digits(q)
    lower, upper = rational(lower, "observation lower bound"), rational(upper, "observation upper bound")
    if lower > upper:
        raise ValueError("nonempty certified source observation interval required")
    a, b = q*lower+fmpq(1, 2), q*upper+fmpq(1, 2)
    first, last = int(a.numerator)//int(a.denominator), int(b.numerator)//int(b.denominator)
    return {"status": "CERTIFIED_UNIQUE_ROUNDING" if first == last else "UNKNOWN_ROUNDING_BOUNDARY",
            "modulus": q, "lower": str(lower), "upper": str(upper),
            "first_integer": first, "last_integer": last,
            "value": first % q if first == last else None,
            "midpoint_guess_on_ambiguous_interval": False}


def gaussian_rounding_loss(q, alpha, records, interval_width):
    root_digits(q)
    integer(records, "positive output record count", 1)
    alpha, width = rational(alpha, "Gaussian alpha"), rational(interval_width, "maximum source interval width")
    if not 0 < alpha < 1 or width < 0:
        raise ValueError("positive subunit alpha and nonnegative interval width required")
    # Y=qX has a Gaussian fractional-part density bounded by1+1/(q*alpha).
    # An ambiguous containing interval of width h requires Y within q*h
    # on either side of a half-integer, irrespective of adaptive interval placement.
    per_input = min(fmpq(1), 2*width*(q+1/alpha))
    return {"maximum_normalized_observation_interval_width": str(width),
            "per_input_rounding_abort_probability_upper": str(per_input),
            "two_M_input_rounding_abort_union_upper": str(min(fmpq(1), 2*records*per_input)),
            "source_interval_contains_true_observation_is_assumed_not_inferred": True,
            "input_errors_are_continuous_D_alpha_before_rounding": True}


def round_source_intervals(samples):
    samples = tuple(samples)
    if not samples or len(samples) % 2:
        raise ValueError("complete even continuous-source sample list required")
    output, certificates = [], []
    for sample in samples:
        certificate = round_observation_interval(sample["modulus"], sample["lower"], sample["upper"])
        certificates.append(certificate)
        if certificate["value"] is None:
            return {"status": "UNKNOWN_SOURCE_ROUNDING", "records": (), "certificates": certificates,
                    "partial_samples_reused_as_full_transcript": False}
        output.append(NoisyLinearRecord(sample["label"], certificate["value"], sample["modulus"], sample["source_id"]))
    if len({s.source_id for s in output}) != len(output) or any(
            s.modulus != output[0].modulus or len(s.label) != len(output[0].label) for s in output):
        raise ValueError("distinct consistent original interval source records required")
    return {"status": "CERTIFIED_INTERVAL_SOURCE_ROUNDING", "records": tuple(output),
            "certificates": certificates, "partial_samples_reused_as_full_transcript": False}


def sampling_budget(records, failure_bits):
    integer(records, "positive complete record count", 1)
    integer(failure_bits, "positive failure bits", 1)
    proposals = 2*(failure_bits+(2*records-1).bit_length())
    bits = failure_bits+(6*records*proposals-1).bit_length()
    union = min(fmpq(1), records*sampler_failure_bound(bits, proposals))
    if union > fmpq(1, 2**failure_bits):
        raise ArithmeticError("scalable sampler budget failed its exact confidence bound")
    return {"failure_bits": failure_bits, "max_bits": bits, "max_proposals": proposals,
            "block_bits": 8, "M_record_sampler_abort_union_upper": str(union),
            "fixed_precision_is_asymptotically_sufficient": False}


def rounded_gaussian_profile(n, q, alpha, records, failure_bits=64):
    integer(n, "positive source dimension", 1)
    integer(records, "positive complete output record count", 1)
    root_digits(q)
    alpha = rational(alpha, "Gaussian width parameter")
    if not 0 < alpha < 1:
        raise ValueError("Gaussian alpha must lie strictly between0 and1")
    # The source paper uses D_alpha(x) proportional to exp(-pi*x^2/alpha^2),
    # NOT standard deviation alpha. After E=nearest(qX), E[E^2]<=q^2*a^2/pi+1/2.
    V = q*q*alpha*alpha/3+fmpq(1, 2)
    source_guard = (alpha*q)**2 >= 4*n
    classical_guard = q*q >= 2**n
    budget = sampling_budget(records, failure_bits)
    precision = q.bit_length()+records.bit_length()+failure_bits+3
    width = fmpq(1, 2**precision)
    rounding = gaussian_rounding_loss(q, alpha, records, width)
    transcript = degradation_bound(q, records, V, budget["max_bits"], budget["max_proposals"])
    composed = min(fmpq(1), rational(transcript["complete_transcript_success_loss_upper"], "transcript loss")
                   +rational(rounding["two_M_input_rounding_abort_union_upper"], "source rounding loss"))
    return {"dimension": n, "modulus": q, "alpha": str(alpha),
            "source_theorem": "Brakerski et al.2013 Theorem2.16 (search LWE)",
            "source_url": "https://arxiv.org/html/1306.0281",
            "source_error_law": "continuous D_alpha on torus, rounded only AFTER scaling by q",
            "Gaussian_width_is_standard_deviation": False,
            "rounded_integer_error_second_moment_upper": str(V),
            "alpha_q_at_least_2_sqrt_n": source_guard,
            "q_at_least_2_to_n_over_two": classical_guard,
            "published_quantum_worst_case_source_parameter_guard": source_guard,
            "published_classical_worst_case_source_parameter_guard": source_guard and classical_guard,
            "modulus_is_imported_from_prime_only_theorem": False,
            "source_precision_adapter_implemented": True,
            "source_rounding_precision_bits": precision, "sampler_budget": budget,
            "source_rounding_loss": rounding,
            "composed_success_loss_upper": str(composed),
            "conditional_transcript_bound": transcript,
            "hardness_transfer_admitted": False,
            "remaining_debt": ["external review of composed reduction",
                               "source oracle supplies containing intervals at charged precision",
                               "decoder success and source sample-count premises",
                               "no quantum input bridge or native efficient receiver"]}


@dataclass(frozen=True)
class NoisyLinearRecord:
    label: tuple
    value: int
    modulus: int
    source_id: str

    def __post_init__(self):
        root_digits(self.modulus)
        object.__setattr__(self, "label", tuple(self.label))
        if not self.label or any(type(x) is not int or not 0 <= x < self.modulus for x in self.label):
            raise ValueError("canonical nonempty full-root label required")
        if type(self.value) is not int or not 0 <= self.value < self.modulus:
            raise ValueError("canonical noisy linear value required")
        if type(self.source_id) is not str or not self.source_id:
            raise ValueError("distinct original classical source ID required")

    def public(self):
        return {"label": self.label, "value": self.value, "modulus": self.modulus, "source_id": self.source_id}


def convert_pairs(samples, rng, second_moment, max_bits=64, max_proposals=128):
    samples = tuple(samples)
    if not samples or len(samples) % 2 or any(not isinstance(s, NoisyLinearRecord) for s in samples):
        raise ValueError("nonempty even list of original noisy-linear records required")
    q, n = samples[0].modulus, len(samples[0].label)
    if any(s.modulus != q or len(s.label) != n for s in samples):
        raise ValueError("shared full-root modulus and dimension required")
    if len({s.source_id for s in samples}) != len(samples):
        raise ValueError("reusing an original error sample cannot create independent pairs")
    bound = degradation_bound(q, len(samples)//2, second_moment, max_bits, max_proposals)
    # This public reduction-side mask uniformizes ANY fixed source secret.
    # The black-box native decoder receives the transcript, not source truth.
    mask = tuple(rng.randrange(q) for _ in range(n))
    output, runs, ancestry = [], [], []
    for a, c in zip(samples[::2], samples[1::2]):
        run = certified_sample_noise(q, rng, max_bits, max_proposals)
        runs.append(run)
        if run["noise"] is None:
            break
        values = tuple((s.value+sum(x*y for x, y in zip(s.label, mask))+e) % q
                       for s, e in zip((a, c), run["noise"]))
        output.append(CovariantRecord(a.label, c.label, values, q).public())
        ancestry.append((a.source_id, c.source_id))
    complete = len(output)*2 == len(samples)
    return {"status": "CONDITIONAL_CLASSICAL_TRANSCRIPT_DEGRADATION" if complete else "UNKNOWN_INCOMPLETE_TRANSCRIPT",
            "modulus": q, "secret_dimension": n, "reduction_side_secret_mask": mask,
            "records": output, "source_ancestry": ancestry, "sampler_runs": runs,
            "sampler_config": {"max_bits": max_bits, "max_proposals": max_proposals, "block_bits": 8},
            "conditional_bound": bound, "complete_transcript": complete,
            "partial_outputs_can_replace_the_promised_complete_source": False,
            "input_labels_chosen_or_mutated": False, "unknown_secret_input": False,
            "native_unknown_quantum_states_prepared": 0, "hardness_transfer_admitted": False,
            "accepted_speedup_candidate": False}


def unmask(candidate, mask, q):
    root_digits(q)
    candidate, mask = tuple(candidate), tuple(mask)
    if not mask or len(candidate) != len(mask) or any(type(x) is not int or not 0 <= x < q for x in candidate+mask):
        raise ValueError("equal-length canonical candidate and reduction mask required")
    return tuple((x-y) % q for x, y in zip(candidate, mask))


def calibration(n, digits, count, seed):
    q, rng = 3**digits, random.Random(seed)
    secret = tuple(rng.randrange(q) for _ in range(n))
    samples, errors = [], []
    # Calibration law only: chi(-1)=chi(1)=1/4, chi(0)=1/2, V=1/2.
    # This is NOT a Gaussian LWE-hardness source.
    for i in range(2*count):
        label = tuple(rng.randrange(q) for _ in range(n))
        error = (-1, 0, 0, 1)[rng.randrange(4)]
        errors.append(error)
        samples.append(NoisyLinearRecord(label, (sum(a*s for a, s in zip(label, secret))+error) % q,
                                         q, f"noise-degradation-{seed}-source-{i}"))
    converted = convert_pairs(samples, rng, "1/2")
    hidden = tuple((s+t) % q for s, t in zip(secret, converted["reduction_side_secret_mask"]))
    for j, record in enumerate(converted["records"]):
        residual = CovariantRecord(**record).residual(hidden)
        expected = tuple((errors[2*j+k]+converted["sampler_runs"][j]["noise"][k]) % q for k in range(2))
        if residual != expected:
            raise ArithmeticError("public source transform did not preserve the intended noisy equation")
    return {"n": n, "root_digits": digits, "count": count, "seed": seed,
            "calibration_secret": secret, "source_errors_diagnostic": errors,
            "source_records": tuple(s.public() for s in samples), "converted": converted,
            "calibration_distribution_is_LWE_hardness_source": False,
            "underlying_unknown_native_states_simulated_or_prepared": False}


def build_report():
    controls = [calibration(4, r, 16, 128000+r) for r in (2, 4, 16, 80)]
    profiles = [rounded_gaussian_profile(n, 3**r, alpha, M)
                for n, r, alpha, M in ((64, 16, "1/1048576", 512), (64, 64, "1/1048576", 512),
                                       (64, 2, "1/1048576", 512), (64, 16, "1/2", 512))]
    rounding_controls = [round_observation_interval(9, "5/36", "7/36"),
                         round_observation_interval(9, "1/10", "1/9"),
                         round_observation_interval(3**80, 1-fmpq(1, 3**80*65536), 1+fmpq(1, 3**80*65536)),
                         round_observation_interval(3**80, -fmpq(1, 3**80)-fmpq(1, 3**80*65536),
                                                    -fmpq(1, 3**80)+fmpq(1, 3**80*65536))]
    class FixedRNG:
        def __init__(self, pair, coin):
            self.proposals, self.coin = iter(pair), coin

        def randrange(self, q):
            return next(self.proposals)

        def getrandbits(self, bits):
            return self.coin
    failure_controls = [{"modulus": 9, "max_bits": 64, "max_proposals": 1, "block_bits": 8,
                         "result": certified_sample_noise(9, FixedRNG((3, 6), 0), max_proposals=1)},
                        {"modulus": 9, "max_bits": 1, "max_proposals": 1, "block_bits": 8,
                         "result": certified_sample_noise(9, FixedRNG((1, 0), 1), max_bits=1, max_proposals=1)}]
    return {"status": "CONDITIONAL_CLASSICAL_NOISE_DEGRADATION_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "controls": controls, "rounded_Gaussian_source_profiles": profiles,
            "rounding_controls": rounding_controls,
            "sampler_failure_controls": failure_controls,
            "finite_convolution_controls": [{"modulus": q, "chi_zero": "1/2", "chi_plus_minus_one_each": "1/4",
                                             "source_second_moment": "1/2"} for q in (3, 9)],
            "parameter_guards_are_complete_hardness_proof": False,
            "native_quantum_input_bridge_or_efficient_receiver": False,
            "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "source_transform_controls": len(report["controls"]),
                      "complete_transcripts": sum(c["converted"]["complete_transcript"] for c in report["controls"]),
                      "source_profiles": len(report["rounded_Gaussian_source_profiles"]),
                      "hardness_transfer_admitted": False, "quantum_input_bridge": False}, indent=2))


if __name__ == "__main__":
    main()
