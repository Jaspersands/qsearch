"""Formal controls for all-anchor claims; no generated hidden-oracle problem."""
from flint import fq_default_ctx
import sympy as sp

from theorems.iterated_quadratic_jet import QuadraticIteration, analyze


def test_all_base_field_fixed_anchors_can_miss_an_extension_constraint():
    p = 7
    u, v, z, a = sp.symbols("u v z a")
    polynomial = (u**p-u)**3*v
    for anchor in range(p):
        shifted = sp.Poly(polynomial.subs(u, u+anchor), u, v, z, modulus=p)
        assert all(sum(powers) > 2 for powers, _ in shifted.terms())
    # This coefficient is nonzero as a FORMAL polynomial in the anchor,
    # despite vanishing at every base-field anchor.
    linear_v = sp.Poly(sp.diff(polynomial, v).subs(u, a), a, modulus=p)
    assert not linear_v.is_zero
    E = fq_default_ctx(p, 2)
    anchor = E.gen()
    coefficient = (anchor**p-anchor)**3
    assert coefficient != E(0)
    # v -> v+z changes the extension-anchor linear jet by coefficient*z.
    assert coefficient*E(1) != E(0)


def test_prime_orbit_sum_operator_identity_is_exact():
    X = sp.symbols("X")
    for p in (7, 11, 13, 17):
        assert sp.Poly(sum(X**j for j in range(p)), X, modulus=p) == sp.Poly(
            (X-1)**(p-1), X, modulus=p)
        # This characteristic-p identity must not be generalized to all T.
        assert sp.Poly(sum(X**j for j in range(p-1)), X, modulus=p) != sp.Poly(
            (X-1)**(p-2), X, modulus=p)


def test_orbit_sum_has_delayed_terms_but_every_fixed_anchor_two_jet_agrees():
    p, dimension = 7, 5
    A = [[int(i == j) for j in range(dimension)] for i in range(dimension)]
    B = [[[0]*dimension for _ in range(dimension)] for _ in range(dimension)]
    B[0][1][2] = B[0][2][1] = pow(2, -1, p)
    B[1][2][2] = B[2][1][1] = 1
    problem = QuadraticIteration(p, dimension, p, [0]*dimension,
                                  A, B, [1, 0, 0, 0, 0])
    result = analyze(problem, anchors=[[a, 0, 0, 0, 0] for a in range(p)])
    assert result["kernel_dimension"] == 6
    assert result["status"] == "UNKNOWN_FULL_STABILIZER"
    assert result["full_stabilizer_generators"] is None
    for anchor, jet in enumerate(result["anchor_jets"]):
        assert jet["constant"] == anchor
        assert jet["linear"] == [1, 0, 0, 0, 0]
        assert jet["quadratic"] == [[0]*dimension for _ in range(dimension)]

    # Independent truncated composition, not the production jet recurrence.
    x, y, z = sp.symbols("x y z")
    left, right = sp.Poly(x, x, y, modulus=p), sp.Poly(y, x, y, modulus=p)
    total = sp.Poly(0, x, y, modulus=p)

    def truncate(poly):
        return sp.Poly.from_dict({powers: c for powers, c in poly.terms()
                                 if sum(powers) <= p+1}, (x, y), modulus=p)

    for _ in range(p):
        total = truncate(total+left*right)
        left, right = truncate(left+right**2), truncate(right+left**2)
    expected = sp.Poly(-x*y**7+2*x**4*y**4-x**7*y, x, y, modulus=p)
    assert total == expected
    assert all(sum(powers) == p+1 for powers, _ in total.terms())
    assert not sp.Poly(total.as_expr().subs(y, y+z)-total.as_expr(),
                       x, y, z, modulus=p).is_zero
    h = x**3-y**3
    assert total == sp.Poly(-x*y*h**2, x, y, modulus=p)
    assert sp.expand(y**2*sp.diff(h, x)+x**2*sp.diff(h, y)) == 0
    discrete_change = sp.Poly(h.subs({x: x+y**2, y: y+x**2}, simultaneous=True)-h,
                              x, y, modulus=p)
    assert discrete_change == sp.Poly(-h*(3*x*y+x**3+y**3), x, y, modulus=p)
    assert not discrete_change.is_zero


def test_additive_flow_accumulated_quadratic_cost_can_vanish_identically():
    x, y = sp.symbols("x y")
    for p in (7, 11):
        # R=(x+y^2,y) has R^j=(x+j*y^2,y); this is not a claim for
        # arbitrary tangent-to-identity quadratic maps.
        total = sum((x+j*y**2)*y for j in range(p))
        assert sp.Poly(total, x, y, modulus=p).is_zero
