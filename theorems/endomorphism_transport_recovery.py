"""Classical recovery WITH a full evaluable target End lattice and Gram form.

Inputs are already torsion-action matrices in compatible bases, not curve
points. No endomorphism ring, geometric evaluator, or quantum source is
constructed. See research/SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md.
"""

from dataclasses import dataclass
from math import isqrt

from flint import fmpq_mat, fmpz, fmpz_mod_ctx, fmpz_mod_mat

from theorems.projective_lattice_reconstruction import _ldl


def _prime(p):
    if type(p) is not int or p < 2 or not fmpz(p).is_prime():
        raise ValueError("a prime modulus is required")
    return fmpz_mod_ctx(p)


def _rows(a, height=None, width=None):
    a = tuple(tuple(row) for row in a)
    if not a or not a[0] or any(len(row) != len(a[0]) for row in a):
        raise ValueError("a nonempty rectangular matrix is required")
    if any(type(x) is not int for row in a for x in row):
        raise ValueError("matrix entries must be integers")
    if (height is not None and len(a) != height
            or width is not None and len(a[0]) != width):
        raise ValueError("incompatible matrix dimensions")
    return a


def _tuple(a):
    return tuple(tuple(int(a[i, j]) for j in range(a.ncols()))
                 for i in range(a.nrows()))


def _flatten(a):
    return tuple(x for row in a for x in row)


def _null_rows(a):
    """Right-nullspace vectors, returned as rows; FLINT supplies exact RREF."""
    reduced, rank = a.rref()
    width = a.ncols()
    pivots = [next(j for j in range(width) if reduced[i, j] != 0)
              for i in range(rank)]
    result = []
    for free in range(width):
        if free not in pivots:
            vector = [0] * width
            vector[free] = 1
            for i, pivot in enumerate(pivots):
                vector[pivot] = int(-reduced[i, free])
            result.append(tuple(vector))
    return result


def torsion_transport_coordinates(source_actions, target_actions,
                                  weak_transport, multiplier, prime):
    """Columns are target-basis coordinates of ell*W*a*W^-1 modulo r.

    W must represent ONE common nonzero scalar times phi on the FULL
    auxiliary torsion basis. Separate scalars per column do not satisfy
    that promise. Only matrix consistency, not geometric provenance, is
    checked here. All basis maps must be supplied in evaluation form.
    """
    ctx = _prime(prime)
    if type(multiplier) is not int or multiplier < 1 or multiplier % prime == 0:
        raise ValueError("positive multiplier must be invertible at the auxiliary prime")
    weak_transport = _rows(weak_transport)
    d = len(weak_transport)
    _rows(weak_transport, d, d)
    source = [_rows(a, d, d) for a in source_actions]
    target = [_rows(a, d, d) for a in target_actions]
    if d % 2 or len(source) != d*d or len(target) != d*d:
        raise ValueError("full superspecial endomorphism bases in even dimension required")
    source_matrix = fmpz_mod_mat(list(zip(*map(_flatten, source))), ctx)
    target_matrix = fmpz_mod_mat(list(zip(*map(_flatten, target))), ctx)
    w = fmpz_mod_mat(weak_transport, ctx)
    if source_matrix.rank() != d*d or target_matrix.rank() != d*d or w.rank() != d:
        raise ValueError("torsion transport and both action bases must have full rank")
    inverse, basis_inverse = w.inv(), target_matrix.inv()
    images = [_flatten(_tuple(multiplier * w * fmpz_mod_mat(a, ctx) * inverse))
              for a in source]
    return _tuple(basis_inverse * fmpz_mod_mat(list(zip(*images)), ctx))


@dataclass(frozen=True)
class IntegralTransport:
    status: str
    matrix: tuple | None
    product_level: int
    max_coordinate_bound: int
    reason: str


