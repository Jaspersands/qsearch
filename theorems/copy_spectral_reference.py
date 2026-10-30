"""Bounded dense-matrix reference for copies-only controlled evolution.

Register order is control, data, reference (omitted when dimension one),
and finally program during each dilation. Every step consumes a fresh,
uncorrelated copy of rho and discards it. Negative time uses fresh copies;
it does not invert a consumed channel. This is a finite numerical reference,
not a spectral-projection algorithm or a quantum backend/hardware claim.
"""

from dataclasses import dataclass
from numbers import Integral, Real

import numpy as np


MAX_DATA_DIM = 3
MAX_REFERENCE_DIM = 6
MAX_STEPS = 256
_TOL = 1e-10


@dataclass(frozen=True)
class CopyEvolution:
    """Output state, fresh-copy charge, and conservative error allowance.

    half_diamond_bound is min(1, 2*t**2/n), a telescoping allowance, not
    a numerically measured diamond norm. For any supplied reference state,
    half its output trace-norm error is bounded by this allowance.
    """

    state: np.ndarray
    program_copies: int
    half_diamond_bound: float


def _integer(value, name, cap):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
        raise ValueError(f"{name} must be an integer, not a bool")
    if not 1 <= value <= cap:
        raise ValueError(f"{name} must be between 1 and {cap}")
    return int(value)


def _time(value):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError("time must be a finite real number")
    value = float(value)
    if not np.isfinite(value):
        raise ValueError("time must be a finite real number")
    return value


def _density(value, name, *, dimension=None, cap):
    matrix = np.asarray(value, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"{name} must be a square density matrix")
    size = matrix.shape[0]
    if not 1 <= size <= cap or (dimension is not None and size != dimension):
        raise ValueError(f"{name} has invalid dimensions (cap {cap})")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must be finite")
    if not np.allclose(matrix, matrix.conj().T, atol=_TOL, rtol=0):
        raise ValueError(f"{name} must be Hermitian")
    if not np.isclose(np.trace(matrix), 1, atol=_TOL, rtol=0):
        raise ValueError(f"{name} must have unit trace")
    if np.linalg.eigvalsh(matrix).min() < -_TOL:
        raise ValueError(f"{name} must be positive semidefinite")
    return matrix.copy()


def _inputs(state, rho, reference_dim):
    reference_dim = _integer(reference_dim, "reference_dim", MAX_REFERENCE_DIM)
    rho = _density(rho, "rho", cap=MAX_DATA_DIM)
    state = _density(
        state, "state", dimension=2 * len(rho) * reference_dim,
        cap=2 * MAX_DATA_DIM * MAX_REFERENCE_DIM,
    )
    return state, rho, reference_dim


def controlled_partial_swap_unitary(data_dim, theta, *, reference_dim=1):
    """Return P0 tensor I + P1 tensor (cos(theta) I - i sin(theta) SWAP).

    SWAP exchanges data and program, leaving the reference untouched.
    The largest permitted dilation dimension is 2 * 3 * 6 * 3 = 108.
    """
    d = _integer(data_dim, "data_dim", MAX_DATA_DIM)
    r = _integer(reference_dim, "reference_dim", MAX_REFERENCE_DIM)
    theta = _time(theta)
    indices = np.arange(d * r * d).reshape(d, r, d)
    swap = np.eye(d * r * d)[indices.transpose(2, 1, 0).reshape(-1)]
    identity = np.eye(d * r * d, dtype=complex)
    active = np.cos(theta) * identity - 1j * np.sin(theta) * swap
    zero = np.zeros_like(identity)
    return np.block([[identity, zero], [zero, active]])


def _step(state, rho, unitary):
    joint = np.kron(state, rho)
    evolved = unitary @ joint @ unitary.conj().T
    size, d = len(state), len(rho)
    return np.trace(evolved.reshape(size, d, size, d), axis1=1, axis2=3)


def controlled_partial_swap(state, rho, theta, *, reference_dim=1):
    """Apply one physical dilation and partial trace, consuming one copy."""
    state, rho, r = _inputs(state, rho, reference_dim)
    unitary = controlled_partial_swap_unitary(len(rho), theta, reference_dim=r)
    return _step(state, rho, unitary)


def simulate_controlled_density_exponentiation(state, rho, t, n, *, reference_dim=1):
    """Compose n fresh-copy steps for exp(-it P1 tensor rho) tensor I_ref.

    n is charged even for t=0. Both signs of t consume n fresh copies.
    Inputs are validated, never silently normalized or projected onto PSD.
    """
    n = _integer(n, "n", MAX_STEPS)
    t = _time(t)
    state, rho, r = _inputs(state, rho, reference_dim)
    unitary = controlled_partial_swap_unitary(len(rho), t / n, reference_dim=r)
    for _ in range(n):
        state = _step(state, rho, unitary)
    # Saturate before squaring to avoid overflow for large finite times.
    scaled_time = abs(t) / np.sqrt(n)
    bound = 1.0 if scaled_time >= np.sqrt(0.5) else 2 * scaled_time**2
    return CopyEvolution(state, n, float(bound))


def ideal_controlled_evolution(state, rho, t, *, reference_dim=1):
    """Dense ideal comparison only; diagonalizing rho is not a copy oracle."""
    t = _time(t)
    state, rho, r = _inputs(state, rho, reference_dim)
    eigenvalues, vectors = np.linalg.eigh(rho)
    data_unitary = (vectors * np.exp(-1j * t * eigenvalues)) @ vectors.conj().T
    active = np.kron(data_unitary, np.eye(r))
    identity = np.eye(len(rho) * r, dtype=complex)
    zero = np.zeros_like(identity)
    unitary = np.block([[identity, zero], [zero, active]])
    return unitary @ state @ unitary.conj().T
