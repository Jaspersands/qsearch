"""Synchronize pointwise weak images at a SMALL prime using projective frames.

Group operations act on actual caller-supplied points. The finite controls use
Tate-module vectors, not a native curve backend. Global source validity remains
a promise; calibration of a few points cannot certify it.
"""

from dataclasses import dataclass
from itertools import product

from sympy import isprime


@dataclass(frozen=True)
class GroupOperations:
    zero: object
    add: object
    scale: object


def _parameters(prime, dimension, max_entries):
    if type(prime) is not int or not isprime(prime):
        raise ValueError("prime torsion level required")
    if dimension not in (2, 4):
        raise ValueError("elliptic or surface basis required")
    if type(max_entries) is not int or max_entries < 1 or prime**dimension > max_entries:
        raise ValueError("coordinate-table budget exceeded; no large-torsion shortcut")


def coordinate_table(prime, basis, operations, max_entries=1_000_000):
    """Charge O(r^d*d) point operations and O(r^d) storage, d=2 or 4.

    Points must have exact hash/equality in one fixed field embedding.
    This is polynomial in SMALL r, not in log(r).
    """
    basis = tuple(basis)
    _parameters(prime, len(basis), max_entries)
    if any(p == operations.zero or operations.scale(prime, p) != operations.zero for p in basis):
        raise ValueError("nonzero points of the stated prime order required")
    multiples = [[operations.scale(k, p) for k in range(prime)] for p in basis]
    table = {}
    for coefficients in product(range(prime), repeat=len(basis)):
        point = operations.zero
        for i, c in enumerate(coefficients):
            point = operations.add(point, multiples[i][c])
        if point in table:
            raise ValueError("dependent torsion basis")
        table[point] = coefficients
    return table


def calibrate_basis(prime, source_basis, weak_evaluate, source_ops, target_ops,
                    max_entries=1_000_000):
    """Use 2*d-1 calls, then reuse ONE cached common-scalar image tuple.

    Requires one genuine global isogeny, invertible on this prime torsion.
    Each call may select its own nonzero generator, even on repeated inputs.
    """
    source_basis = tuple(source_basis)
    dimension = len(source_basis)
    _parameters(prime, dimension, max_entries)
    source_table = coordinate_table(prime, source_basis, source_ops, max_entries)
    raw_images = tuple(weak_evaluate(p) for p in source_basis)
    target_table = coordinate_table(prime, raw_images, target_ops, max_entries)
    scales, bridges = [1], []
    for j in range(1, dimension):
        bridge_point = source_ops.add(source_basis[0], source_basis[j])
        image = weak_evaluate(bridge_point)
        if image not in target_table:
            raise ValueError("bridge image is outside the target torsion span")
        coefficients = target_table[image]
        x, y = coefficients[0], coefficients[j]
        if not x or not y or any(c for i, c in enumerate(coefficients) if i not in (0, j)):
            raise ValueError("bridge violates an invertible linear projective-frame promise")
        scales.append(y*pow(x, -1, prime) % prime)
        bridges.append({"basis_index": j, "coordinates": list(coefficients)})
    return {
        "images": tuple(target_ops.scale(c, p) for c, p in zip(scales, raw_images)),
        "raw_images": raw_images, "rescaling_factors": scales, "bridges": bridges,
        "weak_point_calls": 2*dimension-1,
        "coordinate_table_entries": len(source_table)+len(target_table),
        "source_dimension": dimension, "prime": prime,
        "global_isogeny_promise_verified": False,
        "other_weak_responses_verified": False,
        "common_scalar_known": False,
    }
