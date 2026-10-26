"""Reduction/falsifier controls, NOT hard instances or a quantum execution."""

from fractions import Fraction
from itertools import product

from flint import fq_default_ctx
import pytest
import sympy as sp

from theorems.succinct_polynomial_stabilizer import (
    plan_orbit_fingerprint, white_box_derivative_guard,
)


@pytest.mark.parametrize("p,d,degree,error", [
    (5, 3, 5, Fraction(1, 100)),
    (7, 5, 0, Fraction(1, 20)),
    (2**127 - 1, 5, 2**400, Fraction(1, 2**100)),
])
def test_exact_all_pairs_budget_is_polynomial_in_log_degree(p, d, degree, error):
    plan = plan_orbit_fingerprint(p, d, degree, error)
    assert plan.collision_probability_upper_bound <= error
    assert plan.fixed_point_bits_upper_bound == d * plan.label_bits_upper_bound
    if plan.extension_degree > 1:
        assert Fraction(degree * plan.group_order_upper_bound**2,
                        p**(plan.extension_degree - 1)) > error
    # log_2(p)>=1; this bound depends on degree BIT LENGTH, not its value.
    assert plan.extension_degree <= (
        2*d*d + degree.bit_length() + error.denominator.bit_length() + 1)


@pytest.mark.parametrize("args", [
    (3, 3, 5), (25, 3, 5), (5, 0, 5), (5, 3, -1),
    (5, True, 5), (5, 3, 5, 0.01), (5, 3, 5, Fraction(0)),
    (5, 3, 5, Fraction(1)),
])
def test_invalid_parameter_contract_rejected(args):
    with pytest.raises(ValueError):
        plan_orbit_fingerprint(*args)


def _ut3_inverse_action(g, point):
    a, b, c = g
    x, y, z = point
    return x - a*y + (a*b-c)*z, y-b*z, z


def _relative_first_row(g, other, p):
    # First-row nonidentity coordinates of other^{-1} * g.
    a, b, c = g
    aa, bb, cc = other
    return (a-aa) % p, (c-cc+aa*bb-aa*b) % p


def test_nonabelian_coset_fibres_and_base_field_aliasing():
    p = 5
    group = list(product(range(p), repeat=3))
    field = fq_default_ctx(p, 3)
    theta = field.gen()
    # phi(theta), phi(theta^2) are independent: ker(phi)=Fp, and
    # 1,theta,theta^2 are a basis. This is a deterministic finite control.
    point = (field(0), theta, theta**2)
    labels = [(_ut3_inverse_action(g, point)[0]**p
               - _ut3_inverse_action(g, point)[0]) for g in group]
    assert len(set(map(str, labels))) == p**2
    for i, g in enumerate(group):
        for j, other in enumerate(group):
            assert (labels[i] == labels[j]) == (
                _relative_first_row(g, other, p) == (0, 0))
    # A nonzero formal polynomial x^p-x is the zero FUNCTION on Fp.
    for g in group:
        value = _ut3_inverse_action(g, (1, 2, 3))[0] % p
        assert (pow(value, p, p)-value) % p == 0


def test_fixed_point_bad_probability_is_not_a_per_query_event():
    p = 5
    field = fq_default_ctx(p, 2)
    theta = field.gen()
    bad = 0
    for a, b in product(range(p), repeat=2):
        point = field(a) + b*theta
        labels = [(point-shift)**2 for shift in range(p)]
        bad += len(set(map(str, labels))) != p
    # ALL polynomial translates of x^2 are distinct. Collisions occur at
    # precisely the base-field points; choose one point and retain it.
    assert Fraction(bad, p*p) == Fraction(1, p)
    assert Fraction(bad, p*p) <= Fraction(sp.binomial(p, 2)*2, p*p)


def test_derivatives_can_both_overestimate_and_underestimate_finite_stabilizer():
    p = 5
    x, y = sp.symbols("x y")
    false_positive = x**p
    false_negative = x**p-x*y**(p-1)
    derivative = lambda f: sp.Poly(y*sp.diff(f, x), x, y, modulus=p)
    assert derivative(false_positive).is_zero
    assert not derivative(false_negative).is_zero
    for t in range(p):
        shifted = lambda f: sp.Poly(f.subs(x, x+t*y)-f, x, y, modulus=p)
        assert shifted(false_positive).is_zero == (t == 0)
        assert shifted(false_negative).is_zero


@pytest.mark.parametrize("kind", ["frobenius", "artin_schreier"])
def test_equivariant_high_degree_lifts_do_not_create_new_stabilizers(kind):
    p = 5
    x = sp.symbols("x:3")
    base = x[0]*x[2] + x[1]**2
    phi = tuple(t**p - (t if kind == "artin_schreier" else 0) for t in x)
    lifted = base.subs(dict(zip(x, phi)), simultaneous=True)
    for g in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (2, 3, 1), (4, 1, 2)]:
        action = _ut3_inverse_action(g, x)
        delta = base.subs(dict(zip(x, action)), simultaneous=True)-base
        lifted_delta = lifted.subs(dict(zip(x, action)), simultaneous=True)-lifted
        expected = delta.subs(dict(zip(x, phi)), simultaneous=True)
        assert sp.Poly(lifted_delta-expected, *x, modulus=p).is_zero
        assert sp.Poly(delta, *x, modulus=p).is_zero == sp.Poly(
            lifted_delta, *x, modulus=p).is_zero


def test_large_prime_frobenius_circuit_requires_no_degree_expansion():
    p = 2**127-1
    field = fq_default_ctx(p, 2)
    x, y = field.gen(), field(2)
    for t in (1, 2, p-1):
        assert (x+t*y)**p != x**p
        assert ((x+t*y)**p-(x+t*y)*y**(p-1)
                == x**p-x*y**(p-1))


def test_white_box_large_characteristic_guard_does_not_charge_numeric_degree():
    p = 2**127-1
    bounds = white_box_derivative_guard(p, 5, 2**100)
    assert bounds["extension_field_samples_suffice"] == 25
    assert not bounds["degree_expansion_required"]
    for args in [(p, 5, 2**400), (5, 2, 5), (5, 5, 1)]:
        with pytest.raises(ValueError):
            white_box_derivative_guard(*args)


def test_derivative_kernel_equals_full_finite_stabilizer_in_guarded_regime():
    p = 7
    white_box_derivative_guard(p, 3, 2)
    x, y, z = sp.symbols("x y z")
    polynomial = x*z + y*y
    # A=a E12+c E13+b E23. d_A(F)=(a+2b)yz+c z^2.
    # Two evaluations span the exact constraint rows in this control.
    rows = sp.polys.matrices.DomainMatrix.from_list_sympy(
        2, 3, [[1, 2, 1], [0, 0, 1]]).convert_to(sp.GF(p))
    assert rows.rank() == 2
    count = 0
    for a, b, c in product(range(p), repeat=3):
        derivative_zero = ((a+2*b) % p == 0 and c == 0)
        # exp(A), not I+A: the quadratic term is essential.
        matrix_c = (c + pow(2, -1, p)*a*b) % p
        image = polynomial.subs(
            {x: x+a*y+matrix_c*z, y: y+b*z}, simultaneous=True)
        finite_symmetry = sp.Poly(image-polynomial, x, y, z, modulus=p).is_zero
        assert derivative_zero == finite_symmetry
        count += finite_symmetry
    assert count == p
