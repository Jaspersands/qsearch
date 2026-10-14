"""Source-preserving native phase descent with an honest recursive decoder.

All receiver gates depend on supplied labels, measurement records and learned
prefixes. True secrets appear only in forward input fixtures. Fixed depth is
a calibration regime, not a new quantum speedup or a growing-depth solver.
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

from flint import fmpq
import numpy as np

from cyclotomic_rescaling_gate import divide_pi, ideal_chart, multiply, pairing, plus, reduce_element, residue
from native_state_hsp_bridge import NativeGroup, ring_words
from nil3_state_hsp_descent_receiver import SuppliedPhaseSample, phase_exponents, solve_full_rank_f3
from ternary_cyclic_extractor import cyclic_recipe
from vector_centre_state_hsp_receiver import ZeroSumBuffer
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_UNIFORM_DESCENT_RECEIVER.md"
REPORT = ROOT/"research/reductions/native_uniform_descent_receiver.json"


class SourceExhausted(RuntimeError):
    pass


@dataclass(frozen=True)
class Packet:
    sample: SuppliedPhaseSample
    original_indices: tuple[int, ...]


def merge_branch(samples, outcomes):
    samples, outcomes = tuple(samples), tuple(outcomes)
    if not samples:
        raise ValueError("nonempty supplied native block required")
    L, n = samples[0].level, len(samples[0].label)
    if L < 2 or any(s.level != L or len(s.label) != n for s in samples):
        raise ValueError("one parent level at least2 and vector dimension required")
    if len(outcomes) != len(samples)-1 or any(type(v) is not int or v not in (0, 1, 2) for v in outcomes):
        raise ValueError("every measured complement coordinate is required")
    if any(sum(residue(s.label[j]) for s in samples) % 3 for j in range(n)):
        raise ValueError("public residue sum is nonzero; same-source descent is invalid")
    offsets = (0,)+outcomes
    G = NativeGroup(L, n)
    combined = [(0, 0)]*n
    for sample, v in zip(samples, offsets):
        for j, a in enumerate(G.rotate(sample.label, v)):
            combined[j] = plus(combined[j], a, L)
    child = tuple(divide_pi(a, L) for a in combined)
    amplitude, log_scale = np.ones(3, complex), 0.
    for sample, v in zip(samples, offsets):
        amplitude *= np.array([sample.state[(t+v) % 3] for t in range(3)])
        scale = float(max(abs(amplitude)))
        if scale == 0:
            raise ValueError("zero-probability branch cannot be conditioned into a sample")
        amplitude /= scale
        log_scale += math.log(scale)
    norm = float(np.vdot(amplitude, amplitude).real)
    probability = math.exp(2*log_scale)*norm
    return SuppliedPhaseSample(child, amplitude/math.sqrt(norm), L-1), {
        "parent_level": L, "child_level": L-1, "public_input_labels": tuple(s.label for s in samples),
        "measured_complement": outcomes, "combined_label_before_division": tuple(combined),
        "child_label": child, "branch_probability_diagnostic": probability,
        "retained_amplitudes": [(float(z.real), float(z.imag)) for z in amplitude/math.sqrt(norm)],
        "ideal_branch_probability": {"base": 3, "exponent": 1-len(samples)},
        "quantum_recipe": cyclic_recipe((1,)*len(samples)),
        "secret_used_by_merge": False, "coherent_pointer_transfer_claimed": False}


def sampled_merge(samples, rng):
    samples = tuple(samples)
    # Sampling latent computational digits gives the exact complement marginal
    # in this pure-state simulator. The quantum recipe never measures the pivot.
    digits = [int(rng.choice(3, p=abs(s.state)**2)) for s in samples]
    outcomes = tuple((v-digits[0]) % 3 for v in digits[1:])
    return merge_branch(samples, outcomes)


class OriginalSource:
    """Finite supplied inputs only. This object has no hidden-secret member."""

    def __init__(self, inputs, level, dimension, copy_cap, retain_trace=False):
        NativeGroup(level, dimension)
        integer(copy_cap, "finite original copy cap", 1)
        if type(retain_trace) is not bool:
            raise ValueError("Boolean finite replay retention required")
        self.inputs, self.level, self.dimension, self.cap = iter(inputs), level, dimension, copy_cap
        self.count = 0
        self.retain_trace, self.input_records = retain_trace, []

    def take(self):
        if self.count >= self.cap:
            raise SourceExhausted("original copy budget exhausted")
        try:
            sample = next(self.inputs)
        except StopIteration as error:
            raise SourceExhausted("finite supplied source exhausted") from error
        if not isinstance(sample, SuppliedPhaseSample) or sample.level != self.level or len(sample.label) != self.dimension:
            raise ValueError("source returned a wrong-level or wrong-dimension input")
        packet = Packet(sample, (self.count,))
        if self.retain_trace:
            self.input_records.append({"original_index": self.count, "public_label": sample.label,
                                       "supplied_amplitudes": [(float(z.real), float(z.imag)) for z in sample.state]})
        self.count += 1
        return packet


class DescentSource:
    def __init__(self, parent, rng):
        if parent.level < 2:
            raise ValueError("parent source must have a positive lower level")
        self.parent, self.rng = parent, rng
        self.level, self.dimension = parent.level-1, parent.dimension
        self.live, self.ready, self.claimed = {}, deque(), set()
        self.emitted = self.SUM_gates = self.measurements = 0
        self.first_records = []
        self.retain_trace, self.output_records = parent.retain_trace, []
        self.digest = hashlib.sha256()
        self.selector = ZeroSumBuffer(self.dimension, self._consume)

    def _consume(self, block):
        packets = [self.live.pop(i) for i in block["original_indices"]]
        if any(tuple(map(residue, p.sample.label)) != lam for p, lam in zip(packets, block["central_characters"])):
            raise ArithmeticError("selector metadata does not match actual supplied inputs")
        child, record = sampled_merge([p.sample for p in packets], self.rng)
        original = tuple(sorted(i for p in packets for i in p.original_indices))
        if len(set(original)) != len(original):
            raise ValueError("an original unknown register was reused")
        self.ready.append(Packet(child, original))
        self.emitted += 1
        self.SUM_gates += len(packets)-1
        self.measurements += len(packets)-1
        record["original_source_indices"] = original
        record["input_original_lineages"] = tuple(p.original_indices for p in packets)
        self.digest.update((json.dumps(exact_json(record), sort_keys=True)+"\n").encode())
        if len(self.first_records) < 8:
            self.first_records.append(record)
        if self.retain_trace:
            self.output_records.append(record)

    def take(self):
        while not self.ready:
            packet = self.parent.take()
            if self.claimed.intersection(packet.original_indices):
                raise ValueError("source supplied overlapping physical lineages")
            self.claimed.update(packet.original_indices)
            index = self.selector.inputs
            self.live[index] = packet
            # ONLY coarse residues choose supports. No state or higher label
            # digit is inspected by this selection policy.
            self.selector.push(tuple(map(residue, packet.sample.label)))
        return self.ready.popleft()

    def record(self):
        coverage = self.selector.finish()
        if set(self.live) != set(coverage["leftover_original_indices"]):
            raise ArithmeticError("unconsumed registers vanished from the source ledger")
        return {"parent_level": self.parent.level, "child_level": self.level,
                "coverage": coverage, "outputs_emitted": self.emitted,
                "known_SUM_gates": self.SUM_gates, "complement_measurements": self.measurements,
                "first_output_records": self.first_records, "all_output_records_sha256": self.digest.hexdigest(),
                "complete_output_records": self.output_records if self.retain_trace else None,
                "selection_uses_only_coarse_residues": True,
                "higher_label_or_secret_filtering_used": False,
                "child_state_prepared_from_secret": False}


def centre_element(level):
    out = reduce_element((1, 0), level)
    for _ in range(level-1):
        out = multiply(out, (-1, 1), level)
    return out


def digit_measurement(sample, learned_lower, rng):
    L, n = sample.level, len(sample.label)
    if L == 1:
        if learned_lower is not None:
            raise ValueError("level1 has no supplied lower secret")
        lower = ((0, 0),)*n
    else:
        if learned_lower is None or len(learned_lower) != n or any(reduce_element(v, L-1) != tuple(v) for v in learned_lower):
            raise ValueError("actually learned canonical lower prefix required")
        lower = tuple(reduce_element(v, L) for v in learned_lower)
    exponents = phase_exponents(sample.label, lower, L)
    q = 3**((L+1)//2)
    corrected = sample.state*np.exp(-2j*np.pi*np.array([float(Fraction(e, q)) for e in exponents]))
    points = np.arange(3)
    output = np.exp(-2j*np.pi*np.outer(points, points)/3)@corrected/math.sqrt(3)
    probabilities = abs(output)**2
    probabilities /= probabilities.sum()
    outcome = int(rng.choice(3, p=probabilities))
    row = []
    for a in sample.label:
        f = 3*pairing(a, centre_element(L), L)
        if f.denominator != 1:
            raise ArithmeticError("top ideal must have order3")
        row.append(int(f) % 3)
    return tuple(row), outcome


def resource_contract(dimension, level, overhead=8):
    integer(dimension, "positive dimension", 1)
    integer(level, "positive native level", 1)
    integer(overhead, "positive independent-row overhead", 1)
    NativeGroup(level, dimension)
    W, K = (dimension+1)**2, dimension+overhead
    cap = K*sum(W**j for j in range(level))
    error = min(fmpq(1), level*fmpq(3**dimension-1, 2*3**K))
    return {"dimension": dimension, "level": level, "coarse_window": W,
            "fresh_digit_samples_per_level": K, "original_copy_upper": str(cap),
            "ideal_IID_rank_failure_upper": str(error),
            "copy_model": "K*(1+W+...+W^(level-1)) for this measured descent",
            "every_fixed_level_is_polynomial": True, "universal_copy_lower_bound": False,
            "hardware_or_noise_error_included": False,
            "unknown_quantum_buffer_upper": (level-1)*W+level,
            "source_law_requires_coarse_only_selection": True}


def receive(source, rng, overhead=8):
    n, L = source.dimension, source.level
    contract = resource_contract(n, L, overhead)
    streams, stages, consumed_final = [], [], []

    def descend(current):
        current_level = current.level
        lower = None
        if current_level > 1:
            child = DescentSource(current, rng)
            streams.append(child)
            lower = descend(child)
            if lower is None:
                return None
        rows, rhs, packet_ids, labels = [], [], [], []
        for _ in range(contract["fresh_digit_samples_per_level"]):
            packet = current.take()
            consumed_final.extend(packet.original_indices)
            row, measured = digit_measurement(packet.sample, lower, rng)
            rows.append(row)
            rhs.append(measured)
            packet_ids.append(packet.original_indices)
            labels.append(packet.sample.label)
        digits = solve_full_rank_f3(rows, rhs, n)
        stages.append({"level": current_level, "learned_lower": lower, "public_rows": rows,
                       "measured_outcomes": rhs, "recovered_top_digits": digits,
                       "digit_measurement_original_lineages": packet_ids,
                       "public_input_labels": labels,
                       "unknown_secret_used_by_stage": False})
        if digits is None:
            return None
        lower = ((0, 0),)*n if lower is None else tuple(reduce_element(v, current_level) for v in lower)
        return tuple(plus(v, multiply(centre_element(current_level), (u, 0), current_level), current_level) for v, u in zip(lower, digits))

    exhausted = None
    try:
        answer = descend(source)
    except SourceExhausted as error:
        answer, exhausted = None, str(error)
    if len(set(consumed_final)) != len(consumed_final):
        raise ArithmeticError("final measurements reused an original physical lineage")
    ledgers = [s.record() for s in streams]
    leftovers = sorted(i for s in streams for p in s.live.values() for i in p.original_indices)
    if len(set(leftovers)) != len(leftovers) or set(leftovers).intersection(consumed_final):
        raise ArithmeticError("leftover and consumed lineages overlap")
    if set(leftovers).union(consumed_final) != set(range(source.count)):
        raise ArithmeticError("some supplied original copies have no accounted final fate")
    return {"status": "IDEAL_NATIVE_REFERENCE_SECRET_DECODED" if answer is not None else "NO_RECOVERY_FROM_FINITE_SUPPLIED_SOURCE",
            "recovered_native_secret": answer, "resource_contract": contract,
            "original_inputs_supplied": source.count, "completed_digit_stages": stages,
            "descent_streams": ledgers, "measured_original_lineages": sorted(consumed_final),
            "unconsumed_original_lineages": leftovers, "source_exhaustion": exhausted,
            "complete_original_input_records": source.input_records if source.retain_trace else None,
            "receiver_takes_hidden_secret": False, "quantum_hardware_executed": False,
            "general_StateHSP_receiver_supplied": False, "new_quantum_speedup_established": False}


def forward_fixture(level, secret, seed):
    """Forward input preparation for tests ONLY, never used by receive."""
    G = NativeGroup(level, len(secret))
    import random
    rng = random.Random(seed)
    h0, _, h1 = ideal_chart(level)[0]
    while True:
        label = tuple((rng.randrange(h0), rng.randrange(h1)) for _ in secret)
        yield SuppliedPhaseSample(label, G.supplied_phase_state(label, secret), level)


def receiver_control(dimension, level, seed):
    G = NativeGroup(level, dimension)
    h0, _, h1 = ideal_chart(level)[0]
    rng = np.random.default_rng(seed)
    truth = tuple((int(rng.integers(0, h0)), int(rng.integers(0, h1))) for _ in range(dimension))
    plan = resource_contract(dimension, level)
    source = OriginalSource(forward_fixture(level, truth, seed+1), level, dimension, int(plan["original_copy_upper"]), retain_trace=True)
    result = receive(source, np.random.default_rng(seed+2))
    if result["recovered_native_secret"] != G.vector(truth):
        raise ArithmeticError("committed source-driven native calibration failed")
    return {"dimension": dimension, "level": level, "truth_fixture_only": truth, "result": result}


def uniform_label_census():
    records = []
    for L in (2, 3):
        labels = ring_words(L)
        left = [a for a in labels if residue(a) == 1]
        right = [a for a in labels if residue(a) == 2]
        for outcome in range(3):
            counts = {b: 0 for b in ring_words(L-1)}
            for a, b in product(left, right):
                rotated = NativeGroup(L).rotate((b,), outcome)[0]
                child = divide_pi(plus(a, rotated, L), L)
                counts[child] += 1
            if len(set(counts.values())) != 1:
                raise ArithmeticError("coarse-only conditional label law is not uniform")
            records.append({"parent_level": L, "conditioned_residues": (1, 2),
                            "complement_outcome": outcome,
                            "child_label_counts": [{"label": b, "count": c} for b, c in counts.items()]})
    return records


def build_report():
    controls = [receiver_control(n, L, 12000+100*n+L) for n, L in ((1, 2), (1, 3), (2, 3), (4, 3), (1, 4))]
    return {"status": "NATIVE_SOURCE_PRESERVING_DESCENT_AND_REFERENCE_RECOVERY_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "source_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
                              for name in ("native_uniform_descent_receiver.py", "nil3_state_hsp_descent_receiver.py",
                                           "native_state_hsp_bridge.py", "cyclotomic_rescaling_gate.py",
                                           "ternary_cyclic_extractor.py", "vector_centre_state_hsp_receiver.py")},
            "conditional_uniform_label_censuses": uniform_label_census(), "source_driven_receiver_controls": controls,
            "scaling_contracts": [resource_contract(n, L) for n in (8, 32, 128) for L in (2, 3, 4, n)],
            "full_source_and_noise_promises_proved_from_data": False,
            "quantum_hardware_executed": False, "novelty_verified": False,
            "polynomial_growing_depth_receiver_supplied": False, "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    r = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(r), indent=2)+"\n")
    print(json.dumps({"status": r["status"], "source_driven_recoveries": len(r["source_driven_receiver_controls"]),
                      "uniform_label_censuses": 6, "original_copy_counts": [c["result"]["original_inputs_supplied"] for c in r["source_driven_receiver_controls"]],
                      "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()
