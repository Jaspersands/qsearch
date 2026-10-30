"""Bounded polar tangents and capped dense controls, not a scalable preparer.

The matrix routines cost exponentially in patch size. The schedule control
reads exact target states and must never be presented as native state access.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import math

import numpy as np
from scipy.linalg import eigh, expm, svd


def trace_norm(matrix):
    return float(np.sum(svd(matrix, compute_uv=False)))


def _hermitian(matrix):
    matrix = np.asarray(matrix, dtype=complex)
    if (matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]
            or not 1 <= len(matrix) <= 256 or not np.isfinite(matrix).all()
            or not np.allclose(matrix, matrix.conj().T, atol=1e-11, rtol=0)):
        raise ValueError("finite Hermitian matrix of dimension at most 256 required")
    return (matrix + matrix.conj().T) / 2


def density(matrix):
    matrix = _hermitian(matrix)
    if abs(np.trace(matrix) - 1) > 1e-10 or eigh(matrix, eigvals_only=True)[0] < -1e-10:
        raise ValueError("positive trace-one density matrix required")
    return matrix


def project_density(matrix):
    """Euclidean projection onto PSD trace-one matrices, not clip/renormalize."""
    matrix = _hermitian(matrix)
    values, vectors = eigh(matrix)
    descending = values[::-1]
    shifts = (np.cumsum(descending) - 1) / np.arange(1, len(values) + 1)
    active = np.flatnonzero(descending > shifts)
    theta = shifts[active[-1]]
    projected = np.maximum(values - theta, 0)
    return (vectors * projected) @ vectors.conj().T


def tangent_loss(rho, observable, generator):
    mean = float(np.trace(rho @ observable).real)
    comm = observable @ generator - generator @ observable
    return float((1 - mean**2 + np.trace(
        rho @ (generator.conj().T @ generator - comm))).real)


@dataclass(frozen=True)
class Tangent:
    generator: np.ndarray
    loss: float
    off_diagonal_trace_norm: float
    amplitude: float


def polar_tangent(rho, observable):
    """Minimize loss over K=c[[0,W],[-W*,0]], 0<=c<=1, W unitary.

    The eigenspaces of the supplied Hermitian involution must have equal
    dimension (as for a nonidentity Pauli). No eigenvalue of rho is inverted.
    """
    rho, observable = density(rho), _hermitian(observable)
    size = len(rho)
    if (observable.shape != rho.shape or size % 2
            or not np.allclose(observable @ observable, np.eye(size), atol=1e-10, rtol=0)):
        raise ValueError("matching balanced Hermitian involution required")
    values, vectors = eigh(observable)
    positive, negative = np.flatnonzero(values > 0), np.flatnonzero(values < 0)
    if len(positive) != size // 2 or len(negative) != size // 2:
        raise ValueError("involution must have equal eigenspace dimensions")
    basis = vectors[:, np.concatenate((positive, negative))]
    rotated = basis.conj().T @ rho @ basis
    half = size // 2
    off = rotated[:half, half:]
    left, singular, right = svd(off, full_matrices=True)
    r = float(np.sum(singular))
    amplitude = min(1.0, 2 * r)
    block = amplitude * (left @ right)
    zero = np.zeros_like(block)
    generator = basis @ np.block([[zero, block], [-block.conj().T, zero]]) @ basis.conj().T
    return Tangent(generator, tangent_loss(rho, observable, generator), r, amplitude)


def pauli(word):
    alphabet = {"I": np.eye(2), "X": np.array([[0, 1], [1, 0]]),
                "Y": np.array([[0, -1j], [1j, 0]]), "Z": np.diag([1, -1])}
    if not isinstance(word, str) or not 1 <= len(word) <= 8 or set(word) - alphabet.keys():
        raise ValueError("Pauli word on 1 through 8 qubits required")
    out = np.ones((1, 1), dtype=complex)
    for letter in word:
        out = np.kron(out, alphabet[letter])
    return out


def reconstruct_marginal(qubits, expectation):
    """Reference Pauli reconstruction. The callback access is NOT supplied here."""
    if type(qubits) is not int or not 1 <= qubits <= 5:
        raise ValueError("dense reconstruction control limited to 1 through 5 qubits")
    size, raw = 1 << qubits, np.zeros((1 << qubits, 1 << qubits), dtype=complex)
    for letters in product("IXYZ", repeat=qubits):
        word = "".join(letters)
        value = 1.0 if set(word) == {"I"} else expectation(word)
        if not np.isreal(value) or not np.isfinite(value):
            raise ValueError("finite real Pauli estimates required")
        raw += float(value) * pauli(word) / size
    return project_density(raw)


def tfd_pauli_pullback(vertices, edges, word):
    """Pull Q through W: W|TFD>=|pilot>|0>. Return (sign, word) or None.

    Registers are L_0,...,L_(m-1),R_0,...,R_(m-1). This explicit canonical
    Clifford preserves all Y phases; None means an X/Y on a zero ancilla.
    """
    if (type(vertices) is not int or not 1 <= vertices <= 4096
            or not isinstance(word, str) or len(word) != 2 * vertices
            or set(word) - set("IXYZ")):
        raise ValueError("explicit Pauli on the paired canonical register required")
    normalized = set()
    for edge in edges:
        if (len(edge) != 2 or any(type(i) is not int or not 0 <= i < vertices for i in edge)
                or edge[0] == edge[1]):
            raise ValueError("simple graph edge required")
        edge = tuple(sorted(edge))
        if edge in normalized:
            raise ValueError("duplicate edge")
        normalized.add(edge)
    x = sum(1 << i for i, letter in enumerate(word) if letter in "XY")
    z = sum(1 << i for i, letter in enumerate(word) if letter in "ZY")
    phase = word.count("Y")
    for i in range(vertices):
        if (x >> (vertices + i)) & 1:
            x ^= 1 << i
        if (z >> i) & 1:
            z ^= 1 << (vertices + i)
    for j, i in sorted(normalized):
        a, b = i, vertices + j
        xa, xb = (x >> a) & 1, (x >> b) & 1
        phase += 2 * xa * xb
        z ^= (xa << b) | (xb << a)
    for i in range(vertices, 2 * vertices):
        xi, zi = (x >> i) & 1, (z >> i) & 1
        phase += 2 * xi * zi
        if xi != zi:
            x ^= 1 << i
            z ^= 1 << i
    if x >> vertices:
        return None
    pulled = "".join({(0, 0): "I", (1, 0): "X", (0, 1): "Z", (1, 1): "Y"}[
        ((x >> i) & 1, (z >> i) & 1)] for i in range(vertices))
    phase = (phase - pulled.count("Y")) % 4
    if phase % 2:
        raise ArithmeticError("Hermitian pullback acquired an imaginary scalar")
    return (-1 if phase == 2 else 1), pulled


def _layout(keep, qubits):
    keep = tuple(keep)
    if (type(qubits) is not int or not 1 <= qubits <= 8 or not keep
            or len(set(keep)) != len(keep)
            or any(type(k) is not int or not 0 <= k < qubits for k in keep)):
        raise ValueError("distinct retained qubits in a capped register required")
    return keep + tuple(k for k in range(qubits) if k not in keep)


def reduced_operator(matrix, keep, qubits):
    """Partial trace of an arbitrary operator; big-endian qubit numbering."""
    order = _layout(keep, qubits)
    matrix = np.asarray(matrix, dtype=complex)
    if matrix.shape != (1 << qubits, 1 << qubits):
        raise ValueError("operator dimension does not match register")
    a, b = 1 << len(keep), 1 << (qubits - len(keep))
    permuted = matrix.reshape([2] * (2 * qubits)).transpose(
        order + tuple(k + qubits for k in order)).reshape(a, b, a, b)
    return np.einsum("abcb->ac", permuted)


def lift_operator(matrix, keep, qubits):
    order = _layout(keep, qubits)
    matrix = np.asarray(matrix, dtype=complex)
    if matrix.shape != (1 << len(keep), 1 << len(keep)):
        raise ValueError("local operator dimension does not match patch")
    inverse = tuple(np.argsort(order))
    out = np.kron(matrix, np.eye(1 << (qubits - len(keep))))
    return out.reshape([2] * (2 * qubits)).transpose(
        inverse + tuple(k + qubits for k in inverse)).reshape(1 << qubits, 1 << qubits)


def far_covariance(psi, observable, patch, qubits):
    """Exact trace-norm supremum over ALL far observables, not Pauli probes."""
    _layout(patch, qubits)
    far = tuple(i for i in range(qubits) if i not in patch)
    if not far:
        return 0.0
    mean = np.vdot(psi, observable @ psi).real
    weighted = np.outer((observable @ psi - mean * psi), psi.conj())
    return trace_norm(reduced_operator(weighted, far, qubits))


def dense_schedule_control(terms, initial, beta, steps, patches):
    """Exact target-state access for a small validation, NOT a native algorithm."""
    initial = np.asarray(initial, dtype=complex)
    qubits = int(math.log2(initial.size)) if initial.size else 0
    if (initial.ndim != 1 or not 1 <= qubits <= 6 or initial.size != 1 << qubits
            or not np.isfinite(initial).all() or abs(np.linalg.norm(initial) - 1) > 1e-10
            or type(steps) is not int or not 1 <= steps <= 128
            or not np.isfinite(beta) or beta < 0 or not terms or len(terms) != len(patches)):
        raise ValueError("bounded normalized dense schedule control required")
    matrices, local_ops = [], []
    for (coupling, word), patch in zip(terms, patches):
        if not np.isfinite(coupling) or len(word) != qubits:
            raise ValueError("finite coupling and full register Pauli required")
        _layout(patch, qubits)
        if any(letter != "I" and k not in patch for k, letter in enumerate(word)):
            raise ValueError("patch omits observable support")
        local = pauli("".join(word[k] for k in patch))
        if np.allclose(local, np.eye(len(local))):
            raise ValueError("identity terms should be removed before the control")
        matrices.append(pauli(word))
        local_ops.append(local)
    lam = sum(abs(j) for j, _ in terms)
    if beta * lam > 20:
        raise ValueError("dense path control limited to beta*norm_sum <= 20")
    hamiltonian = sum(j * op for (j, _), op in zip(terms, matrices))
    energies, eigenvectors = eigh(hamiltonian)
    coordinates = eigenvectors.conj().T @ initial

    def target(time):
        # A common spectral shift avoids irrelevant exponential overflow.
        out = eigenvectors @ (np.exp(-time * (energies - energies[0]) / 2) * coordinates)
        return out / np.linalg.norm(out)

    state, dt, max_residual, max_eta = initial.copy(), beta / steps, 0.0, 0.0
    accumulated_tangent = 0.0
    for index in range(steps):
        exact = target(index * dt)
        pure = np.outer(exact, exact.conj())
        weighted_residual = 0.0
        for (coupling, _), op, local, patch in zip(terms, matrices, local_ops, patches):
            rho = reduced_operator(pure, patch, qubits)
            k = lift_operator(polar_tangent(rho, local).generator, patch, qubits)
            tangent = (op - np.vdot(exact, op @ exact).real * np.eye(len(op))) @ exact
            residual = float(np.linalg.norm(tangent - k @ exact))
            eta = far_covariance(exact, op, patch, qubits)
            max_residual, max_eta = max(max_residual, residual), max(max_eta, eta)
            if residual**2 > 2 * eta + 2e-10:
                raise AssertionError("polar tangent covariance bound failed")
            weighted_residual += abs(coupling) * residual / 2
            state = expm(-dt * coupling * k / 2) @ state
        accumulated_tangent += dt * weighted_residual
    error = float(np.linalg.norm(state - target(beta)))
    return {"steps": steps, "vector_error": error,
            "max_tangent_residual": max_residual, "max_far_covariance": max_eta,
            "tangent_error_bound": accumulated_tangent,
            "discretization_bound": beta**2 * lam**2 / steps,
            "total_bound": accumulated_tangent + beta**2 * lam**2 / steps,
            "uses_dense_exact_target_access": True, "quantum_executed": False}


def endpoint_plan(terms, beta, norm_sum, epsilon, patch_qubits):
    if type(terms) is not int or terms < 1 or type(patch_qubits) is not int or not 1 <= patch_qubits <= 4096:
        raise ValueError("positive term count and patch size at most 4096 required")
    beta, norm_sum, epsilon = F(beta), F(norm_sum), F(epsilon)
    if beta < 0 or norm_sum < 0 or not 0 < epsilon < 1:
        raise ValueError("nonnegative time/norm and error in (0,1) required")
    length = beta * norm_sum
    residual = epsilon / (2 * (1 + length))
    steps = max(1, math.ceil(4 * length**2 / epsilon))
    dimension = 1 << patch_qubits
    covariance = residual**2 / 8
    trace_error = residual**2 / 40
    return {"steps": steps, "local_dimension_log2": patch_qubits,
            "pauli_estimates": terms * steps * (dimension**2 - 1),
            "local_covariance_required": str(covariance),
            "marginal_trace_error": str(trace_error),
            "pauli_additive_error": str(trace_error / dimension),
            "polar_objective_error_budget": str(residual**2 / 2),
            "gate_operator_error": str(epsilon / (4 * terms * steps)),
            "vector_error_budget": str(length * residual / 2 + length**2 / steps + epsilon / 4),
            "exact_target_marginals_granted": False,
            "production_observable_estimator_implemented": False,
            "correlation_promise_verified": False, "quantum_executed": False}


def ball_ledger(vertices, degree, radius):
    if any(type(v) is not int or v < 0 for v in (vertices, degree, radius)) or vertices < 1:
        raise ValueError("positive vertex count and nonnegative degree/radius required")
    if degree == 0:
        size = 1
    elif degree == 1:
        size = 1 + int(radius > 0)
    else:
        size = 1 + degree * sum((degree - 1)**k for k in range(radius))
    size = min(vertices, size)
    return {"vertices": vertices, "degree_bound": degree, "radius": radius,
            "ball_vertices_bound": size, "paired_patch_qubits_bound": 2 * size,
            "pauli_count_log2_bound": 4 * size, "ledger_only": True}
