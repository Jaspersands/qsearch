"""Bounded candidate lists from a regular target spectrum and source pullback.

The source pullback and characteristic polynomial must come from genuine
public geometry. Arithmetic checks do not certify that promise. No hidden
kernel, target order, or geometric ell-torsion basis is accepted as input.
"""

from dataclasses import dataclass
from pathlib import Path
import sys

from flint import fmpz_mod_poly_ctx
from sympy import Matrix, eye, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"source-residual-algebra-2026-10-24"))
from residual_algebra import analyze_rank_one
from residual import adjoint, check_prime, column_basis, compatible_neighbor, nullspace
from kernel_output import (action, alternating_form, check_split, integer_matrix,
                           lift_split, matrix_multiply, matrix_star, mod, product_actions)


@dataclass(frozen=True)
class CandidateList:
    status: str
    candidates: tuple
    image_ranks: tuple
    factors: tuple
    residual_polynomial: tuple = ()
    root_abort_bound: str = "0"
    geometric_input_verified: bool = False
    exact_source_products_checked: bool = False


def _polynomial_matrix(coefficients, matrix, prime):
    result = zeros(matrix.rows)
    for coefficient in reversed(coefficients):
        result = mod(result*matrix+int(coefficient)*eye(matrix.rows), prime)
    return result


def regular_candidates(alpha_squared, coefficients, ell, *, rng=None, root_attempt_cap=128):
    """Use a compatible PUBLIC prime-square source action of phi^dagger gamma phi.

    coefficients are ascending coefficients of the actual degree-four
    target characteristic polynomial. Return NOT_REGULAR rather than
    interpreting a repeated spectrum as hard or an empty candidate set.
    """
    check_prime(ell)
    if ell == 2:
        raise ValueError("odd prime required")
    alpha = mod(integer_matrix(alpha_squared), ell*ell)
    if alpha.shape != (4, 4) or len(coefficients) != 5 or coefficients[-1] != 1:
        raise ValueError("surface action and monic degree-four polynomial required")
    ctx = fmpz_mod_poly_ctx(ell)
    chi = ctx(list(coefficients))
    _, factorization = chi.factor()
    factors = tuple(sorted((tuple(int(f[j]) for j in range(f.degree()+1)), int(e))
                           for f, e in factorization))
    if any(exponent != 1 for _, exponent in factors):
        return CandidateList("NOT_REGULAR_USE_EXISTING_GENERAL_GATES", (), (), factors)

    alphabet = (alpha, mod(adjoint(alpha), ell*ell))
    image = column_basis(Matrix.hstack(*alphabet), ell)
    words = []
    for first in alphabet:
        for second in alphabet:
            product = mod(first*second, ell*ell)
            if mod(product, ell) != zeros(4):
                raise ValueError("source product is not divisible by ell")
            words.append(integer_matrix(product/ell))
    full_image = column_basis(Matrix.hstack(image, *words), ell)
    ranks = (image.cols, full_image.cols)
    if full_image.cols > 2 or mod(full_image.T*alternating_form(2)*full_image, ell) != zeros(full_image.cols):
        raise ValueError("word images do not fit a Lagrangian kernel")

    residual_polynomial, abort = (), "0"
    if full_image.cols == 2:
        candidates = (full_image,)
    elif full_image.cols == 1:
        if image.cols != 1:
            raise ValueError("zero first image cannot grow under genuine source products")
        out = analyze_rank_one([alpha], ell, rng=rng, root_attempt_cap=root_attempt_cap)
        beta = out.operators[0]
        residual_polynomial = tuple(reversed([int(x) % ell for x in beta.charpoly().all_coeffs()]))
        if chi % ctx(list(residual_polynomial)) != 0:
            raise ValueError("residual spectrum does not divide the target spectrum")
        if mod(beta-int(beta[0, 0])*eye(2), ell) == zeros(2):
            raise ValueError("regular target spectrum contradicts scalar residual")
        candidates, abort = out.candidates, out.root_abort_bound
    else:
        beta = mod(integer_matrix(alpha/ell), ell)
        recovered = tuple(reversed([int(x) % ell for x in beta.charpoly().all_coeffs()]))
        if ctx(list(recovered)) != chi:
            raise ValueError("divided source action has a different characteristic polynomial")
        candidates = []
        # At most four simple factors: at most sixteen subsets, never ell points.
        for mask in range(1 << len(factors)):
            selected = ctx([1])
            for index, (factor, _) in enumerate(factors):
                if mask & (1 << index):
                    selected *= ctx(list(factor))
            if selected.degree() != 2:
                continue
            kernel = nullspace(_polynomial_matrix([int(selected[j]) for j in range(3)], beta, ell), ell)
            if kernel.cols != 2:
                raise ArithmeticError("squarefree primary component has wrong dimension")
            if mod(kernel.T*alternating_form(2)*kernel, ell) == zeros(2):
                candidates.append(kernel)
        candidates = tuple(candidates)
        if len(candidates) > 6:
            raise ArithmeticError("regular degree-four candidate bound violated")

    for candidate in candidates:
        if not all(compatible_neighbor(a, candidate, ell) for a in alphabet):
            raise ValueError("candidate failed the independent prime-square lattice criterion")
    status = ("INCONSISTENT_WITH_GEOMETRIC_PROMISE" if not candidates else
              "UNIQUE_UNDER_GEOMETRIC_PROMISE" if len(candidates) == 1 else
              "BOUNDED_LIST_REQUIRES_ORIGINAL_VERIFICATION")
    return CandidateList(status, tuple(candidates), ranks, factors, residual_polynomial, abort)


