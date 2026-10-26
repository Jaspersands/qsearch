"""Actual reversible variable-weight CORDIC decisions, updates and rotations.

No herald truth tables: exact signed square-root comparison is reduced to
CDKM arithmetic. A compute/rotate/uncompute compiler retains every decision;
it is not a whole BPQM receiver or a fault-tolerant synthesis implementation.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import sys

from qiskit import QuantumCircuit, QuantumRegister
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.ternary_coherent_reliability import (
    adder_kernel, append_adder, apply_basis, multiplier, natural,
    permutation_ops, root_difference_sign, rotation_program, cordic_digits, rotation_matrix,
)

REPORT = ROOT/"research/phase_workbench/ternary_cordic_step.json"


def multi_x(circuit, controls, target, clean_chain):
    """Positive multi-control X, explicitly lowered using clean AND scratch."""
    controls = tuple(controls)
    if len(controls) <= 2:
        if controls:
            circuit.mcx(list(controls), target)
        else:
            circuit.x(target)
        return
    if len(clean_chain) < len(controls)-2:
        raise ValueError("not enough charged clean AND-chain scratch")
    circuit.ccx(controls[0], controls[1], clean_chain[0])
    for i in range(2, len(controls)-1):
        circuit.ccx(clean_chain[i-2], controls[i], clean_chain[i-1])
    circuit.ccx(clean_chain[len(controls)-3], controls[-1], target)
    for i in reversed(range(2, len(controls)-1)):
        circuit.ccx(clean_chain[i-2], controls[i], clean_chain[i-1])
    circuit.ccx(controls[0], controls[1], clean_chain[0])


def copy_word(circuit, source, target, *, shift=0):
    """Sign-extend and shift a two's-complement word into a clean target."""
    for i in range(shift, len(target)):
        circuit.cx(source[min(i-shift, len(source)-1)], target[i])


def emit_permutation(circuit, operations, wires, *, inverse=False):
    for mask, target in reversed(operations) if inverse else operations:
        circuit.mcx([wires[i] for i in range(len(wires)) if mask >> i & 1], wires[target])


def negate_controlled(circuit, word, sign, one, helper):
    for qubit in word:
        circuit.cx(sign, qubit)
    circuit.x(one[0])
    append_adder(circuit, one, word, helper, controls=(sign,))
    circuit.x(one[0])


def greater_equal(circuit, left, right, output, difference, carry, cin):
    """Toggle output by unsigned left>=right, cleaning the entire comparison."""
    if len(left) != len(right) or len(left) != len(difference):
        raise ValueError("equal comparator widths required")
    for source, target in zip(right, difference):
        circuit.cx(source, target)
        circuit.x(target)
    circuit.x(cin)
    wires = [cin, *left, *difference, carry]
    kernel = adder_kernel(len(left), "full")
    for positions in kernel:
        circuit.mcx([wires[i] for i in positions[:-1]], wires[positions[-1]])
    circuit.cx(carry, output)
    for positions in reversed(kernel):
        circuit.mcx([wires[i] for i in positions[:-1]], wires[positions[-1]])
    circuit.x(cin)
    for source, target in zip(right, difference):
        circuit.x(target)
        circuit.cx(source, target)


def nonzero(circuit, word, output, chain):
    circuit.x(output)
    for q in word:
        circuit.x(q)
    multi_x(circuit, word, output, chain)
    for q in word:
        circuit.x(q)


def pattern_x(circuit, controls, values, target, chain):
    for q, value in zip(controls, values):
        if not value:
            circuit.x(q)
    multi_x(circuit, controls, target, chain)
    for q, value in zip(controls, values):
        if not value:
            circuit.x(q)


