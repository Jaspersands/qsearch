"""Exact algebra/source falsifiers, not a quantum algorithm benchmark."""
from dataclasses import replace
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb
import random

import numpy as np
import pytest

from theorems.ambient_section_potential import polynomial_section_fixture, section_word_certificate
from theorems.graded_hsp_phase_descent import (
    UT4Product, coset_fixture, dilation_product_kernel, moment,
    project_top_center, right_correlations,
)
from theorems.nonabelian_jet_homogenization import (
    FilteredEvaluation, PolynomialJetGroup, bch_certificate, resource_profile,
    ambient_jet_certificate,
)
from theorems.right_abelian_induced_source import upper_triangular_lie
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra
from theorems.ut5_matrix_phase_alignment import _identity, _rank
from tests.test_ambient_section_potential import _matrix_exp, _matrix_log, _matrix_multiply


def normal_fixture(size=5, p=17, m=1):
    ambient, all_slots = upper_triangular_lie(size, p)
    slots = tuple(ij for ij in all_slots if ij[1]-ij[0] >= 2)
    positions = [all_slots.index(ij) for ij in slots]
    def expand(v):
        return tuple(v[slots.index(ij)] if ij in slots else 0 for ij in all_slots)
    def bracket(x, y):
        value = ambient.bracket(expand(x), expand(y))
        return tuple(value[i] for i in positions)
    algebra = PublicLieAlgebra(p, len(slots), bracket)
    group = PolynomialJetGroup(algebra, tuple(j-i for i, j in slots), m, size-1)
    def matrix(v):
        return [[v[slots.index((i, j))] if (i, j) in slots else 0 for j in range(size)]
                for i in range(size)]
    return group, slots, matrix


def design(group):
    """Bounded diagnostic unisolvent design; production points are random."""
    scalar = max(group.weights)
    keys = [(alpha, d) for i, alpha, d in group.indices if group.weights[i] == scalar]
    keys = list(dict.fromkeys(keys))
    rows, points = [], []
    for s, y in product(range(1, scalar+1), product(range(scalar), repeat=group.quotient_width)):
        row = []
        for alpha, d in keys:
            value = pow(s, d, group.p)
            for u, a in zip(y, alpha):
                value = value*pow(u, a, group.p) % group.p
            row.append(value)
        if _rank(rows+[row], group.p) > len(rows):
            rows.append(row)
            points.append((y, s))
        if len(rows) == len(keys):
            break
    assert len(rows) == len(keys)
    return tuple(points)+(((1,)*group.quotient_width, 1),)


def random_polynomial(group, rng, *, jet=False):
    keys = group.indices if jet else tuple((i, alpha, 0) for i, alpha, d in group.indices if d == 1)
    # Include the maximum allowed potential degree, omitted by d=1 indices.
    if not jet:
        from theorems.affine_phase_erasure import monomials
        keys = tuple((i, a, 0) for i, w in enumerate(group.weights)
                     for a in monomials(group.quotient_width, w))
    return {key: v for key in keys if (v := rng.randrange(group.p))}


@pytest.mark.parametrize("degree", range(1, 8))
def test_universal_bch_certificates(degree):
    assert bch_certificate(degree)


@pytest.mark.parametrize("p", [19, 2**127-1])
def test_nonmetabelian_normal_bch_matches_independent_matrix_exponential(p):
    group, slots, matrix = normal_fixture(9, p)
    units = _identity(len(slots))
    e = lambda i, j: units[slots.index((i-1, j-1))]
    a = group.algebra.bracket(e(1, 3), e(3, 5))
    b = group.algebra.bracket(e(5, 7), e(7, 9))
    assert group.algebra.bracket(a, b) == tuple(e(1, 9))  # N'' != 0.
    rng = random.Random(413)
    for _ in range(4):
        x, y = [tuple(rng.randrange(p) for _ in slots) for _ in range(2)]
        expected = _matrix_log(_matrix_multiply(_matrix_exp(matrix(x), p), _matrix_exp(matrix(y), p), p), p)
        assert group.normal_multiply(x, y) == tuple(expected[i][j] for i, j in slots)


