"""Exact ternary message circuits and a division-free CORDIC rotation contract.

Actual reversible header arithmetic and digit-controlled rotations; CORDIC
digit generation is an exact CLASSICAL reference, not a compiled quantum gate.
No growing-block decoder or quantum speedup is claimed.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import sys

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import ControlledGate
from qiskit.circuit.library import RYGate
from qiskit.synthesis.arithmetic import adder_ripple_c04

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORT = ROOT / "research/phase_workbench/ternary_coherent_reliability.json"


def natural(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def triple(values):
    values = tuple(values)
    if len(values) != 3:
        raise ValueError("three integer spectral weights required")
    for value in values:
        natural(value, "spectral weight")
    return values


@dataclass(frozen=True)
class Header:
    weights: tuple[int, int, int]
    capacity: int

    def __post_init__(self):
        object.__setattr__(self, "weights", triple(self.weights))
        natural(self.capacity, "product of original leaf denominators", 1)
        if sum(self.weights) > self.capacity:
            raise ValueError("denominator exceeds charged original-leaf capacity")

    @property
    def spectrum(self):
        total = sum(self.weights)
        return None if total == 0 else tuple(Fraction(w, total) for w in self.weights)

    @property
    def width(self):
        return self.capacity.bit_length()


def combine(left, right, kind, selector=0, *, signs=(1, 1)):
    """Distinct-leaf composition; capacity multiplication charges both sources.

    selector is the herald h for check, or surviving frequency t for fiber.
    selector=3 is the unused two-qubit qutrit encoding, completed by zero header.
    """
    if kind not in ("bit", "check", "fiber") or signs not in tuple(product((1, -1), repeat=2)):
        raise ValueError("bit/check/fiber node and explicit +/- coefficient signs required")
    natural(selector, "two-qubit selector")
    if selector > 3:
        raise ValueError("selector must fit its two-qubit register")
    a = tuple(left.weights[(signs[0]*j) % 3] for j in range(3))
    b = tuple(right.weights[(signs[1]*j) % 3] for j in range(3))
    if kind == "bit":
        weights = tuple(sum(a[(t-j) % 3]*b[j] for j in range(3)) for t in range(3))
    elif selector == 3:
        weights = (0, 0, 0)
    else:
        weights = tuple(a[(j+selector if kind == "check" else selector-j) % 3]*b[j]
                        for j in range(3))
    return Header(weights, left.capacity*right.capacity)


@lru_cache(maxsize=128)
def adder_kernel(width, kind):
    """Lower the established CDKM adder to its exact CX/CCX permutation gates."""
    natural(width, "adder width", 1)
    circuit = adder_ripple_c04(width, kind=kind).decompose()
    if circuit.global_phase != 0:
        raise RuntimeError("unexpected arithmetic global phase")
    result = []
    for instruction in circuit.data:
        if instruction.operation.name not in ("cx", "ccx"):
            raise RuntimeError("CDKM lowering changed: re-audit before using")
        result.append(tuple(circuit.find_bit(q).index for q in instruction.qubits))
    return tuple(result)


def append_adder(circuit, a, b, helper, *, carry=None, controls=()):
    if len(a) != len(b):
        raise ValueError("equal-width adder inputs required")
    wires = [*a, *b, *([] if carry is None else [carry]), helper]
    for positions in adder_kernel(len(a), "fixed" if carry is None else "half"):
        circuit.mcx([*controls, *(wires[i] for i in positions[:-1])], wires[positions[-1]])


def multiplier(width):
    """Standard shift-and-add multiplication using Qiskit's CDKM half adders."""
    natural(width, "multiplier width", 1)
    a, b, out, helper = (QuantumRegister(n, name) for n, name in
                         ((width, "a"), (width, "b"), (2*width, "out"), (1, "help")))
    circuit = QuantumCircuit(a, b, out, helper)
    for i in range(width):
        append_adder(circuit, a, out[i:i+width], helper[0], carry=out[i+width], controls=(b[i],))
    return circuit


@dataclass
class MessageProgram:
    circuit: QuantumCircuit
    width: int
    kind: str
    signs: tuple[int, int]
    left: tuple[int, ...]
    right: tuple[int, ...]
    selector: tuple[int, ...]
    output: tuple[int, ...]
    scratch: tuple[int, ...]

    @property
    def output_width(self):
        # Three arbitrary products can be added without overflow, even off-source.
        return 2*self.width+2

    def encode(self, left, right, selector=0):
        state = 0
        for values, wires in ((triple(left), self.left), (triple(right), self.right)):
            for j, value in enumerate(values):
                if value >= 1 << self.width:
                    raise ValueError("input weight would overflow the actual circuit register")
                state |= value << wires[j*self.width]
        natural(selector, "selector")
        if selector > 3:
            raise ValueError("two-qubit selector required")
        return state | (selector << self.selector[0])

    def read_output(self, state):
        mask = (1 << self.output_width)-1
        return tuple((state >> self.output[j*self.output_width]) & mask for j in range(3))


