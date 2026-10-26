"""Independent orbit-state falsifiers; no hard-instance or quantum-run claims."""
from fractions import Fraction
from itertools import product
from math import factorial
import random

import numpy as np
import pytest

from theorems.central_character_descent import HeisenbergFixture
from theorems.rees_hsp_reduction import make_rees_cover, _units
from theorems.rees_projective_source import (
    MomentDesign, design_from_scalar_rows, find_moment_design, projective_source_budget,
)
from theorems.right_abelian_induced_source import upper_triangular_lie, derived_length_three_witness
from tests.test_ambient_section_potential import _matrix_exp


@pytest.mark.parametrize("p,c,length", [(43, 9, 14), (2**127-1, 9, 14), (5, 3, 4)])
def test_small_cyclic_design_has_exact_moments_at_growing_prime(p, c, length):
    design = find_moment_design(p, c, rng=random.Random(1729))
    assert design.method == "verified_small_cyclic_subgroup"
    assert len(set(design.points)) == design.copies_per_block == length
    assert design.moments == (0,)*c
    assert length <= factorial(c+1)


def test_scalar_product_construction_and_characteristic_boundary():
    design = design_from_scalar_rows(3, 2, ((1, 2), (1, 1, 1)))
    assert design.points == (1, 1, 1, 2, 2, 2)
    assert len(set(design.points)) == design.degree == 2
    assert design.copies_per_block == 6  # Not two: multiplicities are physical.
    mutable = list(design.points)
    frozen = MomentDesign(3, 2, mutable, "copied_input")
    mutable[0] = 0
    assert frozen.points == design.points
    large = find_moment_design(1000000007, 4, max_order=4, rng=random.Random(41))
    assert large.method == "scalar_certificate_multiplicative_convolution"
    assert large.moments == (0,)*4
    assert 5 <= len(set(large.points)) <= large.copies_per_block <= factorial(5)
    assert find_moment_design(47, 2, rng=random.Random(9)).copies_per_block <= 6


def test_invalid_moments_coverage_and_scalar_witnesses_are_rejected():
    for p, c, points in ((5, 2, (1, 4)), (5, 2, (1,)*5), (5, 1, (1,)*5), (5, 2, (0, 1)),
                         (9, 2, (1, 8)), (3, 3, (1, 2))):
        with pytest.raises(ValueError):
            MomentDesign(p, c, points, "invalid")
    for rows in (((0, 0), (1, 1, 1)), ((1, 2), (1, 0, 0)),
                 ((1, 2), (1, 1, 1, 0)), ((1, 2),), ((1, -1), (1, 1, 1))):
        with pytest.raises(ValueError):
            design_from_scalar_rows(3, 2, rows)
    # The previously unsupported quartic case now uses a checked scalar row.
    assert find_moment_design(13, 4, max_order=4, rng=random.Random(19)).moments == (0,)*4
    with pytest.raises(ValueError):
        find_moment_design(7, 2, max_trials=0)


def _ut3_source(kind="line", perturb=False):
    group = HeisenbergFixture(3)
    algebra, _ = upper_triangular_lie(3, 3)
    cover = make_rees_cover(algebra, _units(3))
    design = find_moment_design(3, 2, rng=random.Random(5))
    H = tuple((t, 0, 0) if kind == "line" else (0, 0, t) for t in range(3))
    state = np.zeros(27, dtype=complex)
    for t, h in enumerate(H):
        state[group.index[h]] = np.exp(2j*np.pi*t/3)/np.sqrt(3)
    if perturb:
        translated = np.zeros_like(state)
        for h in group.elements:
            translated[group.index[group.multiply((0, 1, 1), h)]] = state[group.index[h]]
        state = np.sqrt(0.8)*state+np.sqrt(0.2)*translated
    def act(g, psi=state):
        result = np.zeros_like(psi)
        result[group.right_permutation(g)] = psi
        return result
    def encode(v):
        x, z, y = v
        return x, y, (z+x*y*2) % 3
    addresses = tuple(product(range(3), repeat=4))
    expected = np.empty((81, 81))
    for i, a in enumerate(addresses):
        for j, b in enumerate(addresses):
            difference = cover.multiply(tuple(-x % 3 for x in b), a)
            expected[i, j] = all(encode(v) in H for v in cover.coefficients(difference)) / 81
    def kernel(points):
        result = np.ones((81, 81), dtype=complex)
        for s in points:
            rows = np.array([act(encode(cover.evaluate(a, s))) for a in addresses])
            result *= rows @ rows.conj().T
        return result
    return group, cover, design, H, state, act, encode, addresses, expected, kernel