def test_formal_cocycle_dilation_and_noncommutative_orientation():
    group, _, _ = normal_fixture(5, 17, 2)
    rng = random.Random(51)
    potential = random_polynomial(group, rng)
    zero = (0, 0)
    for _ in range(5):
        q, r, y = [tuple(rng.randrange(17) for _ in zero) for _ in range(3)]
        scale = rng.randrange(1, 17)
        curve = lambda v: group.normalized_curve_fixture(potential, v)
        qr = tuple((a+b) % 17 for a, b in zip(q, r))
        ys = tuple((a+scale*b) % 17 for a, b in zip(y, q))
        assert curve(qr) == group.multiply(curve(q), group.substitute(curve(r), q))
        assert curve(ys) == group.multiply(curve(y), group.substitute(curve(q), y, scale))
        assert curve(tuple(scale*a % 17 for a in q)) == group.substitute(curve(q), zero, scale)
        hq, hr = (curve(q), q), (curve(r), r)
        assert group.semidirect_multiply(hq, hr) == (curve(qr), qr)
        assert group.dilate(group.semidirect_multiply(hq, hr), scale) == group.semidirect_multiply(
            group.dilate(hq, scale), group.dilate(hr, scale))
    wrong = lambda q: group.multiply(group.substitute(potential, q), group.scale(potential, -1))
    assert wrong((4, 7)) != group.multiply(wrong((1, 2)), group.substitute(wrong((3, 5)), (1, 2)))


def test_normalized_curve_on_nonmetabelian_normal_and_pointwise_oracle_free_maps():
    group, slots, matrix = normal_fixture(9, 19)
    potential = {(i, (w,), 0): (i+1) % 19 for i, w in enumerate(group.weights) if (i+1) % 19}
    f2 = group.normalized_curve_fixture(potential, (2,))
    f3 = group.normalized_curve_fixture(potential, (3,))
    assert group.normalized_curve_fixture(potential, (5,)) == group.multiply(f2, group.substitute(f3, (2,)))
    u, t = (4,), 3
    before = group.evaluate(potential, u, t)
    after = group.evaluate(potential, ((4+3*2) % 19,), t)
    expected = _matrix_log(_matrix_multiply(_matrix_exp(matrix(tuple(-a % 19 for a in before)), 19),
                                           _matrix_exp(matrix(after), 19), 19), 19)
    assert group.evaluate(f2, u, t) == tuple(expected[i][j] for i, j in slots)
    assert group.evaluate(group.multiply(f2, f3), u, t) == group.normal_multiply(
        group.evaluate(f2, u, t), group.evaluate(f3, u, t))


def test_nonnormal_public_subgroup_factorization_and_spectator_invariance():
    group, slots, _ = normal_fixture()
    alignment = FilteredEvaluation(group, design(group))
    rng = random.Random(15)
    assert alignment.spectator_dimension > 0
    found_nonnormal = False
    for _ in range(6):
        carrier = tuple(tuple(rng.randrange(17) for _ in slots) for _ in alignment.points)
        j, k = alignment.factor(carrier)
        assert alignment.multiply(alignment.embed(j), k) == carrier
        a = random_polynomial(group, rng, jet=True)
        moved = alignment.multiply(alignment.embed(a), carrier)
        next_j, next_k = alignment.factor(moved)
        assert next_j == group.multiply(a, j)
        assert next_k == k
        # Conjugating E(a) by arbitrary carrier generally leaves E(J).
        inverse = tuple(tuple(-x % 17 for x in row) for row in carrier)
        conjugate = alignment.multiply(alignment.multiply(carrier, alignment.embed(a)), inverse)
        _, outside = alignment.factor(conjugate)
        found_nonnormal |= any(any(row) for row in outside)
    assert found_nonnormal, "test must not accidentally use an ideal/normal embedding"


