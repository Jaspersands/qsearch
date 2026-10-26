"""Public odd-prime Clifford plans with exact symmetric-Weyl conventions.

Known modular Clifford synthesis, not a new algorithm or circuit search.
The output is an O(R^2) list of one/two-qudit arithmetic primitives, not a
dense p^R matrix or a fault-tolerant qubit backend. See the class-four note.
No hidden support, potential, phase coefficients or state copies are inputs.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import (
    _canonical, _identity, _product, _transpose, verify_alignment,
)


@dataclass(frozen=True)
class CliffordGate:
    kind: str
    sites: tuple[int, ...]
    parameter: int = 0


@dataclass(frozen=True)
class PrimeCliffordPlan:
    p: int
    width: int
    symplectic: tuple[tuple[int, ...], ...]
    gates: tuple[CliffordGate, ...]

    @property
    def gate_bound(self):
        return 4*self.width*self.width+3*self.width

    @property
    def primitive_counts(self):
        return dict(Counter(gate.kind for gate in self.gates))


def _validate_gate(gate, p, width):
    if not isinstance(gate, CliffordGate):
        raise ValueError("CliffordGate primitive required")
    arity = {"fourier": 1, "scale": 1, "phase": 1, "add": 2, "cz": 2, "swap": 2}
    if gate.kind not in arity or len(gate.sites) != arity[gate.kind]:
        raise ValueError("unknown primitive or wrong arity")
    if (any(type(i) is not int or not 0 <= i < width for i in gate.sites)
            or len(set(gate.sites)) != len(gate.sites)):
        raise ValueError("distinct valid qudit sites required")
    if type(gate.parameter) is not int:
        raise ValueError("integer primitive parameter required")
    if gate.kind == "fourier":
        if gate.parameter not in (-1, 1):
            raise ValueError("Fourier sign must be +1 or -1")
    elif gate.kind == "swap":
        if gate.parameter:
            raise ValueError("swap has no field parameter")
    elif not 0 <= gate.parameter < p or (gate.kind == "scale" and not gate.parameter):
        raise ValueError("canonical field parameter required, nonzero for scale")


def _left_action(matrix, gate, p):
    """Left multiply a tableau by a primitive using O(R) field operations."""
    r = len(matrix)//2
    i = gate.sites[0]
    value = gate.parameter
    if gate.kind == "fourier":
        x, z = matrix[i], matrix[r+i]
        matrix[i] = [(-value*t) % p for t in z]
        matrix[r+i] = [(value*t) % p for t in x]
    elif gate.kind == "scale":
        matrix[i] = [(value*t) % p for t in matrix[i]]
        matrix[r+i] = [(pow(value, -1, p)*t) % p for t in matrix[r+i]]
    elif gate.kind == "phase":
        matrix[r+i] = [(z+value*x) % p for x, z in zip(matrix[i], matrix[r+i])]
    else:
        j = gate.sites[1]
        if gate.kind == "swap":
            matrix[i], matrix[j] = matrix[j], matrix[i]
            matrix[r+i], matrix[r+j] = matrix[r+j], matrix[r+i]
        elif gate.kind == "add":
            matrix[j] = [(y+value*x) % p for x, y in zip(matrix[i], matrix[j])]
            matrix[r+i] = [(x-value*y) % p for x, y in zip(matrix[r+i], matrix[r+j])]
        else:  # cz: omega^(value*t_i*t_j)
            matrix[r+i] = [(z+value*x) % p for z, x in zip(matrix[r+i], matrix[j])]
            matrix[r+j] = [(z+value*x) % p for z, x in zip(matrix[r+j], matrix[i])]


def symplectic_action(p, width, gates):
    """Replay a chronological primitive list, without Hilbert-space tables."""
    ring(p)
    if type(width) is not int or width < 1:
        raise ValueError("positive qudit width required")
    matrix = _identity(2*width)
    for gate in gates:
        _validate_gate(gate, p, width)
        _left_action(matrix, gate, p)
    return tuple(map(tuple, matrix))


def _inverse(gate, p):
    if gate.kind == "fourier":
        parameter = -gate.parameter
    elif gate.kind == "scale":
        parameter = pow(gate.parameter, -1, p)
    else:
        parameter = -gate.parameter % p
    return CliffordGate(gate.kind, gate.sites, parameter)


def compile_symplectic(p, symplectic):
    """Deterministic symplectic elimination, including singular X/X blocks.

    D(x,z)|t> = omega^(x.z/2+z.t)|t+x> and Omega((x,z),(a,b))=z.a-x.b.
    Every emitted primitive has EXACT covariance D(v) -> D(S_gate v),
    not just equality up to a v-dependent phase. A global circuit phase
    is irrelevant. Gate matrices and the universal reduction proof are
    documented in CLASS_FOUR_VARIABLE_RADICAL_SOURCE.md.
    """
    ring(p)
    if not symplectic or len(symplectic) % 2:
        raise ValueError("positive even-dimensional symplectic matrix required")
    n = len(symplectic)
    for row in symplectic:
        _canonical(row, n, p)
    r = n//2
    form = [[0]*n for _ in range(n)]
    for j in range(r):
        form[j][r+j], form[r+j][j] = p-1, 1
    matrix = [list(row) for row in symplectic]
    if _product(_product(_transpose(matrix), form, p), matrix, p) != form:
        raise ValueError("matrix does not preserve the declared symplectic form")
    reduction = []

    def emit(kind, sites, parameter=0):
        if (kind in ("phase", "cz", "add") and not parameter) or (kind == "scale" and parameter == 1):
            return
        gate = CliffordGate(kind, sites, parameter)
        _validate_gate(gate, p, r)
        _left_action(matrix, gate, p)
        reduction.append(gate)

    def upper(sites, parameter):
        # x -> x+Bz equals F^-1 (z -> z-Bx) F on these sites.
        if not parameter:
            return
        for site in sites:
            emit("fourier", (site,), 1)
        emit("phase" if len(sites) == 1 else "cz", sites, -parameter % p)
        for site in reversed(sites):
            emit("fourier", (site,), -1)

    for j in range(r):
        pivot = next((i for i in range(j, r) if matrix[i][j]), None)
        if pivot is None:
            pivot = next(i for i in range(j, r) if matrix[r+i][j])
            emit("fourier", (pivot,), 1)
        if pivot != j:
            emit("swap", (j, pivot))
        emit("scale", (j,), pow(matrix[j][j], -1, p))
        for i in range(j+1, r):
            emit("add", (j, i), -matrix[i][j] % p)
        for i in range(j+1, r):
            emit("cz", (j, i), -matrix[r+i][j] % p)
        emit("phase", (j,), -matrix[r+j][j] % p)
        if any(matrix[i][j] != int(i == j) for i in range(n)):
            raise ArithmeticError("first symplectic-column reduction failed")
        if matrix[r+j][r+j] != 1:
            raise ArithmeticError("symplectic partner normalization failed")
        for i in range(j+1, r):
            emit("add", (i, j), matrix[r+i][r+j])
        for i in range(j+1, r):
            upper((j, i), -matrix[i][r+j] % p)
        upper((j,), -matrix[j][r+j] % p)
        if any(matrix[i][r+j] != int(i == r+j) for i in range(n)):
            raise ArithmeticError("second symplectic-column reduction failed")
    if matrix != _identity(n):
        raise ArithmeticError("symplectic elimination did not reach identity")
    gates = tuple(_inverse(gate, p) for gate in reversed(reduction))
    plan = PrimeCliffordPlan(p, r, tuple(map(tuple, symplectic)), gates)
    if len(gates) > plan.gate_bound or symplectic_action(p, r, gates) != plan.symplectic:
        raise ArithmeticError("compiled primitive plan failed exact replay")
    return plan


def compile_alignment(alignment):
    """Realize a verified public jet alignment; no hidden data is accepted."""
    if not verify_alignment(alignment):
        raise ValueError("valid public jet alignment required")
    return compile_symplectic(alignment.maps.p, alignment.symplectic)