def message_program(width, kind, *, signs=(1, 1)):
    """Uniform circuit in weight width; no enumeration of upstream herald words.

    Contract: clean output and scratch. All input/selector wires are preserved;
    dirty ancilla inputs still have a total unitary, but not this arithmetic law.
    """
    natural(width, "message weight width", 1)
    combine(Header((0, 1, 1), 2), Header((0, 1, 1), 2), kind, signs=signs)
    w = 2*width+2
    left, right, selector, output, temporary, padding, helper = (
        QuantumRegister(n, name) for n, name in
        ((3*width, "left"), (3*width, "right"), (2, "selector"),
         (3*w, "out"), (2*width, "product"), (2, "padding"), (1, "help")))
    circuit = QuantumCircuit(left, right, selector, output, temporary, padding, helper)
    multiply = multiplier(width)
    # Explicit primitive expansion permits phase-free sparse basis verification.
    multiply_ops = permutation_ops(multiply)
    for t, j in product(range(3), repeat=2):
        index = (t-j if kind in ("bit", "fiber") else j+t) % 3
        left_index, right_index = signs[0]*index % 3, signs[1]*j % 3
        a = left[left_index*width:(left_index+1)*width]
        b = right[right_index*width:(right_index+1)*width]
        wires = [*a, *b, *temporary, helper[0]]
        for mask, target in multiply_ops:
            circuit.mcx([wires[i] for i in range(len(wires)) if mask >> i & 1], wires[target])
        out_index = t if kind == "bit" else j
        controls = () if kind == "bit" else tuple(selector)
        if controls:
            for bit in range(2):
                if not (t >> bit & 1):
                    circuit.x(selector[bit])
        append_adder(circuit, [*temporary, *padding], output[out_index*w:(out_index+1)*w],
                     helper[0], controls=controls)
        if controls:
            for bit in range(2):
                if not (t >> bit & 1):
                    circuit.x(selector[bit])
        for mask, target in reversed(multiply_ops):
            circuit.mcx([wires[i] for i in range(len(wires)) if mask >> i & 1], wires[target])
    indices = lambda register: tuple(circuit.find_bit(q).index for q in register)
    return MessageProgram(circuit, width, kind, signs, indices(left), indices(right),
                          indices(selector), indices(output), indices([*temporary, *padding, *helper]))


def permutation_ops(circuit):
    """Read actual positive controlled-X gates, refusing unmodeled phases/gates."""
    if circuit.global_phase != 0:
        raise ValueError("sparse permutation evaluator cannot ignore a global phase")
    result = []
    for instruction in circuit.data:
        op = instruction.operation
        if not (op.name == "x" or isinstance(op, ControlledGate) and op.base_gate.name == "x"
                and op.ctrl_state == (1 << op.num_ctrl_qubits)-1):
            raise ValueError(f"not an exact positive controlled-X: {op.name}")
        wires = tuple(circuit.find_bit(q).index for q in instruction.qubits)
        result.append((sum(1 << q for q in wires[:-1]), wires[-1]))
    return tuple(result)


def apply_basis(operations, state, *, inverse=False):
    natural(state, "basis word")
    for mask, target in reversed(operations) if inverse else operations:
        if state & mask == mask:
            state ^= 1 << target
    return state


def apply_sparse(operations, amplitudes, *, inverse=False):
    # No mathematical update oracle: execute every actual gate on each basis word.
    result = {}
    for state, amplitude in amplitudes.items():
        target = apply_basis(operations, state, inverse=inverse)
        if target in result:
            raise ArithmeticError("noninjective supposedly reversible gate program")
        result[target] = amplitude
    return result


def root_difference_sign(p, q, a, b):
    """Sign of p*sqrt(b)-q*sqrt(a), using only exact integer comparisons."""
    if type(p) is not int or type(q) is not int:
        raise ValueError("signed integer CORDIC coefficients required")
    natural(a, "first squared amplitude")
    natural(b, "second squared amplitude")
    # Fold exact zero terms into the sign tests before squaring.
    u, v = p if b else 0, q if a else 0
    if u >= 0 > v:
        return 1
    if v >= 0 > u:
        return -1
    comparison = p*p*b-q*q*a
    sign = (comparison > 0)-(comparison < 0)
    return -sign if u < 0 else sign


