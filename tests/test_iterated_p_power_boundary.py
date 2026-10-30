"""Formal controls for the p-iterate boundary of a low-jet attack."""
import sympy as sp


def test_p_iterate_cancels_low_jets_but_not_the_first_restricted_derivation():
    p = 7
    x, y, z = sp.symbols("x y z")

    def poly(expression):
        return sp.Poly(expression, x, y, modulus=p)

    def truncate(value):
        return sp.Poly.from_dict({powers: c for powers, c in value.terms()
                                 if sum(powers) <= p+1}, (x, y), modulus=p)

    a, b = poly(x), poly(y)
    for _ in range(p):
        a, b = truncate(a+b*b), truncate(b+a*a)
    derivative = poly(x)
    for _ in range(p):
        derivative = poly(y*y*derivative.diff(x).as_expr()+x*x*derivative.diff(y).as_expr())
    expected = poly(-x**6*y**2+2*x**3*y**5-y**8)
    assert derivative == expected and not derivative.is_zero
    assert a == poly(x)+derivative
    assert all(sum(powers) in (1, p+1) for powers, _ in a.terms())
    # Embed x,y,z into the first three coordinates of UT5. This shear
    # preserves the entire 2-jet x but changes the actual degree-eight part.
    changed = expected.as_expr().subs(y, y+z)
    assert not sp.Poly(changed-expected.as_expr(), x, y, z, modulus=p).is_zero


def test_prime_iteration_can_also_be_exact_identity_not_a_hard_instance():
    p = 7
    x, y = sp.symbols("x y")
    value = sp.Poly(x, x, y, modulus=p)
    for _ in range(p):
        value += sp.Poly(y*y, x, y, modulus=p)
    assert value == sp.Poly(x, x, y, modulus=p)


def test_fixed_anchor_gradients_resolve_the_coupled_control():
    p = 7

    def derivative_at(start):
        point = sp.Matrix(start)
        jacobian = sp.eye(2)
        for _ in range(p):
            x, y = point
            local = sp.Matrix([[1, 2*y], [2*x, 1]])
            jacobian = (local*jacobian).applyfunc(lambda t: t % p)
            point = sp.Matrix([x+y*y, y+x*x]).applyfunc(lambda t: t % p)
        return jacobian

    assert derivative_at((0, 0)) == sp.eye(2)
    assert derivative_at((1, 0)) == sp.Matrix([[1, 2], [3, 4]])
    # The two independent gradient rows fix the first two rows of g.
    # Every remaining UT3 generator commutes with the original map exactly.
    x, y, z, w, v, a, b, c = sp.symbols("x y z w v a b c")
    point = sp.Matrix([x, y, z, w, v])
    g = sp.eye(5)
    g[2, 3], g[2, 4], g[3, 4] = a, b, c

    def polynomial_map(t):
        return sp.Matrix([t[0]+t[1]**2, t[1]+t[0]**2, t[2], t[3], t[4]])

    assert (polynomial_map(g*point)-g*polynomial_map(point)).applyfunc(sp.expand) == sp.zeros(5, 1)


def test_symmetric_two_by_two_flag_count_matches_exact_generic_probability():
    p = 7
    count = sum(a != 0 and (a*c-b*b) % p != 0
                for a in range(p) for b in range(p) for c in range(p))
    assert count == (p-1)**2*p