def reconstruct_integral_transport(gram, residues, squared_norm_bounds):
    """Unique bounded integer columns from exact residues, or UNKNOWN.

    Fullness of End(B), evaluation provenance, and correctness of the
    supplied Rosati norm bounds are external promises. No LLL is needed:
    conjugation cancels each auxiliary scalar before coordinate recovery.
    """
    gram = _rows(gram)
    d = len(gram)
    _rows(gram, d, d)
    if any(gram[i][j] != gram[j][i] for i in range(d) for j in range(d)):
        raise ValueError("Gram form must be symmetric")
    _ldl(gram)
    bounds = tuple(squared_norm_bounds)
    if not bounds or any(type(x) is not int or x < 0 for x in bounds):
        raise ValueError("one nonnegative integer squared-norm bound per column required")
    inverse = fmpq_mat(gram).inv()
    coordinate_bounds = [
        [isqrt(bound * int(inverse[i, i].numerator) // int(inverse[i, i].denominator))
         for bound in bounds] for i in range(d)]
    max_bound = max(map(max, coordinate_bounds))
    level, values, seen = 1, [[0] * len(bounds) for _ in range(d)], set()
    for prime, matrix in residues:
        _prime(prime)
        if prime in seen:
            raise ValueError("auxiliary primes must be distinct")
        seen.add(prime)
        matrix = _rows(matrix, d, len(bounds))
        inverse_level = pow(level, -1, prime)
        for i in range(d):
            for j in range(len(bounds)):
                values[i][j] += level * ((matrix[i][j] - values[i][j]) * inverse_level % prime)
        level *= prime
    if not seen:
        raise ValueError("at least one auxiliary residue is required")
    if level <= 2 * max_bound:
        return IntegralTransport("UNKNOWN", None, level, max_bound,
                                 "insufficient level for unique signed coordinate lifting")
    values = tuple(tuple(x if 2*x <= level else x-level for x in row) for row in values)
    for j, bound in enumerate(bounds):
        norm = sum(values[i][j] * gram[i][k] * values[k][j]
                   for i in range(d) for k in range(d))
        if norm > bound:
            return IntegralTransport("UNKNOWN", None, level, max_bound,
                                     "lifted column exceeds the supplied squared-norm bound")
    return IntegralTransport("UNIQUE_BOUNDED_TRANSPORT", values, level, max_bound,
                             "unique bounded columns under the supplied lattice promises")


@dataclass(frozen=True)
class KernelRecovery:
    status: str
    kernel_basis: tuple | None
    stabilizer_dimension: int
    annihilator_dimension: int
    reason: str


def kernel_from_integral_transport(transport, source_split_basis, prime, form):
    """Recover K from ker(a -> phi*a*phi^dagger mod ell End(B)).

    source_split_basis is in the SAME source order basis as the transport
    columns. Returned kernel_basis consists of row-listed column vectors.
    Algebraic checks do not certify an unknown ring's saturation at ell.
    """
    ctx = _prime(prime)
    form = _rows(form)
    d = len(form)
    _rows(form, d, d)
    if d % 2:
        raise ValueError("even torsion dimension required")
    n = d // 2
    jform = fmpz_mod_mat(form, ctx)
    zero = fmpz_mod_mat([[0]*d for _ in range(d)], ctx)
    if (jform.rank() != d or jform + jform.transpose() != zero
            or any(jform[i, i] != 0 for i in range(d))):
        raise ValueError("nondegenerate alternating form required")
    source = [_rows(a, d, d) for a in source_split_basis]
    if len(source) != d*d:
        raise ValueError("full source split basis required")
    split = fmpz_mod_mat(list(zip(*map(_flatten, source))), ctx)
    if split.rank() != d*d:
        raise ValueError("source basis is not a split matrix-algebra basis")
    transport = fmpz_mod_mat(_rows(transport, d*d, d*d), ctx)
    coefficients = _null_rows(transport)
    pdim = len(coefficients)
    if pdim != 3*n*n:
        return KernelRecovery("UNKNOWN", None, pdim, 0,
                              "transport kernel does not have parabolic dimension")
    matrices = []
    for row in coefficients:
        flat = split * fmpz_mod_mat([[x] for x in row], ctx)
        matrices.append(fmpz_mod_mat([[int(flat[a*d+b, 0]) for b in range(d)]
                                     for a in range(d)], ctx))
    # Tr(XY) pairs entries X_ab with Y_ba, not Y_ab.
    constraints = [[int(a[c, r]) for r in range(d) for c in range(d)] for a in matrices]
    perpendicular = _null_rows(fmpz_mod_mat(constraints, ctx))
    images = [tuple(row[a*d+b] for a in range(d))
              for row in perpendicular for b in range(d)]
    reduced, rank = fmpz_mod_mat(images, ctx).rref()
    udim = len(perpendicular)
    if rank != n:
        return KernelRecovery("UNKNOWN", None, pdim, udim,
                              "trace-annihilator image has the wrong dimension")
    vectors = tuple(tuple(int(reduced[i, k]) for k in range(d)) for i in range(rank))
    kernel = fmpz_mod_mat(list(zip(*vectors)), ctx)
    kernel_perp = fmpz_mod_mat(_null_rows(kernel.transpose()), ctx)
    if any((kernel_perp * a * kernel).rank() != 0 for a in matrices):
        return KernelRecovery("UNKNOWN", None, pdim, udim,
                              "transport kernel does not preserve its recovered image")
    if (kernel.transpose() * jform * kernel).rank() != 0:
        return KernelRecovery("UNKNOWN", None, pdim, udim,
                              "recovered subspace is not Lagrangian")
    return KernelRecovery("RECOVERED_UNDER_INPUT_PROMISES", vectors, pdim, udim,
                          "full stabilizer algebra and Lagrangian image verified")