def cordic_digits(a, b, steps):
    """CLASSICAL exact digit generator; weights may have arbitrarily tiny ratios.

    digit=0 means +atan(2^-i); digit=1 means the negative angle. Equalities
    choose +. Zero pairs are explicitly disabled, not normalized or dropped.
    """
    natural(a, "first squared amplitude")
    natural(b, "second squared amplitude")
    natural(steps, "CORDIC steps", 1)
    p, q, growth = 1, 0, 1
    digits, trace = [], []
    for i in range(steps):
        sigma = 1 if root_difference_sign(p, q, a, b) >= 0 else -1
        digits.append(int(sigma < 0))
        p, q = (p << i)-sigma*q, (q << i)+sigma*p
        growth *= (1 << i)+1
        if abs(p)+abs(q) > growth:
            raise ArithmeticError("uniform integer CORDIC growth bound failed")
        trace.append({"iteration": i, "p": str(p), "q": str(q), "digit": digits[-1]})
    return {"enabled": bool(a+b), "digits": digits, "trace": trace,
            "signed_coefficient_width_sufficient": growth.bit_length()+1,
            "ideal_real_angle_error_upper": str(Fraction(1, 1 << (steps-1))),
            "digit_generation_uses_division_sqrt_or_floating_point": False,
            "digit_generation_reversible_circuit_compiled": False}


def rotation_program(steps, pair=(0, 1)):
    """Actual digit-controlled qutrit rotation; |11> and disabled blocks fixed.

    The weight-to-digit circuit is NOT supplied by this function. Constant
    angles are floating-point logical gates; fault-tolerant synthesis is unpaid.
    """
    natural(steps, "rotation steps", 1)
    if pair not in ((0, 1), (0, 2)):
        raise ValueError("a computational-qutrit 01 or 02 Givens pair required")
    if steps > 1022:
        raise ValueError("UNKNOWN: floating-point constant-angle reference cap")
    digits, enabled, data = QuantumRegister(steps, "digits"), QuantumRegister(1, "enabled"), QuantumRegister(2, "data")
    circuit = QuantumCircuit(digits, enabled, data)
    target, other = (data[0], data[1]) if pair == (0, 1) else (data[1], data[0])
    for i in range(steps):
        alpha = math.atan(math.ldexp(1., -i))
        circuit.append(RYGate(-2*alpha).control(2, ctrl_state=1, annotated=False), [enabled[0], other, target])
        circuit.append(RYGate(4*alpha).control(3, ctrl_state=5, annotated=False), [enabled[0], other, digits[i], target])
    return circuit


def rotation_matrix(record, pair=(0, 1)):
    """Small classical reference for the same constant-angle gate product."""
    if pair not in ((0, 1), (0, 2)):
        raise ValueError("01/02 pair required")
    matrix = np.eye(3)
    if record["enabled"]:
        for i, digit in enumerate(record["digits"]):
            angle = (1 if digit == 0 else -1)*math.atan(math.ldexp(1., -i))
            c, s = math.cos(angle), math.sin(angle)
            gate = np.eye(3)
            x, y = pair
            gate[x, x] = gate[y, y] = c
            gate[x, y], gate[y, x] = s, -s
            matrix = gate @ matrix
    return matrix


def compression_reference(weights, steps):
    w0, w1, w2 = triple(weights)
    first, second = cordic_digits(w0, w1, steps), cordic_digits(w0+w1, w2, steps)
    return rotation_matrix(second, (0, 2)) @ rotation_matrix(first), (first, second)


def precision_budget(compressions, epsilon, *, source_error=0, gate_synthesis_error=0):
    natural(compressions, "compression occurrences across the ENTIRE sampler")
    eps, source, synthesis = map(Fraction, (epsilon, source_error, gate_synthesis_error))
    if not 0 < eps <= 1 or min(source, synthesis) < 0 or source+synthesis >= eps:
        raise ValueError("a positive remaining uniform operator/TV error budget is required")
    steps = 1
    while Fraction(4*compressions, 1 << steps) > eps-source-synthesis:
        steps += 1
    return {"compression_occurrences_including_A_and_Adjoint_and_root_inverses": compressions,
            "CORDIC_steps_sufficient": steps,
            "uniform_ideal_constant_rotation_operator_error_upper": str(Fraction(4*compressions, 1 << steps)),
            "source_trace_error_assumed": str(source), "total_gate_operator_error_assumed": str(synthesis),
            "total_output_TV_perturbation_upper": str(min(Fraction(1), Fraction(4*compressions, 1 << steps)+source+synthesis)),
            "target_TV": str(eps), "herald_branches_are_not_summed": True,
            "weight_arithmetic_must_be_exact_and_uncomputed": True,
            "error_relative_to_ideal_decoder_not_native_target": True,
            "gate_synthesis_budget_has_been_implemented": False}


