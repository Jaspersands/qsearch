"""Actual hiding-output source, noncentral-side falsifier and strict scope witnesses."""
from itertools import product
import random

import numpy as np
import pytest
import sympy as sp

from theorems.right_abelian_induced_source import (
    FiliformNormal, derived_length_three_witness, symbolic_filiform_cocycle,
    upper_triangular_lie, evaluate_induced_cocycle_fixture,
)


@pytest.mark.parametrize("p,k", [(5, 4), (11, 7), (2**127-1, 4)])
def test_right_chart_and_induced_cocycle_are_exact(p, k):
    group, rng = FiliformNormal(p, k), random.Random(315+k)
    for _ in range(20):
        g, h, v = (tuple(rng.randrange(p) for _ in range(group.width)) for _ in range(3))
        x = tuple(rng.randrange(p) for _ in range(2))
        fiber = tuple(rng.randrange(p) for _ in range(k-1))
        assert group.multiply(group.multiply(g, h), v) == group.multiply(g, group.multiply(h, v))
        assert group.multiply(g, group.inverse(g)) == (0,)*group.width
        assert group.from_right_coordinates(*group.right_coordinates(g)) == g
        gx, kg = group.induced_action(g, x)
        assert gx == tuple((a+b) % p for a, b in zip(g[:2], x))
        actual = group.right_coordinates(group.multiply(g, group.from_right_coordinates(x, fiber)))
        assert actual == (gx, tuple((a+b) % p for a, b in zip(fiber, kg)))
        hx, kh = group.induced_action(h, x)
        ghx, kgh = group.induced_action(g, hx)
        assert group.induced_action(group.multiply(g, h), x) == (
            ghx, tuple((a+b) % p for a, b in zip(kh, kgh)))
    # I is genuinely noncentral, so this is not a renamed central fixture.
    a = (1,)+(0,)*k
    i = (0, 0, 1)+(0,)*(k-2)
    assert group.multiply(a, i) != group.multiply(i, a)


@pytest.mark.parametrize("k", [3, 4, 5, 7])
def test_symbolic_phase_is_actual_linear_log_section_word(k):
    gvars, xvars, polynomials = symbolic_filiform_cocycle(k)
    assert max(sp.Poly(f, *gvars, *xvars).total_degree() for f in polynomials) <= k
    if k >= 4:
        all_terms = [powers for f in polynomials for powers, _ in sp.Poly(f, *gvars, *xvars).terms()]
        assert max(sum(a[:len(gvars)]) for a in all_terms) > 2
        assert max(sum(a[len(gvars):]) for a in all_terms) > 2
    rng = random.Random(842+k)
    for p in (17, 2**127-1):
        group = FiliformNormal(p, k)
        for _ in range(3):
            logarithm = tuple(rng.randrange(p) for _ in gvars)
            x = tuple(rng.randrange(p) for _ in xvars)
            substitution = dict(zip((*gvars, *xvars), (*logarithm, *x)))
            expected = []
            for polynomial in polynomials:
                value = polynomial.subs(substitution)
                numerator, denominator = value.as_numer_denom()
                expected.append(int(numerator)*pow(int(denominator), -1, p) % p)
            assert group.induced_action(group.exp(logarithm), x)[1] == tuple(expected)


def test_complete_small_instrument_uses_all_right_fiber_characters():
    p, k = 3, 2
    group = FiliformNormal(p, k)
    normal = tuple(product(range(p), repeat=group.width))
    carriers = tuple(product(range(p), repeat=2))
    labels = tuple(product(range(p), repeat=k-1))
    lookup = {x: j for j, x in enumerate(carriers)}
    transform = np.zeros((len(normal), len(normal)), complex)
    for j, g in enumerate(normal):
        x, fiber = group.right_coordinates(group.inverse(g))
        for row, label in enumerate(labels):
            transform[row*len(carriers)+lookup[x], j] = np.exp(
                2j*np.pi*sum(a*b for a, b in zip(label, fiber))/p)/np.sqrt(len(labels))
    np.testing.assert_allclose(transform.conj().T @ transform, np.eye(len(normal)), atol=2e-14)
    assert not np.allclose(transform[len(carriers):].conj().T @ transform[len(carriers):], np.eye(len(normal)))