@pytest.mark.parametrize("kind", ["line", "center"])
def test_actual_regular_orbit_source_erases_unknown_character_including_even_grade(kind):
    group, cover, design, H, state, act, encode, addresses, expected, kernel = _ut3_source(kind)
    values = {g: np.vdot(state, act(g)) for g in group.elements}
    assert {g for g, value in values.items() if abs(value) > 1-1e-10} == set(H)
    assert abs(values[H[1]]-1) > 1
    if kind == "line":
        assert any(group.multiply(group.multiply(g, H[1]), group.inverse(g)) not in H for g in group.elements)
    actual = kernel(design.points)/81
    np.testing.assert_allclose(actual, expected, atol=2e-14)
    assert np.linalg.eigvalsh(actual).min() > -1e-12
    np.testing.assert_allclose(np.trace(actual), 1, atol=1e-13)
    # Ordinary Rees evaluation points do not automatically cancel the phase.
    bare = kernel(cover.points)/81
    if kind == "center":
        assert np.max(np.abs(bare-expected)) > 0.01


def test_nonorthogonal_orbits_obey_full_source_bound_after_amplification():
    group, _, design, H, state, act, _, _, expected, kernel = _ut3_source(perturb=True)
    values = {g: abs(np.vdot(state, act(g))) for g in group.elements}
    assert {g for g, value in values.items() if value > 1-1e-10} == set(H)
    gamma = 1-max(value for g, value in values.items() if g not in H)
    assert gamma > 0.3
    block = kernel(design.points)
    distances = []
    for k in (1, 2, 4):
        actual = block**k/81
        distance = np.linalg.svd(actual-expected, compute_uv=False).sum()/2
        assert distance <= np.sqrt(81)*(1-gamma)**k/2+1e-13
        distances.append(distance)
        assert np.linalg.eigvalsh(actual).min() > -1e-12
    assert distances[0] > 1e-6 and distances[-1] < distances[0]


def test_reusing_one_copy_invents_symmetries_despite_valid_moments():
    _, cover, design, _, state, act, encode, addresses, expected, kernel = _ut3_source()
    bad = next(i for i in range(81) if expected[i, 0] == 0)
    reused = state.copy()
    for s in design.points:
        reused = act(encode(cover.evaluate(addresses[bad], s)), reused)
    # Each of two commuting evaluations occurs three times on ONE copy.
    np.testing.assert_allclose(reused, state, atol=1e-13)
    assert abs(kernel(design.points)[bad, 0]) < 1e-13