def test_complete_register_permutation_and_all_spectator_branch_masses():
    p = 7
    algebra = PublicLieAlgebra(p, 1, lambda x, y: (0,))
    group = PolynomialJetGroup(algebra, (2,), 1, 2)
    alignment = FilteredEvaluation(group, design(group))
    assert len(alignment.points) == 4 and group.dimension == 3
    seen, masses = set(), Counter()
    for xs in product(range(p), repeat=4):
        jet, spectator = alignment.factor(tuple((x,) for x in xs))
        encoded = tuple(jet.get(key, 0) for key in group.indices), spectator
        assert encoded not in seen
        seen.add(encoded)
        masses[spectator] += 1
    assert len(seen) == p**4 and len(masses) == p
    assert set(masses.values()) == {p**3}
    # Original B-copy kernel plus fresh q; condition on Y and on spectator.
    initial_entry = Fraction(1, p**(2*4+1))
    y_mass, spectator_mass = Fraction(1, p**4), Fraction(1, p)
    assert initial_entry/y_mass/spectator_mass == Fraction(1, p**(1+group.dimension))


def test_actual_ambient_certificate_has_no_metabelian_normal_restriction():
    algebra, slots = upper_triangular_lie(9, 19)
    certificate = ambient_jet_certificate(algebra, _identity(len(slots)))
    assert certificate.verify(algebra)
    assert certificate.group.quotient_width == 8
    normal = certificate.normal_basis
    first = algebra.span([algebra.bracket(x, y) for x in normal for y in normal])
    second = algebra.span([algebra.bracket(x, y) for x in first for y in first])
    assert len(second) == 1
    # A claimed deep coordinate cannot contain a shallower vector.
    modified = list(normal)
    high, low = 0, len(normal)-1
    modified[high] = tuple((x+y) % 19 for x, y in zip(modified[high], modified[low]))
    with pytest.raises(ValueError, match="actual ambient filtration"):
        replace(certificate, normal_basis=tuple(modified)).verify(algebra)


def test_graph_coset_support_equals_aligned_matrix_source():
    group, slots, _ = normal_fixture()
    alignment = FilteredEvaluation(group, design(group))
    rng = random.Random(16)
    potential = random_polynomial(group, rng)
    q, r = (3,), (6,)
    fq, fr = [group.normalized_curve_fixture(potential, v) for v in (q, r)]
    carrier = tuple(tuple(rng.randrange(17) for _ in slots) for _ in alignment.points)
    increment = group.multiply(group.scale(fr, -1), fq)
    other = alignment.multiply(alignment.embed(increment), carrier)
    j, k = alignment.factor(carrier)
    jr, kr = alignment.factor(other)
    assert k == kr
    assert group.multiply(fq, j) == group.multiply(fr, jr)
    u = ((r[0]-q[0]) % 17,)
    hidden_graph = group.normalized_curve_fixture(potential, u), u
    assert group.semidirect_multiply((group.scale(j, -1), q), hidden_graph) == (group.scale(jr, -1), r)
    for (y, s), x, xr in zip(alignment.points, carrier, other):
        pq = group.evaluate(potential, ((y[0]+s*q[0]) % 17,), 0)
        pr = group.evaluate(potential, ((y[0]+s*r[0]) % 17,), 0)
        assert group.normal_multiply(pq, x) == group.normal_multiply(pr, xr)
    corrupted = dict(jr)
    key = group.indices[0]
    changed = (corrupted.get(key, 0)+1) % 17
    corrupted.pop(key, None)
    if changed:
        corrupted[key] = changed
    assert group.multiply(fq, j) != group.multiply(fr, corrupted)


