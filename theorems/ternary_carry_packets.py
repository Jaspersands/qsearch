"""Native odd-level cyclotomic kernel packets, not IID phase-state outputs.

LOCAL DERIVATION / REVIEW PENDING. L3 gives classical cubic phases;
higher odd levels retain deeper phases and do not get a fixed-degree decoder.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import nmod_mat
import numpy as np

from cyclotomic_rescaling_gate import _lambda, ideal_chart, multiply, pairing, reduce_element, residue

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_carry_packets.json"


@dataclass(frozen=True)
class TernaryPacket:
    labels: tuple
    level: int
    pivots: tuple
    free: tuple
    reduced_rows: tuple
    syndrome: tuple

    @property
    def phase_modulus(self):
        return 3**((self.level+1)//2)

    @property
    def retained(self):
        return len(self.free)

    @property
    def consumed(self):
        return len(self.labels)

    @property
    def secret_dimension(self):
        return len(self.labels[0])

    def assignment(self, z):
        if len(z) != self.retained or any(type(x) is not int or not 0 <= x < 3 for x in z):
            raise ValueError("canonical retained ternary assignment required")
        physical = [0]*self.consumed
        for j, f in enumerate(self.free):
            physical[f] = z[j]
        for row, pivot, y in zip(self.reduced_rows, self.pivots, self.syndrome):
            physical[pivot] = (y-sum(row[f]*physical[f] for f in self.free)) % 3
        return tuple(physical)

    def component_frequencies(self, physical):
        if len(physical) != self.consumed or any(type(j) is not int or not 0 <= j < 3 for j in physical):
            raise ValueError("one canonical input digit per native qutrit required")
        q = self.phase_modulus
        out = []
        for l in range(self.secret_dimension):
            value = sum(pairing((1, 0), multiply(row[l], _lambda(j, self.level), self.level), self.level)
                        for row, j in zip(self.labels, physical))*q
            if value.denominator != 1:
                raise AssertionError("integer-secret phase frequency is not integral")
            out.append(int(value) % q)
        return tuple(out)

    def residual(self, z):
        base = self.component_frequencies(self.assignment((0,)*self.retained))
        actual = self.component_frequencies(self.assignment(z))
        difference = tuple((a-b) % self.phase_modulus for a, b in zip(actual, base))
        if any(x % 3 for x in difference):
            raise AssertionError("public kernel failed actual phase divisibility")
        return tuple(x//3 for x in difference)

    def resource_record(self):
        return {"parent_level": self.level, "input_native_qutrits": self.consumed,
                "measured_qutrits": len(self.pivots), "retained_joint_qutrits": self.retained,
                "SUM_gates": sum(bool(row[f]) for row in self.reduced_rows for f in self.free),
                "uniform_syndrome_probability_denominator": 3**len(self.pivots),
                "parent_integer_secret_modulus": self.phase_modulus,
                "retained_phase_modulus": self.phase_modulus//3,
                "higher_secret_digit_retained_in_this_output": False,
                "acquiring_intermediate_odd_level_inputs_charged_here": False,
                "outputs_certified_as_IID_PSP_samples": False,
                "all_syndromes_kept": True, "unknown_preparation_or_inverse_used": False}


def compile_packet(labels, level=3, syndrome=None):
    ideal_chart(level)
    if level < 3 or level % 2 == 0:
        raise ValueError("odd parent level>=3 required for this integer-secret frequency chart")
    if not labels or not labels[0] or any(len(row) != len(labels[0]) for row in labels):
        raise ValueError("nonempty rectangular native label vectors required")
    labels = tuple(tuple(reduce_element(y, level) for y in row) for row in labels)
    m, n = len(labels), len(labels[0])
    matrix = nmod_mat([[residue(labels[j][l]) for j in range(m)] for l in range(n)], 3)
    rref, rank = matrix.rref()
    rows = tuple(tuple(int(rref[i, j]) for j in range(m)) for i in range(rank))
    pivots = tuple(next(j for j, v in enumerate(row) if v) for row in rows)
    free = tuple(j for j in range(m) if j not in pivots)
    syndrome = (0,)*rank if syndrome is None else tuple(syndrome)
    if len(syndrome) != rank or any(type(y) is not int or not 0 <= y < 3 for y in syndrome):
        raise ValueError("one canonical syndrome digit per independent row required")
    return TernaryPacket(labels, level, pivots, free, rows, syndrome)


def _interpolate(tables, retained):
    if retained > 6:
        raise ValueError("dense interpolation is calibration only; retain<=6")
    points = list(product(range(3), repeat=retained))
    inv = nmod_mat([[1, x, x*x % 3] for x in range(3)], 3).inv()
    inverse = np.array([[int(inv[i, j]) for j in range(3)] for i in range(3)])
    components = []
    for l in range(len(tables[0])):
        c = np.array([row[l] for row in tables], dtype=np.int64).reshape((3,)*retained)
        for axis in range(retained):
            c = np.moveaxis(c, axis, 0)
            shape = c.shape
            c = (inverse @ c.reshape(3, -1) % 3).reshape(shape)
            c = np.moveaxis(c, 0, axis)
        coefficients = [{"powers": list(e), "coefficient": int(c[e])} for e in points if int(c[e])]
        degree = max((sum(x["powers"]) for x in coefficients), default=0)
        components.append({"component": l, "degree": degree, "coefficients": coefficients})
    return components


def classical_polynomial(packet):
    if packet.level != 3:
        raise ValueError("classical F3 cubic expansion only established at parent level3")
    if packet.retained > 6:
        raise ValueError("dense interpolation is calibration only; retain<=6")
    points = list(product(range(3), repeat=packet.retained))
    components = _interpolate([packet.residual(z) for z in points], packet.retained)
    assert all(c["degree"] <= 3 for c in components)
    return {"field": 3, "maximum_total_degree": max(c["degree"] for c in components),
            "component_polynomials": components,
            "quadratic_stabilizer_learning_automatically_applies": False,
            "identical_unknown_packet_copies_supplied": False}


def cubic_signature(packet):
    return tuple(tuple((tuple(c["powers"]), c["coefficient"])
                       for c in row["coefficients"] if sum(c["powers"]) == 3)
                 for row in classical_polynomial(packet)["component_polynomials"])


def matched_cubic_sum(packets, shifts):
    if len(packets) != 3 or len(shifts) != 3:
        raise ValueError("three supplied packets and shifts required; no cloning")
    first = packets[0]
    if any(p.level != 3 or p.retained != first.retained or p.secret_dimension != first.secret_dimension for p in packets):
        raise ValueError("same level3 retained width and secret coordinates required")
    for p, shift in zip(packets, shifts):
        p.assignment(shift)
    if any(cubic_signature(p) != cubic_signature(first) for p in packets[1:]):
        raise ValueError("public leading cubic tensors mismatch; degree cancellation not admitted")
    tables = []
    for z in product(range(3), repeat=first.retained):
        values = [p.residual(tuple((x+y) % 3 for x, y in zip(z, shift))) for p, shift in zip(packets, shifts)]
        tables.append(tuple(sum(row[l] for row in values) % 3 for l in range(first.secret_dimension)))
    components = _interpolate(tables, first.retained)
    assert all(c["degree"] <= 2 for c in components)
    return {"conditional_sum_degree": max(c["degree"] for c in components),
            "component_polynomials": components, "public_frequency_table": [list(row) for row in tables],
            "required_independent_input_packet_count": 3,
            "physical_source_lineage_programmatically_verified": False, "native_source_matching_supplied": False,
            "quadratic_state_is_a_secret_decoder": False}


def physical_control(labels, secret, level):
    packet = compile_packet(labels, level)
    if packet.consumed > 7 or packet.retained > 5:
        raise ValueError("dense physical replay is bounded calibration, not scalable decoder")
    if len(secret) != packet.secret_dimension or any(type(s) is not int for s in secret):
        raise ValueError("one integer-secret calibration value per component required")
    shape = (3,)*packet.consumed
    joint = np.empty(shape, dtype=complex)
    for old in product(range(3), repeat=packet.consumed):
        target = list(old)
        for row, p in zip(packet.reduced_rows, packet.pivots):
            target[p] = (old[p]+sum(row[f]*old[f] for f in packet.free)) % 3
        frequencies = packet.component_frequencies(old)
        angle = 2*math.pi*(sum(s*f for s, f in zip(secret, frequencies)) % packet.phase_modulus)/packet.phase_modulus
        joint[tuple(target)] = 3**(-packet.consumed/2)*np.exp(1j*angle)
    points = list(product(range(3), repeat=packet.retained))
    branches = []
    for y in product(range(3), repeat=len(packet.pivots)):
        child = compile_packet(labels, level, y)
        base = child.component_frequencies(child.assignment((0,)*child.retained))
        actual = []
        residuals = [child.residual(z) for z in points]
        for z, residual in zip(points, residuals):
            target = [0]*packet.consumed
            for p, digit in zip(packet.pivots, y):
                target[p] = digit
            for f, digit in zip(packet.free, z):
                target[f] = digit
            value = joint[tuple(target)]
            theta = (sum(s*f for s, f in zip(secret, base))+3*sum(s*f for s, f in zip(secret, residual))) % packet.phase_modulus
            expected = 3**(-packet.consumed/2)*np.exp(2j*math.pi*theta/packet.phase_modulus)
            assert abs(value-expected) < 4e-12
            actual.append(value)
        probability = float(sum(abs(x)**2 for x in actual))
        assert abs(probability-3**(-len(packet.pivots))) < 4e-12
        normalized = np.array(actual)/math.sqrt(probability)
        if child.retained > 1:
            flat = normalized.reshape(3, -1)
            rho = flat @ flat.conj().T
            purity = float(np.trace(rho @ rho).real)
        else:
            purity = 1.0
        branches.append({"syndrome": list(y), "public_residual_frequency_table": [list(x) for x in residuals],
                         "probability": probability,
                         "full_unnormalized_joint_amplitudes": [[float(x.real), float(x.imag)] for x in actual],
                         "first_retained_qutrit_purity": purity,
                         "classical_cubic_polynomial": classical_polynomial(child) if level == 3 else None})
    return {"native_labels": labels, "integer_secret_calibration": secret, "resources": packet.resource_record(),
            "pivots": list(packet.pivots), "free_columns": list(packet.free),
            "public_RREF_rows": [list(row) for row in packet.reduced_rows], "all_syndrome_branches": branches,
            "physical_full_output_norm": float(sum(abs(joint.ravel())**2)),
            "constant_fraction_retained_registers_is_a_decoder": False}


def run_controls():
    controls = []
    for level in (3, 5):
        for seed in range(46011, 46014):
            rng = random.Random(seed)
            h0, _, h1 = ideal_chart(level)[0]
            labels = [[(rng.randrange(h0), rng.randrange(h1)) for _ in range(2)] for _ in range(5)]
            c = physical_control(labels, [1, 2], level)
            c["unfiltered_label_seed"] = seed
            controls.append(c)
    # Conditional algebra only: fresh batches must match the first low matrix.
    base = controls[0]["native_labels"][:4]
    packets = [compile_packet(base, 3)]
    rng = random.Random(46091)
    for _ in range(2):
        fresh = [[plus_low_high(y, rng) for y in row] for row in base]
        packets.append(compile_packet(fresh, 3))
    h = packets[0].retained
    zero = (0,)*h
    conditional = []
    for shift in product(range(3), repeat=h):
        shifts = [zero, shift, tuple((x+1) % 3 for x in shift)]
        result = matched_cubic_sum(packets, shifts)
        conditional.append({"three_packet_native_labels": [p.labels for p in packets],
                            "initial_syndromes": [p.syndrome for p in packets],
                            "source_condition": "two fresh independently uniform high-label batches conditioned on the first low matrix",
                            "conditional_high_label_seed": 46091,
                            "difference_shifts": shifts, "conditional_algebraic_sum": result,
                            "full_three_packet_quantum_instrument_replayed": False})
    return {"status": "NATIVE_TERNARY_KERNEL_PACKETS_CUBIC_RECEIVER_BLOCKED_LOCAL_REVIEW_PENDING",
            "native_controls": controls,
            "conditional_algebraic_sum_controls": conditional,
            "higher_level_fourth_difference_countercontrol": higher_difference_control(controls[3]),
            "literal_low_matrix_match_ledger": {
                "secret_dimension": packets[0].secret_dimension, "native_qutrits_per_batch": packets[0].consumed,
                "second_and_third_IID_low_matrices_both_match_first_probability": {
                    "base": 3, "exponent": -2*packets[0].secret_dimension*packets[0].consumed},
                "initial_zero_syndromes_for_three_packets_probability": {
                    "base": 3, "exponent": -3*len(packets[0].pivots)},
                "probabilities_are_conditioning_costs_not_optimal_matching_lower_bounds": True,
                "more_general_public_tensor_alignment_excluded": False},
            "next_obligations": ["A decoder for different public random polynomial packets, not copies of one unknown state.",
                "A growing-level source law and complexity bound; level3 cubic learning alone is not enough.",
                "Restore and account for full secret-digit recursion; each packet drops the top secret digit.",
                "Retained correlated qutrits are not counted as IID PSP outputs."],
            "claim_gate": {"new_algorithm": False, "candidate_accepted": False, "Shor_level_improvement": False,
                "polynomial_phase_learning_transfer_established": False, "constant_fraction_IID_PSP_output_rate": False,
                "independent_human_review": False}}


def plus_low_high(y, rng):
    z = (rng.randrange(3), rng.randrange(3))
    high = multiply((-1, 1), z, 3)
    return reduce_element((residue(y)+high[0], high[1]), 3)


def higher_difference_control(control):
    branch = control["all_syndrome_branches"][0]
    h = control["resources"]["retained_joint_qutrits"]
    if h != 3 or control["resources"]["parent_level"] != 5:
        raise ValueError("countercontrol requires the specified L5 three-register source")
    points = list(product(range(3), repeat=h))
    table = dict(zip(points, branch["public_residual_frequency_table"]))
    directions = [(1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    difference = [sum((-1)**mask.bit_count()*table[tuple(sum(directions[k][j] for k in range(4)
                if mask >> k & 1) % 3 for j in range(h))][l] for mask in range(16)) % 9
                  for l in range(len(table[points[0]]))]
    assert any(difference)
    return {"parent_level": 5, "native_control_index": 3, "syndrome": branch["syndrome"],
            "origin": [0]*h, "four_additive_directions": directions,
            "residual_phase_modulus": 9, "fourth_difference_by_secret_component": difference,
            "fixed_classical_cubic_receiver_transfer_allowed": False,
            "general_higher_level_receiver_excluded": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "native_controls": len(report["native_controls"]), "new_algorithm": False}))


if __name__ == "__main__":
    main()