def test_existing_quadratic_lift_correctly_rejects_new_required_products():
    from theorems.ut5_scalar_phase_compiler import _multiply
    with pytest.raises(ArithmeticError, match="quadratic parameter lift"):
        _multiply({((0,), (0, 0)): 1}, {((0,), (0,)): 1}, 43)


def test_original_hiding_output_has_fixed_noncentral_character_sources():
    p, k = 5, 4
    group = FiliformNormal(p, k)
    normal = tuple(product(range(p), repeat=group.width))
    carriers = tuple(product(range(p), repeat=2))
    index = {x: j for j, x in enumerate(carriers)}
    order, carrier_size, fiber_size = len(normal), len(carriers), p**(k-1)
    group_order = p*p*order
    h = group.exp((1,)+(0,)*k)
    powers = [(0,)*group.width]
    for _ in range(p-1):
        powers.append(group.multiply(powers[-1], h))
    assert group.multiply(powers[-1], h) == (0,)*group.width

    def section(q):
        return group.exp((0, q[1])+(0,)*(k-1))

    # G=F_p^2 x N, H={(u,0,h^u)}; f is a canonical ORIGINAL gH label.
    # This fixes H and the oracle before deriving any potential kernel.
    def oracle_label(q, n):
        return q[1], group.multiply(n, powers[-q[0] % p])

    for u in range(p):
        q, n = (2, 1), normal[137]
        assert oracle_label(((q[0]+u) % p, q[1]), group.multiply(n, powers[u])) == oracle_label(q, n)

    row_cache = {}
    def labels(q):
        if q not in row_cache:
            row_cache[q] = [oracle_label(q, group.multiply(n, section(q))) for n in normal]
            assert len(set(row_cache[q])) == order  # transverse intersection
        return row_cache[q]

    right = [group.right_coordinates(group.inverse(n)) for n in normal]
    left = [group.left_coordinates(group.inverse(n)) for n in normal]
    def transform(label, coordinates):
        matrix = np.zeros((carrier_size, order), complex)
        for col, (x, fiber) in enumerate(coordinates):
            exponent = sum(a*b for a, b in zip(label, fiber)) % p
            matrix[index[x], col] = np.exp(2j*np.pi*exponent/p)/np.sqrt(fiber_size)
        return matrix

    def block(K, L, q, r):
        # The actual equality table has at most one nonzero per row. Contract
        # that exact sparse table, not a desired W(g(q)^-1*g(r)) source.
        lookup = {value: j for j, value in enumerate(labels(r))}
        matches = [lookup.get(value) for value in labels(q)]
        if all(j is None for j in matches):
            return np.zeros((carrier_size, carrier_size), complex)
        assert all(j is not None for j in matches)
        return K @ L[:, matches].conj().T/group_order

    def potential(q):
        return group.multiply(group.multiply(section(q), powers[q[0]]), group.inverse(section(q)))

    def sector(label, g):
        result = np.zeros((carrier_size, carrier_size), complex)
        for col, x in enumerate(carriers):
            out, cocycle = group.induced_action(g, x)
            exponent = sum(a*b for a, b in zip(label, cocycle)) % p
            result[index[out], col] = np.exp(2j*np.pi*exponent/p)
        return result

    for label in ((0, 0, 0), (0, 0, 1), (2, 1, 4)):
        K = transform(label, right)
        np.testing.assert_allclose(K @ K.conj().T, np.eye(carrier_size), atol=2e-14)
        for q, r in (((0, 0), (0, 0)), ((0, 0), (1, 0)), ((0, 1), (2, 1)), ((0, 0), (1, 1))):
            actual = block(K, K, q, r)
            expected = (sector(label, potential(q)).conj().T @ sector(label, potential(r))/group_order
                        if q[1] == r[1] else np.zeros_like(actual))
            np.testing.assert_allclose(actual, expected, atol=2e-17)
            if q == r:
                assert p*p*np.trace(actual).real == pytest.approx(1/fiber_size)
                assert p*p*np.trace(actual).real != pytest.approx(1/p)  # not center normalization

    # In LEFT-I coordinates the Fourier label changes under conjugation.
    # For g=exp(X), E(1) sends output label (0,0,1) to input (1/2,1,1).
    lam, mu = (0, 0, 1), (pow(2, -1, p), 1, 1)
    correct = block(transform(lam, right), transform(mu, right), (0, 0), (1, 0))
    incorrect = block(transform(lam, left), transform(mu, left), (0, 0), (1, 0))
    np.testing.assert_allclose(correct, 0, atol=2e-17)
    assert np.linalg.norm(incorrect)*group_order > 1


