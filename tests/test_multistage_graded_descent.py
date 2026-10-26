"""Two physical central instruments, not a full Rees/outer quantum receiver.

All matrices are bounded F5 fixtures. The quadratic witness search below is
EXHAUSTIVE TEST DATA, never a production SDE backend or complexity claim.
"""
from functools import cached_property, lru_cache
from itertools import product
import random

import numpy as np
import pytest

from theorems.central_character_descent import (
    check_moment, controlled_discard, exhaustive_scale_fixture,
)
from theorems.weighted_two_erasure_cascade import solve_bezout_sde_weights


class _Filiform:
    """F5 acts on F5^3 by exp(xD), D(y,z,w)=(0,y,z)."""

    def __init__(self, width):
        assert width in (2, 3, 4)
        self.width = width

    @cached_property
    def elements(self):
        return tuple(product(range(5), repeat=self.width))

    @cached_property
    def index(self):
        return {g: i for i, g in enumerate(self.elements)}

    def mul(self, a, b):
        x, y, z, w = a+(0,)*(4-self.width)
        X, Y, Z, W = b+(0,)*(4-self.width)
        return tuple(t % 5 for t in (x+X, y+Y, z+Z+x*Y, w+W+x*Z+3*x*x*Y)[:self.width])

    def inv(self, a):
        x, y, z, w = a+(0,)*(4-self.width)
        return tuple(t % 5 for t in (-x, -y, -z+x*y, -w+x*z-3*x*x*y)[:self.width])

    def dilate(self, a, scale):
        return tuple(x*pow(scale, d, 5) % 5 for x, d in zip(a, (1, 1, 2, 3)))

    def right(self, a):
        inverse = self.inv(a)
        return np.array([self.index[self.mul(x, inverse)] for x in self.elements])

    def density(self, hidden):
        # Hidden data belongs ONLY to input and expected-output construction.
        return np.array([[int(self.mul(self.inv(x), y) in hidden)/len(self.elements)
                          for y in self.elements] for x in self.elements], dtype=complex)


@lru_cache(maxsize=2)
def _public_actions(width):
    group, quotient = _Filiform(width), _Filiform(width-1)
    central_pullbacks = [np.argsort(group.right((0,)*(width-1)+(t,))) for t in range(5)]
    controls = {s: np.array([group.right(group.dilate(q+(0,), s)) for q in quotient.elements])
                for s in range(1, 5)}
    return central_pullbacks, controls


def _central_instrument(rho, width):
    """Literal P_lambda rho P_lambda^dagger using sparse permutation sums."""
    pullbacks, _ = _public_actions(width)
    branches = []
    for label in range(5):
        phases = np.exp(-2j*np.pi*label*np.arange(5)/5)/5
        left = sum(phase*rho[rows, :] for phase, rows in zip(phases, pullbacks))
        projected = sum(phase.conjugate()*left[:, columns]
                        for phase, columns in zip(phases, pullbacks))
        mass = float(np.trace(projected).real)
        if mass > 1e-12:
            branches.append((label, mass, projected/mass))
        else:
            assert np.max(np.abs(projected)) < 1e-13
    np.testing.assert_allclose(sum(mass for _, mass, _ in branches), 1, atol=1e-12)
    np.testing.assert_allclose(sum(mass*state for _, mass, state in branches), rho, atol=1e-12)
    return branches


def _descent_outputs(rho, width):
    """No hidden-subgroup argument; use observed labels and public operations."""
    _, controls = _public_actions(width)
    branches = _central_instrument(rho, width)
    size, degree = 5**(width-1), width-1
    factors = {(label, scale): size*controlled_discard(state, control)
               for label, _, state in branches for scale, control in controls.items()}
    arity = 2 if degree == 3 else 3
    for records in product(branches, repeat=arity):
        labels = tuple((label,) for label, _, _ in records)
        if degree == 3:
            # The real public solver supports bijective cubing at p=5.
            weights, _, _, _ = solve_bezout_sde_weights(5, labels, degree)
        else:
            # Only a finite falsifier: 5^3 assignments, never production.
            weights = exhaustive_scale_fixture(labels, 5, degree)
        active = check_moment(labels, weights, 5, degree)
        out = np.ones((size, size), dtype=complex)/size
        for i in active:
            out *= factors[labels[i][0], weights[i]]
        mass = float(np.prod([mass for _, mass, _ in records]))
        yield labels, mass, out


def _hidden(kind):
    if kind == "X":
        return {(x, 0, 0, 0) for x in range(5)}
    if kind == "XW":
        return {(x, 0, 0, w) for x, w in product(range(5), repeat=2)}
    if kind == "XZW":
        return {(x, 0, z, w) for x, z, w in product(range(5), repeat=3)}
    if kind == "Z":
        return {(0, 0, z, 0) for z in range(5)}
    raise ValueError(kind)