@dataclass
class StepProgram:
    circuit: QuantumCircuit
    coefficient_width: int
    weight_width: int
    iteration: int
    p: tuple[int, ...]
    q: tuple[int, ...]
    a: tuple[int, ...]
    b: tuple[int, ...]
    digit: int
    p_next: tuple[int, ...]
    q_next: tuple[int, ...]
    scratch: tuple[int, ...]

    def encode(self, p, q, a, b):
        state = 0
        for value, wires, signed in ((p, self.p, True), (q, self.q, True),
                                     (a, self.a, False), (b, self.b, False)):
            if type(value) is not int:
                raise ValueError("exact integer circuit input required")
            lower, upper = (-(1 << (len(wires)-1)), 1 << (len(wires)-1)) if signed else (0, 1 << len(wires))
            if not lower <= value < upper:
                raise ValueError("circuit input overflow")
            state |= (value % (1 << len(wires))) << wires[0]
        return state

    def read(self, state):
        values = []
        for wires in (self.p_next, self.q_next):
            value = (state >> wires[0]) & ((1 << len(wires))-1)
            if value >> (len(wires)-1):
                value -= 1 << len(wires)
            values.append(value)
        return state >> self.digit & 1, *values


def step_program(coefficient_width, weight_width, iteration):
    """Actual out-of-place step, clean output/ancilla contract and total unitary.

    Original P,Q,a,b are kept. The digit and new P,Q are retained, enabling
    a caller to reverse the entire history without erasure or postselection.
    """
    m = natural(coefficient_width, "signed coefficient width", 2)
    w = natural(weight_width, "squared-amplitude width", 1)
    i = natural(iteration, "CORDIC iteration")
    n, k = m+i+2, max(2*m, w)
    circuit = QuantumCircuit()

    def register(size, name):
        if size == 0:
            return ()
        reg = QuantumRegister(size, name)
        circuit.add_register(reg)
        return tuple(reg)

    p, q, a, b = (register(size, name) for size, name in ((m, "P"), (m, "Q"), (w, "a"), (w, "b")))
    digit = register(1, "digit")[0]
    pn, qn = register(n, "Pnext"), register(n, "Qnext")
    input_output_qubits = circuit.num_qubits
    ap, aq, copy = register(m, "absP"), register(m, "absQ"), register(m, "copy")
    psq, qsq = register(2*m, "P2"), register(2*m, "Q2")
    pad_square, pad_weight = register(k-2*m, "pad_square"), register(k-w, "pad_weight")
    u, v = register(2*k, "P2b"), register(2*k, "Q2a")
    difference = register(2*k, "difference")
    carry, helper = register(1, "carry")[0], register(1, "helper")[0]
    one = register(m, "one")
    geuv, gevu = register(1, "geuv")[0], register(1, "gevu")[0]
    nzu, nzv = register(1, "nzu")[0], register(1, "nzv")[0]
    su, sv = register(1, "signedU")[0], register(1, "signedV")[0]
    chain = register(max(1, 2*k-2), "AND_chain")
    ep, eq = register(n, "extendedP"), register(n, "extendedQ")

    square_ops = permutation_ops(multiplier(m))
    weighted_ops = permutation_ops(multiplier(k))
    for source, absolute, square in ((p, ap, psq), (q, aq, qsq)):
        for source_bit, target in zip(source, absolute):
            circuit.cx(source_bit, target)
        negate_controlled(circuit, absolute, source[-1], one, helper)
        for source_bit, target in zip(absolute, copy):
            circuit.cx(source_bit, target)
        emit_permutation(circuit, square_ops, [*absolute, *copy, *square, helper])
        for source_bit, target in zip(absolute, copy):
            circuit.cx(source_bit, target)
    emit_permutation(circuit, weighted_ops, [*psq, *pad_square, *b, *pad_weight, *u, helper])
    emit_permutation(circuit, weighted_ops, [*qsq, *pad_square, *a, *pad_weight, *v, helper])
    greater_equal(circuit, u, v, geuv, difference, carry, helper)
    greater_equal(circuit, v, u, gevu, difference, carry, helper)
    nonzero(circuit, u, nzu, chain)
    nonzero(circuit, v, nzv, chain)
    circuit.ccx(p[-1], nzu, su)
    circuit.ccx(q[-1], nzv, sv)
    predicate_instructions = tuple(circuit.data)
    pattern_x(circuit, (su, sv, geuv), (0, 0, 0), digit, chain)
    pattern_x(circuit, (su, sv, gevu), (1, 1, 0), digit, chain)
    pattern_x(circuit, (su, sv), (1, 0), digit, chain)
    # All predicate instructions are exact self-inverse controlled-X gates.
    for instruction in reversed(predicate_instructions):
        circuit.append(instruction.operation, instruction.qubits)

    copy_word(circuit, p, pn, shift=i)
    copy_word(circuit, q, qn, shift=i)
    copy_word(circuit, p, ep)
    copy_word(circuit, q, eq)
    add_kernel = adder_kernel(n, "fixed")

    def add(source, target, inverse):
        wires = [*source, *target, helper]
        for positions in reversed(add_kernel) if inverse else add_kernel:
            circuit.mcx([digit, *(wires[j] for j in positions[:-1])], wires[positions[-1]])

    circuit.x(digit)
    add(eq, pn, True)
    add(ep, qn, False)
    circuit.x(digit)
    add(eq, pn, False)
    add(ep, qn, True)
    copy_word(circuit, p, ep)
    copy_word(circuit, q, eq)
    indices = lambda wires: tuple(circuit.find_bit(bit).index for bit in wires)
    return StepProgram(circuit, m, w, i, indices(p), indices(q), indices(a), indices(b),
                       circuit.find_bit(digit).index, indices(pn), indices(qn),
                       tuple(range(input_output_qubits, circuit.num_qubits)))


