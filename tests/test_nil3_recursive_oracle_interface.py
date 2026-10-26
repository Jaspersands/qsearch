"""Finite countercontrols for the written ISS composition, not its execution."""

from itertools import product

import numpy as np
import pytest

from theorems.nil3_cocycle_receiver import free_two_step_three


def _coordinate_span(group, coordinates):
    values = set()
    for entries in product(range(group.p), repeat=len(coordinates)):
        vector = [0] * group.dimension
        for i, value in zip(coordinates, entries):
            vector[i] = value
        values.add(tuple(vector))
    return values


def _normalizer_of_coordinate_subgroup(group, coordinates):
    generators = [
        tuple(int(i == j) for j in range(group.dimension)) for i in coordinates
    ]
    outside = set(range(group.dimension)) - set(coordinates)
    normalizer = set()
    for g in product(range(group.p), repeat=group.dimension):
        inverse = group.scale(-1, g)
        images = [group.bch(group.bch(inverse, h), g) for h in generators]
        if all(not any(image[i] for i in outside) for image in images):
            normalizer.add(g)
    return normalizer


def test_normalizer_must_be_recomputed_in_original_ambient_group():
    group = free_two_step_three(5)
    # Basis X,Y,Z,A,B with [X,Y]=Z, [X,Z]=A, [Y,Z]=B.
    tower = [[0], [0, 3, 4], [0, 2, 3, 4], list(range(5))]
    assert [len(_coordinate_span(group, indices)) for indices in tower] == [
        5, 125, 625, 3125
    ]
    for current, expected in zip(tower, tower[1:]):
        assert _normalizer_of_coordinate_subgroup(group, current) == (
            _coordinate_span(group, expected)
        )

    # H=G is allowed. An ideal solver confined forever to the first
    # normalizer returns only 125 of H's 3125 elements.
    hidden = _coordinate_span(group, tower[-1])
    first_ambient = _coordinate_span(group, tower[1])
    assert hidden & first_ambient == first_ambient
    assert first_ambient < hidden


@pytest.mark.parametrize("p", [2, 3, 5, 7])
def test_arbitrary_minimal_generator_powers_can_lose_order_p_hidden_subgroup(p):
    ambient = set(product(range(p * p), range(p)))
    g1, g2 = (1, 0), (1, 1)

    def scale(k, g):
        return (k * g[0] % (p * p), k * g[1] % p)

    def span(left, right):
        return {
            ((i * left[0] + j * right[0]) % (p * p),
             (i * left[1] + j * right[1]) % p)
            for i in range(p * p)
            for j in range(p * p)
        }

    assert span(g1, g2) == ambient
    assert len({scale(k, g1) for k in range(p * p)}) == p * p
    assert len({scale(k, g2) for k in range(p * p)}) == p * p
    assert len(ambient) == p**3  # Neither generator can be omitted.

    wrong = span(scale(p, g1), scale(p, g2))
    kernel = {g for g in ambient if scale(p, g) == (0, 0)}
    correct_basis_kernel = span((p, 0), (0, 1))
    hidden = {(0, b) for b in range(p)}
    assert wrong < kernel == correct_basis_kernel
    assert len(wrong) == p
    assert len(kernel) == p * p
    assert not hidden <= wrong
    assert hidden <= kernel


@pytest.mark.parametrize("p", [2, 3])
def test_small_characteristic_order_p_elements_need_not_form_a_subgroup(p):
    identity = np.eye(p + 1, dtype=np.int64)
    a, b = identity.copy(), identity.copy()
    for i in range(p - 1):
        a[i, i + 1] = 1
    b[p - 1, p] = 1
    assert np.array_equal(np.linalg.matrix_power(a, p) % p, identity)
    assert np.array_equal(np.linalg.matrix_power(b, p) % p, identity)
    assert not np.array_equal(np.linalg.matrix_power(a @ b, p) % p, identity)
    assert np.array_equal(np.linalg.matrix_power(a @ b, p * p) % p, identity)


@pytest.fixture(scope="module")
def quotient_oracle_control():
    group = free_two_step_three(5)
    known = _coordinate_span(group, [0])
    hidden = _coordinate_span(group, [0, 2, 3])
    normalizer = _coordinate_span(group, [0, 3, 4])
    quotient = list(product(range(group.p), repeat=2))

    def section(q, nonlinear=False):
        a, b = q
        return ((a * a + b) % group.p if nonlinear else 0, 0, 0, a, b)

    def hiding_value(g):
        return min(group.bch(g, h) for h in hidden)

    return group, known, hidden, normalizer, quotient, section, hiding_value


def test_quotient_oracle_is_section_independent_without_homomorphic_lift(
    quotient_oracle_control,
):
    group, known, hidden, normalizer, quotient, section, oracle = quotient_oracle_control
    assert known < hidden
    assert not hidden <= normalizer
    assert len(hidden & normalizer) // len(known) == group.p
    labels = {q: oracle(section(q)) for q in quotient}
    for q in quotient:
        assert section(q) in normalizer
        assert section(q, True) in normalizer
        assert oracle(section(q, True)) == labels[q]
        difference = group.bch(group.scale(-1, section(q)), section(q, True))
        assert difference in known
        for other in quotient:
            assert (labels[q] == labels[other]) == (q[1] == other[1])

    # This alternative section is public and valid, but deliberately
    # nonhomomorphic. The quotient oracle must not require a splitting.
    assert group.bch(section((1, 0), True), section((1, 0), True)) != section(
        (2, 0), True
    )


def test_leaving_public_lift_workspace_dephases_hidden_cosets(
    quotient_oracle_control,
):
    _, _, _, _, quotient, section, oracle = quotient_oracle_control
    dimension = len(quotient)
    labels = [oracle(section(q)) for q in quotient]
    lifts = [section(q) for q in quotient]
    # Trace out the oracle's label. A clean lift/uncompute retains all
    # equal-label edges; discarding the still-populated lift does not.
    clean = np.array([
        [int(labels[i] == labels[j]) for j in range(dimension)]
        for i in range(dimension)
    ], dtype=float) / dimension
    dirty = np.array([
        [int(labels[i] == labels[j] and lifts[i] == lifts[j])
         for j in range(dimension)]
        for i in range(dimension)
    ], dtype=float) / dimension
    assert np.array_equal(dirty, np.eye(dimension) / dimension)
    assert not np.array_equal(clean, dirty)
    assert np.isclose(np.trace(clean @ clean), 1 / 5)
    assert np.isclose(np.trace(dirty @ dirty), 1 / 25)
