"""Constructive signed-pair isometry; bounded simulation is verification only.

The plan uses controlled one-qubit gates, controlled swaps and reversible
Boolean gates. It does not perform circuit search, enumerate a large-field
matrix, synthesize Clifford+T rotations, or implement the entire decoder.
"""

from collections import Counter
from dataclasses import dataclass, replace
from fractions import Fraction
import math

import numpy as np


@dataclass(frozen=True)
class Gate:
    kind: str
    targets: tuple[int, ...] = ()
    controls: tuple[tuple[int, int], ...] = ()
    ratio: tuple[int, int] = (0, 1)
    power: int = 0
    adjoint: bool = False

    def inverse(self):
        if self.kind == "ry":
            return replace(self, adjoint=not self.adjoint)
        if self.kind == "phase":
            return replace(self, power=-self.power)
        return self


def inverse(gates):
    return tuple(g.inverse() for g in reversed(gates))


def uniform_interval(count, bits, controls=()):
    """A_count|0> = uniform on [0,count); a unitary on the padded space.

    Rotation probabilities are exact integer ratios. Computing finite-gate
    rotation angles to sufficient precision is a separately charged task.
    """
    if not isinstance(count, int) or count < 1 or count > (1 << len(bits)):
        raise ValueError("count must fit the supplied register")
    if count == 1:
        return ()
    if count == 1 << len(bits):
        return tuple(Gate("h", (b,), controls) for b in bits)
    high, low = bits[-1], bits[:-1]
    half = 1 << len(low)
    if count <= half:
        return uniform_interval(count, low, controls + ((high, 0),))
    right = count - half
    return (
        (Gate("ry", (high,), controls, (right, count)),)
        + tuple(Gate("h", (b,), controls + ((high, 0),)) for b in low)
        + uniform_interval(right, low, controls + ((high, 1),))
    )


def compare_greater(a, b, target, scratch):
    """XOR [a>b] into target; scratch starts and ends zero.

    Store equality of successive high-bit prefixes, use their disjoint first
    differing-bit events, then reverse the prefix computation. No table oracle.
    """
    if len(a) != len(b) or len(scratch) != len(a) - 1:
        raise ValueError("comparator width/scratch mismatch")
    prefix = ()
    compute, output = [], []
    for step, i in enumerate(reversed(range(len(a)))):
        output.append(Gate("x", (target,), prefix + ((a[i], 1), (b[i], 0))))
        if i:
            eq = scratch[step]
            compute.extend((
                Gate("x", (eq,), prefix + ((a[i], 0), (b[i], 0))),
                Gate("x", (eq,), prefix + ((a[i], 1), (b[i], 1))),
            ))
            prefix = ((eq, 1),)
    return tuple(compute + output) + inverse(compute)


@dataclass(frozen=True)
class PairCircuit:
    q: int
    width: int
    a: tuple[int, ...]
    b: tuple[int, ...]
    swap_flag: int
    orientation: int
    compare_scratch: tuple[int, ...]
    prepare: tuple[Gate, ...]
    fractional_swap: tuple[Gate, ...]
    uniform_phase: tuple[Gate, ...]
    sort: tuple[Gate, ...]

    @property
    def qubits(self):
        return 3 * self.width + 1

    @property
    def gates(self):
        return self.prepare + self.fractional_swap + self.uniform_phase + self.sort


def pair_circuit(q):
    if not isinstance(q, int) or q < 2:
        raise ValueError("alphabet size must be an integer at least two")
    n = (q - 1).bit_length()
    a, b = tuple(range(n)), tuple(range(n, 2 * n))
    flag, orientation = 2 * n, 2 * n + 1
    scratch = tuple(range(2 * n + 2, 3 * n + 1))
    prep = uniform_interval(q, b)
    spectral = ((Gate("h", (flag,)),)
                + tuple(Gate("swap", (x, y), ((flag, 1),)) for x, y in zip(a, b))
                + (Gate("h", (flag,)),))
    fractional = spectral + (Gate("phase", controls=((flag, 1),), power=1),) + inverse(spectral)
    first = uniform_interval(q, a)
    phase = inverse(first) + (Gate("phase", controls=tuple((x, 0) for x in a), power=-1),) + first
    sorting = (compare_greater(a, b, orientation, scratch)
               + tuple(Gate("swap", (x, y), ((orientation, 1),)) for x, y in zip(a, b))
               + (Gate("h", (orientation,)), Gate("x", (orientation,))))
    return PairCircuit(q, n, a, b, flag, orientation, scratch, prep, fractional, phase, sorting)


def prepare_phi_zero(q, bits, flag):
    """Prepare phi_0 without a QFT, returning the temporary flag to zero."""
    if not isinstance(q, int) or not 2 <= q <= (1 << len(bits)) or flag in bits:
        raise ValueError("invalid alphabet or preparation register")
    gates = (Gate("ry", (flag,), ratio=(1, q), adjoint=True),)
    gates += uniform_interval(q - 1, bits, ((flag, 1),))
    # Controlled increment maps [0,q-2] to [1,q-1], with no modular wrap.
    gates += tuple(Gate("x", (bits[i],), ((flag, 1),) + tuple((b, 1) for b in bits[:i]))
                   for i in reversed(range(len(bits))))
    gates += (Gate("x", (flag,)), Gate("x", (flag,), tuple((b, 0) for b in bits)))
    return gates