def ledger(program):
    operations = permutation_ops(program.circuit)
    return {"signed_coefficient_width": program.coefficient_width, "weight_width": program.weight_width,
            "iteration": program.iteration, "next_coefficient_width": len(program.p_next),
            "actual_qubits_including_retained_inputs_outputs_and_scratch": program.circuit.num_qubits,
            "actual_controlled_X_gates": len(operations),
            "actual_maximum_X_controls": max(mask.bit_count() for mask, _ in operations),
            "header_or_weight_truth_table_used": False,
            "unsigned_comparison_handles_zero_and_negative_coefficients": True}


def step_size(m, w, i):
    """Exact gate/layout count for this implementation, before allocating it."""
    natural(m, "coefficient width", 2)
    natural(w, "weight width", 1)
    natural(i, "iteration")
    n, k = m+i+2, max(2*m, w)
    multiply_count = lambda bits: bits*(6*bits+1)
    predicate = 20*m+12+2*multiply_count(m)+2*multiply_count(k)+80*k
    return {"next_width": n, "gates": 2*predicate+30*n-2*i+19,
            "qubits": 8*m+w+7+4*n+10*k,
            "scratch": 6*m+10*k-w+6+2*n}


def rotation_size(weight_width, steps):
    w = natural(weight_width, "weight width", 1)
    natural(steps, "CORDIC steps", 1)
    sizes, m = [], 2
    for i in range(steps):
        size = step_size(m, w, i)
        sizes.append(size)
        m = size["next_width"]
    return {"steps": sizes,
            "gates": 2*(1+sum(s["gates"] for s in sizes))+2*(8*w-2)+2*steps,
            "qubits": 2*w+steps+7+max(s["scratch"] for s in sizes)+max(1, 2*w-2)
                      +2*sum(s["next_width"] for s in sizes)}


@dataclass
class VariableRotation:
    circuit: QuantumCircuit
    weight_width: int
    steps: int
    pair: tuple[int, int]
    a: tuple[int, ...]
    b: tuple[int, ...]
    data: tuple[int, ...]
    work: tuple[int, ...]
    predicted_logical_gates: int

    def encode(self, a, b, data=0):
        for value in (a, b):
            natural(value, "nonnegative squared amplitude")
            if value >= 1 << self.weight_width:
                raise ValueError("rotation weight input overflow")
        natural(data, "encoded qutrit")
        if data > 3:
            raise ValueError("two-qubit qutrit required")
        return (a << self.a[0]) | (b << self.b[0]) | (data << self.data[0])


