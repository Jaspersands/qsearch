"""Decisive controls for actual affine support, phases, and public accounting."""
from fractions import Fraction
from itertools import product
from math import comb, prod, sqrt
import random

import numpy as np
import pytest

from theorems.affine_phase_erasure import (
    cancellation_weights, copy_budget, independent_columns, initial_packet,
    leading_columns, merge_branch, monomials, sample_merge, square_weights,
    translate_combine,
)
from theorems.graded_hsp_phase_descent import UT4Product, coset_fixture
from theorems.ut4_affine_phase_receiver import (
    action, graph_relabel_branches, interpolate_potential_fixture, join_coordinates,
    normal_intersection_branches, opaque_classical_query_bound,
    partial_fourier_branch, potential_fixture,
    run_diagnostic, split_coordinates,
)


@pytest.mark.parametrize("p", [7, 11, 23, 1000000007])
@pytest.mark.parametrize("dimension", [1, 3, 6])
def test_public_square_controller(p, dimension):
    rng = random.Random(p + dimension)
    labels = [[rng.randrange(p) for _ in range(dimension)]
              for _ in range((dimension + 1) ** 2)]
    weights = square_weights(p, labels, rng)
    assert any(weights)
    assert all(sum(label[j] * c*c for label, c in zip(labels, weights)) % p == 0
               for j in range(dimension))


def test_zero_columns_and_unsupported_square_field():
    assert square_weights(11, [[0, 0]], random.Random(3)) == [1]
    with pytest.raises(ValueError, match="3 mod 4"):
        square_weights(5, [[1], [2], [3], [4]], random.Random(3))
    with pytest.raises(ValueError, match="needs"):
        square_weights(11, [[1, 0], [0, 1]], random.Random(3))


@pytest.mark.parametrize("rank", [1, 2, 3])
def test_semidirect_chart_and_action(rank):
    group, rng = UT4Product(11, rank), random.Random(rank)
    for _ in range(20):
        g = tuple(rng.randrange(11) for _ in group.identity)
        h = tuple(rng.randrange(11) for _ in group.identity)
        q, a = split_coordinates(group, g)
        r, b = split_coordinates(group, h)
        assert join_coordinates(group, q, a) == g
        combined = join_coordinates(group, tuple((x+y) % 11 for x, y in zip(q, r)),
                                    tuple((x+y) % 11 for x, y in zip(a, action(group, q, b))))
        assert combined == group.multiply(g, h)


@pytest.mark.parametrize("rank", [1, 2])
def test_global_potential_cocycle_including_grade_two(rank):
    group, rng = UT4Product(5, rank), random.Random(rank)
    log = tuple((i + 1) % 5 for i in range(6 * rank))
    h = group.exp(log)
    v, _ = split_coordinates(group, h)
    # All ambient points and all hidden powers, with one shared t across factors.
    for q in product(range(5), repeat=2 * rank):
        base = potential_fixture(group, h, q)
        for t in range(5):
            _, orbit = split_coordinates(group, group.power(h, t))
            shifted = tuple((x + t*y) % 5 for x, y in zip(q, v))
            difference = tuple((a-b) % 5 for a, b in zip(potential_fixture(group, h, shifted), base))
            assert difference == action(group, q, orbit)
    parameters = interpolate_potential_fixture(group, h)
    for _ in range(20):
        label = tuple(rng.randrange(5) for _ in range(4 * rank))
        packet = initial_packet(5, 2 * rank, label)
        q = tuple(rng.randrange(5) for _ in range(2 * rank))
        assert packet.evaluate_fixture(q, parameters) == sum(
            a*b for a, b in zip(label, potential_fixture(group, h, q))) % 5


