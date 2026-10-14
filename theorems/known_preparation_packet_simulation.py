"""Same-original-data simulation of measured native phase compression.

LOCAL DERIVATION / REVIEW PENDING. Explicit classical preparation receipts,
not knowledge recovered from unknown HSP states. Persistent wide coherence
and general quantum circuits are excluded from this restricted primitive API.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import product
import json
from pathlib import Path
import random

from flint import fmpq
import numpy as np

from native_noisy_phase_input import checked_source_bank, native_labels, prepare_inputs
from ternary_certified_noise_sampler import cosine_box
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/KNOWN_PREPARATION_PACKET_SIMULATION.md"
REPORT = ROOT/"research/classical_baselines/known_preparation_packet_simulation.json"
ACCESS = "ORIGINAL_CLASSICAL_RECORDS_AND_PREPARATION_RANDOMNESS"


@dataclass(frozen=True)
class KnownPhasePacket:
    modulus: int
    phase_numerators: tuple[int, ...]
    original_sources: tuple[str, ...]
    access: str = ACCESS

    def __post_init__(self):
        root_digits(self.modulus)
        phases, sources = tuple(self.phase_numerators), tuple(self.original_sources)
        if self.access != ACCESS:
            raise ValueError("original classical preparation access is required; opaque quantum input is not covered")
        if len(phases) not in (2, 3) or any(type(x) is not int or not 0 <= x < self.modulus for x in phases):
            raise ValueError("explicit canonical known phase numerators for a binary/ternary packet required")
        if not sources or len(set(sources)) != len(sources) or any(type(x) is not str or not x for x in sources):
            raise ValueError("distinct paid original classical source IDs required")
        object.__setattr__(self, "phase_numerators", phases)
        object.__setattr__(self, "original_sources", tuple(sorted(sources)))

    def record(self):
        return {"modulus": str(self.modulus), "phase_numerators": tuple(map(str, self.phase_numerators)),
                "original_sources": self.original_sources, "phase_access": self.access}

    def forward_vector(self):
        # Diagnostic only. The certified sampler never uses floating amplitudes.
        return np.array([np.exp(2j*np.pi*float(fmpq(x, self.modulus))) for x in self.phase_numerators])/np.sqrt(len(self.phase_numerators))


def known_source_packets(records, mask):
    records, mask, q, n = checked_source_bank(records, mask)
    packets, receipts = [], []
    for left, right in zip(records[::2], records[1::2]):
        values = tuple((record.value+sum(a*m for a, m in zip(record.label, mask))) % q for record in (left, right))
        packet = KnownPhasePacket(q, (0,)+values, (left.source_id, right.source_id))
        packets.append(packet)
        receipts.append({"raw_source_ids": (left.source_id, right.source_id), "known_phase_values": tuple(map(str, values)),
                         "public_native_ring_label": native_labels(left.label, right.label, q),
                         "packet": packet.record(), "hidden_secret_or_errors_used": False})
    return tuple(packets), {"phase_access": ACCESS, "modulus": str(q), "dimension": n,
                            "original_classical_records": tuple(record.public() for record in records),
                            "preparation_random_mask": mask, "original_record_count": len(records),
                            "known_source_receipts": receipts, "source_error_law_required_for_simulation": False,
                            "source_states_or_hidden_secret_read": False}


def disjoint_sources(packets):
    sources = tuple(x for p in packets for x in p.original_sources)
    if len(set(sources)) != len(sources):
        raise ValueError("a physical source ancestor was reused")
    return tuple(sorted(sources))


def common_index_merge(packets, complement):
    packets, complement = tuple(packets), tuple(complement)
    if not packets or any(len(p.phase_numerators) != 3 for p in packets):
        raise ValueError("nonempty ternary phase block required")
    if len(complement) != len(packets)-1 or any(type(x) is not int or x not in (0, 1, 2) for x in complement):
        raise ValueError("actual measured complement values required")
    sources, q = disjoint_sources(packets), max(p.modulus for p in packets)
    phases = tuple(sum(p.phase_numerators[(t+v) % 3]*(q//p.modulus) for p, v in zip(packets, (0,)+complement)) % q for t in range(3))
    return KnownPhasePacket(q, phases, sources), {"exact_branch_probability_compact": {"base": 3, "exponent": 1-len(packets)},
                                                "complement": complement, "original_sources": sources,
                                                "retained_packets": 1, "unknown_state_inverse_used": False,
                                                "dense_3_to_the_block_size_table_built": False}


def project_binary(packet):
    if len(packet.phase_numerators) != 3:
        raise ValueError("original ternary packet required by this projector")
    return KnownPhasePacket(packet.modulus, packet.phase_numerators[:2], packet.original_sources), fmpq(2, 3)


def binary_merge(left, right, bit):
    if len(left.phase_numerators) != 2 or len(right.phase_numerators) != 2 or type(bit) is not int or bit not in (0, 1):
        raise ValueError("two binary phase packets and an actual measured complement bit required")
    q, sources = max(left.modulus, right.modulus), disjoint_sources((left, right))
    phase = tuple((left.phase_numerators[t]*(q//left.modulus)+right.phase_numerators[t ^ bit]*(q//right.modulus)) % q for t in range(2))
    return KnownPhasePacket(q, phase, sources), fmpq(1, 2)


def known_diagonal(packet, numerators):
    numerators = tuple(numerators)
    if len(numerators) != len(packet.phase_numerators) or any(type(x) is not int for x in numerators):
        raise ValueError("known classical gate numerators of the declared dimension required")
    return KnownPhasePacket(packet.modulus, tuple((a+b) % packet.modulus for a, b in zip(packet.phase_numerators, numerators)), packet.original_sources)


def born_boxes(packet, readout, bits):
    integer(bits, "positive Born enclosure bits", 1)
    q, phases = packet.modulus, packet.phase_numerators
    if readout == "inverse_F3" and len(phases) == 3:
        boxes = []
        for b in range(3):
            cosines = [cosine_box(q, phases[t]-phases[u]-(q//3)*b*(t-u), bits) for t in range(3) for u in range(t)]
            boxes.append((max(fmpq(0), (3+2*sum((a for a, _ in cosines), fmpq(0)))/9),
                          min(fmpq(1), (3+2*sum((z for _, z in cosines), fmpq(0)))/9)))
    elif readout == "anti_trine" and len(phases) == 2:
        boxes = []
        for b in range(3):
            lo, hi = cosine_box(q, phases[1]-phases[0]-(q//3)*b, bits)
            boxes.append(((1-hi)/3, (1-lo)/3))
    else:
        raise ValueError("only specified fixed small-packet readouts are covered")
    if any(not 0 <= lo <= hi <= 1 or hi-lo > fmpq(1, 2**bits) for lo, hi in boxes):
        raise ArithmeticError("Born interval exceeded its declared width")
    return tuple(boxes)


def certified_categorical(box_provider, outcomes, rng, max_bits=64, block_bits=8):
    integer(max_bits, "positive finite sampling precision", 1)
    integer(block_bits, "positive coin block", 1)
    if type(outcomes) is not int or outcomes not in (2, 3):
        raise ValueError("only declared constant-outcome instruments are covered")
    prefix, bits, decisions = 0, 0, []
    result = None
    while bits < max_bits:
        width = min(block_bits, max_bits-bits)
        draw = rng.getrandbits(width)
        if type(draw) is not int or not 0 <= draw < 2**width:
            raise ValueError("canonical independent coin-bit block required")
        prefix, bits = (prefix << width)+draw, bits+width
        boxes = tuple(box_provider(bits))
        if len(boxes) != outcomes or any(not 0 <= lo <= hi <= 1 or hi-lo > fmpq(1, 2**bits) for lo, hi in boxes):
            raise ValueError("certified probability boxes of declared width required")
        if sum((lo for lo, _ in boxes), fmpq(0)) > 1 or sum((hi for _, hi in boxes), fmpq(0)) < 1:
            raise ValueError("probability boxes must cover a normalized instrument")
        cumulative = [(fmpq(0), fmpq(0))]
        for j in range(outcomes-1):
            cumulative.append((sum((lo for lo, _ in boxes[:j+1]), fmpq(0)), sum((hi for _, hi in boxes[:j+1]), fmpq(0))))
        cumulative.append((fmpq(1), fmpq(1)))
        lower, upper = fmpq(prefix, 2**bits), fmpq(prefix+1, 2**bits)
        result = next((j for j in range(outcomes) if lower >= cumulative[j][1] and upper <= cumulative[j+1][0]), None)
        decisions.append({"bits": bits, "coin_prefix": str(prefix), "probability_boxes": tuple((str(lo), str(hi)) for lo, hi in boxes),
                          "outcome": result, "decision": "REFINE" if result is None else "CERTIFIED"})
        if result is not None:
            break
    return {"status": "CERTIFIED_OUTCOME" if result is not None else "EXPLICIT_COIN_PRECISION_ABORT", "outcome": result,
            "decisions": decisions, "max_bits": max_bits, "random_bits_read": bits,
            "unconditional_sampling_error_or_abort_upper": str(min(fmpq(1), fmpq(8, 2**max_bits))),
            "conditional_on_no_abort_is_the_exact_channel": False}


def readout(packet, kind, rng, max_bits=64):
    return certified_categorical(lambda bits: born_boxes(packet, kind, bits), 3, rng, max_bits)


def simulation_budget(max_stochastic_calls, failure_bits=32):
    integer(max_stochastic_calls, "positive adaptive stochastic call cap", 1)
    integer(failure_bits, "positive desired error bits", 1)
    precision = failure_bits+(8*max_stochastic_calls-1).bit_length()
    return {"max_stochastic_calls": str(max_stochastic_calls), "target_failure_bits": failure_bits,
            "per_call_precision_bits": precision,
            "adaptive_unconditional_transcript_error_upper": str(min(fmpq(1), fmpq(8*max_stochastic_calls, 2**precision))),
            "conditioning_away_abort_allowed": False, "private_phase_access": ACCESS,
            "classical_simulation_cost": "polynomial in original records accessed, primitive work, phase/label bit length and log(1/error)",
            "arbitrary_wide_quantum_circuit_covered": False, "unknown_quantum_only_source_covered": False}


def raw_source_fixture(n, digits, count, seed):
    # Secrets/errors exist only in forward tests. The simulator gets raw values.
    q, rng = 3**digits, random.Random(seed)
    secret = tuple(rng.randrange(q) for _ in range(n))
    records = []
    for i in range(2*count):
        label = tuple(rng.randrange(q) for _ in range(n))
        error = (-1, 0, 0, 1)[rng.randrange(4)]
        records.append(NoisyLinearRecord(label, (sum(a*s for a, s in zip(label, secret))+error) % q, q, f"known-phase-{seed}-{i}"))
    mask = tuple(rng.randrange(q) for _ in range(n))
    packets, receipt = known_source_packets(records, mask)
    actual = prepare_inputs(records, mask, "1/2")
    if any(tuple(map(int, row["known_phase_values"])) != recipe["known_phase_values"] for row, recipe in zip(receipt["known_source_receipts"], actual.reduction_side_recipes)):
        raise ArithmeticError("classical receipts differ from the actual preparation code")
    return packets, receipt


def adaptive_law_control():
    packets, source = raw_source_fixture(2, 2, 4, 17002)
    rows = []
    # All paths of a fixed primitive harness, not a candidate/oracle benchmark.
    # Controller settings depend ONLY on public measured v and f.
    for v in range(3):
        pivot, _ = common_index_merge(packets[:2], (v,))
        corrected = known_diagonal(pivot, (0, v*(pivot.modulus//3), v*v*(pivot.modulus//3)))
        f_boxes = born_boxes(corrected, "inverse_F3", 24)
        for f in range(3):
            stem = {"complement": v, "first_F3_outcome": f, "feedback_gate_numerators": (0, v*3, v*v*3)}
            rows.append({**stem, "terminal": "LEFT_PROJECTION_REJECT", "joint_probability_box": tuple(str(x/9) for x in f_boxes[f])})
            rows.append({**stem, "terminal": "RIGHT_PROJECTION_REJECT", "joint_probability_box": tuple(str(2*x/27) for x in f_boxes[f])})
            left, _ = project_binary(packets[2])
            right, _ = project_binary(packets[3])
            for bit in (0, 1):
                child, _ = binary_merge(left, right, bit)
                child = known_diagonal(child, (0, f*(child.modulus//3)))
                boxes = born_boxes(child, "anti_trine", 24)
                for outcome in range(3):
                    lo, hi = f_boxes[f]
                    a, b = boxes[outcome]
                    rows.append({**stem, "terminal": "ANTI_TRINE", "binary_complement": bit, "anti_trine_outcome": outcome,
                                 "retained_packet_before_readout": child.record(), "joint_probability_box": (str(2*lo*a/27), str(2*hi*b/27))})
    return {"source": source, "paths": rows, "complete_paths": 72,
            "lower_total": str(sum(fmpq(r["joint_probability_box"][0]) for r in rows)),
            "upper_total": str(sum(fmpq(r["joint_probability_box"][1]) for r in rows)),
            "public_controller_reads_private_phase_values": False,
            "counterfactual_paths_are_simultaneous_physical_outputs": False}


def adaptive_sample_control(digits, seed):
    packets, source = raw_source_fixture(2, digits, 6, seed)
    rng, budget = random.Random(seed+1), simulation_budget(16, 24)
    precision, transcript = budget["per_call_precision_bits"], []
    complement = []
    for _ in range(2):
        draw = certified_categorical(lambda bits: ((fmpq(1, 3), fmpq(1, 3)),)*3, 3, rng, precision)
        transcript.append({"instrument": "common_index_complement_coordinate", "sampling": draw})
        if draw["outcome"] is None:
            return {"source": source, "budget": budget, "transcript": transcript, "status": "EXPLICIT_SAMPLER_ABORT"}
        complement.append(draw["outcome"])
    complement = tuple(complement)
    pivot, merge = common_index_merge(packets[:3], complement)
    first = readout(pivot, "inverse_F3", rng, precision)
    transcript.append({"instrument": "common_index_then_inverse_F3", "merge": merge, "packet_before_readout": pivot.record(), "sampling": first})
    if first["outcome"] is None:
        return {"source": source, "budget": budget, "transcript": transcript, "status": "EXPLICIT_SAMPLER_ABORT"}
    accepted = []
    for packet in packets[3:]:
        sample = certified_categorical(lambda bits: ((fmpq(2, 3), fmpq(2, 3)), (fmpq(1, 3), fmpq(1, 3))), 2, rng, precision)
        transcript.append({"instrument": "project_basis01", "packet_before_projection": packet.record(), "sampling": sample})
        if sample["outcome"] is None:
            return {"source": source, "budget": budget, "transcript": transcript, "status": "EXPLICIT_SAMPLER_ABORT"}
        if sample["outcome"] == 0:
            accepted.append(project_binary(packet)[0])
    if len(accepted) >= 2:
        draw = certified_categorical(lambda bits: ((fmpq(1, 2), fmpq(1, 2)),)*2, 2, rng, precision)
        transcript.append({"instrument": "CNOT_complement_bit", "sampling": draw})
        if draw["outcome"] is None:
            return {"source": source, "budget": budget, "transcript": transcript, "status": "EXPLICIT_SAMPLER_ABORT"}
        bit = draw["outcome"]
        child, probability = binary_merge(accepted[0], accepted[1], bit)
        child = known_diagonal(child, (0, first["outcome"]*(child.modulus//3)))
        result = readout(child, "anti_trine", rng, precision)
        transcript.append({"instrument": "measured_CNOT_then_feedback_anti_trine", "binary_complement": bit,
                           "complement_probability_exact": str(probability), "packet_before_readout": child.record(), "sampling": result})
    return {"source": source, "budget": budget, "transcript": transcript,
            "status": "EXPLICIT_SAMPLER_ABORT" if any(t["sampling"]["outcome"] is None for t in transcript) else "CERTIFIED_ADAPTIVE_TRANSCRIPT",
            "classical_hidden_secret_used": False, "unknown_quantum_input_simulated": False}


def build_report():
    controls = [adaptive_sample_control(d, 17100+d) for d in (1, 2, 16, 64)]
    return {"status": "SCOPED_SAME_ORIGINAL_DATA_MEASURED_PACKET_SIMULATION_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
                                  for name in ("native_noisy_phase_input.py", "ternary_certified_noise_sampler.py")},
            "complete_adaptive_law_control": adaptive_law_control(), "certified_sample_controls": controls,
            "scaling_contracts": [simulation_budget(T, 32) for T in (16, 2**20, 2**64, 2**128)],
            "original_classical_preparation_access_required": True,
            "specified_measured_compression_family_has_a_classical_simulator": True,
            "unknown_HSP_phase_source_dequantized": False, "arbitrary_known_preparation_quantum_circuits_dequantized": False,
            "persistent_coherent_phase_vectors_covered": False, "physical_hardware_error_certified": False,
            "general_LWE_quantum_algorithms_ruled_out": False, "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    r = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(r), indent=2)+"\n")
    print(json.dumps({"status": r["status"], "complete_adaptive_paths": 72,
                      "certified_transcript_statuses": [c["status"] for c in r["certified_sample_controls"]],
                      "restricted_same_original_data_simulation_constructed": True,
                      "unknown_quantum_only_sources_covered": False, "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()