def variable_rotation(weight_width, steps, pair=(0, 1), *, max_gates=2_000_000):
    """Compute integer digits, rotate a coherent qutrit, reverse ALL arithmetic.

    This implements the complete local variable-weight Givens interface, not
    just rotation application with precomputed advice. Logical Ry constants
    are numerical; a fault-tolerant gate-synthesis budget remains separate.
    """
    w = natural(weight_width, "weight width", 1)
    natural(steps, "CORDIC steps", 1)
    natural(max_gates, "explicit reference gate cap", 1)
    if pair not in ((0, 1), (0, 2)):
        raise ValueError("01/02 Givens pair required")
    plan = rotation_size(w, steps)
    sizes, count = plan["steps"], plan["gates"]
    if count > max_gates:
        raise ValueError(f"UNKNOWN: explicit reference cap; {count} logical gates required")
    circuit = QuantumCircuit()

    def register(size, name):
        reg = QuantumRegister(size, name)
        circuit.add_register(reg)
        return tuple(reg)

    a, b, data = register(w, "a"), register(w, "b"), register(2, "data")
    input_qubits = circuit.num_qubits
    digits, enabled = register(steps, "digits"), register(1, "enabled")[0]
    p, q = register(2, "P0"), register(2, "Q0")
    workspace = register(max(s["scratch"] for s in sizes), "workspace")
    chain = register(max(1, 2*w-2), "enable_chain")
    circuit.x(p[0])
    for i in range(steps):
        body = step_program(len(p), w, i)
        pn = register(len(body.p_next), f"P{i+1}")
        qn = register(len(body.q_next), f"Q{i+1}")
        mapping = [None]*body.circuit.num_qubits
        for old, new in ((body.p, p), (body.q, q), (body.a, a), (body.b, b),
                         ((body.digit,), (digits[i],)), (body.p_next, pn), (body.q_next, qn),
                         (body.scratch, workspace)):
            for index, wire in zip(old, new):
                mapping[index] = wire
        for instruction in body.circuit.data:
            circuit.append(instruction.operation, [mapping[body.circuit.find_bit(bit).index]
                                                  for bit in instruction.qubits])
        p, q = pn, qn
    computation = tuple(circuit.data)
    nonzero(circuit, (*a, *b), enabled, chain)
    application = rotation_program(steps, pair)
    circuit.compose(application, qubits=[*digits, enabled, *data], inplace=True)
    nonzero(circuit, (*a, *b), enabled, chain)
    for instruction in reversed(computation):
        circuit.append(instruction.operation, instruction.qubits)
    if len(circuit.data) != count or circuit.num_qubits != plan["qubits"]:
        raise ArithmeticError("pre-allocation gate/qubit formula disagrees with actual program")
    indices = lambda wires: tuple(circuit.find_bit(bit).index for bit in wires)
    return VariableRotation(circuit, w, steps, pair, indices(a), indices(b), indices(data),
                            tuple(range(input_qubits, circuit.num_qubits)), count)


def sparse_gate_program(circuit):
    """Actual X/controlled-X/controlled-Ry instructions; no function oracle."""
    if circuit.global_phase != 0:
        raise ValueError("unmodeled circuit phase")
    operations = []
    for instruction in circuit.data:
        op = instruction.operation
        wires = tuple(circuit.find_bit(bit).index for bit in instruction.qubits)
        base = op.base_gate if hasattr(op, "base_gate") else op
        if base.name == "x":
            controls, state = wires[:-1], getattr(op, "ctrl_state", 0)
            operations.append((sum(1 << q for q in controls), sum(((state >> j) & 1) << q
                               for j, q in enumerate(controls)), wires[-1], None))
        elif base.name == "ry":
            controls, state = wires[:-1], getattr(op, "ctrl_state", 0)
            operations.append((sum(1 << q for q in controls), sum(((state >> j) & 1) << q
                               for j, q in enumerate(controls)), wires[-1], float(base.params[0])))
        else:
            raise ValueError(f"unmodeled gate {op.name}")
    return tuple(operations)


def apply_sparse_gates(operations, amplitudes, *, inverse=False):
    amplitudes = dict(amplitudes)
    for mask, state, target, angle in reversed(operations) if inverse else operations:
        result = {}
        if angle is not None:
            angle = -angle if inverse else angle
            c, s = math.cos(angle/2), math.sin(angle/2)
        for word, amplitude in amplitudes.items():
            if word & mask != state:
                result[word] = result.get(word, 0)+amplitude
            elif angle is None:
                new = word ^ (1 << target)
                result[new] = result.get(new, 0)+amplitude
            else:
                flipped = word ^ (1 << target)
                result[word] = result.get(word, 0)+c*amplitude
                result[flipped] = result.get(flipped, 0)+(-s if word >> target & 1 else s)*amplitude
        amplitudes = result
    return amplitudes