def test_symbolic_potential_identity_for_all_generator_coefficients():
    import sympy as s
    a, b, c, u, v, w, x, z, tau, t = s.symbols("a b c u v w x z tau t")

    def orbit(t):
        return (u*t + a*b*t**2/2, b*t, v*t - b*c*t**2/2,
                w*t + (a*v-u*c)*t**2/2 - a*b*c*t**3/3)

    def phi(x, z, n):
        U, B, V, W = n
        return (U+x*B, B, V-z*B, W+x*V-z*U-x*z*B)

    potential = tuple(s.expand(y) for y in phi(x-a*tau, z-c*tau, orbit(tau)))
    assert max(s.Poly(y, x, z, tau).total_degree() for y in potential) == 3
    shifted = [y.subs({x: x+a*t, z: z+c*t, tau: tau+t}, simultaneous=True) for y in potential]
    assert all(s.expand(after-before-expected) == 0 for after, before, expected
               in zip(shifted, potential, phi(x, z, orbit(t))))


def test_opaque_classical_family_count_and_query_bound():
    group = UT4Product(5)
    # Prime order makes nonidentity elements belong to a unique cyclic H.
    families, seen = set(), set()
    for element in product(range(5), repeat=6):
        q, _ = split_coordinates(group, element)
        if not any(q) or element in seen:
            continue
        subgroup = {group.power(element, t) for t in range(1, 5)}
        assert not (seen & subgroup)
        seen.update(subgroup)
        families.add(min(subgroup))
    expected, bound = opaque_classical_query_bound(5, 1, 2)
    assert len(families) == expected == 3750
    assert len(seen) == 5**6 - 5**4
    assert bound == Fraction(2, expected)
    assert opaque_classical_query_bound(5, 1, 1000)[1] == 1
    with pytest.raises(ValueError, match="query count"):
        opaque_classical_query_bound(5, 1, -1)


def test_actual_partial_qft_has_shared_potential_and_uniform_labels():
    group, rng = UT4Product(11), random.Random(71)
    h = group.exp((1, 2, 3, 4, 5, 6))
    for _ in range(30):
        a = tuple(rng.randrange(11) for _ in group.identity)
        label = tuple(rng.randrange(11) for _ in range(4))
        state, probability = partial_fourier_branch(group, coset_fixture(group, h, a), label)
        assert probability == pytest.approx(11 ** -4)
        phases = [value * np.exp(-2j * np.pi * sum(
            x*y for x, y in zip(label, potential_fixture(group, h, q))) / 11)
                  for q, value in state.items()]
        assert max(abs(z - phases[0]) for z in phases) < 2e-13


@pytest.mark.parametrize("rank", [1, 2])
def test_learned_line_gives_graph_states_without_oracle_restriction(rank):
    group, rng = UT4Product(11, rank), random.Random(101 + rank)
    h = group.exp(tuple((i + 2) % 11 for i in range(6 * rank)))
    direction, _ = split_coordinates(group, h)
    # Any nonzero representative of the learned line is allowed.
    v = tuple(3*x % 11 for x in direction)
    normalized_generator = group.power(h, 3)
    for _ in range(20):
        a = tuple(rng.randrange(11) for _ in group.identity)
        branches = graph_relabel_branches(group, coset_fixture(group, h, a), v)
        assert len(branches) == 1
        branch = next(iter(branches.values()))
        assert len(branch) == 11
        offsets = set()
        for point in branch:
            t, normal = point[0], point[1:]
            _, orbit = split_coordinates(group, group.power(normalized_generator, t))
            offsets.add(tuple((x-y) % 11 for x, y in zip(normal, orbit)))
        assert len(offsets) == 1
        assert sum(abs(a)**2 for a in branch.values()) == pytest.approx(1)
    wrong = list(v)
    wrong[-1] = (wrong[-1] + 1) % 11
    branches = graph_relabel_branches(group, coset_fixture(group, h, group.identity), wrong)
    assert len(branches) > 1


