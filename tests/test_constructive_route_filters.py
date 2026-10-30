"""Exact controls for two rejected constructive routes, not hardness tests."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product

from flint import fq_default_poly_ctx
import pytest
import sympy as sp

from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_gibbs_target import reciprocal_bound
from theorems.inverse_trace_smt import verify_word


def test_full_support_norm_relaxation_lift_count_and_exact_reweighted_law():
    bits, length, checks, q = 3, 6, 2, 8
    context = field(bits)
    ring = fq_default_poly_ctx(context)
    values = [element(bits, i) for i in range(q)]
    instance = {"bits": bits, "points": list(range(length)), "targets": [1]*length,
                "checks": checks, "field_modulus_coefficients": list(map(int, context.modulus().coeffs()))}
    beta = [values[i]**4 for i in instance["points"]]
    P = ring.one()
    for point in beta:
        P *= ring.gen()+point
    D = P.derivative()
    basis = [P//(ring.gen()+point) for point in beta]
    allowed = [i for i in range(1, q) if (values[i]**-1).trace() == 1]
    fibres, lifts, seen_pairs = defaultdict(Counter), Counter(), set()
    for word in product(allowed, repeat=length):
        if not verify_word(instance, word):
            continue
        b = [values[i]**4 for i in word]
        B = sum((value*term for value, term in zip(b, basis)), ring.zero())
        assert B.degree() <= length-checks-1
        local = [[a for a in values if a*a+a*v+v*v == 1] for v in b]
        assert all(len(options) == 2 for options in local)
        for a in product(*local):
            A = sum((value*term for value, term in zip(a, basis)), ring.zero())
            F = A*A+A*B+B*B
            assert F.degree() <= 2*length-2 and F % P == D*D % P
            assert A != A+B and (A+B)**2+(A+B)*B+B*B == F
            assert tuple(encoded((B(point)/D(point))**2) for point in beta) == word
            pair = tuple(map(encoded, A.coeffs())), tuple(map(encoded, B.coeffs()))
            assert pair not in seen_pairs
            seen_pairs.add(pair)
            fibres[tuple(map(encoded, F.coeffs()))][word] += 1
            lifts[word] += 1
    assert len(lifts) == 68 and set(lifts.values()) == {2**length}
    assert len(fibres) == 1418
    proposal_count, envelope = q**(length-1), (q+1)*2**(length-1)
    output = Counter()
    for counts in fibres.values():
        size = sum(counts.values())
        assert 2 <= size <= envelope and size % 2 == 0
        for word, multiplicity in counts.items():
            output[word] += Fraction(1, proposal_count)*Fraction(size, envelope)*Fraction(multiplicity, size)
    assert set(output.values()) == {Fraction(2**length, proposal_count*envelope)}
    success = sum(output.values())
    assert success == Fraction(17, 36864)
    assert all(weight/success == Fraction(1, 68) for weight in output.values())
    productive_upper = Fraction(2**(length-1)*len(lifts), proposal_count)
    prange = Fraction(len(lifts), (q//2)**(length-checks))
    assert Fraction(len(fibres), proposal_count) <= productive_upper
    assert productive_upper == prange*Fraction(2, q)**(checks-1)


def test_native_degree17_full_support_progression_is_worse_than_prange():
    bits, length, checks = 17, 289, 36
    q = 1 << bits
    _, eta = reciprocal_bound(bits, length, checks)
    upper = (1+eta)/(2*q**(checks-1))
    assert upper < Fraction(1, 2**595)
    assert Fraction(2, q)**(checks-1) == Fraction(1, 2**560)


@pytest.mark.parametrize("base_index", range(3))
@pytest.mark.parametrize("outer_index", range(4))
def test_scalar_postcomposition_preserves_all_ut3_stabilizers(base_index, outer_index):
    p = 5
    x, y, z = sp.symbols("x y z")
    base = [x*z+y*y+1, x**5-x*y**4, x*x*y+y*y*z+z+2][base_index]

    def poly(expression):
        return sp.Poly(expression, x, y, z, modulus=p)

    def frobenius(value):
        return sp.Poly.from_dict({tuple(p*e for e in powers): coefficient
                                 for powers, coefficient in value.terms()},
                                (x, y, z), modulus=p)

    def outer(value):
        if outer_index == 0:
            return frobenius(value)
        if outer_index == 1:
            return frobenius(value)-value
        first = frobenius(value)+value**2
        return first if outer_index == 2 else frobenius(first)+first**2

    original, composed = poly(base), outer(poly(base))
    assert composed.total_degree() >= p
    for a, b, c in product(range(p), repeat=3):
        transformed = poly(base.subs({x: x-a*y+(a*b-c)*z, y: y-b*z}, simultaneous=True))
        assert (outer(transformed) == composed) == (transformed == original)


def test_scalar_closure_needs_linear_action_p_group_and_nonconstant_outer():
    x = sp.symbols("x")
    polynomial = lambda expression: sp.Poly(expression, x, modulus=5)
    # The translation p-group does not fix the origin.
    assert polynomial((x+1)**5-(x+1)) == polynomial(x**5-x)
    assert polynomial(x+1) != polynomial(x)
    # A linear order-two group in characteristic five has a nontrivial character.
    assert polynomial((-x)**2) == polynomial(x**2)
    assert polynomial(-x) != polynomial(x)
    # A linear p-group shear changes F, while a constant outer erases it.
    y, t = sp.symbols("y t")
    original, changed = sp.Poly(x, x, y, modulus=5), sp.Poly(x+y, x, y, modulus=5)
    assert changed != original
    constant = sp.Poly(1, t, modulus=5)
    assert constant.as_expr().subs(t, original.as_expr()) == constant.as_expr().subs(t, changed.as_expr())
    # Formal equality cannot be replaced by equality of base-field functions.
    formal = sp.Poly((x+y)**5-(x+y), x, y, modulus=5)
    assert formal != sp.Poly(x**5-x, x, y, modulus=5)
    assert all((a**5-a) % 5 == 0 for a in range(5))
