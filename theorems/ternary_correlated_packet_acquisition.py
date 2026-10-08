"""Original-native acquisition of correlated carry packets.

LOCAL DERIVATION / REVIEW PENDING. One root step retains K-rank joint
registers, not IID native samples and not a secret decoder.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import native_source
from ternary_carry_packets import compile_packet
from ternary_cyclic_extractor import curvatures, cyclic_output, random_even_source, zero_sum_support
from ternary_phase_depth import NativePhaseHierarchy

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_correlated_packet_acquisition.json"
DERIVATION = ROOT / "research/TERNARY_CORRELATED_PACKET_ACQUISITION.md"


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def word(value, width):
    value = tuple(value)
    if len(value) != width or any(type(x) is not int or x not in (0, 1, 2) for x in value):
        raise ValueError("canonical ternary word of the required width needed")
    return value


def retention_ledger(n, root_digits, odd_inputs):
    integer(n, "secret dimension", 1)
    integer(root_digits, "parent root digits", 2)
    integer(odd_inputs, "odd inputs", n+1)
    return {"dimension": n, "parent_root_digits": root_digits,
            "original_native_input_cap_required": odd_inputs*(n+1)**2,
            "intermediate_odd_inputs": odd_inputs, "outer_rank_upper_bound": n,
            "retained_joint_logical_registers_lower_bound": odd_inputs-n,
            "residual_root_digits": root_digits-1,
            "residual_phase_modulus": str(3**(root_digits-1)),
            "native_additive_degree_upper_bound": 2*root_digits-1,
            "one_root_step_original_supply_polynomial_in_n_and_K": True,
            "full_depth_cost_obtained_by_repeating_this_ledger": False,
            "joint_outputs_are_fresh_native_samples": False,
            "efficient_secret_decoder_supplied": False}


@dataclass(frozen=True)
class PacketAcquisition:
    source: object
    source_ids: tuple
    supports: tuple
    certificates: tuple

    @classmethod
    def from_source(cls, source, odd_inputs, source_ids, input_cap):
        integer(odd_inputs, "odd input count", 1)
        integer(input_cap, "original native input cap", 1)
        if type(source.level) is not int or source.level < 4 or source.level % 2:
            raise ValueError("original even native level >=4 required")
        if not source.labels or not source.labels[0] or any(len(row) != len(source.labels[0]) for row in source.labels):
            raise ValueError("nonempty rectangular original native labels required")
        if odd_inputs <= source.dimension:
            raise ValueError("more odd inputs than secret coordinates required")
        required = odd_inputs*(source.dimension+1)**2
        if required > input_cap or source.inputs != required:
            raise ValueError("exact original source window required within input cap")
        source_ids = tuple(source_ids)
        if (len(source_ids) != required or any(type(x) is not str or not x for x in source_ids)
                or len(set(source_ids)) != required):
            raise ValueError("one distinct nonempty source ID per original input required")
        canonical = native_source(source.labels, source.level)
        if (canonical.labels != source.labels or canonical.frequencies != source.frequencies
                or source.modulus != canonical.modulus):
            raise ValueError("canonical actual native labels and frequencies required")
        window = (source.dimension+1)**2
        vectors = curvatures(source)
        supports, certificates = [], []
        for k in range(odd_inputs):
            offset = k*window
            certificate = zero_sum_support(vectors[offset:offset+window])
            supports.append(tuple(offset+i for i in certificate["support"]))
            certificates.append(certificate)
        return cls(source, source_ids, tuple(supports), tuple(certificates))

    @property
    def active(self):
        return tuple(i for support in self.supports for i in support)

    @property
    def unused(self):
        active = set(self.active)
        return tuple(i for i in range(self.source.inputs) if i not in active)

    @property
    def pointers(self):
        return tuple(i for support in self.supports for i in support[1:])

    def branch(self, pointers, syndrome=None):
        pointers = word(pointers, len(self.pointers))
        anchor = [0]*self.source.inputs
        for i, digit in zip(self.pointers, pointers):
            anchor[i] = digit
        labels = []
        for support in self.supports:
            selected = set(support)
            mask = tuple(int(i in selected) for i in range(self.source.inputs))
            labels.append(cyclic_output(self.source, mask, anchor)["native_odd_output_labels"])
        packet = compile_packet(labels, self.source.level-1, syndrome)
        return AcquiredPacket(self, tuple(anchor), packet)

    def forward(self, original):
        original = word(original, self.source.inputs)
        intermediate = [0]*len(self.supports)
        pointer_map = {}
        for j, support in enumerate(self.supports):
            intermediate[j] = original[support[0]]
            for i in support[1:]:
                pointer_map[i] = (original[i]-intermediate[j]) % 3
        pointers = tuple(pointer_map[i] for i in self.pointers)
        frame = self.branch(pointers).packet
        syndrome = tuple(sum(a*x for a, x in zip(row, intermediate)) % 3 for row in frame.reduced_rows)
        logical = tuple(intermediate[f] for f in frame.free)
        unused = tuple(original[i] for i in self.unused)
        return pointers, syndrome, logical, unused

    def inverse(self, pointers, syndrome, logical, unused):
        return self.branch(pointers, syndrome).lift(logical, unused)

    def source_record(self):
        return {"original_even_level": self.source.level,
                "dimension": self.source.dimension, "parent_modulus": str(self.source.modulus),
                "acquired_original_native_inputs": self.source.inputs,
                "odd_inputs_acquired": len(self.supports), "active_original_inputs": len(self.active),
                "untouched_original_inputs": len(self.unused),
                "original_source_ids": self.source_ids,
                "active_original_source_ids": tuple(self.source_ids[i] for i in self.active),
                "untouched_original_source_ids": tuple(self.source_ids[i] for i in self.unused),
                "odd_input_original_ancestors": tuple(tuple(self.source_ids[i] for i in s) for s in self.supports),
                "fixed_disjoint_curvature_only_windows": True,
                "distinct_ids_certify_physical_independence": False,
                "IID_odd_label_law_premise": "IID original full frequency pairs; independent parents; curvature-only support selection",
                "IID_odd_label_law_status": "LOCAL_DERIVATION_REVIEW_PENDING",
                "untouched_curvature_labels_claimed_fresh_IID": False,
                "intermediate_odd_input_acquisition_charged": True,
                "upstream_DCP_or_LWE_input_acquisition_implemented_here": False,
                "upstream_conversion_cap_and_joint_error_obligations_remain": True,
                "unknown_preparation_inverse_or_amplification_used": False}


@dataclass(frozen=True)
class AcquiredPacket:
    acquisition: PacketAcquisition
    anchor: tuple
    packet: object

    def lift(self, logical, unused=None):
        physical = self.packet.assignment(word(logical, self.packet.retained))
        unused = (0,)*len(self.acquisition.unused) if unused is None else word(unused, len(self.acquisition.unused))
        original = list(self.anchor)
        for support, digit in zip(self.acquisition.supports, physical):
            for i in support:
                original[i] = (original[i]+digit) % 3
        for i, digit in zip(self.acquisition.unused, unused):
            original[i] = digit
        return tuple(original)

    def original_residual(self, logical, unused=None):
        source = self.acquisition.source
        actual = source.value(self.lift(logical, unused))
        base = source.value(self.lift((0,)*self.packet.retained, unused))
        difference = tuple((a-b) % source.modulus for a, b in zip(actual, base))
        if any(x % 3 for x in difference):
            raise ArithmeticError("true original phase is not divisible by three")
        return tuple(x//3 for x in difference)

    def resources(self):
        acquisition, packet = self.acquisition, self.packet
        exponent = len(acquisition.pointers)+len(packet.pivots)
        return {**acquisition.source_record(), "odd_level": packet.level,
                "measured_inner_pointer_qutrits": len(acquisition.pointers),
                "measured_outer_syndrome_qutrits": len(packet.pivots),
                "retained_joint_logical_qutrits": packet.retained,
                "minimum_retained_joint_logical_qutrits": len(acquisition.supports)-acquisition.source.dimension,
                "inner_SUM_inverse_gates": len(acquisition.pointers),
                "outer_SUM_gates": packet.resource_record()["SUM_gates"],
                "Gaussian_support_kernel_calls": sum(c["Gaussian_kernel_calls"] for c in acquisition.certificates),
                "raw_joint_branch_probability": str(Fraction(1, 3**exponent)),
                "raw_joint_branch_probability_exponent_base_three": exponent,
                "retained_phase_modulus": str(packet.phase_modulus//3),
                "retained_additive_degree_upper_bound": packet.level,
                "all_pointer_and_syndrome_outcomes_accepted": True,
                "outputs_certified_as_IID_native_samples": False,
                "matched_packet_copies_or_unknown_weighted_phase_oracle_supplied": False,
                "unused_original_registers_measured_or_discarded": False,
                "highest_parent_secret_digit_retained_in_packet_payload": False,
                "highest_parent_secret_digit_lost_from_untouched_original_registers": False,
                "global_branch_phase_dropped_only_after_both_measurements": True,
                "hardware_synthesis_and_aggregate_error_certificate_supplied": False,
                "efficient_decoder_or_full_depth_speedup_supplied": False}


def physical_control(acquisition, secret):
    """Replay the COMPLETE active subsystem; untouched factors are not enumerated."""
    active, source = acquisition.active, acquisition.source
    if len(active) > 9:
        raise ValueError("complete active-subsystem replay capped at nine qutrits")
    secret = tuple(secret)
    if len(secret) != source.dimension or any(type(s) is not int for s in secret):
        raise ValueError("one integer calibration secret per coordinate required")
    # First replay actual SUM permutations, grouping only by measured inner pointers.
    inner = {}
    scale = 3**(-len(active)/2)
    for digits in product(range(3), repeat=len(active)):
        original = [0]*source.inputs
        for i, digit in zip(active, digits):
            original[i] = digit
        pointers, intermediate = [], []
        for support in acquisition.supports:
            pivot = original[support[0]]
            intermediate.append(pivot)
            pointers.extend((original[i]-pivot) % 3 for i in support[1:])
        theta = sum(a*s for a, s in zip(source.value(original), secret)) % source.modulus
        key = tuple(pointers), tuple(intermediate)
        if key in inner:
            raise ArithmeticError("inner SUM map is not injective")
        inner[key] = scale*np.exp(2j*math.pi*theta/source.modulus)
    records, max_error, norm, min_purity = [], 0., 0., 1.
    for pointers in product(range(3), repeat=len(acquisition.pointers)):
        frame = acquisition.branch(pointers).packet
        outer = {}
        for physical in product(range(3), repeat=frame.consumed):
            syndrome = tuple(sum(a*x for a, x in zip(row, physical)) % 3 for row in frame.reduced_rows)
            logical = tuple(physical[f] for f in frame.free)
            key = syndrome, logical
            if key in outer:
                raise ArithmeticError("outer Gaussian SUM map is not injective")
            outer[key] = inner[pointers, physical]
        for syndrome in product(range(3), repeat=len(frame.pivots)):
            branch = acquisition.branch(pointers, syndrome)
            packet = branch.packet
            hierarchy = NativePhaseHierarchy.from_packet(packet)
            base = source.value(branch.lift((0,)*packet.retained))
            values, frequencies = [], []
            for logical in product(range(3), repeat=packet.retained):
                residual = branch.original_residual(logical)
                if residual != packet.residual(logical) or residual != hierarchy.derivative(logical, ()):
                    raise ArithmeticError("packet hierarchy disagrees with original root phases")
                theta = (sum(a*s for a, s in zip(base, secret))+3*sum(a*s for a, s in zip(residual, secret))) % source.modulus
                expected = scale*np.exp(2j*math.pi*theta/source.modulus)
                actual = outer[syndrome, logical]
                max_error = max(max_error, float(abs(actual-expected)))
                values.append(actual)
                frequencies.append(residual)
            probability = float(sum(abs(x)**2 for x in values))
            exact = Fraction(branch.resources()["raw_joint_branch_probability"])
            if abs(probability-float(exact)) > 4e-12:
                raise ArithmeticError("branch probability did not charge all measured wires")
            normalized = np.asarray(values)/math.sqrt(probability)
            if packet.retained > 1:
                flat = normalized.reshape(3, -1)
                reduced = flat @ flat.conj().T
                purity = float(np.trace(reduced @ reduced).real)
            else:
                purity = 1.
            min_purity = min(min_purity, purity)
            norm += probability
            records.append({"pointers": pointers, "syndrome": syndrome,
                            "odd_native_labels": packet.labels, "RREF_rows": packet.reduced_rows,
                            "pivots": packet.pivots, "free": packet.free,
                            "base_original_frequency": base, "logical_residual_frequencies": frequencies,
                            "raw_branch_probability": str(exact), "measured_probability": probability,
                            "first_logical_register_purity": purity,
                            "unnormalized_active_amplitudes": [[float(x.real), float(x.imag)] for x in values],
                            "resources": branch.resources()})
    if max_error > 4e-12 or abs(norm-1.) > 4e-12:
        raise ArithmeticError("complete original instrument replay failed")
    return {"original_labels": source.labels, "original_frequencies": source.frequencies,
            "source": acquisition.source_record(), "supports": acquisition.supports,
            "support_certificates": acquisition.certificates, "calibration_secret": secret,
            "complete_active_words_replayed": 3**len(active), "untouched_word_cube_enumerated": False,
            "all_measurement_branches": records, "total_raw_probability": norm,
            "maximum_amplitude_error": max_error, "minimum_first_register_purity": min_purity,
            "entangled_calibration_is_population_or_speedup_evidence": False}


def public_control(n, level, odd_inputs, seed):
    count = odd_inputs*(n+1)**2
    source = random_even_source(n, level, count, seed)
    acquisition = PacketAcquisition.from_source(source, odd_inputs, tuple(f"native-{seed}-{i}" for i in range(count)), count)
    pointers = tuple((i+seed) % 3 for i in range(len(acquisition.pointers)))
    frame = acquisition.branch(pointers).packet
    syndrome = tuple((i+1) % 3 for i in range(len(frame.pivots)))
    branch = acquisition.branch(pointers, syndrome)
    hierarchy = NativePhaseHierarchy.from_packet(branch.packet)
    if 3**branch.packet.retained > 2187:
        raise ValueError("bounded public table control capped at 2187 logical words")
    points = tuple(product(range(3), repeat=branch.packet.retained))
    unused = (2,)*len(acquisition.unused)
    residuals = []
    for logical in points:
        value = branch.original_residual(logical)
        if value != hierarchy.derivative(logical, ()) or value != branch.original_residual(logical, unused):
            raise ArithmeticError("original-root or untouched-factor identity failed")
        original = branch.lift(logical, unused)
        if acquisition.inverse(*acquisition.forward(original)) != original:
            raise ArithmeticError("two-stage basis permutation failed round trip")
        residuals.append(value)
    return {"seed": seed, "original_labels": source.labels, "original_frequencies": source.frequencies,
            "supports": acquisition.supports, "pointers": pointers, "syndrome": syndrome,
            "odd_native_labels": branch.packet.labels, "RREF_rows": branch.packet.reduced_rows,
            "pivots": branch.packet.pivots, "free": branch.packet.free,
            "resources": branch.resources(), "logical_residual_frequencies": residuals,
            "whole_original_word_cube_enumerated": False, "bounded_logical_words_checked": len(points)}


def run_controls():
    # Pinned, selected calibration: bounded active replay and non-product output.
    seed, n, level, K = 88401, 1, 6, 4
    count = K*(n+1)**2
    source = random_even_source(n, level, count, seed)
    acquisition = PacketAcquisition.from_source(source, K, tuple(f"native-{seed}-{i}" for i in range(count)), count)
    dense = physical_control(acquisition, (1,))
    return {"status": "ORIGINAL_SOURCE_CORRELATED_PACKET_ACQUISITION_EXACT_DECODER_OPEN_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dense_original_instrument_control": dense,
            "dense_seed_selection_is_population_evidence": False,
            "public_original_root_controls": [public_control(2, 6, 5, 88402), public_control(3, 8, 7, 88403)],
            "analytic_retention_ledgers": [retention_ledger(n, r, 2*n) for n, r in ((2, 3), (8, 5), (32, 7), (128, 9))],
            "candidate_record_accepted": False, "novel_algorithm_or_quantum_speedup_claimed": False,
            "closed_debt": "Intermediate odd inputs acquired from charged original even native inputs with all outcome branches retained.",
            "remaining_blockers": ["Polynomial-time decoder for the correlated growing-depth phase payload.",
                                   "Costed useful multi-depth instrument, not assuming IID logical outputs.",
                                   "Upstream bounded supply and joint error guarantees; native gate/error compilation.",
                                   "External proof review and novelty check."],
            "routine_CLI_registry_and_Git_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "active_words": report["dense_original_instrument_control"]["complete_active_words_replayed"],
                      "maximum_amplitude_error": report["dense_original_instrument_control"]["maximum_amplitude_error"]}, indent=2))


if __name__ == "__main__":
    main()