def test_normal_subgroup_case_needs_no_free_restricted_oracle():
    group = UT4Product(11)
    a = (2, 4, 6, 8, 1, 3)
    inside = group.exp((0, 2, 0, 4, 5, 6))
    outside = group.exp((1, 2, 3, 4, 5, 6))
    branches = normal_intersection_branches(group, coset_fixture(group, inside, a))
    assert len(branches) == 1
    support = list(next(iter(branches.values())))
    normal_subgroup = {split_coordinates(group, group.power(inside, t))[1] for t in range(11)}
    assert {tuple((x-y) % 11 for x, y in zip(q, support[0])) for q in support} == normal_subgroup
    branches = normal_intersection_branches(group, coset_fixture(group, outside, a))
    assert len(branches) == 11
    assert all(len(branch) == 1 for branch in branches.values())


def test_every_shear_branch_against_independent_permutation_simulator():
    p, v, origins = 5, (1, 2), ((2, 4), (0, 3))
    packets = [initial_packet(p, 2, [1]), initial_packet(p, 2, [3])]
    parameters = tuple((i*i + 1) % p for i in range(len(monomials(2, 3)) - 1))
    states = [{tuple((a + t*b) % p for a, b in zip(origin, v)):
               np.exp(2j * np.pi * packet.evaluate_fixture(
                   tuple((a + t*b) % p for a, b in zip(origin, v)), parameters) / p) / sqrt(p)
               for t in range(p)} for origin, packet in zip(origins, packets)]
    weights, branches = [1, 2], {}
    for q0, a in states[0].items():
        for q1, b in states[1].items():
            for x in product(range(p), repeat=2):
                y = tuple(tuple((qj - c*xj) % p for qj, xj in zip(q, x))
                          for q, c in zip((q0, q1), weights))
                branch = branches.setdefault(y, {})
                branch[x] = branch.get(x, 0j) + a*b/p
    total = Fraction(0)
    for y0 in product(range(p), repeat=2):
        for y1 in product(range(p), repeat=2):
            ys = (y0, y1)
            actual, probability = merge_branch(p, states, weights, ys)
            reference = branches.get(ys, {})
            assert set(actual) == set(reference)
            total += probability
            if not actual:
                continue
            assert len(actual) == p
            assert probability == Fraction(1, p**3)
            assert float(probability) == pytest.approx(sum(abs(a)**2 for a in reference.values()))
            assert all(abs(actual[x] - reference[x]/sqrt(float(probability))) < 1e-13 for x in actual)
            packet = translate_combine(packets, weights, ys)
            ratios = [a * np.exp(-2j * np.pi * packet.evaluate_fixture(x, parameters) / p)
                      for x, a in actual.items()]
            assert max(abs(a - ratios[0]) for a in ratios) < 2e-13
    assert total == 1
    assert len(branches) == p**3


def test_nonparallel_lines_do_not_get_free_parallel_support():
    states = [{(t, 0): 1/sqrt(5) for t in range(5)},
              {(0, t): 1/sqrt(5) for t in range(5)}]
    output, probability = merge_branch(5, states, [1, 1], [(0, 0), (0, 0)])
    assert len(output) == 1
    assert probability == Fraction(1, 5**4)


def test_cubic_controller_reads_only_public_maps_and_lowers_degree():
    rng, p = random.Random(8), 11
    packets = [initial_packet(p, 2, [rng.randrange(p) for _ in range(4)]) for _ in range(5)]
    weights, rank = cancellation_weights(packets, 3, rng)
    assert rank <= 4
    for _ in range(10):
        outcomes = [tuple(rng.randrange(p) for _ in range(2)) for _ in packets]
        child = translate_combine(packets, weights, outcomes)
        assert child.degree <= 2
    assert copy_budget(2, 4)["original_cosets_per_output"] == 21125


def test_zero_weight_copy_is_discarded_not_required_to_match():
    first = {(t, 0): 1/sqrt(5) for t in range(5)}
    second = {(0, t): 1/sqrt(5) for t in range(5)}
    output, probability = merge_branch(5, [first, second], [1, 0], [(0, 0), (4, 4)])
    assert output == first
    assert probability == Fraction(1, 25)


