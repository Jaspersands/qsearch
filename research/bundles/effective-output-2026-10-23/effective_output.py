"""Contravariant module interface, conditional on a correctly recovered K.

This prepares exact algebraic inputs for the published module converter.
No geometric converter, target-ring discovery, or quantum receiver runs here.
"""

from pathlib import Path
import sys

from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"kernel-output-2026-10-23"))
from kernel_output import matrix_on_column, matrix_star, module_pairing


def column_star(order, column):
    column = Matrix(column)
    if column.cols != 1 or column.rows % 4:
        raise ValueError("quaternion column coordinates required")
    return Matrix.vstack(*(order.star(column[4*i:4*i+4, :])
                           for i in range(column.rows//4)))


def integral(matrix):
    matrix = Matrix(matrix)
    if any(x.q != 1 for x in matrix):
        raise ValueError("map does not preserve the full integral module")
    return matrix


def pullback_matrix(order, output, endomorphism):
    """Matrix of beta^*: r -> r*x on J_K^dagger, where beta=phi*x/phi.

    Thus pullback(x*y)=pullback(y)*pullback(x), NOT the other order.
    """
    j, g = output.module_numerator, output.g
    if not output.contains_order(endomorphism):
        raise ValueError("target-order element required")
    adjoint = matrix_star(order, endomorphism, g)
    columns = Matrix.hstack(*(matrix_on_column(order, adjoint, j[:, i], g)
                             for i in range(j.cols)))
    return integral(j.inv()*columns)


def left_order_actions(order, output):
    """Left O action on the adjoint-row module, in its integral Z-basis."""
    j, g = output.module_numerator, output.g
    inverse = j.inv()
    actions = []
    for index in range(4):
        conjugate = order.star(eye(4)[:, index])
        columns = [Matrix.vstack(*(order.multiply(j[4*k:4*k+4, i], conjugate)
                                   for k in range(g))) for i in range(j.cols)]
        actions.append(integral(inverse*Matrix.hstack(*columns)))
    return tuple(actions)


def source_inclusion(order, output):
    """phi^*: J_K^dagger -> O^g, in standard row coordinates of O^g."""
    return integral(Matrix.hstack(*(column_star(order, output.module_numerator[:, i])
                                   for i in range(output.module_numerator.cols))))


def left_hermitian_gram(order, output):
    basis = output.module_basis
    return tuple(tuple(module_pairing(order, basis[:, i], basis[:, j], output.ell)
                       for j in range(basis.cols)) for i in range(basis.cols))


def scalar_base_change(characteristic, base_degree, scalar):
    """Check numerical consequences of the field promise, not its truth.

    The scalar must first be justified from the common source definition
    field. Passing these equations alone does not verify geometric input.
    """
    from sympy import isprime

    p, f, c = int(characteristic), int(base_degree), int(scalar)
    if not isprime(p) or p <= 3 or f < 2 or f % 2 or c*c != p**f:
        raise ValueError("p>3 and a valid scalar-Frobenius square field required")
    normalized = c*c
    if normalized != (-p)**f or normalized % 8 != 1:
        raise AssertionError("quadratic base normalization failed")
    return {"input_degree_over_prime_field": f,
            "normalized_degree_over_prime_field": 2*f,
            "relative_extension_degree": 2,
            "normalized_frobenius": normalized,
            "reference_frobenius_after_base_change": (-p)**f,
            "full_eight_torsion_fixed": True,
            "geometric_field_promise_verified": False,
            "geometric_conversion_executed": False}