@pytest.mark.parametrize("p", [43, 2**127-1])
def test_strictly_larger_ambient_scope_is_not_just_a_class_four_normal_fixture(p):
    from theorems.class_three_ambient_frontend import certify_ambient_class_three_derived
    algebra, basis, report = derived_length_three_witness(p)
    assert report["ambient_class"] == 9
    assert report["normal_class"] == 4
    assert report["derived_dimensions"][-1] == 0
    with pytest.raises(ValueError, match="class 4 > 3"):
        certify_ambient_class_three_derived(algebra, basis)


@pytest.mark.parametrize("p", [43, 2**127-1])
def test_universal_word_matches_actual_ambient_matrix_right_fiber(p):
    from tests.test_metabelian_phase_extension import finite_matrix_exp_log
    from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates
    algebra, basis, _ = derived_length_three_witness(p)
    normal = algebra.lower_central_series(basis)[1]
    ideal = algebra.lower_central_series(normal)[1]
    adapted = algebra.span(ideal+normal)
    carrier_basis = adapted[len(ideal):]
    assert len(ideal) == 10 and len(carrier_basis) == 7
    slots = tuple((i, j) for i in range(10) for j in range(i+1, 10))
    def matrix(vector):
        result = np.zeros((10, 10), dtype=object)
        for ij, value in zip(slots, vector):
            result[ij] = value
        return result
    def linear_combination(space, rng):
        scalars = [rng.randrange(p) for _ in space]
        return tuple(sum(a*v[j] for a, v in zip(scalars, space)) % p for j in range(algebra.dimension))
    rng = random.Random(9913)
    for _ in range(4):
        a, x = (linear_combination(carrier_basis, rng) for _ in range(2))
        b = linear_combination(ideal, rng)
        compiled = evaluate_induced_cocycle_fixture(algebra, 4, a, b, x)
        A, B, X = matrix(a), matrix(b), matrix(x)
        product_matrix = (finite_matrix_exp_log((-A-X) % p, p)
                          @ finite_matrix_exp_log((A+B) % p, p)
                          @ finite_matrix_exp_log(X, p)) % p
        logarithm = finite_matrix_exp_log(product_matrix, p, logarithm=True)
        actual = tuple(int(logarithm[ij]) for ij in slots)
        assert compiled == actual
        assert _fmpz_solve_coordinates(ideal, compiled, p) is not None


def test_translation_only_complete_regular_ansatz_cannot_cover_nonmetabelian_normal():
    # In ut_9, N=L' contains E13,E35,E57,E79. Its second derived algebra
    # contains [[E13,E35],[E57,E79]]=E19, so N is NOT metabelian.
    algebra, slots = upper_triangular_lie(9, 43)
    def unit(i, j):
        return tuple(int(ij == (i, j)) for ij in slots)
    first = algebra.bracket(unit(0, 2), unit(2, 4))
    second = algebra.bracket(unit(4, 6), unit(6, 8))
    assert algebra.bracket(first, second) == unit(0, 8)
    assert any(algebra.bracket(first, second))
