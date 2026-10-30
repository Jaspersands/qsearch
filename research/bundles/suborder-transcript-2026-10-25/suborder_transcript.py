"""Small-prime suborder intertwiners, not a native endomorphism-ring solver."""

from math import gcd
from pathlib import Path
import sys

from sympy import GF, Matrix, eye, isprime, zeros
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
sys.path.insert(0, str(ROOT / "large-prime-source-audit-2026-10-25"))
from kernel_output import check_split, flat, mod
from projective_calibration import coordinate_table


def degree_envelope(scale, characteristic):
    """Bound for the PRIMITIVE global intertwiner; existence is not verified."""
    if type(scale) is not int or scale < 1:
        raise ValueError("positive integral suborder scale required")
    if type(characteristic) is not int or characteristic <= 3 or not isprime(characteristic):
        raise ValueError("prime characteristic > 3 required")
    modulus = scale
    while modulus % characteristic == 0:
        modulus //= characteristic
    return {"source_scale": scale, "query_modulus": modulus,
            "degree_multiple": characteristic*modulus,
            "primitive_global_map_exists": "requires algebra dictionary and geometric input promises",
            "degree_is_known": False}


def simultaneous_intertwiner(order, source_actions, target_actions, prime, scale):
    """Solve B_i*T=T*A_i, for supplied actions of scale*b_i, in F_r.

    Checks local algebra and uniqueness only. It does NOT infer a global map,
    its degree, the full target order, or correct native evaluator provenance.
    """
    if type(prime) is not int or not isprime(prime):
        raise ValueError("prime auxiliary level required")
    if type(scale) is not int or scale < 1 or gcd(scale, prime) != 1:
        raise ValueError("auxiliary prime must not divide the source scale")
    if len(source_actions) != 4 or len(target_actions) != 4:
        raise ValueError("four scaled basis actions required")
    source = tuple(mod(x, prime) for x in source_actions)
    target = tuple(mod(x, prime) for x in target_actions)
    inverse_scale = pow(scale, -1, prime)
    check_split(order, tuple(mod(inverse_scale*x, prime) for x in source), prime)
    check_split(order, tuple(mod(inverse_scale*x, prime) for x in target), prime)
    units = [Matrix(2, 2, [int(i == j) for i in range(4)]) for j in range(4)]
    constraints = Matrix.vstack(*[
        Matrix.hstack(*(flat(b*u-u*a) for u in units)) for a, b in zip(source, target)
    ])
    kernel = mod(DomainMatrix.from_Matrix(constraints).convert_to(GF(prime))
                 .nullspace().to_Matrix().T, prime)
    if kernel.shape != (4, 1):
        raise ValueError("local representations must have a unique projective intertwiner")
    first = next(int(x) for x in kernel if x)
    transform = Matrix(2, 2, list(mod(pow(first, -1, prime)*kernel, prime)))
    if transform.det() % prime == 0:
        raise ValueError("intertwiner must be invertible at the auxiliary prime")
    if any(mod(b*transform-transform*a, prime) != zeros(2) for a, b in zip(source, target)):
        raise ArithmeticError("intertwiner equation failed")
    return {"matrix": transform, "prime": prime, "source_scale": scale,
            "solution_dimension": 1, "global_map_verified": False,
            "isogeny_degree_inferred": False, "target_order_recovered": False}


def transcript_from_points(order, prime, scale, source_basis, target_basis,
                           source_evaluators, target_evaluators, source_ops, target_ops,
                           max_entries=1_000_000):
    """Evaluate FOUR known scaled order elements on TWO points at each end.

    Actual torsion bases, fields and point operations must be supplied. Tables
    cost O(r^2), not polylog(r). Callbacks are for known endomorphisms, NOT an
    unknown isogeny, its kernel, its weak oracle, or the full target order.
    """
    source_basis, target_basis = tuple(source_basis), tuple(target_basis)
    if len(source_basis) != 2 or len(target_basis) != 2:
        raise ValueError("two elliptic torsion points at each end required")
    if len(source_evaluators) != 4 or len(target_evaluators) != 4:
        raise ValueError("four effective scaled basis elements at each end required")
    if type(prime) is not int or not isprime(prime):
        raise ValueError("prime auxiliary level required")
    if type(scale) is not int or scale < 1 or gcd(scale, prime) != 1:
        raise ValueError("auxiliary prime must not divide the source scale")
    tables = [coordinate_table(prime, basis, operations, max_entries)
              for basis, operations in ((source_basis, source_ops), (target_basis, target_ops))]
    actions = []
    for basis, evaluators, table in zip((source_basis, target_basis),
                                      (source_evaluators, target_evaluators), tables):
        matrices = []
        for evaluate in evaluators:
            images = [evaluate(point) for point in basis]
            if any(image not in table for image in images):
                raise ValueError("endomorphism image outside the stated prime torsion")
            matrices.append(Matrix.hstack(*(Matrix(table[image]) for image in images)))
        actions.append(matrices)
    result = simultaneous_intertwiner(order, *actions, prime, scale)
    images = []
    for j in range(2):
        point = target_ops.zero
        for i in range(2):
            point = target_ops.add(point, target_ops.scale(int(result["matrix"][i, j]), target_basis[i]))
        images.append(point)
    result.update({"images": tuple(images), "known_source_endomorphism_calls": 8,
                   "known_suborder_endomorphism_calls": 8, "unknown_isogeny_calls": 0,
                   "coordinate_table_entries": sum(len(t) for t in tables)})
    return result
