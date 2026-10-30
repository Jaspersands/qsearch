"""Classify reconstructed product-projector pullbacks, not arbitrary PPAVs.

The input is public source-order data. Geometric provenance and sufficient
legal auxiliary access remain promises; arithmetic checks do not certify them.
Only the surface case is implemented. No elliptic backend is executed here.
"""

from dataclasses import dataclass
from pathlib import Path
import sys

from sympy import Matrix, isprime, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "source-pullback-2026-10-23"))
from pullback import column_basis
from kernel_output import (
    action, alternating_form, check_split, integer_matrix, matrix_multiply,
    matrix_star, mod, product_actions,
)


def standard_projectors(order):
    zero = zeros(4, 1)
    return (Matrix.vstack(order.unit, zero, zero, zero),
            Matrix.vstack(zero, zero, zero, order.unit))


@dataclass(frozen=True)
class ProductDichotomy:
    status: str
    kernel_basis: Matrix | None
    target_to_source: tuple
    ranks: tuple
    geometric_input_verified: bool = False
    elliptic_backend_executed: bool = False
    classical_hardness_established: bool = False


def classify_projectors(order, ell, splitting, pullbacks):
    """Return K under the input promise, or route two elliptic subproblems."""
    if type(ell) is not int or ell < 3 or not isprime(ell):
        raise ValueError("odd prime ell required")
    check_split(order, splitting, ell)
    pullbacks = tuple(integer_matrix(a) for a in pullbacks)
    if len(pullbacks) != 2 or any(a.shape != (16, 1) for a in pullbacks):
        raise ValueError("two reconstructed surface-projector pullbacks required")
    projectors = standard_projectors(order)
    identity = projectors[0] + projectors[1]
    if pullbacks[0] + pullbacks[1] != ell * identity:
        raise ValueError("projectors must sum to ell times the source identity")
    for i, a in enumerate(pullbacks):
        if matrix_star(order, a) != a:
            raise ValueError("projector pullback must be self-adjoint")
        trace = (order.traces * (a[:4, :] + a[12:, :]))[0]
        if trace != 2 * ell:
            raise ValueError("each target projector must have elliptic rank")
        for j, b in enumerate(pullbacks):
            expected = ell * a if i == j else zeros(16, 1)
            if matrix_multiply(order, a, b) != expected:
                raise ValueError("scaled orthogonal-projector identity failed")

    actions = product_actions(splitting)
    images = tuple(mod(action(a, actions), ell) for a in pullbacks)
    ranks = tuple(column_basis(a, ell).cols for a in images)
    if ranks == (2, 2):
        kernel = column_basis(Matrix.hstack(*images), ell)
        if kernel.cols != 2 or mod(kernel.T * alternating_form(2) * kernel, ell) != zeros(2):
            raise ValueError("projector images are not one Lagrangian plane")
        return ProductDichotomy("CLASSICAL_KERNEL_UNDER_INPUT_PROMISE", kernel, (), ranks)
    if ranks != (0, 0):
        raise ValueError("ranks contradict the product surface dichotomy")

    routing = []
    for a in pullbacks:
        beta = integer_matrix(a / ell)
        matches = [j for j, e in enumerate(projectors) if beta == e]
        if len(matches) != 1:
            raise ValueError("integral projection is not a standard source factor")
        routing.append(matches[0])
    if sorted(routing) != [0, 1]:
        raise ValueError("isolated source factors must be distinct")
    return ProductDichotomy("TWO_ELLIPTIC_WEAK_INSTANCES", None, tuple(routing), ranks)


def restrict_weak_blocks(weak_action, prime, target_to_source):
    """Restrict a legal response in PRODUCT frames; do not infer provenance.

    The returned blocks retain the original common scalar, even its correlation
    across factors. This neither obtains new levels nor unmasks a response.
    """
    if type(prime) is not int or prime < 3 or not isprime(prime):
        raise ValueError("odd auxiliary prime required")
    routing = tuple(target_to_source)
    if len(routing) != 2 or any(type(j) is not int for j in routing) or sorted(routing) != [0, 1]:
        raise ValueError("target-to-source permutation required")
    w = mod(integer_matrix(weak_action), prime)
    if w.shape != (4, 4):
        raise ValueError("four by four response in product frames required")
    blocks = []
    for i, j in enumerate(routing):
        if w[2*i:2*i+2, 2*(1-j):2*(1-j)+2] != zeros(2):
            raise ValueError("response does not respect the certified factor routing")
        block = w[2*i:2*i+2, 2*j:2*j+2]
        if int(block.det()) % prime == 0:
            raise ValueError("auxiliary elliptic response must be invertible")
        blocks.append(block)
    return tuple(blocks)
