"""Independent finite controls and an easy exact MPO; no research instances."""

import math

import numpy as np
from scipy.linalg import expm

from paired_mpo import MPO, PAULI


def word_matrix(word):
    result = np.array([[1]], dtype=complex)
    for letter in word:
        result = np.kron(result, PAULI[letter])
    return result


def sector_filter(z, interactions=True):
    c = [(-1)**((f & z).bit_count()) for f in (1, 2, 3)]
    terms = [(0.7, "XII"), (-0.4, "IXI"), (0.6, "IIX"),
             (0.3 + 0.4*c[0], "ZII"), (-0.2 + 0.5*c[1], "IZI"),
             (0.1 - 0.3*c[2], "IIZ"), (0.5, "ZZI"), (-0.4, "IZZ")]
    h = sum(value * word_matrix(word) for value, word in terms
            if interactions or word not in ("ZZI", "IZZ"))
    h += (0.6*c[0] - 0.3*c[1] + 0.2*c[2]) * np.eye(8)
    return expm(-0.7 * h / 2)


def direct_tfd_expectation(filters, cl, cr, a, b):
    """Exponential reference on the FULL central/local system, capped at 8 qubits."""
    r, n = len(cl), len(a)
    if r + n > 8 or len(filters) != 2**r or len(cr) != r or len(b) != n:
        raise ValueError("Invalid or oversized dense reference")
    d = 2**n
    if any(f.shape != (d, d) for f in filters):
        raise ValueError("Invalid filter dimensions")
    full = np.zeros((2**r*d, 2**r*d), dtype=complex)
    for z, block in enumerate(filters):
        full[d*z:d*(z+1), d*z:d*(z+1)] = block
    # Central integer bit zero is the first character in the public word.
    left = np.kron(word_matrix(cl[::-1]), word_matrix(a))
    right = np.kron(word_matrix(cr[::-1]), word_matrix(b))
    value = np.trace(full.conj().T @ left @ full @ right.T) / np.vdot(full, full)
    if abs(value.imag) > 1e-10:
        raise ArithmeticError("Hermitian observable has nonreal expectation")
    return float(value.real)


def exact_ising_mpo(n, coupling):
    """Bond-two diagonal exp(coupling sum Z_i Z_(i+1)); an EASY calibration."""
    if n < 2 or not math.isfinite(coupling) or abs(coupling) > 10:
        raise ValueError("Invalid calibration parameters")
    first = np.zeros((1, 2, 2, 2), dtype=complex)
    middle = np.zeros((2, 2, 2, 2), dtype=complex)
    last = np.zeros((2, 2, 2, 1), dtype=complex)
    for s in range(2):
        first[0, s, s, s] = 1
        for previous in range(2):
            value = math.exp(coupling * (-1)**(s + previous))
            middle[previous, s, s, s] = value
            last[previous, s, s, 0] = value
    return MPO((first,) + tuple(middle.copy() for _ in range(n-2)) + (last,))