def test_nonabelian_nonnormal_hidden_support_in_actual_ut4_regular_action():
    p = 5
    algebra, slots = upper_triangular_lie(4, p)
    cover = make_rees_cover(algebra, _units(6))
    design = find_moment_design(p, 3, rng=random.Random(1729))
    pos = {ij: i for i, ij in enumerate(slots)}
    zero = (0,)*6
    def mul(a, b):
        return tuple((a[pos[i, j]]+b[pos[i, j]]+
                      sum(a[pos[i, k]]*b[pos[k, j]] for k in range(i+1, j))) % p for i, j in slots)
    def inv(a):
        out = [0]*6
        for gap in range(1, 4):
            for i in range(4-gap):
                j = i+gap
                out[pos[i, j]] = (-a[pos[i, j]]-sum(a[pos[i, k]]*out[pos[k, j]]
                                                     for k in range(i+1, j))) % p
        return tuple(out)
    def encode(v):
        matrix = [[v[pos[i, j]] if (i, j) in pos else 0 for j in range(4)] for i in range(4)]
        exponential = _matrix_exp(matrix, p)
        return tuple(exponential[i][j] for i, j in slots)
    H = {tuple(a if ij == (0, 1) else b if ij == (0, 2) else d if ij == (1, 2) else 0
               for ij in slots) for a, b, d in product(range(p), repeat=3)}
    e01, e12, e23 = [tuple(int(ij == pair) for ij in slots) for pair in ((0, 1), (1, 2), (2, 3))]
    assert mul(e01, e12) != mul(e12, e01)
    assert mul(mul(e23, e12), inv(e23)) not in H
    state = {h: np.exp(2j*np.pi*h[pos[0, 1]]/p)/np.sqrt(len(H)) for h in H}
    def orbit(g):
        return {mul(h, inv(g)): value for h, value in state.items()}
    hidden_units = [u for u in _units(cover.dimension) if all(encode(v) in H for v in cover.coefficients(u))]
    rng = random.Random(37)
    addresses = [(0,)*cover.dimension]+hidden_units
    for _ in range(4):
        a = tuple(rng.randrange(p) for _ in range(cover.dimension))
        addresses.extend((a, cover.multiply(a, hidden_units[0])))
    size = len(addresses)
    actual = np.ones((size, size), dtype=complex)
    for s in design.points:
        states = [orbit(encode(cover.evaluate(a, s))) for a in addresses]
        actual *= np.array([[sum(value*states[j].get(g, 0).conjugate() for g, value in states[i].items())
                             for j in range(size)] for i in range(size)])
    expected = np.array([[all(encode(v) in H for v in cover.coefficients(
        cover.multiply(tuple(-x % p for x in b), a))) for b in addresses] for a in addresses])
    np.testing.assert_allclose(actual, expected, atol=3e-14)
    assert np.count_nonzero(expected) not in (size, size*size)


def test_complete_budget_is_copy_only_and_does_not_cover_mixed_conjugation():
    algebra, ambient, *_ = derived_length_three_witness(43)
    cover = make_rees_cover(algebra, ambient)
    design = find_moment_design(43, 9, rng=random.Random(1729))
    budget = projective_source_budget(cover, design, Fraction(1, 10), Fraction(1, 20))
    assert budget["total_fresh_copies"] == 14*budget["blocks_per_leaf"]*budget["source_leaves"]
    assert budget["total_controlled_action_calls"] == budget["total_fresh_copies"]
    assert (budget["copy_and_action_error_per_use"]*budget["total_fresh_copies"]
            + budget["receiver_error_bound"]+budget["source_replacement_error_bound"]
            == budget["total_error_bound"] <= Fraction(1, 20))
    for key in ("ordinary_hiding_oracle_required", "conjugate_state_required", "preparation_inverse_required",
                "mixed_conjugation_symmetry_covered", "quantum_receiver_implemented", "speedup_claim_allowed"):
        assert not budget[key]
    group = HeisenbergFixture(3)
    rho = np.eye(27)/27
    R = np.eye(27)[np.argsort(group.right_permutation((1, 0, 0)))]
    np.testing.assert_allclose(R @ rho @ R.conj().T, rho)
    assert abs(np.trace(rho @ R)) < 1e-14  # Conjugation symmetry is not scalar support symmetry.
    with pytest.raises(ValueError):
        projective_source_budget(cover, design, Fraction(0))
    with pytest.raises(ValueError):
        design.inputs(make_rees_cover(upper_triangular_lie(3, 3)[0], _units(3)), (0,)*4)