def from_source_pullback(order, alpha, coefficients, ell, splitting, *, split_squared=None,
                         rng=None, root_attempt_cap=128):
    """Consume the old exact CRT output, with full-order/public-chart checks."""
    from dataclasses import replace

    alpha = integer_matrix(alpha)
    if alpha.shape != (16, 1):
        raise ValueError("sixteen source coordinates required")
    alphabet = (alpha, matrix_star(order, alpha))
    for first in alphabet:
        for second in alphabet:
            integer_matrix(matrix_multiply(order, first, second)/ell)
    check_split(order, splitting, ell)
    lifted = lift_split(order, splitting, ell) if split_squared is None else tuple(split_squared)
    check_split(order, lifted, ell*ell)
    if any(mod(a-b, ell) != zeros(2) for a, b in zip(lifted, splitting)):
        raise ValueError("prime-square chart must extend the original public chart")
    result = regular_candidates(action(alpha, product_actions(lifted)), coefficients, ell,
                                rng=rng, root_attempt_cap=root_attempt_cap)
    return replace(result, exact_source_products_checked=True)


def select_original(candidates, ell, hiding_function):
    """At most 13 classical calls to the ORIGINAL source, conditional on its fibers."""
    check_prime(ell)
    if not 1 <= len(candidates) <= 6:
        raise ValueError("a nonempty bounded candidate list is required")
    form = alternating_form(2)
    for candidate in candidates:
        if candidate.shape != (4, 2) or column_basis(candidate, ell).cols != 2 or mod(candidate.T*form*candidate, ell) != zeros(2):
            raise ValueError("Lagrangian candidate basis required")
    if len(candidates) == 1:
        return {"kernel": candidates[0], "original_source_calls": 0,
                "source_fibers_verified": False}
    identity_label = hiding_function(eye(4))
    accepted, calls = [], 1
    for candidate in candidates:
        matches = []
        for column in range(2):
            vector = candidate[:, column]
            matches.append(hiding_function(mod(eye(4)+vector*vector.T*form, ell)) == identity_label)
            calls += 1
        if all(matches):
            accepted.append(candidate)
    if len(accepted) != 1:
        raise ValueError("original source does not select exactly one listed kernel")
    return {"kernel": accepted[0], "original_source_calls": calls,
            "source_fibers_verified": False}