def test_actual_nonhomogeneous_hidden_subgroup_lifts_without_secret_in_public_alignment():
    p = 11
    ambient, slots = upper_triangular_lie(4, p)
    e = lambda i, j: tuple(int(ij == (i-1, j-1)) for ij in slots)
    zero = (0,)*len(slots)
    # H=<exp(E12+E24)> is NOT preserved by ambient Carnot dilation.
    hlog = tuple((a+b) % p for a, b in zip(e(1, 2), e(2, 4)))
    group, normal_slots, _ = normal_fixture(4, p, 3)
    qpoly = polynomial_section_fixture(section_word_certificate(3), ambient,
        ((zero, e(2, 3), e(3, 4)), (e(1, 2), zero, zero), (e(2, 4), zero, zero)))
    potential = {(i, alpha, 0): value[slots.index(ij)] for alpha, value in qpoly.items()
                 for i, ij in enumerate(normal_slots) if value[slots.index(ij)]}
    h = (group.normalized_curve_fixture(potential, (1, 0, 0)), (1, 0, 0))
    assert group.dilate(h, 3) == (group.normalized_curve_fixture(potential, (3, 0, 0)), (3, 0, 0))
    assert tuple(a*pow(3, j-i, p) % p for a, (i, j) in zip(hlog, slots)) != tuple(3*a % p for a in hlog)
    # Compare original group cosets, with x the INVERTED normal coordinate.
    actual = UT4Product(p)
    order = ((0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3))
    def original(q, x):
        log_normal = {ij: -a % p for ij, a in zip(normal_slots, x)}
        log_section = dict(zip(order[:3], q))
        return actual.multiply(actual.exp(tuple(log_normal.get(ij, 0) for ij in order)),
                               actual.exp(tuple(log_section.get(ij, 0) for ij in order)))
    alignment = FilteredEvaluation(group, design(group))
    q, r = (2, 3, 4), (7, 3, 4)
    fq, fr = [group.normalized_curve_fixture(potential, v) for v in (q, r)]
    rng = random.Random(17)
    x = tuple(tuple(rng.randrange(p) for _ in normal_slots) for _ in alignment.points)
    xr = alignment.multiply(alignment.embed(group.multiply(group.scale(fr, -1), fq)), x)
    generator = actual.exp(tuple(hlog[slots.index(ij)] for ij in order))
    for (y, s), a, b in zip(alignment.points, x, xr):
        left_q = tuple((yi+s*qi) % p for yi, qi in zip(y, q))
        right_q = tuple((yi+s*qi) % p for yi, qi in zip(y, r))
        difference = actual.multiply(actual.inverse(original(left_q, a)), original(right_q, b))
        assert difference == actual.power(generator, 5*s % p)
    # A quotient difference outside U cannot become a coset edge.
    assert actual.multiply(actual.inverse(original((0, 0, 0), (0, 0, 0))),
                           original((0, 1, 0), (0, 0, 0))) not in {
                               actual.power(generator, i) for i in range(p)}


def test_central_descent_cancels_phase_only_when_hidden_support_is_preserved():
    group, p = UT4Product(7), 7
    labels, scales = [[1], [1]], [1, 3]
    assert not any(moment(labels, scales, 3, p))
    assert any(moment(labels, scales, 1, p))  # Not the old two-moment construction.
    representatives = [(1, 2, 3, 4, 5, 6), (6, 5, 4, 3, 2, 1)]
    def run(logarithm):
        generator = group.exp(logarithm)
        kernels = []
        for a, label in zip(representatives, labels):
            state, probability = project_top_center(group, coset_fixture(group, generator, a), label)
            assert probability == pytest.approx(1/p)
            kernels.append(right_correlations(group, state))
        output = dilation_product_kernel(group, kernels, scales)
        hz = {group.multiply(group.power(generator, h), group.center([z])) for h, z in product(range(p), repeat=2)}
        return max(abs(output.get(g, 0)-int(g in hz)) for g in set(output) | hz)
    assert run([1, 2, 3, 0, 0, 0]) < 1e-12
    assert run([1, 2, 3, 1, 0, 0]) > 0.9


