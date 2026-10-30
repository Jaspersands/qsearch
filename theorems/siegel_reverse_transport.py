"""Reverse-transport kernel recovery from already supplied torsion matrices.

The source lattice, its Rosati Gram form, and its split actions are known.
Target maps must be actually computable polarized automorphisms, not free
advice or weakly evaluated maps. No target End/Hom lattice is used. Matrix
checks cannot certify geometric provenance, common masks, or containment of
the reverse maps in a promised source suborder. See the accompanying note.
"""

from dataclasses import dataclass
from math import isqrt

from flint import fmpz_mod_mat

from theorems.endomorphism_transport_recovery import (
    IntegralTransport, _flatten, _prime, _rows, _tuple,
    reconstruct_integral_transport,
)


def _odd_prime(prime):
    ctx = _prime(prime)
    if prime == 2:
        raise ValueError("an odd prime is required")
    return ctx


def _form(rows, dimension, ctx):
    matrix = fmpz_mod_mat(_rows(rows, dimension, dimension), ctx)
    if (matrix.rank() != dimension
            or (matrix + matrix.transpose()).rank() != 0
            or any(matrix[i, i] != 0 for i in range(dimension))):
        raise ValueError("a nondegenerate alternating form is required")
    return matrix


def _source_basis(actions, dimension, ctx):
    actions = tuple(_rows(a, dimension, dimension) for a in actions)
    if len(actions) != dimension**2:
        raise ValueError("a full rank source action basis is required")
    basis = fmpz_mod_mat(list(zip(*map(_flatten, actions))), ctx)
    if basis.rank() != dimension**2:
        raise ValueError("source actions are not a split matrix-algebra basis")
    return basis


