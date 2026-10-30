"""Fixed exact controls for a commuting tuple with Hamilton centralizer quotient.

This is not an algebra backend or a complexity test. The nonsplit conclusion
uses the rational sum-of-squares argument in the parent audit, not dimensions,
centre dimension, or a finite search for zero divisors.
"""

import pytest
from sympy import Matrix, Poly, Rational, diag, expand, eye, kronecker_product
from sympy import linsolve, symbols, zeros


# Signed, one-based indices in the Hamilton basis (1, i, j, k), with k = i*j.
HAMILTON_TABLE = (
    (1, 2, 3, 4),
    (2, -1, 4, -3),
    (3, -4, -1, 2),
    (4, 3, -2, -1),
)
U = Matrix([[0, -1, 0, 0], [1, 0, 0, 0],
            [0, 0, 0, -1], [0, 0, 1, 0]])
V = Matrix([[0, 0, -1, 0], [0, 0, 0, 1],
            [1, 0, 0, 0], [0, -1, 0, 0]])
RIGHT = (
    eye(4),
    Matrix([[0, -1, 0, 0], [1, 0, 0, 0],
            [0, 0, 0, 1], [0, 0, -1, 0]]),
    Matrix([[0, 0, -1, 0], [0, 0, 0, -1],
            [1, 0, 0, 0], [0, 1, 0, 0]]),
    Matrix([[0, 0, 0, -1], [0, 0, 1, 0],
            [0, -1, 0, 0], [1, 0, 0, 0]]),
)


def _upper_block(x):
    assert x.shape == (4, 4)
    return zeros(4).row_join(x).col_join(zeros(4, 8))


def _signed_element(basis, signed_index):
    return (1 if signed_index > 0 else -1) * basis[abs(signed_index) - 1]


TUPLE = tuple(_upper_block(x) for x in (eye(4), U, V))
MATRIX_UNITS = tuple(
    eye(4)[:, i] * eye(4)[:, j].T for i in range(4) for j in range(4)
)
RADICAL = tuple(_upper_block(x) for x in MATRIX_UNITS)
QUOTIENT_LIFTS = tuple(diag(x, x) for x in RIGHT)
CENTRALIZER_BASIS = QUOTIENT_LIFTS + RADICAL


@pytest.fixture(scope="module")
def centralizer_kernel():
    # SymPy vec stacks columns: vec(X*N - N*X) = (N.T tensor I - I tensor N)vec(X).
    equations = Matrix.vstack(*(
        kronecker_product(n.T, eye(8)) - kronecker_product(eye(8), n)
        for n in TUPLE
    ))
    return equations, Matrix.hstack(*equations.nullspace())


def test_explicit_left_and_right_multiplication_against_independent_table():
    basis = tuple(eye(4)[:, j] for j in range(4))
    left = (eye(4), U, V, U * V)
    for a in range(4):
        for b in range(4):
            expected = _signed_element(basis, HAMILTON_TABLE[a][b])
            assert left[a] * basis[b] == expected
            assert RIGHT[b] * basis[a] == expected
            assert left[a] * RIGHT[b] == RIGHT[b] * left[a]
    assert U**2 == V**2 == -eye(4)
    assert U * V == -V * U
    assert U * V != V * U


def test_commuting_square_zero_tuple_and_generated_algebra_quotient_q():
    algebra_basis = (eye(8),) + TUPLE
    assert set(entry for n in TUPLE for entry in n) == {-1, 0, 1}
    assert Matrix.hstack(*(x.vec() for x in algebra_basis)).rank() == 4
    assert Matrix.hstack(*(x.vec() for x in TUPLE)).rank() == 3
    for x in TUPLE:
        for y in TUPLE:
            assert x * y == y * x == zeros(8)
    # Closure follows from these products. Projection to the identity coefficient
    # has the three-dimensional square-zero kernel and quotient Q.
    for i, x in enumerate(algebra_basis):
        for j, y in enumerate(algebra_basis):
            product = x * y
            expected = y if i == 0 else x if j == 0 else zeros(8)
            assert product == expected
            assert product[0, 0] == x[0, 0] * y[0, 0]


def test_exact_centralizer_kernel_equals_right_hamilton_plus_upper_blocks(
    centralizer_kernel,
):
    equations, kernel = centralizer_kernel
    span = Matrix.hstack(*(x.vec() for x in CENTRALIZER_BASIS))
    assert equations.shape == (192, 64)
    assert kernel.shape == (64, 20)
    assert equations.rank() == 44
    assert span.rank() == 20
    assert equations * kernel == equations * span == zeros(192, 20)
    assert span.row_join(kernel).rank() == 20

    right_span = Matrix.hstack(*(x.vec() for x in RIGHT))
    for column in kernel.columnspace():
        x = Matrix(8, 8, lambda row, col: column[row + 8 * col])
        assert x[4:, :4] == zeros(4)
        assert x[:4, :4] == x[4:, 4:]
        assert right_span.row_join(x[:4, :4].vec()).rank() == 4


