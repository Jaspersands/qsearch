"""Bounded exact identities for the unmarked-pencil reduction, not a solver.

The cubic/quartic fixtures supply their similarity witnesses explicitly. These
tests make no complexity, expanded-witness-size, quantum, or hardness claims.
"""

from math import gcd, lcm

import pytest
import sympy as sp


x = sp.Symbol("x")

CUBIC = {
    "f": sp.Poly(x**3 - x - 1, x, domain=sp.QQ),
    "M": sp.Matrix([[0, 0, 1], [1, 0, 1], [0, 1, 0]]),
    "g": sp.Matrix([[2, 1], [3, 2]]),
    "A0": sp.Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]]),
    "L": sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]]),
    "R": sp.Matrix([[1, 0, 1], [0, 1, 0], [0, 0, 1]]),
    "target_det_abs": 7,
}
QUARTIC = {
    "f": sp.Poly(x**4 - x - 1, x, domain=sp.QQ),
    "M": sp.Matrix([[0, 0, 0, 1], [1, 0, 0, 1],
                    [0, 1, 0, 0], [0, 0, 1, 0]]),
    "g": sp.Matrix([[2, 1], [3, 1]]),
    "A0": sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 0],
                     [0, 0, 1, 1], [0, 0, 0, 1]]),
    "L": sp.Matrix([[1, 0, 0, 0], [1, 1, 0, 0],
                    [0, 0, 0, 1], [0, 0, 1, 0]]),
    "R": sp.Matrix([[1, 0, 0, 1], [0, 1, 1, 0],
                    [0, 0, 1, 0], [0, 0, 0, 1]]),
    "target_det_abs": 17,
}


def _remainder(expression, modulus):
    return sp.Poly(expression, x, domain=sp.QQ).rem(modulus)


def _mobius_element(g, modulus):
    a, b, c, d = list(g)
    denominator = sp.Poly(a + b*x, x, domain=sp.QQ)
    if denominator.gcd(modulus).degree() != 0:
        raise ValueError("denominator is not invertible modulo the polynomial")
    inverse = sp.invert(denominator, modulus)
    return _remainder((c + d*x)*inverse.as_expr(), modulus)


def _coefficient_kernel_matrix(beta, modulus):
    # Coordinates in (1, alpha, ..., alpha**(n-1)), columns (a, b, c, d).
    columns = (beta.as_expr(), x*beta.as_expr(), -1, -x)
    return sp.Matrix.hstack(*[
        sp.Matrix([_remainder(column, modulus).nth(i)
                   for i in range(modulus.degree())])
        for column in columns
    ])


