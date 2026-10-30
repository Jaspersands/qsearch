"""Bounded paired-sector MPO contraction, not a Gibbs/MPO preparation backend.

Thermal MPO construction and central sampling are separately paid inputs.
NumPy arithmetic here is a diagnostic, not an interval certificate.
"""

from dataclasses import dataclass
from fractions import Fraction
import math

import numpy as np


PAULI = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.diag([1, -1]).astype(complex),
}


@dataclass(frozen=True)
class MPO:
    tensors: tuple
    log_scale: float = 0.0

    def __post_init__(self):
        if not self.tensors or not math.isfinite(self.log_scale):
            raise ValueError("A nonempty finite MPO is required")
        previous = 1
        for tensor in self.tensors:
            if tensor.ndim != 4 or tensor.shape[:3] != (previous, 2, 2):
                raise ValueError("Expected (left, row, column, right) qubit tensors")
            if not np.all(np.isfinite(tensor)) or tensor.shape[3] < 1:
                raise ValueError("Nonfinite or empty tensor")
            previous = tensor.shape[3]
        if previous != 1:
            raise ValueError("Open right bond")

    @property
    def n(self):
        return len(self.tensors)


def pauli_word(word, n):
    if len(word) != n or any(letter not in PAULI for letter in word):
        raise ValueError("Invalid Pauli word")
    return tuple(PAULI[letter] for letter in word)


def overlap(left, right, a_word, b_word):
    """Return phase, log magnitude of Tr(left^dag A right B^T)."""
    if left.n != right.n:
        raise ValueError("MPO lengths differ")
    a = pauli_word(a_word, left.n)
    b = pauli_word(b_word, left.n)
    env = np.ones((1, 1), dtype=complex)
    scale = left.log_scale + right.log_scale
    for lt, rt, ai, bi in zip(left.tensors, right.tensors, a, b):
        # bi[j,l], NOT bi[l,j], implements B^T in the matrix trace.
        env = np.einsum("ab,aijc,ik,bkld,jl->cd", env, lt.conj(), ai, rt, bi,
                        optimize=True)
        size = float(np.max(np.abs(env)))
        if size == 0:
            return 0j, -math.inf
        if not math.isfinite(size):
            raise ArithmeticError("Nonfinite contraction; increase precision")
        env /= size
        scale += math.log(size)
    value = complex(env[0, 0])
    return value / abs(value), scale + math.log(abs(value))


def log_norm_squared(mpo):
    phase, magnitude = overlap(mpo, mpo, "I" * mpo.n, "I" * mpo.n)
    if not math.isfinite(magnitude) or abs(phase - 1) > 1e-8:
        raise ArithmeticError("Invalid or zero MPO norm")
    return magnitude


def paired_value(left, right, a_word, b_word, phase=1):
    if abs(abs(phase) - 1) > 1e-10:
        raise ValueError("Observable phase must have unit modulus")
    lnorm, rnorm = log_norm_squared(left), log_norm_squared(right)
    angle, magnitude = overlap(left, right, a_word, b_word)
    if angle == 0:
        return 0.0
    denominator = float(np.logaddexp(lnorm, rnorm))
    value = 2 * (phase * angle).real * math.exp(magnitude - denominator)
    if not math.isfinite(value) or abs(value) > 1 + 1e-8:
        raise ArithmeticError("Cauchy-Schwarz bound violated numerically")
    return value


def masks(word):
    pauli_word(word, len(word))
    xmask = sum(1 << i for i, letter in enumerate(word) if letter in "XY")
    zmask = sum(1 << i for i, letter in enumerate(word) if letter in "YZ")
    return xmask, zmask, word.count("Y")


def sector_value(z, get_mpo, central_left, central_right, local_left, local_right):
    """Uses two requested sectors only; no enumeration of central labels."""
    if len(central_left) != len(central_right) or not 0 <= z < 2**len(central_left):
        raise ValueError("Invalid central word/label")
    x, zz, y = masks(central_left)
    xp, zzp, yp = masks(central_right)
    if x != xp:
        return 0.0
    partner = z ^ x
    phase = (1j ** (y + yp)) * (-1 if ((zz ^ zzp) & partner).bit_count() % 2 else 1)
    return paired_value(get_mpo(z), get_mpo(partner), local_left, local_right, phase)


def error_budget(eta, sampler_tv, arithmetic=Fraction(0)):
    eta, sampler_tv, arithmetic = map(Fraction, (eta, sampler_tv, arithmetic))
    if not 0 <= eta < 1 or not 0 <= sampler_tv <= 1 or not 0 <= arithmetic:
        raise ValueError("Invalid error contract")
    return {
        "mpo_bias": 4 * eta + 2 * eta * eta,
        "sampling_bias": 2 * sampler_tv,
        "arithmetic_bias": arithmetic,
        "total_bias": 4 * eta + 2 * eta * eta + 2 * sampler_tv + arithmetic,
    }


def dense_to_mpo(matrix, n):
    """Bounded TEST adapter; exponential storage, no thermal guarantee."""
    if not 1 <= n <= 8 or matrix.shape != (2**n, 2**n):
        raise ValueError("Dense diagnostic is limited to 1..8 qubits")
    order = [j for i in range(n) for j in (i, n + i)]
    rest = np.asarray(matrix, dtype=complex).reshape((2,) * (2*n)).transpose(order)
    rest = rest.reshape((4,) * n)
    tensors, rank = [], 1
    for i in range(n - 1):
        u, singular, vh = np.linalg.svd(rest.reshape(rank * 4, -1), full_matrices=False)
        new_rank = len(singular)
        tensors.append(u.reshape(rank, 2, 2, new_rank))
        rest = singular[:, None] * vh
        rank = new_rank
    tensors.append(rest.reshape(rank, 2, 2, 1))
    return MPO(tuple(tensors))