def test_dephased_control_has_uniform_fourier_output():
    # Dephasing the source leaves no off-diagonals for the permutation and
    # computational-basis measurement to preserve. A diagonal line mixture
    # has uniform Fourier probabilities, not an annihilator sample.
    p = 5
    points = list(product(range(p), repeat=2))
    rho = np.diag([1/p if q[1] == 2*q[0] % p else 0 for q in points])
    fourier = np.array([[np.exp(-2j*np.pi*sum(a*b for a, b in zip(x, y))/p)/p
                         for y in points] for x in points])
    probabilities = np.real(np.diag(fourier @ rho @ fourier.conj().T))
    assert np.max(abs(probabilities - 1/p**2)) < 1e-14


def test_full_random_source_schedule():
    report = run_diagnostic()
    assert report["counts"]["source_cosets"] == 21125
    assert report["counts"]["merges"] == {"3": 4225, "2": 25, "1": 1}
    assert report["counts"]["zero_fourier_labels"] == 0
    assert report["counts"]["single_active_input_merges"] == {"3": 0, "2": 0, "1": 0}
    ranks = report["counts"]["max_equation_rank"]
    assert 0 < ranks["3"] <= 4
    assert 0 < ranks["2"] <= 12
    assert 0 < ranks["1"] <= 24
    assert report["all_outcomes_retained"]
    assert not report["rare_label_postselection"]
    assert not report["full_hsp_receiver_executed"]
    assert not report["novelty_established"]
    assert report["max_relative_phase_error"] < 1e-9
    assert report["outputs"][0]["fourier_mass_outside_annihilator"] < 1e-16


def _moment_embedding(p, width, labels, degree, moments):
    basis = [alpha for alpha in monomials(width, 3) if any(alpha)]
    column = []
    for delta in monomials(width, degree):
        if sum(delta) != degree:
            continue
        for alpha in basis:
            gamma = tuple(a - d for a, d in zip(alpha, delta))
            factor = prod(comb(a, d) for a, d in zip(alpha, delta)) if min(gamma) >= 0 else 0
            for label in range(labels):
                column.append(factor * moments.get((label, gamma), 0) % p)
    return column


@pytest.mark.parametrize("degree", [1, 2, 3])
def test_translation_moment_embedding_is_injective(degree):
    p, width, labels = 5, 3, 2
    indices = [(a, gamma) for a in range(labels)
               for gamma in monomials(width, 3 - degree)]
    columns = [
        _moment_embedding(p, width, labels, degree, {index: 1})
        for index in indices
    ]
    assert independent_columns(columns, p)[1] == len(indices)
    assert len(indices) == labels * comb(width + 3 - degree, 3 - degree)