def _primitive_integer_matrix(matrix):
    entries = [sp.Rational(entry) for entry in matrix]
    denominator = lcm(*(int(entry.q) for entry in entries))
    integers = [int(denominator*entry) for entry in entries]
    content = gcd(*(abs(entry) for entry in integers))
    if not content:
        raise ValueError("zero does not define a projective line")
    integers = [entry // content for entry in integers]
    if next(entry for entry in integers if entry) < 0:
        integers = [-entry for entry in integers]
    return sp.Matrix(2, 2, integers)


def _gl2z_lift(matrix):
    primitive = _primitive_integer_matrix(matrix)
    return primitive if abs(primitive.det()) == 1 else None


def _evaluate_at_matrix(polynomial, matrix):
    return sum((polynomial.nth(i)*matrix**i
                for i in range(polynomial.degree() + 1)),
               sp.zeros(matrix.rows))


def _inverse_mix(g, B0, B1):
    inverse = g.inv()
    return (inverse[0, 0]*B0 + inverse[0, 1]*B1,
            inverse[1, 0]*B0 + inverse[1, 1]*B1)


@pytest.fixture(params=[pytest.param(CUBIC, id="cubic"),
                       pytest.param(QUARTIC, id="quartic")])
def pencil(request):
    case = request.param
    A0, M, g, L, R = (case[key] for key in ("A0", "M", "g", "L", "R"))
    A1 = A0*M
    a, b, c, d = list(g)
    B0 = L*(a*A0 + b*A1)*R
    B1 = L*(c*A0 + d*A1)*R
    return {**case, "A1": A1, "B0": B0, "B1": B1}


def test_explicit_irreducible_inputs_have_only_source_slice_unimodular(pencil):
    f, M = pencil["f"], pencil["M"]
    assert f.degree() in (3, 4)
    assert f.is_irreducible
    assert f.gcd(f.diff()).degree() == 0
    assert sp.Poly(M.charpoly(x).as_expr(), x, domain=sp.QQ) == f
    assert pencil["A0"].inv()*pencil["A1"] == M
    for key in ("A0", "g", "L", "R"):
        assert abs(pencil[key].det()) == 1
    assert abs(pencil["B0"].det()) == pencil["target_det_abs"] > 1
    for key in ("A0", "A1", "B0", "B1"):
        assert all(entry.is_Integer for entry in pencil[key])


def test_mobius_denominator_root_and_matrix_identity_are_exact(pencil):
    f, M, g = (pencil[key] for key in ("f", "M", "g"))
    a, b, c, d = list(g)
    denominator = sp.Poly(a + b*x, x, domain=sp.QQ)
    inverse = sp.invert(denominator, f)
    assert _remainder(denominator.as_expr(), f) != sp.Poly(0, x, domain=sp.QQ)
    assert _remainder(denominator.as_expr()*inverse.as_expr(), f).as_expr() == 1

    beta = _mobius_element(g, f)
    U, V = a*sp.eye(M.rows) + b*M, c*sp.eye(M.rows) + d*M
    assert abs(U.det()) == pencil["target_det_abs"]
    N = pencil["B0"].inv()*pencil["B1"]
    assert N == pencil["R"].inv()*U.inv()*V*pencil["R"]
    assert _evaluate_at_matrix(beta, M) == U.inv()*V

    h = sp.Poly(N.charpoly(x).as_expr(), x, domain=sp.QQ)
    determinant_h = sp.Poly(
        (x*pencil["B0"] - pencil["B1"]).det()/pencil["B0"].det(),
        x, domain=sp.QQ,
    )
    assert h == determinant_h
    assert h.is_irreducible
    assert _remainder(h.as_expr().subs(x, beta.as_expr()), f).is_zero
    assert _remainder((a + b*x)*beta.as_expr() - (c + d*x), f).is_zero


def test_coefficient_kernel_is_the_unique_correct_projective_line(pencil):
    g, f = pencil["g"], pencil["f"]
    beta = _mobius_element(g, f)
    equations = _coefficient_kernel_matrix(beta, f)
    assert equations.shape == (f.degree(), 4)
    assert equations*sp.Matrix(list(g)) == sp.zeros(f.degree(), 1)
    assert equations*sp.Matrix(list(g.T)) != sp.zeros(f.degree(), 1)
    assert equations.rank() == 3
    basis = equations.nullspace()
    assert len(basis) == 1
    recovered = _gl2z_lift(sp.Matrix(2, 2, list(basis[0])))
    assert recovered == g


@pytest.mark.parametrize("scale", [sp.Rational(3, 7), sp.Rational(-5, 11),
                                  sp.Integer(2)])
def test_primitive_line_lift_is_invariant_under_rational_rescaling(pencil, scale):
    g = pencil["g"]
    assert _primitive_integer_matrix(scale*g) == g
    assert _gl2z_lift(scale*g) == g
    entries = list(_primitive_integer_matrix(scale*g))
    assert gcd(*(abs(int(entry)) for entry in entries)) == 1


def test_nonunit_primitive_determinant_rejects_even_rational_determinant_one(pencil):
    bad = sp.diag(1, 4)
    rational_representative = bad/2
    assert rational_representative.det() == 1
    assert _primitive_integer_matrix(rational_representative) == bad
    assert _gl2z_lift(rational_representative) is None

    beta = _mobius_element(bad, pencil["f"])
    assert beta.as_expr() == 4*x
    basis = _coefficient_kernel_matrix(beta, pencil["f"]).nullspace()
    assert len(basis) == 1
    primitive = _primitive_integer_matrix(sp.Matrix(2, 2, list(basis[0])))
    assert primitive == bad
    assert primitive.det() == 4
    assert _gl2z_lift(primitive) is None
    assert _gl2z_lift(sp.diag(1, 2)) is None
    assert _gl2z_lift(sp.Matrix([[1, 1], [2, 2]])) is None


def test_zero_denominator_and_zero_projective_vector_are_rejected(pencil):
    with pytest.raises(ValueError, match="denominator"):
        _mobius_element(sp.Matrix([[0, 0], [1, 1]]), pencil["f"])
    with pytest.raises(ValueError, match="zero"):
        _primitive_integer_matrix(sp.zeros(2))


def test_quartic_field_identification_need_not_have_a_mobius_transporter():
    f, M = QUARTIC["f"], QUARTIC["M"]
    beta = sp.Poly(x**2, x, domain=sp.QQ)
    h = sp.Poly(x**4 - 2*x**2 - x + 1, x, domain=sp.QQ)
    assert h.is_irreducible
    assert sp.Poly((M**2).charpoly(x).as_expr(), x, domain=sp.QQ) == h
    assert _remainder(h.as_expr().subs(x, beta.as_expr()), f).is_zero
    # alpha = beta**2 - 1, so beta generates the same field, but not by Mobius.
    assert _remainder(beta.as_expr()**2 - 1 - x, f).is_zero
    equations = _coefficient_kernel_matrix(beta, f)
    assert equations.rank() == 4
    assert equations.nullspace() == []


def test_inverse_mix_and_native_left_right_reconstruction(pencil):
    f, M = pencil["f"], pencil["M"]
    beta = _mobius_element(pencil["g"], f)
    line = _coefficient_kernel_matrix(beta, f).nullspace()[0]
    g = _gl2z_lift(sp.Matrix(2, 2, list(line)))
    B0_prime, B1_prime = _inverse_mix(g, pencil["B0"], pencil["B1"])
    assert B0_prime == pencil["L"]*pencil["A0"]*pencil["R"]
    assert B1_prime == pencil["L"]*pencil["A1"]*pencil["R"]
    assert abs(B0_prime.det()) == 1
    C = B0_prime.inv()*B1_prime
    assert all(entry.is_Integer for entry in C)

    # Supplied fixture witness only: no integral-similarity algorithm is invoked.
    S = pencil["R"].inv()
    assert C == S*M*S.inv()
    L = B0_prime*S*pencil["A0"].inv()
    R = S.inv()
    assert L == pencil["L"]
    assert R == pencil["R"]
    assert abs(L.det()) == abs(R.det()) == 1
    a, b, c, d = list(g)
    assert L*(a*pencil["A0"] + b*pencil["A1"])*R == pencil["B0"]
    assert L*(c*pencil["A0"] + d*pencil["A1"])*R == pencil["B1"]
    assert _inverse_mix(-g, pencil["B0"], pencil["B1"]) == (-B0_prime, -B1_prime)


def test_inverse_mix_unimodularity_gate_is_not_implied_by_field_identity(pencil):
    B0, B1 = pencil["B0"], pencil["B1"]
    assert (2*B0).inv()*(2*B1) == B0.inv()*B1
    B0_prime, _ = _inverse_mix(pencil["g"], 2*B0, 2*B1)
    assert abs(B0_prime.det()) == 2**pencil["M"].rows
    assert abs(B0_prime.det()) != 1


def test_quadratic_equal_maximal_extensions_do_not_imply_order_homothety():
    """Separate n=2 control, not an application of the unique-line argument."""
    M = sp.Matrix([[0, 5], [1, 0]])
    N = sp.Matrix([[-1, 2], [2, 1]])
    f = sp.Poly(x**2 - 5, x, domain=sp.QQ)
    assert f.is_irreducible
    assert sp.Poly(M.charpoly(x).as_expr(), x, domain=sp.QQ) == f
    assert sp.Poly(N.charpoly(x).as_expr(), x, domain=sp.QQ) == f

    # Columns are (1, omega) in (1, sqrt(5)), omega = (1 + sqrt(5))/2.
    D = sp.Matrix([[1, sp.Rational(1, 2)], [0, sp.Rational(1, 2)]])
    assert D.rank() == 2
    assert D.inv()*M*D == N
    assert all(entry.is_Integer for entry in D.inv())  # R is contained in O_K.
    assert D[:, 0] == sp.Matrix([1, 0])  # Both orders contain 1.
    omega_on_R, omega_on_OK = (sp.eye(2) + M)/2, (sp.eye(2) + N)/2
    assert not all(entry.is_Integer for entry in omega_on_R)
    assert all(entry.is_Integer for entry in omega_on_OK)
    assert omega_on_OK**2 - omega_on_OK - sp.eye(2) == sp.zeros(2)

    # O_K has integral basis (1, omega) of squarefree discriminant 5. Since
    # 1 belongs to R subset O_K, both extended ideals equal O_K. A unital
    # order is its own multiplier ring; homothety preserves that ring.
    traces = sp.Matrix([[2, sp.trace(omega_on_OK)],
                        [sp.trace(omega_on_OK), sp.trace(omega_on_OK**2)]])
    assert traces.det() == 5
    assert N.applyfunc(lambda entry: entry % 2) == sp.eye(2)
    for sign in (-1, 1):
        assert (sign*M).applyfunc(lambda entry: entry % 2) != sp.eye(2)
