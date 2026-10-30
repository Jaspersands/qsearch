"""Source-side weak-isogeny attack, conditional on genuine input maps.

No unknown isogeny, target order, or hidden kernel is an algorithm input.
The callbacks must supply actual small-torsion actions in compatible
symplectic frames. This is arithmetic extraction, not a geometry backend.
"""

from dataclasses import dataclass
from math import isqrt, prod
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "kernel-output-2026-10-23"))
from kernel_output import (
    action, alternating_form, check_split, integer_matrix, inverse_mod,
    matrix_multiply, matrix_star, mod, product_actions,
)


def _prime(value):
    if type(value) is not int or value < 3 or not isprime(value):
        raise ValueError("odd prime required")


def _matrix(value, shape):
    value = integer_matrix(value)
    if value.shape != shape:
        raise ValueError(f"matrix shape must be {shape}")
    return value


def adjoint(value):
    value = _matrix(value, (4, 4))
    form = alternating_form(2)
    return form.inv() * value.T * form


def source_gram(order):
    basis = eye(16)
    gram = zeros(16)
    for i in range(16):
        for j in range(16):
            z = matrix_multiply(order, matrix_star(order, basis[:, i]), basis[:, j])
            gram[i, j] = (order.traces * (z[:4, :] + z[12:, :]))[0]
    gram = integer_matrix(gram)
    if gram.is_positive_definite is not True:
        raise ValueError("positive definite integral source Gram required")
    return gram


@dataclass(frozen=True)
class ResiduePacket:
    weak_action: Matrix
    target_maps: tuple


@dataclass(frozen=True)
class PullbackResult:
    coordinates: tuple
    trace_pairings: tuple
    primes: tuple
    modulus: int
    pairing_bound: int
    weak_basis_points_required: int
    target_basis_points_required: int
    source_basis_points_required: int
    norm_bounds: tuple