def coherent_control(program):
    """Falsifier with complex amplitudes across weights AND every qutrit value."""
    rng = np.random.default_rng(412)
    sources = [(a, b, d) for a, b in ((0, 0), (0, 3), (1, 2), (3, 1)) for d in range(4)]
    amplitudes = rng.normal(size=len(sources))+1j*rng.normal(size=len(sources))
    amplitudes /= np.linalg.norm(amplitudes)
    source, expected = {}, {}
    for (a, b, d), amplitude in zip(sources, amplitudes):
        source[program.encode(a, b, d)] = amplitude
        matrix = np.eye(4)
        matrix[:3, :3] = rotation_matrix(cordic_digits(a, b, program.steps), program.pair)
        for out in range(4):
            target = program.encode(a, b, out)
            expected[target] = expected.get(target, 0)+matrix[out, d]*amplitude
    operations = sparse_gate_program(program.circuit)
    actual = apply_sparse_gates(operations, source)
    error = sum(abs(actual.get(word, 0)-expected.get(word, 0))**2 for word in actual.keys() | expected.keys())**.5
    garbage_probability = sum(abs(amp)**2 for word, amp in actual.items() if any(word >> q & 1 for q in program.work))
    recovered = apply_sparse_gates(operations, actual, inverse=True)
    inverse_error = sum(abs(recovered.get(word, 0)-source.get(word, 0))**2 for word in recovered.keys() | source.keys())**.5
    if max(error, garbage_probability, inverse_error) > 1e-11:
        raise ArithmeticError("coherent variable-weight rotation, cleanup or inverse failed")
    return {"weight_width": program.weight_width, "CORDIC_steps": program.steps, "pair": list(program.pair),
            "coherent_source_basis_words": len(source), "actual_qubits": program.circuit.num_qubits,
            "actual_logical_gates": len(program.circuit.data), "full_state_reference_residual_numeric": error,
            "arithmetic_garbage_probability_numeric": garbage_probability,
            "inverse_recovery_residual_numeric": inverse_error,
            "dense_many_qubit_statevector_or_ideal_arithmetic_oracle_used": False}


def run_controls():
    paths = [Path(__file__), ROOT/"theorems/ternary_coherent_reliability.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    small = step_program(2, 1, 0)
    operations = permutation_ops(small.circuit)
    count = 0
    output_mask = sum(1 << bit for bit in (*small.p_next, *small.q_next, small.digit))
    for p, q, a, b in product(range(-2, 2), range(-2, 2), range(2), range(2)):
        original = small.encode(p, q, a, b)
        actual = apply_basis(operations, original)
        sigma = -1 if root_difference_sign(p, q, a, b) < 0 else 1
        if small.read(actual) != (int(sigma < 0), p-sigma*q, q+sigma*p):
            raise ArithmeticError("actual signed CORDIC decision/update failed")
        if actual & ~output_mask != original or apply_basis(operations, actual, inverse=True) != original:
            raise ArithmeticError("scratch cleanup, input preservation or inverse failed")
        count += 1
    resources = [ledger(small), ledger(step_program(4, 4, 2)), ledger(step_program(8, 8, 4))]
    rotations = [coherent_control(variable_rotation(2, 3, pair)) for pair in ((0, 1), (0, 2))]
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}:
        raise RuntimeError("producer or dependency changed during run")
    large = rotation_size(64, 52)
    return {"schema_version": 1, "status": "REVERSIBLE_VARIABLE_WEIGHT_CORDIC_ROTATION_REVIEW_PENDING",
            "source_sha256": hashes, "exhaustive_clean_small_input_cases": count,
            "resources": resources, "exact_variable_weight_decision_update_gates_implemented": True,
            "coherent_variable_weight_rotation_controls": rotations,
            "whole_CORDIC_history_and_rotation_composition_compiled": True,
            "large_rotation_cost_prediction": {"weight_bits": 64, "steps": 52,
                "predicted_logical_gates": large["gates"], "predicted_qubits": large["qubits"],
                "large_circuit_allocated_or_executed": False, "fault_tolerant_synthesis_included": False},
            "whole_LDPC_receiver_compiled": False, "speedup_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
