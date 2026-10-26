"""Finite algebra/certificate falsifiers, NOT a quantum receiver or solver."""

import itertools
import random
from fractions import Fraction

import pytest
from flint import fq_default_ctx, nmod_mat

from theorems.symplectic_field_chart import (
    candidate_verification_queries, chart_probability, classical_success_bound,
    coefficient_verification_pairs, graph_basis, graph_polynomial, query_matrix,
    recover_symmetric_matrix, symplectic_inverse, upper_unipotent,
)
from theorems.symplectic_socle_probes import (
    add, eye, multiply, scale, symplectic_form, transpose,
)


def symmetric(n, entries):
    out = [[0] * n for _ in range(n)]
    for (i, j), value in zip(itertools.combinations_with_replacement(range(n), 2), entries):
        out[i][j] = out[j][i] = value
    return tuple(map(tuple, out))


def canonical_rows(rows, p):
    reduced, rank = nmod_mat(rows, p).rref()
    return tuple(tuple(int(reduced[i, j]) for j in range(reduced.ncols())) for i in range(rank))


def image(g, rows, p):
    return canonical_rows(transpose(multiply(g, transpose(rows), p)), p)


def lagrangians_rank_two(p):
    """Enumerate RREF subspaces, independently of the graph-chart formulas."""
    j = symplectic_form(2)
    result = []
    for pivots in itertools.combinations(range(4), 2):
        free = [(r, c) for r in range(2) for c in range(pivots[r] + 1, 4) if c not in pivots]
        for values in itertools.product(range(p), repeat=len(free)):
            rows = [[0] * 4 for _ in range(2)]
            for r, pivot in enumerate(pivots):
                rows[r][pivot] = 1
            for (r, c), value in zip(free, values):
                rows[r][c] = value
            rows = tuple(map(tuple, rows))
            if multiply(multiply(rows, j, p), transpose(rows), p) == ((0, 0), (0, 0)):
                result.append(rows)
    assert len(set(result)) == len(result)
    return result