def reverse_torsion_coordinates(source_actions, target_automorphisms,
                                weak_transport, multiplier, prime, *,
                                source_form, target_form):
    """Return source coefficient columns of ell*W^-1*u*W modulo r.

    W maps column coordinates from the source torsion basis to the target
    torsion basis. The target actions and target_form use that SAME basis.
    If the weak images themselves are the target basis, W is the identity.
    Each source action is in the ordered integral source lattice basis.

    Forms check the local polarized-automorphism and square-similitude
    conditions. These necessary checks do not prove that W=a_r*phi_r for
    one common scalar, or that the u's are actual geometric automorphisms.
    Target actions must be exact: a separate mask on u does NOT cancel.
    """
    ctx = _odd_prime(prime)
    _odd_prime(multiplier)
    if multiplier == prime:
        raise ValueError("auxiliary prime must differ from the multiplier")
    weak_transport = _rows(weak_transport)
    dimension = len(weak_transport)
    if dimension % 2:
        raise ValueError("even torsion dimension required")
    w = fmpz_mod_mat(_rows(weak_transport, dimension, dimension), ctx)
    source = _source_basis(source_actions, dimension, ctx)
    ja = _form(source_form, dimension, ctx)
    jb = _form(target_form, dimension, ctx)
    if w.rank() != dimension:
        raise ValueError("weak transport must be invertible")
    pairing = w.transpose() * jb * w
    i, j = next((i, j) for i in range(dimension) for j in range(dimension)
                if ja[i, j] != 0)
    similitude = int(pairing[i, j] / ja[i, j])
    square = similitude * pow(multiplier, -1, prime) % prime
    if (pairing != similitude * ja
            or pow(square, (prime - 1) // 2, prime) != 1):
        raise ValueError("weak transport must have multiplier ell times a unit square")
    target = tuple(fmpz_mod_mat(_rows(u, dimension, dimension), ctx)
                   for u in target_automorphisms)
    if not target:
        raise ValueError("at least one target automorphism is required")
    if any(u.transpose() * jb * u != jb for u in target):
        raise ValueError("target actions must preserve the target polarization")
    inverse = w.inv()
    images = [_flatten(_tuple(multiplier * inverse * u * w)) for u in target]
    return _tuple(source.inv() * fmpz_mod_mat(list(zip(*images)), ctx))


def reconstruct_reverse_transport(source_gram, residues, multiplier):
    """Reconstruct beta_u in the source lattice, with exact Rosati norms.

    residues is a sequence of (auxiliary_prime, coefficient_matrix), with
    one column per target automorphism in a fixed order across levels.
    The source rank is (2g)^2 and every beta_u has norm squared 2g*ell^2.
    The Gram form must describe the SAME integral basis at every level.

    A fixture suborder is sufficient if all beta_u belong to it and its
    actions at the used primes and ell realize the promised splitting.
    These are external promises, not inferred from local invertibility.
    """
    _odd_prime(multiplier)
    gram = _rows(source_gram)
    rank = len(gram)
    _rows(gram, rank, rank)
    dimension = isqrt(rank)
    if dimension**2 != rank or dimension % 2:
        raise ValueError("source lattice rank must be the square of an even dimension")
    residues = tuple(residues)
    if not residues:
        raise ValueError("at least one auxiliary residue is required")
    columns = len(_rows(residues[0][1], rank)[0])
    for prime, _ in residues:
        _odd_prime(prime)
        if prime == multiplier:
            raise ValueError("auxiliary prime must differ from the multiplier")
    norm = dimension * multiplier**2
    result = reconstruct_integral_transport(gram, residues, [norm] * columns)
    if result.status != "UNIQUE_BOUNDED_TRANSPORT":
        return result
    for j in range(columns):
        actual = sum(result.matrix[i][j] * gram[i][k] * result.matrix[k][j]
                     for i in range(rank) for k in range(rank))
        if actual != norm:
            return IntegralTransport(
                "UNKNOWN", None, result.product_level, result.max_coordinate_bound,
                "lifted column does not have the exact polarized reverse Rosati norm")
    return IntegralTransport(
        result.status, result.matrix, result.product_level, result.max_coordinate_bound,
        "unique source coordinates and exact reverse Rosati norms under input promises")


@dataclass(frozen=True)
class ReverseKernelRecovery:
    status: str
    kernel_basis: tuple | None
    image_dimension: int
    map_ranks: tuple
    reason: str


def kernel_from_reverse_transport(transport, source_split_basis, prime, form):
    """Recover K as the joint image of reverse maps reduced modulo ell.

    transport contains integral coefficient COLUMNS in the same ordered
    source basis as source_split_basis. Use successfully reconstructed
    columns; this stage alone does not check their integer Rosati norms.
    Returned kernel vectors are columns listed as rows, in canonical RREF.

    The original isogeny and target automorphisms imply image(beta_u) <= K
    and beta_u(K)=0. A dimension-g Lagrangian joint image satisfying these
    necessary conditions recovers K only UNDER those geometric promises.
    """
    ctx = _odd_prime(prime)
    form = _rows(form)
    dimension = len(form)
    if dimension % 2:
        raise ValueError("even torsion dimension required")
    g = dimension // 2
    ja = _form(form, dimension, ctx)
    source = _source_basis(source_split_basis, dimension, ctx)
    coefficients = fmpz_mod_mat(_rows(transport, dimension**2), ctx)
    flat = source * coefficients
    maps = [fmpz_mod_mat(
        [[int(flat[i*dimension+j, k]) for j in range(dimension)]
         for i in range(dimension)], ctx) for k in range(flat.ncols())]
    ranks = tuple(a.rank() for a in maps)
    images = [tuple(int(a[i, j]) for i in range(dimension))
              for a in maps for j in range(dimension)]
    reduced, rank = fmpz_mod_mat(images, ctx).rref()

    def unknown(reason):
        return ReverseKernelRecovery("UNKNOWN", None, rank, ranks, reason)

    if any(r > g for r in ranks):
        return unknown("an individual reverse map has rank greater than g")
    if rank > g:
        return unknown("combined image rank exceeds g")
    if rank == 0:
        return unknown("reverse maps give zero information modulo ell")
    vectors = tuple(tuple(int(reduced[i, j]) for j in range(dimension))
                    for i in range(rank))
    image = fmpz_mod_mat(list(zip(*vectors)), ctx)
    if (image.transpose() * ja * image).rank() != 0:
        return unknown("combined image is not isotropic")
    if any((a * image).rank() != 0 for a in maps):
        return unknown("reverse maps do not annihilate their combined image")
    if rank < g:
        return unknown("insufficient image span to recover the whole kernel")
    return ReverseKernelRecovery(
        "RECOVERED_UNDER_INPUT_PROMISES", vectors, rank, ranks,
        "dimension-g Lagrangian image and common annihilation verified")