def circuit_ledger(program):
    operations = permutation_ops(program.circuit)
    return {"input_weight_width": program.width, "node": program.kind,
            "coefficient_signs": list(program.signs), "output_weight_width": program.output_width,
            "qubits_including_all_inputs_outputs_and_scratch": program.circuit.num_qubits,
            "actual_controlled_X_gates": len(operations),
            "actual_maximum_X_controls": max(mask.bit_count() for mask, _ in operations),
            "primitive_gate_counts": dict(program.circuit.count_ops()),
            "upstream_herald_history_enumeration_used": False,
            "arbitrary_clean_input_weights_no_overflow": True}


def run_controls():
    paths = [Path(__file__), ROOT/"theorems/ternary_coloring_bpqm.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    circuits, basis_checks = [], []
    for kind in ("bit", "check", "fiber"):
        program = message_program(1, kind)
        operations = permutation_ops(program.circuit)
        count = 0
        for values in product(range(2), repeat=6):
            left, right = Header(values[:3], 3), Header(values[3:], 3)
            for h in range(4):
                original = program.encode(left.weights, right.weights, h)
                actual = apply_basis(operations, original)
                expected = combine(left, right, kind, h).weights
                if program.read_output(actual) != expected or apply_basis(operations, actual, inverse=True) != original:
                    raise ArithmeticError("actual header gate law or inverse failed")
                if any(actual >> q & 1 for q in program.scratch):
                    raise ArithmeticError("arithmetic scratch not cleaned")
                # Every non-output wire is required to be exactly its input value.
                output_mask = sum(1 << q for q in program.output)
                if actual & ~output_mask != original:
                    raise ArithmeticError("input or selector overwritten")
                count += 1
        basis_checks.append({"node": kind, "exhaustive_one_bit_inputs_including_unused_selector": count})
    for width in (1, 2, 4, 8, 16):
        circuits.extend(circuit_ledger(message_program(width, kind)) for kind in ("bit", "check", "fiber"))
    examples = []
    for weights in ((0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 2, 3), (1, 1 << 1024, 1)):
        matrix, records = compression_reference(weights, 32)
        if sum(weights):
            # Scale before floating-point conversion: enormous integer weights are legal.
            vector = np.array([math.sqrt(Fraction(w, sum(weights))) for w in weights])
            residual = float(np.linalg.norm(matrix @ vector-np.array([1., 0., 0.])))
        else:
            residual = float(np.max(abs(matrix-np.eye(3))))
        if residual > 4/(1 << 32)+1e-13:
            raise ArithmeticError("CORDIC compression exceeds its uniform ideal-angle bound")
        examples.append({"weights": list(map(str, weights)), "steps": 32,
                         "compression_residual_numeric": residual,
                         "signed_coefficient_width_sufficient": records[0]["signed_coefficient_width_sufficient"],
                         "zero_pairs_disabled": [not r["enabled"] for r in records]})
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}:
        raise RuntimeError("producer or dependency changed during run")
    return {"schema_version": 1,
            "status": "EXACT_HEADER_GATES_AND_INTEGER_CORDIC_CONTRACT_REVIEW_PENDING",
            "source_sha256": hashes, "qiskit_version": __import__("qiskit").__version__,
            "exhaustive_gate_checks": basis_checks, "actual_circuit_scaling": circuits,
            "rare_and_dark_rotation_controls": examples,
            "example_whole_program_precision_budget": precision_budget(10**12, "1/1000"),
            "exact_message_header_circuits_implemented": True,
            "digit_controlled_rotation_gates_implemented": True,
            "coherent_CORDIC_digit_generation_compiled": False,
            "full_LDPC_receiver_compiled": False,
            "quantum_speedup_or_classical_hardness_established": False,
            "local_derivation_independently_reviewed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({k: report[k] for k in ("status", "exhaustive_gate_checks",
                     "rare_and_dark_rotation_controls", "example_whole_program_precision_budget",
                     "coherent_CORDIC_digit_generation_compiled", "full_LDPC_receiver_compiled")}, indent=2))


if __name__ == "__main__":
    main()