@pytest.mark.parametrize('p', [3, 5, 7, 2**127 - 1])
def test_actual_query_action_and_full_coefficient_reconstruction(p):
    rng = random.Random(271)
    for n in (2, 3, 5):
        for _ in range(5):
            s = symmetric(n, [rng.randrange(p) for _ in range(n * (n + 1) // 2)])
            x = symmetric(n, [rng.randrange(p) for _ in range(n * (n + 1) // 2)])
            coefficients = []
            for j in range(n):
                i = (j + 1) % n
                b, c = graph_polynomial(s, i, j, p)
                coefficients.append(b)
                t = rng.randrange(p)
                g = query_matrix(x, t, i, j, p)
                assert multiply(symplectic_inverse(g, p), g, p) == eye(2 * n)
                # Independent exact block normalization, including large primes.
                acted = multiply(g, graph_basis(s, p), p)
                bottom_inverse = add(eye(n), scale(transpose(tuple(tuple(int(r == i and k == j)
                    for k in range(n)) for r in range(n))), t, p), p)
                normalized = multiply(acted[:n], bottom_inverse, p)
                expected = add(add(s, x, p), add(scale(b, t, p), scale(c, t * t, p), p), p)
                assert normalized == expected
            assert recover_symmetric_matrix(coefficients, p) == s


@pytest.mark.parametrize('p', [3, 5])
@pytest.mark.parametrize('secret', [(0, 0, 0), (1, 2, 1)])
def test_complete_small_fibers_have_the_hpgp_minus_sign(p, secret):
    s = symmetric(2, [v % p for v in secret])
    w = transpose(graph_basis(s, p))
    b, c = graph_polynomial(s, 0, 1, p)
    fibers = {}
    for entries in itertools.product(range(p), repeat=3):
        x = symmetric(2, entries)
        for t in range(p):
            # These actual subspace images only label the TEST oracle.
            label = image(query_matrix(x, t, 0, 1, p), w, p)
            fibers.setdefault(label, []).append((x, t))
    assert len(fibers) == p**3
    for fiber in fibers.values():
        assert len(fiber) == p
        assert {t for _, t in fiber} == set(range(p))
        offsets = {add(x, add(scale(b, t, p), scale(c, t * t, p), p), p) for x, t in fiber}
        assert len(offsets) == 1  # X = z - P(t), not z + P(t).


@pytest.mark.parametrize('p', [3, 5])
def test_exact_chart_count_includes_all_non_graph_lagrangians(p):
    spaces = lagrangians_rank_two(p)
    graphs = {canonical_rows(transpose(graph_basis(symmetric(2, values), p)), p)
              for values in itertools.product(range(p), repeat=3)}
    assert len(spaces) == (p + 1) * (p * p + 1)
    assert len(graphs) == p**3
    assert graphs < set(spaces)
    assert Fraction(len(graphs), len(spaces)) == chart_probability(2, p)


@pytest.mark.parametrize('outer_chart', [False, True])
def test_final_verifier_accepts_exactly_the_correct_hidden_subspace(outer_chart):
    p = 3
    spaces = lagrangians_rank_two(p)
    change = (multiply(upper_unipotent(((1, 1), (1, 2)), p), symplectic_form(2), p)
              if outer_chart else eye(4))
    for entries in itertools.product(range(p), repeat=3):
        s = symmetric(2, entries)
        candidate = image(change, transpose(graph_basis(s, p)), p)
        queries = candidate_verification_queries(s, p, change)
        assert len(queries) == 3
        for w in spaces:
            accepted = all(image(g, w, p) == w for g in queries)
            assert accepted == (candidate == w)


def test_bad_chart_can_pass_every_local_check_but_not_final_verification():
    p = 3
    hidden = ((1, 0, 0, 0), (0, 1, 0, 0))  # L0, not transverse to L0.
    zero = ((0, 0), (0, 0))
    for entries in itertools.product(range(p), repeat=3):
        for t in range(p):
            assert image(query_matrix(symmetric(2, entries), t, 0, 1, p), hidden, p) == hidden
    for j in range(2):
        pairs = coefficient_verification_pairs(zero, zero, (j + 1) % 2, j, p)
        assert all(image(a, hidden, p) == image(b, hidden, p) for a, b in pairs)
    fake_s = recover_symmetric_matrix([zero, zero], p)
    assert any(image(g, hidden, p) != hidden for g in candidate_verification_queries(fake_s, p))


@pytest.mark.parametrize('p', [3, 5, 11])
def test_single_point_certificate_can_miss_wrong_coefficients(p):
    s = ((1, 2), (2, 0))
    w = transpose(graph_basis(s, p))
    b, c = graph_polynomial(s, 0, 1, p)
    d = ((1, 0), (0, 0))
    pairs = coefficient_verification_pairs(add(b, d, p), add(c, scale(d, -1, p), p), 0, 1, p)
    assert image(pairs[0][0], w, p) == image(pairs[0][1], w, p)
    assert image(pairs[1][0], w, p) != image(pairs[1][1], w, p)


@pytest.mark.parametrize('p', [3, 5, 7])
def test_noncentral_full_group_queries_obey_graph_fixed_fraction_bound(p):
    rng = random.Random(941)
    spaces = [canonical_rows(transpose(graph_basis(symmetric(2, entries), p)), p)
              for entries in itertools.product(range(p), repeat=3)]
    centers = [eye(4), scale(eye(4), -1, p)]
    assert all(all(image(z, w, p) == w for w in spaces) for z in centers)
    g = eye(4)
    saw_both_off_diagonal_blocks = False
    for _ in range(45):
        x = symmetric(2, [rng.randrange(p) for _ in range(3)])
        # Include general Bruhat positions, not only the HPGP probe subgroup.
        step = multiply(query_matrix(x, rng.randrange(p), 0, 1, p), symplectic_form(2), p)
        g = multiply(g, step, p)
        assert multiply(symplectic_inverse(g, p), g, p) == eye(4)
        saw_both_off_diagonal_blocks |= (any(g[r][c] for r in range(2) for c in range(2, 4))
                                        and any(g[r][c] for r in range(2, 4) for c in range(2)))
        if g not in centers:
            fixed = sum(image(g, w, p) == w for w in spaces)
            assert Fraction(fixed, len(spaces)) <= Fraction(2, p)
    assert saw_both_off_diagonal_blocks


def test_query_bound_has_the_correct_regime_and_cannot_count_center_collisions():
    assert classical_success_bound(2, 101, 0) == Fraction(1, 101**3)
    assert classical_success_bound(2, 101, 1) == Fraction(1, 101**3)
    assert classical_success_bound(2, 101, 2) == Fraction(1, 101**3) + Fraction(2, 101)
    assert classical_success_bound(2, 101, 20) == 1
    # Growing n alone does not make this lower bound strong at fixed q.
    assert classical_success_bound(100, 3, 3) == 1
    assert chart_probability(100, 3) > Fraction(1, 2)
    with pytest.raises(ValueError):
        classical_success_bound(2, 101, -1)


def test_unmarked_quotient_collision_has_a_symplectic_torsion_witness():
    # Geometric deduction: SIEGEL_NATURAL_SOURCE_AUDIT.md, Section 2.
    # This checks the torsion action only, not a computed isogeny codomain.
    p = 3
    beta = ((0, 0, 2, 0), (0, 1, 0, 0), (1, 0, 0, 0), (0, 0, 0, 1))
    w = ((1, 0, 0, 0), (0, 1, 0, 0))
    assert multiply(symplectic_inverse(beta, p), beta, p) == eye(4)
    assert image(beta, w, p) != w
    assert multiply(beta, beta, p) == ((2, 0, 0, 0), (0, 1, 0, 0),
                                      (0, 0, 2, 0), (0, 0, 0, 1))
    assert not any(x * x % p == p - 1 for x in range(p))


def test_extension_field_prime_variable_fibers_and_verifier():
    k = fq_default_ctx(3, 2, 'a')
    a, zero, one = k.gen(), k(0), k(1)

    def mm(left, right):
        return [[sum((x * y for x, y in zip(row, col)), zero) for col in zip(*right)] for row in left]

    def plus(left, right):
        return [[x + y for x, y in zip(r, s)] for r, s in zip(left, right)]

    def scalar(mat, t):
        return [[t * x for x in row] for row in mat]

    def upper(x):
        return [[one, zero, x[0][0], x[0][1]], [zero, one, x[1][0], x[1][1]],
                [zero, zero, one, zero], [zero, zero, zero, one]]

    def inv2(mat):
        b, c = mat[0]
        d, e = mat[1]
        det = b * e - c * d
        assert det != 0  # FLINT field zeros are truthy.
        return scalar([[e, -c], [-d, b]], det.inverse())

    s = [[a, a + one], [a + one, one]]
    identity = [[one, zero], [zero, one]]
    e = [[zero, one], [zero, zero]]
    et = list(map(list, zip(*e)))
    b = plus(mm(e, s), mm(s, et))
    c = mm(mm(e, s), et)
    values = [k([i, j]) for i, j in itertools.product(range(3), repeat=2)]

    def key(mat):
        return tuple(tuple(int(v) for v in x.to_list()) for row in mat for x in row)

    fibers = {}
    for entries in itertools.product(values, repeat=3):
        x = [[entries[0], entries[1]], [entries[1], entries[2]]]
        for ti in range(3):
            t = k(ti)  # The scalar variable is F3, not Z/9 or all F9.
            levi = plus(identity, scalar(e, t))
            inverse_transpose = plus(identity, scalar(et, -t))
            diagonal = [levi[0] + [zero, zero], levi[1] + [zero, zero],
                        [zero, zero] + inverse_transpose[0], [zero, zero] + inverse_transpose[1]]
            acted = mm(mm(upper(x), diagonal), s + identity)
            actual = mm(acted[:2], inv2(acted[2:]))
            poly = plus(scalar(b, t), scalar(c, t * t))
            assert actual == plus(plus(s, x), poly)
            fibers.setdefault(key(actual), []).append((ti, key(plus(x, poly))))
    assert len(fibers) == 9**3
    assert all(len(fiber) == 3 and len({z for _, z in fiber}) == 1
               and {t for t, _ in fiber} == {0, 1, 2} for fiber in fibers.values())
    # An Fq-basis suffices for verification by Fq-linearity of the hidden W.
    # It does NOT generate the full unipotent group additively over F3.
    for j in range(2):
        i = 1 - j
        ej = [[k(int(r == i and col == j)) for col in range(2)] for r in range(2)]
        bj = plus(mm(ej, s), mm(s, list(map(list, zip(*ej)))))
        recovered = [bj[i][col] / k(2 if col == i else 1) for col in range(2)]
        assert recovered == s[j]
    form = [[k(v) for v in row] for row in symplectic_form(2)]
    symmetric_basis = [[[one, zero], [zero, zero]], [[zero, one], [one, zero]],
                       [[zero, zero], [zero, one]]]
    for candidate in (s, [[zero, zero], [zero, zero]], plus(s, [[a, zero], [zero, zero]])):
        transport = [candidate[0] + [-one, zero], candidate[1] + [zero, -one],
                     [one, zero, zero, zero], [zero, one, zero, zero]]
        inverse = scalar(mm(mm(form, list(map(list, zip(*transport)))), form), -one)
        accepted = True
        for basis in symmetric_basis:
            g = mm(mm(transport, upper(basis)), inverse)
            actual = mm(g, s + identity)
            accepted &= actual[:2] == mm(s, actual[2:])
        assert accepted == (candidate == s)


@pytest.mark.parametrize('n,p', [(1, 3), (2, 2), (2, 4)])
def test_out_of_scope_parameters_are_rejected(n, p):
    with pytest.raises(ValueError):
        upper_unipotent(eye(n), p)


def test_malformed_certificates_and_non_symplectic_changes_are_rejected():
    with pytest.raises(ValueError):
        query_matrix(((0, 1), (0, 0)), 1, 0, 1, 3)
    with pytest.raises(ValueError):
        candidate_verification_queries(eye(2), 3, scale(eye(4), 0, 3))
    with pytest.raises(ValueError):
        candidate_verification_queries(eye(2), 3, eye(6))
    with pytest.raises(ValueError):
        recover_symmetric_matrix([eye(2), eye(2)], 3)
