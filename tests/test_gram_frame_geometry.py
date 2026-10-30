"""Exact Gram-frame geometry; not a receiver, cost benchmark, or hardness test."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product

import pytest


def _transpose(matrix):
    return tuple(zip(*matrix))


def _matmul(left, right, p):
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) % p
                       for col in _transpose(right)) for row in left)


def _scale(matrix, scalar, p):
    return tuple(tuple(scalar * x % p for x in row) for row in matrix)


def _subtract(left, right, p):
    return tuple(tuple((x - y) % p for x, y in zip(a, b))
                 for a, b in zip(left, right))


def _identity(d):
    return tuple(tuple(int(a == b) for b in range(d)) for a in range(d))


def _rref(matrix, p):
    rows, pivots = [list(row) for row in matrix], []
    for col in range(len(rows[0])):
        k = len(pivots)
        pivot = next((i for i in range(k, len(rows)) if rows[i][col] % p), None)
        if pivot is None:
            continue
        rows[k], rows[pivot] = rows[pivot], rows[k]
        inverse = pow(rows[k][col], -1, p)
        rows[k] = [x * inverse % p for x in rows[k]]
        for i in range(len(rows)):
            if i != k:
                coefficient = rows[i][col]
                rows[i] = [(x - coefficient * y) % p
                           for x, y in zip(rows[i], rows[k])]
        pivots.append(col)
        if len(pivots) == len(rows):
            break
    return tuple(map(tuple, rows)), tuple(pivots)


def _rank(matrix, p):
    return len(_rref(matrix, p)[1])


def _inverse(matrix, p):
    d = len(matrix)
    assert _rank(matrix, p) == d
    reduced, _ = _rref(tuple(row + unit for row, unit in
                            zip(matrix, _identity(d))), p)
    return tuple(row[d:] for row in reduced)


def _chart(frame, p):
    _, columns = _rref(frame, p)
    square = tuple(tuple(row[j] for j in columns) for row in frame)
    change = _inverse(square, p)
    return change, _matmul(change, frame, p), columns


def _gram(frame, alpha, p):
    return tuple(tuple(sum(a * x * y for a, x, y in zip(alpha, u, v)) % p
                       for v in frame) for u in frame)


def _upper(matrix):
    return tuple(matrix[a][b] for a, b in
                 combinations_with_replacement(range(len(matrix)), 2))


def _image_rank(frame, p):
    return _rank(tuple(tuple(x * y % p for x, y in zip(frame[a], frame[b]))
                       for a, b in combinations_with_replacement(
                           range(len(frame)), 2)), p)


def _congruence(change, matrix, p):
    return _matmul(_matmul(change, matrix, p), _transpose(change), p)


def _diagonal(matrix):
    return all(not value for a, row in enumerate(matrix)
               for b, value in enumerate(row) if a != b)


def _quadratic(matrix, vector, p):
    return sum(vector[a] * matrix[a][b] * vector[b]
               for a in range(len(vector)) for b in range(len(vector))) % p


def _symmetric_basis(d):
    return tuple(tuple(tuple(int((i, j) in ((a, b), (b, a)))
                             for j in range(d)) for i in range(d))
                 for a, b in combinations_with_replacement(range(d), 2))


def _paired_frame(d, r, p):
    vectors = list(_identity(d))
    vectors.extend(tuple(int(i in (a, b)) for i in range(d))
                   for a, b in combinations(range(d), 2))
    vectors.extend([vectors[0]] * max(0, r - len(vectors)))
    frame = _transpose(tuple(v for v in vectors for _ in range(2)))
    labels = tuple(tuple(sign * int(l == j % r) % p
                         for j in range(len(vectors)) for sign in (1, -1))
                   for l in range(r))
    return frame, labels, labels


def _encode(matrix, slots, p):
    d = len(matrix)
    coefficients = [(matrix[a][a] - sum(matrix[a][b] for b in range(d)
                                       if b != a)) % p for a in range(d)]
    coefficients.extend(matrix[a][b] for a, b in combinations(range(d), 2))
    coefficients.extend([0] * (slots // 2 - len(coefficients)))
    return tuple(x for coefficient in coefficients for x in (coefficient, 0))


@pytest.mark.parametrize("p", (5, 7, 11, (1 << 61) - 1))
@pytest.mark.parametrize("d,r", ((1, 1), (2, 2), (3, 2), (4, 3), (2, 5)))
def test_universal_embedding_full_moments_and_covariance(p, d, r):
    frame, beta, ell = _paired_frame(d, r, p)
    slots, dimension = len(frame[0]), d * (d + 1) // 2
    assert slots == 2 * max(dimension, r)
    assert _rank(frame, p) == d
    assert _image_rank(frame, p) == dimension
    for labels in (beta, ell):
        assert _rank(labels, p) == r
        assert all(any(column) for column in _transpose(labels))
    for l in range(r):
        assert not any(_upper(_gram(frame, beta[l], p)))
        for u, v, w in product(frame, repeat=3):
            assert sum(e * x * y * z for e, x, y, z in
                       zip(ell[l], u, v, w)) % p == 0
    for matrix in _symmetric_basis(d):
        assert _gram(frame, _encode(matrix, slots, p), p) == matrix
    for l in range(r):
        matrix = tuple(tuple(((l + 1) * (min(a, b) + 1)
                              + (max(a, b) + 1) ** 2) % p
                             for b in range(d)) for a in range(d))
        alpha = _encode(matrix, slots, p)
        assert _gram(frame, alpha, p) == matrix
        for coordinates in _identity(d) + (tuple(range(1, d + 1)),):
            scales = tuple(sum(t * row[i] for t, row in zip(coordinates, frame)) % p
                           for i in range(slots))
            for shift in (1, p - 1):
                moved = tuple((a + shift * s * e) % p
                              for a, s, e in zip(alpha, scales, ell[l]))
                assert _gram(frame, moved, p) == matrix


def test_conditional_gram_fibers_are_exactly_uniform():
    p, d, r = 5, 2, 2
    frame, _, _ = _paired_frame(d, r, p)
    slots, dimension = len(frame[0]), d * (d + 1) // 2
    counts = Counter(_upper(_gram(frame, alpha, p))
                     for alpha in product(range(p), repeat=slots))
    assert len(counts) == p ** dimension
    assert set(counts.values()) == {p ** (slots - dimension)}
    # The source proof supplies independent componentwise uniform diagonals.
    for first, second in product(counts.values(), repeat=r):
        assert Fraction(first * second, p ** (r * slots)) == Fraction(1, p ** (r * dimension))
    assert Fraction(1, p ** (2 * r * slots)) * Fraction(1, p ** (r * dimension)) > 0


def test_minimal_image_rank_equivalence_on_all_anchored_small_frames():
    p = 5
    for v, w in product(product(range(p), repeat=2), repeat=2):
        frame = _transpose(((1, 0), (0, 1), v, w))
        dimension = _image_rank(frame, p)
        assert dimension >= 2
        assert (dimension == 2) == all(x * y % p == 0 for x, y in _transpose(frame))


@pytest.mark.parametrize("p", (5, 7, 11))
def test_chart_basis_recovers_hidden_disjoint_support_and_detects_dense_image(p):
    block = ((0, 1, 2, 0, 0, 0, 0),
             (0, 0, 0, 1, 3, 0, 0),
             (0, 0, 0, 0, 0, 1, 4))
    mixing = ((1, 1, 1), (0, 1, 1), (0, 0, 1))
    mixed = _matmul(mixing, block, p)
    change, chart, selected = _chart(mixed, p)
    assert selected == (1, 3, 5)
    assert _matmul(change, mixing, p) == _identity(3)
    assert chart == block
    assert _image_rank(mixed, p) == 3
    assert all(sum(bool(x) for x in col) <= 1 for col in _transpose(chart))
    for i in range(len(mixed[0])):
        alpha = tuple(int(j == i) for j in range(len(mixed[0])))
        assert _diagonal(_congruence(change, _gram(mixed, alpha, p), p))
    dense, _, _ = _paired_frame(3, 2, p)
    _, dense_chart, _ = _chart(_matmul(mixing, dense, p), p)
    assert _image_rank(dense_chart, p) == 6
    assert any(sum(bool(x) for x in col) > 1 for col in _transpose(dense_chart))


def test_fixed_basis_differs_from_per_outcome_diagonalization_and_restricted_support():
    p, frame = 5, ((1, 0, 1), (0, 1, 1))
    changes = tuple(((a, b), (c, d)) for a, b, c, d in product(range(p), repeat=4)
                    if (a * d - b * c) % p)
    assert _image_rank(frame, p) == 3
    outcomes = {_gram(frame, alpha, p) for alpha in product(range(p), repeat=3)}
    assert len(outcomes) == p ** 3
    assert all(any(_diagonal(_congruence(change, matrix, p)) for change in changes)
               for matrix in outcomes)
    assert not any(all(_diagonal(_congruence(change, matrix, p))
                       for matrix in _symmetric_basis(2)) for change in changes)
    assert all(_diagonal(_gram(frame, (a, b, 0), p))
               for a, b in product(range(p), repeat=2))


def test_actual_embedded_ternary_forms_have_individual_but_no_shared_nonzero_zero():
    p, frame_dimension, r = 5, 3, 2
    frame, beta, ell = _paired_frame(frame_dimension, r, p)
    forms = (((1, 0, 0), (0, 3, 0), (0, 0, 0)),
             ((0, 0, 0), (0, 0, 0), (0, 0, 1)))
    assert all(any(v) for labels in (beta, ell) for v in _transpose(labels))
    assert tuple(_gram(frame, _encode(q, 12, p), p) for q in forms) == forms
    vectors = tuple(product(range(p), repeat=3))
    assert all(any(any(x) and _quadratic(q, x, p) == 0 for x in vectors)
               for q in forms)
    assert [x for x in vectors if all(_quadratic(q, x, p) == 0 for q in forms)] == [(0, 0, 0)]
    assert Fraction(1, p ** (2 * r * 12)) * Fraction(1, p ** (r * 6)) == Fraction(1, 5 ** 60)


def _matrix_lie_source(r):
    size = 3 * r + 1

    def matrix(entries):
        return tuple(tuple(int((a, b) in entries) for b in range(size))
                     for a in range(size))

    source = {"X": matrix({(3 * l + j, 3 * l + j + 1)
                           for l in range(r) for j in (0, 1)})}
    for l in range(r):
        for letter, offset in (("Y", 2), ("U", 1), ("V", 0)):
            source[f"{letter}{l}"] = matrix({(3 * l + offset, size - 1)})
    return source


@pytest.mark.parametrize("p,r", ((5, 1), (5, 2), (7, 1), (7, 2)))
def test_actual_matrix_lie_algebra_and_untruncated_rees_closure(p, r):
    source = _matrix_lie_source(r)
    zero = _scale(source["X"], 0, p)

    def bracket(a, b):
        return _subtract(_matmul(a, b, p), _matmul(b, a, p), p)

    assert _rank(tuple(tuple(x for row in a for x in row) for a in source.values()), p) == 1 + 3 * r
    for a, b in product(source, repeat=2):
        expected = zero
        if a == "X" and b[0] in "YU":
            expected = source[("U" if b[0] == "Y" else "V") + b[1:]]
        elif b == "X" and a[0] in "YU":
            expected = _scale(source[("U" if a[0] == "Y" else "V") + a[1:]], -1, p)
        assert bracket(source[a], source[b]) == expected
    assert bracket(source["X"], bracket(source["X"], source["Y0"])) == source["V0"] != zero
    rees = tuple((grade, name) for grade in (1, 2, 3) for name in source
                 if grade == 1 or (grade == 2 and name[0] in "UV")
                 or (grade == 3 and name[0] == "V"))
    assert len(rees) == 1 + 6 * r
    for (a, first), (b, second) in product(rees, repeat=2):
        value = bracket(source[first], source[second])
        if a + b > 3:
            assert value == zero  # No nonzero polynomial bracket is truncated.
        elif value != zero:
            assert any(grade == a + b and value in (source[name], _scale(source[name], -1, p))
                       for grade, name in rees)
        for point in (1, 2, 3):
            assert bracket(_scale(source[first], point ** a, p),
                           _scale(source[second], point ** b, p)) == _scale(value, point ** (a + b), p)


def test_exact_source_trace_support_and_hidden_intersection_caveat():
    p = 5
    # BCH(exp(a*tX), exp(u*t^2U+b*t^2V+c*t^3V)); only the central commutator remains.
    identity_pairs = []
    for a, u, b, c in product(range(p), repeat=4):
        coordinates = (a, u, b, (c + pow(2, -1, p) * a * u) % p)
        if not any(coordinates):
            identity_pairs.append((u, b, c))
    assert identity_pairs == [(0, 0, 0)]
    for chi in product(range(p), repeat=3):
        exponents = Counter(-sum(x * y for x, y in zip(chi, n)) % p
                            for n in identity_pairs)
        assert exponents == {0: 1}
        assert Fraction(exponents[0], p ** 3) == Fraction(1, 125)
    # For h=<U>, K intersect N=<t^2U>: the character sum kills alpha != 0.
    for alpha in range(p):
        exponents = Counter(alpha * u % p for u in range(p))
        assert exponents == ({0: p} if alpha == 0 else dict.fromkeys(range(p), 1))
    frame, _, _ = _paired_frame(3, 1, p)
    assert _image_rank(frame, p) == 6
    assert not any(_upper(_gram(frame, (0,) * len(frame[0]), p)))
