"""Exact F5 witness-selector obstruction, not a general receiver lower bound.

The fixture retains lower-grade coherence. It tests the line-cover condition
for a diagonal, branchwise exact all-grade selector on FOUR actual class-three
Rees sources. All dual-certificate checks use integers, not an LP solver.
"""

from collections import Counter
from fractions import Fraction
from itertools import product

import pytest


P = 5
POINTS = tuple(product(range(P), repeat=4))
DUAL = {
    (0, 0, 0, 0): 30,
    (0, 0, 0, 1): 10,
    (0, 0, 1, 1): 20,
    (0, 0, 1, 2): 0,
    (0, 0, 1, 4): 10,
    (0, 1, 1, 1): 0,
    (0, 1, 1, 2): 0,
    (0, 1, 1, 3): 5,
    (0, 1, 1, 4): 10,
    (0, 1, 2, 3): 0,
    (1, 1, 1, 1): 30,
    (1, 1, 1, 2): 5,
    (1, 1, 1, 3): 0,
    (1, 1, 1, 4): 0,
    (1, 1, 2, 2): 0,
    (1, 1, 2, 3): 10,
    (1, 1, 2, 4): 5,
    (1, 1, 3, 4): 10,
    (1, 1, 4, 4): 0,
    (1, 2, 3, 4): 10,
}


def _canonical(alpha):
    return min(tuple(sorted(t * x % P for x in alpha)) for t in range(1, P))


def _shift(alpha, scale, t=1):
    return tuple((x + t * s) % P for x, s in zip(alpha, scale))


def _moment(alpha, scale):
    return sum(x * s * s for x, s in zip(alpha, scale)) % P


@pytest.fixture(scope="module")
def cover():
    scales = tuple(s for s in POINTS if any(s)
                   and next(x for x in s if x) == 1
                   and sum(x ** 3 for x in s) % P == 0)
    lines = []
    coverage = Counter()
    for s in scales:
        seen = set()
        for alpha in POINTS:
            if alpha in seen or _moment(alpha, s):
                continue
            line = frozenset(_shift(alpha, s, t) for t in range(P))
            seen.update(line)
            coverage.update(line)
            lines.append((s, line))
    return scales, tuple(lines), coverage


def test_all_labels_have_witnesses_but_witnesses_are_not_selectors(cover):
    scales, lines, coverage = cover
    assert len(scales) == 31
    assert len(lines) == 775
    assert set(coverage) == set(POINTS)
    assert min(coverage.values()) > 0
    for s, line in lines:
        assert len(line) == P
        assert all(_moment(alpha, s) == 0 for alpha in line)
        assert all(_shift(alpha, s) in line for alpha in line)


def test_projective_representatives_do_not_drop_a_witness():
    for s in POINTS:
        if not any(s) or sum(x ** 3 for x in s) % P:
            continue
        factor = pow(next(x for x in s if x), -1, P)
        normalized = tuple(factor * x % P for x in s)
        assert next(x for x in normalized if x) == 1
        assert sum(x ** 3 for x in normalized) % P == 0
        assert {_shift((0,) * 4, s, t) for t in range(P)} == {
            _shift((0,) * 4, normalized, t) for t in range(P)
        }


def test_exact_dual_excludes_complete_diagonal_selector(cover):
    _, lines, _ = cover
    assert {_canonical(alpha) for alpha in POINTS} == DUAL.keys()
    prices = {alpha: DUAL[_canonical(alpha)] for alpha in POINTS}
    assert min(prices.values()) == 0
    assert sum(prices.values()) == 3270
    assert min(sum(prices[alpha] for alpha in line) for _, line in lines) == 30

    # Each legal line has five points and dual price at least five after /6.
    # Nonnegative line weights with point coverage <=1 therefore accept at
    # most sum(prices)/6 of the 625 uniformly weighted points.
    acceptance_bound = Fraction(sum(prices.values()), 6 * len(POINTS))
    assert acceptance_bound == Fraction(109, 125)
    assert 1 - acceptance_bound == Fraction(16, 125)
    assert acceptance_bound < 1


def test_uniform_witness_normalization_changes_along_a_valid_action():
    # Three top characters are one; the fourth complete N-character is zero.
    # The zero slot gives at least one witness for every alpha in this slice.
    ell = (1, 1, 1, 0)
    scales = tuple(s for s in POINTS if any(s)
                   and sum(e * x ** 3 for e, x in zip(ell, s)) % P == 0)
    alpha = (0, 0, 0, 0)
    witness = (0, 1, 4, 0)
    moved = tuple((a + s * e) % P for a, s, e in zip(alpha, witness, ell))
    assert _moment(alpha, witness) == _moment(moved, witness) == 0
    count = lambda a: sum(_moment(a, s) == 0 for s in scales)
    assert count(alpha) == 124
    assert count(moved) == 44
    assert Fraction(1, count(alpha)) != Fraction(1, count(moved))
    assert all(count(a + (0,)) > 0 for a in product(range(P), repeat=3))