def simulate(gates, state, *, max_qubits=19):
    """Apply the logical bit gates, without building a dense unitary matrix."""
    out = np.asarray(state, dtype=complex).copy()
    size = out.size
    if out.ndim != 1 or size < 1 or size & (size - 1):
        raise ValueError("state must have power-of-two length")
    n = (size - 1).bit_length()
    if n > max_qubits:
        raise ValueError("finite-control simulation cap exceeded")
    indices = np.arange(size, dtype=np.int64)
    for gate in gates:
        if gate.kind not in {"x", "h", "ry", "swap", "phase"}:
            raise ValueError("unknown gate")
        needed = 2 if gate.kind == "swap" else 0 if gate.kind == "phase" else 1
        occupied = list(gate.targets) + [x for x, _ in gate.controls]
        if (len(gate.targets) != needed or len(set(occupied)) != len(occupied)
                or any(x < 0 or x >= n for x in occupied)
                or any(v not in (0, 1) for _, v in gate.controls)):
            raise ValueError("invalid gate wires")
        allowed = np.ones(size, dtype=bool)
        for wire, bit in gate.controls:
            allowed &= ((indices >> wire) & 1) == bit
        if gate.kind == "phase":
            out[allowed] *= (1j) ** (gate.power % 4)
            continue
        target = gate.targets[0]
        allowed &= ((indices >> target) & 1) == 0
        if gate.kind == "swap":
            other = gate.targets[1]
            allowed &= ((indices >> other) & 1) == 1
            zero = indices[allowed]
            one = zero ^ (1 << target) ^ (1 << other)
        else:
            zero = indices[allowed]
            one = zero ^ (1 << target)
        left, right = out[zero].copy(), out[one].copy()
        if gate.kind in {"x", "swap"}:
            out[zero], out[one] = right, left
        elif gate.kind == "h":
            out[zero], out[one] = (left + right) / math.sqrt(2), (left - right) / math.sqrt(2)
        else:
            num, den = gate.ratio
            if not 0 <= num <= den or den <= 0:
                raise ValueError("invalid rotation probability")
            c, s = math.sqrt((den - num) / den), math.sqrt(num / den)
            if gate.adjoint:
                s = -s
            out[zero], out[one] = c * left - s * right, s * left + c * right
    return out


def input_state(plan, c):
    if plan.qubits > 19:
        raise ValueError("finite-control allocation cap exceeded")
    if not 0 <= c < plan.q:
        raise ValueError("label outside alphabet")
    out = np.zeros(1 << plan.qubits, dtype=complex)
    out[:plan.q] = -1 / math.sqrt(plan.q * (plan.q - 1))
    out[c] += math.sqrt(plan.q / (plan.q - 1))
    return out


def expected_pair(plan, c):
    if plan.qubits > 19:
        raise ValueError("finite-control allocation cap exceeded")
    if not 0 <= c < plan.q:
        raise ValueError("label outside alphabet")
    out = np.zeros(1 << plan.qubits, dtype=complex)
    for other in range(plan.q):
        if other != c:
            lo, hi = sorted((other, c))
            out[lo | (hi << plan.width)] = (1 if c < other else -1) / math.sqrt(plan.q - 1)
    return np.exp(1j * math.pi / 4) * out


def resources(plan):
    """Conservative logical bounds, NOT a transpiled or physical gate count.

    With clean AND chains, each macro lowers to <=100*(controls+1)
    one/two-qubit gates over arbitrary rotations. Reuse at most max-controls
    additional clean scratch. Finite-gate rotation approximation is separate.
    """
    gates = plan.gates
    counts = Counter(g.kind for g in gates)
    controls = max((len(g.controls) for g in gates), default=0)
    return {
        "q": plan.q,
        "bit_width": plan.width,
        "macro_gates": len(gates),
        "gate_kinds": dict(sorted(counts.items())),
        "max_controls": controls,
        "structural_qubits": plan.qubits,
        "lowering_clean_qubits_upper": controls,
        "arbitrary_rotation_elementary_gates_upper": sum(100 * (len(g.controls) + 1) for g in gates),
        "nontrivial_ry_macros": counts["ry"],
        "clifford_t_compiled": False,
        "whole_decoder_compiled": False,
    }


def precision_budget(q, copies, success_lower, tv_fraction=Fraction(1, 4)):
    """Uniform error budget for forward AND inverse local pair maps only.

    Other raw-trial operations must separately fit the remaining TV budget.
    For every elementary lowered operation, error <= per_gate guarantees by
    telescoping total operator error <= local budget. Pure-state trace/TV
    distance is no larger than this bound, including reference systems.
    """
    success_lower, tv_fraction = Fraction(success_lower), Fraction(tv_fraction)
    if not isinstance(copies, int) or copies < 1 or not 0 < success_lower <= 1:
        raise ValueError("positive copies and probability bound required")
    if not 0 < tv_fraction < Fraction(1, 2):
        raise ValueError("reserve a positive part of half the margin for other operations")
    count = 2 * copies * resources(pair_circuit(q))["arbitrary_rotation_elementary_gates_upper"]
    budget = tv_fraction * success_lower
    return {"elementary_call_bound": count, "local_operator_budget": budget,
            "per_elementary_gate_error": budget / count,
            "remaining_other_operations_tv_budget": (Fraction(1, 2) - tv_fraction) * success_lower,
            "compiled_success_lower_if_all_budgets_met": success_lower / 2}
