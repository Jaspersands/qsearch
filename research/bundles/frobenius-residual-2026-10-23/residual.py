"""Prime-square residual information in a skew-Frobenius pullback.

This is a classical candidate-list reduction, conditional on actual weak
isogeny input. It does not construct target Frobenius or geometric labels.
"""

from dataclasses import dataclass, replace
from pathlib import Path
import sys

from sympy import GF, Matrix, eye, zeros
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "source-pullback-2026-10-23"))
sys.path.insert(0, str(ROOT / "scalar-cancellation-2026-10-23"))
from pullback import adjoint, column_basis
from scalar_cancellation import SmoothPowerRoots, check_prime
from kernel_output import (
    action, adapted_basis, alternating_form, check_split, integer_matrix,
    inverse_mod, lift_split, matrix_multiply, matrix_star, mod, product_actions,
)


def nullspace(matrix, prime):
    return mod(DomainMatrix.from_Matrix(Matrix(matrix)).convert_to(GF(prime)).nullspace().to_Matrix().T, prime)


def same_space(first, second, prime):
    return (column_basis(first, prime).cols == column_basis(second, prime).cols
            == column_basis(Matrix.hstack(first, second), prime).cols)


def compatible_neighbor(matrix_squared, kernel, ell):
    """Exact old I_K criterion: A,D vanish mod ell and C mod ell^2."""
    kernel = integer_matrix(kernel)
    if kernel.shape != (4, 2):
        raise ValueError("surface Lagrangian kernel required")
    if mod(kernel.T * alternating_form(2) * kernel, ell) != zeros(2):
        return False
    try:
        frame = adapted_basis(kernel, ell)
    except ValueError:
        return False
    blocks = mod(inverse_mod(frame, ell * ell) * matrix_squared * frame, ell * ell)
    return (mod(blocks[:2, :2], ell) == zeros(2)
            and mod(blocks[2:, 2:], ell) == zeros(2)
            and blocks[2:, :2] == zeros(2))


@dataclass(frozen=True)
class ResidualResult:
    status: str
    image_rank: int
    image_basis: Matrix
    residual_operator: Matrix
    residual_lifts: Matrix
    candidates: tuple
    candidate_count: int
    splitting_type: str
    exact_source_relations_checked: bool = False
    geometric_input_verified: bool = False
    root_draws: int = 0
    root_abort_bound: str = "0"