def test_complete_mixed_density_channel_not_just_coset_marginals():
    class Heisenberg(UT4Product):
        def center(self, coordinates):
            return (0, 0, 0, coordinates[0], 0, 0)
    p = 5
    group = Heisenberg(p)
    elements = [(x, y, 0, z, 0, 0) for x, y, z in product(range(p), repeat=3)]
    position = {g: i for i, g in enumerate(elements)}
    rho = np.zeros((len(elements), len(elements)), dtype=complex)
    for y, z in product(range(p), repeat=2):
        coset = [position[x, y, 0, z, 0, 0] for x in range(p)]
        rho[np.ix_(coset, coset)] = 1/len(elements)
    assert np.trace(rho) == pytest.approx(1)
    kernels = {}
    for label in range(p):
        projector = np.zeros_like(rho)
        for z in range(p):
            phase = np.exp(-2j*np.pi*label*z/p)/p
            for x in elements:
                dest = group.multiply(x, group.inverse(group.center([z])))
                projector[position[dest], position[x]] += phase
        projected = projector @ rho @ projector.conj().T
        assert np.trace(projected) == pytest.approx(1/p)
        projected *= p
        kernels[label] = {g: sum(projected[position[x], position[group.multiply(x, group.inverse(g))]]
                                 for x in elements) for g in elements}
        for x, y, _, z, _, _ in elements:
            expected = np.exp(2j*np.pi*label*z/p) if y == 0 else 0
            assert kernels[label][x, y, 0, z, 0, 0] == pytest.approx(expected, abs=1e-12)
    assert (1+2**2) % p == 0
    representatives = [(x, y, 0, 0, 0, 0) for x, y in product(range(p), repeat=2)]
    output = np.zeros((p*p, p*p), dtype=complex)
    expected = np.zeros_like(output)
    for i, g in enumerate(representatives):
        for j, h in enumerate(representatives):
            difference = group.multiply(group.inverse(h), g)
            output[i, j] = kernels[1][difference]*kernels[1][group.dilate(difference, 2)]/(p*p)
            expected[i, j] = int(g[1] == h[1])/(p*p)
    assert np.max(np.abs(output-expected)) < 1e-12
    assert np.trace(output) == pytest.approx(1)


def test_schema_failures_and_rank_failure_are_not_silent():
    group, _, _ = normal_fixture()
    with pytest.raises(ValueError, match="coordinate filtration"):
        replace(group, weights=tuple(2 for _ in group.weights))
    with pytest.raises(ValueError, match="injective"):
        FilteredEvaluation(group, [((0,), 1)]*11)
    with pytest.raises(ValueError, match="nonzero"):
        FilteredEvaluation(group, [((0,), 0)])
    with pytest.raises(ValueError, match="support"):
        group.validate({(0, (3,), 0): 1})
    with pytest.raises(ValueError, match="support"):
        group.semidirect_multiply(({(0, (0,), 0): 1}, (0,)), ({}, (0,)))
    with pytest.raises(ValueError, match="independent of t"):
        group.normalized_curve_fixture({(0, (0,), 1): 1}, (1,))
    with pytest.raises(ValueError, match="nonzero"):
        group.dilate(({}, (0,)), 0)
    table = {(0, 1): (0, 0, 0, 1, 0), (2, 3): (0, 0, 0, 0, 1)}
    table.update({(j, i): tuple(-a % 17 for a in value) for (i, j), value in list(table.items())})
    def invalid_bracket(x, y):
        return tuple(sum(x[i]*y[j]*value[k] for (i, j), value in table.items()) % 17 for k in range(5))
    with pytest.raises(ValueError, match="Jacobi"):
        PolynomialJetGroup(PublicLieAlgebra(17, 5, invalid_bracket), (2, 2, 2, 4, 6), 1, 6)


def test_dimensions_and_conditional_resource_profile():
    group, _, _ = normal_fixture()
    assert len(group.indices) == group.dimension == sum(comb(1+w, 2) for w in group.weights)
    weights = (6, 5, 4, 4, 3, 3, 2, 9, 8, 8, 7, 7, 7, 6, 6, 5, 5)
    report = resource_profile(weights, 2, 43)
    assert report["jet_dimension"] == 994
    assert report["semidirect_dimension"] == 996
    assert report["grade_dimensions"] == {1: 344, 2: 249, 3: 171, 4: 110, 5: 65, 6: 34, 7: 15, 8: 5, 9: 1}
    assert report["original_queries_ceil_log2"] == 1776
    assert report["receiver_executed"] is False
    assert report["general_sde_implemented"] is False