def test_explicit_sixteen_dimensional_square_zero_two_sided_ideal():
    assert Matrix.hstack(*(x.vec() for x in RADICAL)).rank() == 16
    for x in RADICAL:
        assert x[:4, :4] == x[4:, :4] == x[4:, 4:] == zeros(4)
        for y in RADICAL:
            assert x * y == zeros(8)
    for c in CENTRALIZER_BASIS:
        p = c[:4, :4]
        for q, r in zip(MATRIX_UNITS, RADICAL):
            assert c * r == _upper_block(p * q)
            assert r * c == _upper_block(q * p)
    # The quotient identified below is Hamilton's opposite algebra. Its
    # semisimplicity plus this nilpotent ideal identifies the Jacobson radical.


def test_quotient_multiplication_is_opposite_hamilton_and_centre_is_q():
    assert Matrix.hstack(*(x.vec() for x in RIGHT)).rank() == 4
    for a in range(4):
        for b in range(4):
            # Composition R_a R_b sends x to (x*b)*a, hence reverses products.
            expected = _signed_element(RIGHT, HAMILTON_TABLE[b][a])
            assert RIGHT[a] * RIGHT[b] == expected
            assert QUOTIENT_LIFTS[a] * QUOTIENT_LIFTS[b] == diag(expected, expected)
    assert RIGHT[1] * RIGHT[2] == -RIGHT[3]
    assert RIGHT[2] * RIGHT[1] == RIGHT[3]

    centre_equations = Matrix.vstack(*(
        Matrix.hstack(*((r * s - s * r).vec() for r in RIGHT))
        for s in RIGHT
    ))
    assert centre_equations.rank() == 3
    assert centre_equations.nullspace() == [Matrix([1, 0, 0, 0])]


def test_symbolic_norm_identity_supports_nonsplit_not_dimension_heuristic():
    a, b, c, d = symbols("a b c d", real=True)
    coordinates = (a, b, c, d)
    x = sum((v * r for v, r in zip(coordinates, RIGHT)), zeros(4))
    conjugate = a * RIGHT[0] - b * RIGHT[1] - c * RIGHT[2] - d * RIGHT[3]
    norm = a**2 + b**2 + c**2 + d**2
    assert (x * conjugate).applyfunc(expand) == norm * eye(4)
    assert (conjugate * x).applyfunc(expand) == norm * eye(4)
    assert expand(x.det() - norm**2) == 0
    assert Poly(norm, *coordinates).terms() == [
        ((2, 0, 0, 0), 1), ((0, 2, 0, 0), 1),
        ((0, 0, 2, 0), 1), ((0, 0, 0, 2), 1),
    ]
    # Over Q the sum of squares vanishes only at zero, so every nonzero x
    # has inverse conjugate/norm. M_2(Q), in contrast, has this zero divisor.
    matrix_unit = Matrix([[0, 1], [0, 0]])
    assert matrix_unit != zeros(2) and matrix_unit**2 == zeros(2)


def test_regular_module_control_is_distinct_from_the_eight_dimensional_lattice():
    # Left regular action of Q[epsilon_1, epsilon_2, epsilon_3]/(epsilon)^2
    # on (1, epsilon_1, epsilon_2, epsilon_3), not the faithful 8D module above.
    regular = tuple(eye(4)[:, j] * eye(4)[:, 0].T for j in range(1, 4))
    equations = Matrix.vstack(*(
        kronecker_product(n.T, eye(4)) - kronecker_product(eye(4), n)
        for n in regular
    ))
    kernel = Matrix.hstack(*equations.nullspace())
    regular_algebra = Matrix.hstack(*(x.vec() for x in (eye(4),) + regular))
    assert kernel.shape == (16, 4)
    assert regular_algebra.rank() == regular_algebra.row_join(kernel).rank() == 4
    assert equations * regular_algebra == zeros(48, 4)
    assert TUPLE[0].rows == 8 != regular_algebra.cols


def test_short_local_global_ideal_control_has_exact_intertwiner_obstruction():
    a = Matrix([[0, -5], [1, 0]])
    b = Matrix([[-1, -3], [2, 1]])
    ideal_basis = Matrix([[2, 1], [0, 1]])  # (2, 1 + sqrt(-5)) in (1, sqrt(-5)).
    assert a * ideal_basis == ideal_basis * b
    assert ideal_basis.det() == 2

    p, q, r, s = symbols("p q r s", integer=True)
    unknown = Matrix([[p, r], [q, s]])
    assert linsolve(list(b * unknown - unknown * a), (r, s)) == {
        (-p - 3 * q, 2 * p + q)
    }
    transporter = Matrix([[p, -p - 3 * q], [q, 2 * p + q]])
    determinant = 2 * p**2 + 2 * p * q + 3 * q**2
    assert expand(transporter.det()) == determinant
    assert expand(determinant - 2 * (p + q / 2)**2 - Rational(5, 2) * q**2) == 0
    # q != 0 forces determinant >= 5/2; q = 0 gives 2*p**2, never +/-1.
    # det 2 is a unit at every odd prime; det 3 supplies the prime-2 witness.
    for values, expected_det in [({p: 1, q: 0}, 2), ({p: 0, q: 1}, 3)]:
        local = transporter.subs(values)
        assert b * local == local * a
        assert local.det() == expected_det
