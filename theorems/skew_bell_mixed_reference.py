"""Bounded physical skew-Bell reference, only one qutrit or one ququint.

All inputs are supplied dense density matrices, not copy-oracle access. The
physical branch explicitly forms rho**(tensor 4), permutes registers 2 and 4,
and evaluates Bell-projector Born probabilities on pairs (1,2) and (3,4).
Two independent four-copy batches produce an eight-copy difference law.
No eight-copy density matrix is allocated. This is a finite numerical
reference, not a scalable learner, source preparer, or hardware backend.

Conventions and source: arxiv.org/html/2510.06848v3, Lemma 13, Definition 37,
Theorem 43 (operator identity, before pure-state self-duality), Corollary 46.
Labels are (phase, shift), [u,v] = u_phase*v_shift-u_shift*v_phase.
The paper conjugates the POVM by U, so the physical state receives U.dagger.
The mixed-state Fourier comparison is a separate calculation; its c(u)/p
has total mass Tr(rho**2), not one. Never renormalize it into a distribution.
"""

from dataclasses import dataclass, field
from itertools import product
from numbers import Integral

import numpy as np


MAX_FOUR_COPY_DIM = 625
_TOL = 1e-10


def _prime(prime):
    if isinstance(prime, (bool, np.bool_)) or not isinstance(prime, Integral):
        raise ValueError("prime must be an integer, not a bool")
    if prime not in (3, 5):
        raise ValueError("reference supports only n=1, p=3 or 5 (dense cap 625)")
    return int(prime)