def weak_pullback_actions(ell, prime, packet):
    """Compute phi^dagger gamma phi = ell W^-1 gamma W modulo prime."""
    _prime(ell)
    _prime(prime)
    if prime == ell:
        raise ValueError("auxiliary prime must differ from ell")
    w = mod(_matrix(packet.weak_action, (4, 4)), prime)
    winv = inverse_mod(w, prime)
    form = alternating_form(2)
    pairing = mod(w.T * form * w, prime)
    multiplier = int(pairing[0, 1])
    if not multiplier or pairing != mod(multiplier * form, prime):
        raise ValueError("weak action must be a symplectic similitude")
    ratio = multiplier * pow(ell, -1, prime) % prime
    if pow(ratio, (prime - 1) // 2, prime) != 1:
        raise ValueError("similitude multiplier is incompatible with a common scalar")
    return tuple(mod(ell * winv * _matrix(gamma, (4, 4)) * w, prime)
                 for gamma in packet.target_maps)


def reconstruct_pullbacks(order, ell, characteristic, norm_bounds, auxiliary_primes,
                          split_at, observe_at, *, max_auxiliary_prime):
    """Bounded CRT from legal small levels; reject an insufficient level plan.

    split_at(r) returns the PUBLIC source quaternion splitting at r.
    observe_at(r) returns one common-scalar weak basis and target-map bases.
    Norm bounds and global map compatibility are supplied promises, not
    inferred from finite residue consistency checks.
    """
    _prime(ell)
    _prime(characteristic)
    if ell == characteristic:
        raise ValueError("ell must differ from the characteristic")
    if type(max_auxiliary_prime) is not int or max_auxiliary_prime < 3:
        raise ValueError("explicit small auxiliary-prime cap required")
    bounds = tuple(norm_bounds)
    if not bounds or any(type(x) is not int or x < 0 for x in bounds):
        raise ValueError("nonnegative integral norm bounds for at least one map required")
    gram = source_gram(order)
    if gram.det() != characteristic**8:
        raise ValueError("source discriminant does not match the supplied characteristic")
    bound = max(isqrt(ell * ell * b * int(gram[i, i]))
                for b in bounds for i in range(16))
    primes = tuple(auxiliary_primes)
    if len(set(primes)) != len(primes):
        raise ValueError("auxiliary primes must be distinct")
    for r in primes:
        _prime(r)
        if r in (ell, characteristic) or r > max_auxiliary_prime:
            raise ValueError("illegal auxiliary prime or exceeded level cap")
    if prod(primes) <= 2 * bound:
        raise ValueError("insufficient CRT modulus for the supplied norm bounds")

    residues = [zeros(16, 1) for _ in bounds]
    modulus, used = 1, []
    for r in primes:
        splitting = tuple(split_at(r))
        check_split(order, splitting, r)
        source_actions = product_actions(splitting)
        packet = observe_at(r)
        if len(packet.target_maps) != len(bounds):
            raise ValueError("target map count changed between levels")
        pullbacks = weak_pullback_actions(ell, r, packet)
        inverse = pow(modulus, -1, r)
        for j, a in enumerate(pullbacks):
            for i, e in enumerate(source_actions):
                b = int((adjoint(e) * a).trace()) % r
                residues[j][i] += modulus * ((b - int(residues[j][i])) * inverse % r)
        modulus *= r
        used.append(r)
        if modulus > 2 * bound:
            break

    coordinates, pairings = [], []
    ginv = gram.inv()
    for vector, norm_bound in zip(residues, bounds):
        centered = vector.applyfunc(lambda x: int(x) if 2 * x < modulus else int(x) - modulus)
        if any(abs(x) > bound for x in centered):
            raise ValueError("reconstructed pairing violates the norm bound")
        x = integer_matrix(ginv * centered)
        if int((x.T * gram * x)[0]) > ell * ell * norm_bound:
            raise ValueError("reconstructed map violates the norm bound")
        coordinates.append(x)
        pairings.append(centered)
    return PullbackResult(tuple(coordinates), tuple(pairings), tuple(used), modulus, bound,
                          4 * len(used), 4 * len(bounds) * len(used), 64 * len(used), bounds)


def column_basis(matrix, prime):
    """Pivot columns over the actual residue field, never over Q."""
    work = mod(matrix, prime)
    original, pivot_row, pivots = work.copy(), 0, []
    for col in range(work.cols):
        row = next((r for r in range(pivot_row, work.rows) if work[r, col]), None)
        if row is None:
            continue
        work.row_swap(row, pivot_row)
        work[pivot_row, :] = mod(work[pivot_row, :] * pow(int(work[pivot_row, col]), -1, prime), prime)
        for r in range(work.rows):
            if r != pivot_row:
                work[r, :] = mod(work[r, :] - work[r, col] * work[pivot_row, :], prime)
        pivots.append(col)
        pivot_row += 1
        if pivot_row == work.rows:
            break
    return original[:, pivots] if pivots else zeros(matrix.rows, 0)


@dataclass(frozen=True)
class KernelResult:
    status: str
    known_subspace: Matrix
    rank_history: tuple
    word_counts: tuple
    word_coordinates: tuple
    remaining_lagrangian_extensions: int
    assumptions_verified: bool = False


def extract_kernel(order, ell, splitting, pullbacks, *, include_adjoints=True):
    """Surface-only orbit-rank test, with at most two word layers.

    Conditional COMPLETE means the span equals K under the genuine-input
    promises. It is not a certificate that arbitrary supplied maps arise
    from an isogeny. Partial/empty results never mean classical hardness.
    """
    _prime(ell)
    check_split(order, splitting, ell)
    actions = product_actions(splitting)
    alphabet = tuple(_matrix(x, (16, 1)) for x in pullbacks)
    if not alphabet:
        raise ValueError("at least one pulled-back map required")
    if include_adjoints:
        alphabet += tuple(matrix_star(order, x) for x in alphabet)
    images = [mod(action(x, actions), ell) for x in alphabet]
    for a in images:
        for b in images:
            if mod(a * b, ell) != zeros(4):
                raise ValueError("pullbacks violate the common-kernel product identity")

    known = zeros(4, 0)
    frontier = alphabet
    history, counts, layers = [], [], []
    for depth in (1, 2):
        known = column_basis(Matrix.hstack(known, *(action(x, actions) for x in frontier)), ell)
        if known.cols > 2 or mod(known.T * alternating_form(2) * known, ell) != zeros(known.cols):
            raise ValueError("claimed kernel span is not isotropic of rank at most two")
        history.append(known.cols)
        counts.append(len(frontier))
        layers.append(frontier)
        if known.cols == 2 or (len(history) > 1 and history[-1] == history[-2]) or known.cols == 0:
            break
        if depth == 1:
            # Genuine target products prove this division integral. An
            # arbitrary division/saturation oracle is not being assumed.
            frontier = tuple(integer_matrix(matrix_multiply(order, a, b) / ell)
                             for a in alphabet for b in frontier)
    rank = known.cols
    return KernelResult("COMPLETE_UNDER_INPUT_PROMISE" if rank == 2 else
                        "PARTIAL" if rank else "NO_INFORMATION",
                        known, tuple(history), tuple(counts), tuple(layers),
                        prod(ell**i + 1 for i in range(1, 3 - rank)))