def analyze_local_matrix(matrix_squared, ell, characteristic, *, rng=None, root_attempt_cap=128):
    """Analyze supplied local coefficients; global source promises stay open.

    Call analyze_pullback for exact source-order relation checks. Keeping
    this interface separate permits large-prime local controls without
    pretending that an arbitrary local matrix is an actual geometric input.
    """
    check_prime(ell)
    check_prime(characteristic)
    if characteristic <= 3 or characteristic == ell:
        raise ValueError("p>3 distinct from ell required")
    a = integer_matrix(matrix_squared)
    if a.shape != (4, 4):
        raise ValueError("four by four local action required")
    a = mod(a, ell * ell)
    if mod(a + adjoint(a), ell * ell) != zeros(4):
        raise ValueError("skew-adjoint Frobenius is required; positive-square twists are excluded")
    if mod(a * a, ell * ell) != zeros(4):
        raise ValueError("pullback square must vanish modulo ell squared")
    image = column_basis(a, ell)
    rank = image.cols
    if rank > 2 or mod(image.T * alternating_form(2) * image, ell) != zeros(rank):
        raise ValueError("invalid Frobenius image")
    d = -characteristic % ell
    split = pow(d, (ell - 1) // 2, ell) == 1
    kind = "split" if split else "nonsplit"

    if rank == 2:
        if not compatible_neighbor(a, image, ell):
            return ResidualResult("INCONSISTENT_WITH_INPUT_PROMISE", rank, image, zeros(0),
                                  zeros(4, 0), (), 0, kind)
        return ResidualResult("UNIQUE_UNDER_INPUT_PROMISE", rank, image, zeros(0),
                              zeros(4, 0), (image,), 1, kind)

    if rank == 0:
        beta = mod(integer_matrix(a / ell), ell)
        if mod(beta * beta, ell) != mod(d * eye(4), ell):
            raise ValueError("residual square is not minus p")
        # Complete symbolic count, not enumeration of a large field.
        count = ell + 3 if split else ell + 1
        return ResidualResult("STABLE_LAGRANGIAN_RESIDUAL", rank, image, beta,
                              eye(4), (), count, kind)

    # U=im(a), W=ker(a)=U-perp. Keep the image column first so rows 1:3
    # of the coordinate map describe W/U without a hidden basis choice.
    w = nullspace(a, ell)
    basis = column_basis(Matrix.hstack(image, w), ell)
    if basis.cols != 3:
        raise ValueError("rank-one quotient has incorrect dimension")
    frame = column_basis(Matrix.hstack(basis, eye(4)), ell)
    inverse = inverse_mod(frame, ell)
    divided = integer_matrix(a * basis / ell)
    coordinates = mod(inverse * divided, ell)
    if coordinates[3:, :] != zeros(1, 3) or coordinates[1:3, :1] != zeros(2, 1):
        raise ValueError("division does not induce an operator on W/U")
    beta = coordinates[1:3, 1:3]
    lifts = basis[:, 1:3]
    form = mod(lifts.T * alternating_form(2) * lifts, ell)
    if int(form.det()) % ell == 0 or mod(beta.T * form + form * beta, ell) != zeros(2):
        raise ValueError("residual alternating form or skew adjointness failed")
    if mod(beta * beta, ell) != mod(d * eye(2), ell):
        raise ValueError("residual square is not minus p")
    if not split:
        return ResidualResult("INCONSISTENT_WITH_INPUT_PROMISE", rank, image, beta,
                              lifts, (), 0, kind)
    roots = SmoothPowerRoots(ell, 2, rng=rng, attempt_cap=root_attempt_cap)
    root = roots.root(d)
    if root is None or root == 0:
        raise ArithmeticError("missing certified nonzero square root")
    candidates = []
    for value in (root, -root % ell):
        eigenspace = nullspace(beta - value * eye(2), ell)
        if eigenspace.cols != 1:
            raise ArithmeticError("skew two-dimensional residual must have two distinct eigenlines")
        kernel = column_basis(image.row_join(lifts * eigenspace), ell)
        if not compatible_neighbor(a, kernel, ell):
            raise ArithmeticError("residual eigenline failed the independent lattice criterion")
        candidates.append(kernel)
    return ResidualResult("TWO_CANDIDATES_REQUIRE_ORIGINAL_VERIFICATION", rank, image,
                          beta, lifts, tuple(candidates), 2, kind,
                          root_draws=roots.stats.generator_draws,
                          root_abort_bound=str(roots.abort_bound))


def analyze_pullback(order, alpha, ell, characteristic, splitting, *, split_squared=None,
                     rng=None, root_attempt_cap=128):
    """Use exact source coefficients from bounded weak-action CRT."""
    check_prime(ell)
    check_prime(characteristic)
    alpha = integer_matrix(alpha)
    if alpha.shape != (16, 1):
        raise ValueError("surface source-order coordinates required")
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    if matrix_star(order, alpha) != -alpha:
        raise ValueError("source pullback is not skew-adjoint")
    if matrix_multiply(order, alpha, alpha) != -characteristic * ell * ell * identity:
        raise ValueError("exact source Frobenius relation failed")
    check_split(order, splitting, ell)
    lifted = lift_split(order, splitting, ell) if split_squared is None else tuple(split_squared)
    check_split(order, lifted, ell * ell)
    if any(mod(a - b, ell) != zeros(2) for a, b in zip(lifted, splitting)):
        raise ValueError("prime-square split does not extend the supplied source chart")
    matrix = action(alpha, product_actions(lifted))
    result = analyze_local_matrix(matrix, ell, characteristic, rng=rng, root_attempt_cap=root_attempt_cap)
    return replace(result, exact_source_relations_checked=True)


@dataclass(frozen=True)
class SelectionResult:
    kernel: Matrix
    original_label_queries: int
    selected_index: int
    source_hsp_promise_verified: bool = False


def select_with_original_hiding_function(candidates, ell, hiding_function):
    """Two ordinary calls to the SAME promised Sp4 kernel-stabilizer source.

    The callback's mathematical/geometric promise is NOT established by
    this routine. It must not be replaced by an uncharged new oracle.
    """
    if len(candidates) != 2:
        raise ValueError("exactly two candidates required")
    first, second = (integer_matrix(x) for x in candidates)
    for kernel in (first, second):
        if kernel.shape != (4, 2) or column_basis(kernel, ell).cols != 2:
            raise ValueError("two rank-two candidates required")
        if mod(kernel.T * alternating_form(2) * kernel, ell) != zeros(2):
            raise ValueError("candidate is not Lagrangian")
    vector = next((first[:, i] for i in range(2)
                   if column_basis(second.row_join(first[:, i]), ell).cols > 2), None)
    if vector is None:
        raise ValueError("candidates must be distinct")
    transvection = mod(eye(4) + vector * vector.T * alternating_form(2), ell)
    selected = 0 if hiding_function(transvection) == hiding_function(eye(4)) else 1
    return SelectionResult((first, second)[selected], 2, selected)
