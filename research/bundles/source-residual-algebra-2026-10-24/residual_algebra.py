"""Complete rank-one integrality test for an adjoint-closed target algebra.

Public source coefficients only. This does not obtain target endomorphisms,
validate geometric input, or execute the proposed geometric hiding function.
"""

from dataclasses import dataclass, replace
from pathlib import Path
import sys

from sympy import Matrix, eye, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "frobenius-residual-2026-10-23"))
from residual import (
    SmoothPowerRoots, adjoint, check_prime, column_basis, compatible_neighbor,
    nullspace, select_with_original_hiding_function,
)
from kernel_output import (
    action, alternating_form, check_split, integer_matrix, inverse_mod,
    lift_split, matrix_multiply, matrix_star, mod, product_actions,
)


@dataclass(frozen=True)
class AlgebraResidual:
    status: str
    image_basis: Matrix
    quotient_lifts: Matrix
    operators: tuple
    candidates: tuple
    candidate_count: int
    local_integrality_checks: bool = True
    exact_source_products_checked: bool = False
    geometric_input_verified: bool = False
    root_draws: int = 0
    root_abort_bound: str = "0"


def _common_invariant(line, operators, prime):
    return all(column_basis(line.row_join(beta * line), prime).cols == 1
               for beta in operators)


def analyze_rank_one(matrices_squared, ell, *, rng=None, root_attempt_cap=128):
    """Refine the old rank-one fixed point, without a Frobenius promise.

    Reject a non-stabilized image rather than silently skipping the old
    two-layer word attack. Prime-square matrices are public algebra actions,
    not geometric ell-torsion points. All reported counts are compatibility
    with the supplied endomorphisms, not with the entire original input.
    """
    check_prime(ell)
    if ell == 2:
        raise ValueError("odd prime required")
    original = tuple(integer_matrix(a) for a in matrices_squared)
    if not original or any(a.shape != (4, 4) for a in original):
        raise ValueError("one or more four by four actions required")
    matrices = tuple(mod(a, ell * ell) for a in original)
    matrices += tuple(mod(adjoint(a), ell * ell) for a in matrices)
    image = column_basis(Matrix.hstack(*matrices), ell)
    if image.cols != 1:
        raise ValueError("use the existing rank-zero or rank-two path")

    # Exact target products pull back as alpha_i alpha_j / ell. Their
    # first digits must not expand U; otherwise the old word gate wins.
    words = []
    for a in matrices:
        for b in matrices:
            product = mod(a * b, ell * ell)
            if mod(product, ell) != zeros(4):
                raise ValueError("common-kernel product divisibility failed")
            words.append(integer_matrix(product / ell))
    if column_basis(Matrix.hstack(image, *words), ell).cols != 1:
        raise ValueError("word images have not stabilized at rank one")

    perpendicular = nullspace(image.T * alternating_form(2), ell)
    basis = column_basis(Matrix.hstack(image, perpendicular), ell)
    if basis.cols != 3:
        raise ArithmeticError("incorrect image-perpendicular quotient")
    frame = column_basis(Matrix.hstack(basis, eye(4)), ell)
    inverse = inverse_mod(frame, ell)
    operators = []
    for a in matrices:
        if mod(a * basis, ell) != zeros(4, 3):
            raise ValueError("adjoint-closed actions must kill U-perp modulo ell")
        coordinates = mod(inverse * integer_matrix(a * basis / ell), ell)
        if coordinates[3:, :] != zeros(1, 3) or coordinates[1:3, :1] != zeros(2, 1):
            raise ValueError("divided action does not descend to U-perp/U")
        operators.append(coordinates[1:3, 1:3])
    operators = tuple(operators)
    lifts = basis[:, 1:3]
    if int((lifts.T * alternating_form(2) * lifts).det()) % ell == 0:
        raise ArithmeticError("degenerate quotient form")

    nonscalar = next((b for b in operators
                      if mod(b - int(b[0, 0]) * eye(2), ell) != zeros(2)), None)
    if nonscalar is None:
        return AlgebraResidual("SCALAR_RESIDUAL_ALL_LINES_COMPATIBLE", image,
                               lifts, operators, (), ell + 1)

    trace, determinant = int(nonscalar.trace()) % ell, int(nonscalar.det()) % ell
    discriminant = (trace * trace - 4 * determinant) % ell
    draws, abort = 0, "0"
    if not discriminant:
        roots = (0,)
    elif pow(discriminant, (ell - 1) // 2, ell) != 1:
        roots = ()
    else:
        backend = SmoothPowerRoots(ell, 2, rng=rng, attempt_cap=root_attempt_cap)
        square_root = backend.root(discriminant)
        if square_root is None:
            raise ArithmeticError("residue test disagrees with the root certificate")
        roots = (square_root, -square_root % ell)
        draws, abort = backend.stats.generator_draws, str(backend.abort_bound)

    candidates = []
    for root in roots:
        value = (trace + root) * pow(2, -1, ell) % ell
        line = nullspace(nonscalar - value * eye(2), ell)
        if line.cols != 1:
            raise ArithmeticError("a nonscalar two-dimensional eigenspace must be a line")
        if not _common_invariant(line, operators, ell):
            continue
        kernel = column_basis(image.row_join(lifts * line), ell)
        if not all(compatible_neighbor(a, kernel, ell) for a in matrices):
            raise ArithmeticError("candidate failed the independent prime-square criterion")
        candidates.append(kernel)
    status = {0: "INCONSISTENT_WITH_INPUT_PROMISE",
              1: "UNIQUE_UNDER_INPUT_PROMISE",
              2: "TWO_CANDIDATES_REQUIRE_ORIGINAL_VERIFICATION"}[len(candidates)]
    return AlgebraResidual(status, image, lifts, operators, tuple(candidates),
                           len(candidates), root_draws=draws, root_abort_bound=abort)


def analyze_source_pullbacks(order, pullbacks, ell, splitting, *, split_squared=None,
                             rng=None, root_attempt_cap=128):
    """Use exact reconstructed coefficients; do not certify their provenance."""
    check_prime(ell)
    original = tuple(integer_matrix(a) for a in pullbacks)
    if not original or any(a.shape != (16, 1) for a in original):
        raise ValueError("surface source-order coordinates required")
    alphabet = original + tuple(matrix_star(order, a) for a in original)
    for a in alphabet:
        for b in alphabet:
            integer_matrix(matrix_multiply(order, a, b) / ell)
    check_split(order, splitting, ell)
    lifted = lift_split(order, splitting, ell) if split_squared is None else tuple(split_squared)
    check_split(order, lifted, ell * ell)
    if any(mod(a - b, ell) != zeros(2) for a, b in zip(lifted, splitting)):
        raise ValueError("prime-square chart must extend the original source chart")
    matrices = tuple(action(a, product_actions(lifted)) for a in original)
    result = analyze_rank_one(matrices, ell, rng=rng, root_attempt_cap=root_attempt_cap)
    return replace(result, exact_source_products_checked=True)