def _scalar(value, prime, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
        raise ValueError(f"{name} must be an integer, not a bool")
    if not 0 <= value < prime:
        raise ValueError(f"{name} must be a canonical field element")
    return int(value)


def _parameters(prime, a, b):
    prime = _prime(prime)
    a, b = _scalar(a, prime, "a"), _scalar(b, prime, "b")
    if (a * a + b * b) % prime != prime - 1:
        raise ValueError("skew parameters must satisfy a^2+b^2=-1 modulo p")
    return prime, a, b


def _density(rho, prime):
    rho = np.asarray(rho, dtype=complex)
    if rho.shape != (prime, prime):
        raise ValueError("rho must be a single-qudit p by p density matrix")
    if not np.all(np.isfinite(rho)):
        raise ValueError("rho must be finite")
    if not np.allclose(rho, rho.conj().T, atol=_TOL, rtol=0):
        raise ValueError("rho must be Hermitian")
    if not np.isclose(np.trace(rho), 1, atol=_TOL, rtol=0):
        raise ValueError("rho must have unit trace")
    if np.linalg.eigvalsh(rho).min() < -_TOL:
        raise ValueError("rho must be positive semidefinite")
    return rho.copy()


def _real(values):
    if np.max(np.abs(values.imag)) > _TOL:
        raise ArithmeticError("unexpected imaginary probability residue")
    return values.real.copy()


def weyl_operator(prime, phase, shift):
    """W_(z,x) = omega**(zx/2) X**x Z**z; X|q>=|q+1>."""
    p = _prime(prime)
    z, x = _scalar(phase, p, "phase"), _scalar(shift, p, "shift")
    omega = np.exp(2j * np.pi / p)
    result = np.zeros((p, p), dtype=complex)
    for q in range(p):
        result[(q + x) % p, q] = omega ** ((pow(2, -1, p) * z * x + z * q) % p)
    return result


def bell_basis(prime):
    """Columns z*p+x are |B_(z,x)> = p**(-1/2) vec(W_(z,x)).

    Pair basis index is first*p+second. The formula below constructs kets
    directly, independently of the Weyl/Fourier comparison implementation.
    """
    p = _prime(prime)
    omega = np.exp(2j * np.pi / p)
    basis = np.zeros((p * p, p * p), dtype=complex)
    for z, x, q in product(range(p), repeat=3):
        basis[((q + x) % p) * p + q, z * p + x] = (
            omega ** ((pow(2, -1, p) * z * x + z * q) % p) / np.sqrt(p)
        )
    return basis


def skew_permutation(prime, a, b):
    """Return destinations of the PHYSICAL U.dagger on four registers.

    M=[[a,b],[b,-a]], M.inverse=-M. With row-vector convention B_M|s,t>
    =|(s,t)M>, apply B_M.dagger to registers 2,4 (one-based):
    |r,s,t,u> -> |r,-a*s-b*u,t,-b*s+a*u>, all modulo p.
    Flattening is big-endian: ((r*p+s)*p+t)*p+u.
    """
    p, a, b = _parameters(prime, a, b)
    destinations = np.empty(p**4, dtype=int)
    for source, (r, s, t, u) in enumerate(product(range(p), repeat=4)):
        s_out, u_out = (-a * s - b * u) % p, (-b * s + a * u) % p
        destinations[source] = ((r * p + s_out) * p + t) * p + u_out
    return destinations


def four_copy_bell_law(rho, prime, a, b):
    """Physical Born table P[z1,x1,z2,x2], consuming four source copies.

    No purity, characteristic coefficients, or Fourier formula is used.
    Permutation indexing is exactly U.dagger rho_tensor4 U. Probabilities
    are neither clipped nor renormalized, so normalization bugs stay visible.
    """
    p, a, b = _parameters(prime, a, b)
    rho = _density(rho, p)
    pair = np.kron(rho, rho)
    four_copy_density = np.kron(pair, pair)
    inverse = np.argsort(skew_permutation(p, a, b))
    evolved = four_copy_density[np.ix_(inverse, inverse)]
    bell = bell_basis(p)
    measurement_basis = np.kron(bell, bell)
    probabilities = np.einsum(
        "ij,ij->j", measurement_basis.conj(), evolved @ measurement_basis
    )
    return _real(probabilities).reshape((p,) * 4)


def independent_difference_law(four_copy_law):
    """B[d] = sum_y P[y] P[y+d]: second fresh batch minus first.

    This is classical convolution of independent four-copy measurement
    outcomes, NOT subtraction of the two correlated pairs in one batch.
    """
    law = np.asarray(four_copy_law, dtype=complex)
    if law.ndim != 4 or len(set(law.shape)) != 1:
        raise ValueError("four-copy law must have shape (p,p,p,p)")
    p = _prime(law.shape[0])
    if not np.all(np.isfinite(law)) or np.max(np.abs(law.imag)) > _TOL:
        raise ValueError("four-copy law must be finite and real")
    law = law.real.copy()
    if (law.min() < -_TOL
            or not np.isclose(law.sum(), 1, atol=_TOL, rtol=0)):
        raise ValueError("four-copy law must be normalized and nonnegative")
    result = np.empty_like(law)
    for delta in product(range(p), repeat=4):
        shifted = np.roll(law, tuple(-x for x in delta), axis=(0, 1, 2, 3))
        result[delta] = np.sum(law * shifted)
    return result


@dataclass(frozen=True)
class SkewBellReference:
    """Finite probability tables; source charges are per physical outcome."""

    prime: int
    a: int
    b: int
    four_copy_joint: np.ndarray
    eight_copy_joint: np.ndarray
    four_copy_source_copies: int = field(default=4, init=False)
    difference_source_copies: int = field(default=8, init=False)
    physical_quantum_backend: bool = field(default=False, init=False)

    @property
    def dense_dimension(self):
        return self.prime**4

    @property
    def four_copy_first_marginal(self):
        return self.four_copy_joint.sum(axis=(2, 3))

    @property
    def eight_copy_first_marginal(self):
        return self.eight_copy_joint.sum(axis=(2, 3))


def simulate_skew_bell_mixed(rho, prime, a, b):
    """Run the bounded physical reference, with no Fourier-formula call."""
    p, a, b = _parameters(prime, a, b)
    law = four_copy_bell_law(rho, p, a, b)
    return SkewBellReference(p, a, b, law, independent_difference_law(law))


def _characteristic_squared(rho, prime):
    return np.array([
        abs(np.trace(rho @ weyl_operator(prime, z, x))) ** 2
        for z, x in product(range(prime), repeat=2)
    ]).reshape(prime, prime)


def fourier_marginal(rho, prime, a, b):
    """Independent comparison q(x)=p**(-2) sum_u omega**[x,u] c(u)c(au)c(bu).

    Valid for arbitrary mixed rho; no diagonality or purity normalization.
    Unlike the physical branch, this explicitly inspects Weyl coefficients.
    """
    p, a, b = _parameters(prime, a, b)
    rho = _density(rho, p)
    c = _characteristic_squared(rho, p)
    omega = np.exp(2j * np.pi / p)
    result = np.zeros((p, p), dtype=complex)
    for z, x, v, w in product(range(p), repeat=4):
        result[z, x] += (
            omega ** ((z * w - x * v) % p)
            * c[v, w] * c[a * v % p, a * w % p] * c[b * v % p, b * w % p]
        ) / p**2
    return _real(result)


def pure_convolution_marginal_control(rho, prime, a, b):
    """Negative control: evaluate the PURE-ONLY convolution on mixed rho.

    Marginalize sum_(u,v) p_rho(x+u) p_rho(y+v)
    p_rho(a*u+b*v) p_rho(b*u-a*v), where p_rho=c/p.
    On mixed inputs the result has mass purity**4, NOT one, and is not the
    physical law. Renormalizing it does not in general repair the identity.
    """
    p, a, b = _parameters(prime, a, b)
    rho = _density(rho, p)
    characteristic = _characteristic_squared(rho, p) / p
    result = np.zeros((p, p))
    for uz, ux, vz, vx in product(range(p), repeat=4):
        coefficient = (
            characteristic[(a * uz + b * vz) % p, (a * ux + b * vx) % p]
            * characteristic[(b * uz - a * vz) % p, (b * ux - a * vx) % p]
        )
        result += coefficient * np.roll(characteristic, (-uz, -ux), axis=(0, 1))
    return characteristic.sum() * result