def test_group_is_genuinely_class_three_with_verified_matrix_law_and_nonhomomorphic_section():
    group = _Filiform(4)
    def matrix(a):
        x, y, z, w = a
        return np.array([[1, 0, 0, y], [x, 1, 0, z], [3*x*x % 5, x, 1, w], [0, 0, 0, 1]])
    def comm(a, b):
        return group.mul(group.mul(a, b), group.mul(group.inv(a), group.inv(b)))
    rng = random.Random(871)
    identity = (0,)*4
    for _ in range(100):
        a, b = (tuple(rng.randrange(5) for _ in range(4)) for _ in range(2))
        np.testing.assert_array_equal(matrix(group.mul(a, b)), matrix(a) @ matrix(b) % 5)
        assert group.mul(a, group.inv(a)) == identity
        fifth = identity
        for _ in range(5):
            fifth = group.mul(fifth, a)
        assert fifth == identity
        for s in range(1, 5):
            assert group.dilate(group.mul(a, b), s) == group.mul(group.dilate(a, s), group.dilate(b, s))
    x, y = (1, 0, 0, 0), (0, 1, 0, 0)
    third = comm(x, comm(x, y))
    assert third == (0, 0, 0, 1)
    assert comm(x, third) == comm(y, third) == identity
    quotient = _Filiform(3)
    assert group.mul(x, (0, 0, 1, 0)) != quotient.mul(x[:3], (0, 0, 1))+(0,)


@pytest.mark.parametrize("kind,first_records,second_records", [
    ("X", 25, 125), ("XW", 1, 125), ("XZW", 1, 1), ("Z", 25, 1),
])
def test_two_actual_stages_with_changing_central_intersections(kind, first_records, second_records):
    group, middle, final = _Filiform(4), _Filiform(3), _Filiform(2)
    hidden = _hidden(kind)
    assert all(group.dilate(h, s) in hidden for h in hidden for s in range(1, 5))
    if kind == "X":
        assert group.mul(group.mul((0, 1, 0, 0), (1, 0, 0, 0)), (0, 4, 0, 0)) not in hidden
    if kind == "XZW":
        assert group.mul((1, 0, 0, 0), (0, 0, 1, 0)) != group.mul((0, 0, 1, 0), (1, 0, 0, 0))
    expected_middle = middle.density({h[:3] for h in hidden})
    expected_final = final.density({h[:2] for h in hidden})
    actual_middle, count, mass_sum, source_arities = None, 0, 0.0, set()
    for labels, mass, out in _descent_outputs(group.density(hidden), 4):
        np.testing.assert_allclose(out, expected_middle, atol=2e-13)
        actual_middle = out if actual_middle is None else actual_middle
        count += 1
        mass_sum += mass
        source_arities.add(len(labels))
    assert count == first_records
    assert source_arities == {2}
    np.testing.assert_allclose(mass_sum, 1, atol=1e-12)
    # Feed the ACTUAL reduced density, not an oracle-generated expected state.
    count, mass_sum, raw_copy_counts = 0, 0.0, set()
    for labels, mass, out in _descent_outputs(actual_middle, 3):
        np.testing.assert_allclose(out, expected_final, atol=2e-13)
        count += 1
        mass_sum += mass
        raw_copy_counts.update(len(labels)*arity for arity in source_arities)
    assert count == second_records
    np.testing.assert_allclose(mass_sum, 1, atol=1e-12)
    # The fresh source tree has arities 2 then 3: SIX original inputs per
    # final packet, not two/three or a reused correlated bank of targets.
    assert raw_copy_counts == {6}


def test_skipping_homogenization_really_breaks_cubic_erasure_for_a_slanted_hidden_line():
    group, quotient = _Filiform(4), _Filiform(3)
    hidden = {(t, 0, 0, t) for t in range(5)}
    assert all(group.mul(a, b) in hidden for a in hidden for b in hidden)
    assert group.dilate((1, 0, 0, 1), 2) not in hidden
    expected = quotient.density({h[:3] for h in hidden})
    failing_mass, maximum_error = 0.0, 0.0
    averaged = np.zeros_like(expected)
    for _, mass, out in _descent_outputs(group.density(hidden), 4):
        error = float(np.linalg.norm(out-expected))
        maximum_error = max(maximum_error, error)
        if error > 1e-6:
            failing_mass += mass
        averaged += mass*out
    np.testing.assert_allclose(maximum_error, np.sqrt(2)/5, atol=1e-12)
    np.testing.assert_allclose(failing_mass, 8/25, atol=1e-12)
    # Even the complete record-averaged output is wrong, not merely a
    # separately normalized rare branch of an otherwise correct channel.
    trace_distance = np.abs(np.linalg.eigvalsh(averaged-expected)).sum()/2
    np.testing.assert_allclose(trace_distance, 8/25, atol=1e-12)


def test_final_abelian_image_is_not_the_full_hidden_subgroup_without_rees_or_outer_recovery():
    group = _Filiform(2)
    inputs = [_hidden(kind) for kind in ("X", "XW", "XZW")]
    assert list(map(len, inputs)) == [5, 25, 125]
    outputs = [group.density({h[:2] for h in hidden}) for hidden in inputs]
    np.testing.assert_array_equal(outputs[0], outputs[1])
    np.testing.assert_array_equal(outputs[1], outputs[2])