def test_adaptive_translations_factor_through_exact_public_moments():
    p, width, labels = 11, 2, 2
    raw_labels = [(1, 0), (0, 1), (1, 1)]
    children, expansions = [], []
    for i in range((labels * (width + 1) + 1)**2):
        raw = [initial_packet(p, width, label) for label in raw_labels]
        weights, _ = cancellation_weights(raw, 3)
        outcomes = [((i + k) % p, (i * i + 3 * k) % p) for k in range(3)]
        children.append(translate_combine(raw, weights, outcomes))
        expansions.append(list(zip(raw_labels, outcomes, weights)))
    assert max(child.degree for child in children) == 2

    def check(packets, leaves, degree):
        columns, moment_columns = leading_columns(packets, degree), []
        indices = [(a, gamma) for a in range(labels)
                   for gamma in monomials(width, 3 - degree)]
        for column, expansion in zip(columns, leaves):
            moments = {
                (a, gamma): sum(
                    label[a] * pow(scale, degree, p)
                    * prod(pow(y, exponent, p) for y, exponent in zip(origin, gamma))
                    for label, origin, scale in expansion
                ) % p
                for a, gamma in indices
            }
            assert list(column) == _moment_embedding(p, width, labels, degree, moments)
            moment_columns.append([moments[index] for index in indices])
        assert independent_columns(columns, p)[1] == independent_columns(moment_columns, p)[1]

    check(children, expansions, 2)
    weights, _ = cancellation_weights(children, 2, random.Random(718))
    # Public outcomes deliberately depend on the already selected weights.
    outcomes = [((i + sum(weights)) % p, i * i % p) for i in range(len(children))]
    parent = translate_combine(children, weights, outcomes)
    assert parent.degree <= 1
    leaves = []
    for expansion, scale, origin in zip(expansions, weights, outcomes):
        for label, previous_origin, previous_scale in expansion:
            leaves.append((
                label,
                tuple((a + previous_scale * b) % p
                      for a, b in zip(previous_origin, origin)),
                previous_scale * scale % p,
            ))
    check([parent], [leaves], 1)


@pytest.mark.parametrize("p,degree,nonpower", [(5, 2, 2), (7, 3, 2)])
def test_column_rescaling_does_not_preserve_diagonal_equation_solutions(p, degree, nonpower):
    original = [(x, y) for x in range(p) for y in range(p)
                if (x or y) and (pow(x, degree, p) + nonpower * pow(y, degree, p)) % p == 0]
    rescaled = [(x, y) for x in range(p) for y in range(p)
                if (x or y) and (pow(x, degree, p) + pow(y, degree, p)) % p == 0]
    assert not original
    assert rescaled
    # Row reduction preserves A*c^degree=0. Arbitrary invertible column
    # changes need not lift through the coordinatewise power map.


def _root_by_smooth_primary_digits(value, prime, degree, nonresidue):
    """Test-only realization of the bit-complexity argument, degrees 2 or 3."""
    if not value:
        return 0
    coprime, order, digits = prime - 1, 1, 0
    while coprime % degree == 0:
        coprime //= degree
        order *= degree
        digits += 1
    if not digits:
        return pow(value, pow(degree, -1, prime - 1), prime)
    assert pow(nonresidue, (prime - 1) // degree, prime) != 1
    assert pow(value, (prime - 1) // degree, prime) == 1
    generator = pow(nonresidue, coprime, prime)
    primary = pow(value, coprime * pow(coprime, -1, order), prime)
    other = value * pow(primary, -1, prime) % prime
    unit = pow(generator, order // degree, prime)
    lookup = {pow(unit, digit, prime): digit for digit in range(degree)}
    exponent = 0
    for j in range(digits):
        residual = primary * pow(generator, -exponent, prime) % prime
        digit = lookup[pow(residual, order // degree**(j + 1), prime)]
        exponent += digit * degree**j
    assert pow(generator, exponent, prime) == primary
    assert exponent % degree == 0
    other_root = pow(other, pow(degree, -1, coprime), prime) if coprime > 1 else 1
    return pow(generator, exponent // degree, prime) * other_root % prime


@pytest.mark.parametrize("p,degree", [
    (5, 2), (7, 3), (13, 2), (13, 3), (17, 2),
    (73, 3), (97, 2), (487, 3),
    (18446744069414584321, 2), ((1 << 127) - 1, 3),
])
def test_root_extraction_uses_only_small_radix_digits(p, degree):
    # Fixtures provide a verified nonresidue. The proposed algorithm uses
    # bounded uniform sampling, not this bounded test-fixture search.
    nonresidue = next(x for x in range(2, 64) if pow(x, (p - 1) // degree, p) != 1)
    for base in (0, 1, 2, 7, p - 1, p // 3):
        value = pow(base, degree, p)
        root = _root_by_smooth_primary_digits(value, p, degree, nonresidue)
        assert pow(root, degree, p) == value
