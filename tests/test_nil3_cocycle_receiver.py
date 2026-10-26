"""Non-split cocycle, physical-source, and complete finite recovery controls."""
from itertools import product
import random

import numpy as np
import pytest
from sympy import Matrix, Rational, expand, symbols

from theorems.affine_phase_erasure import initial_packet, monomials
from theorems.folded_rs_decoder import affine_solution
from theorems.nil3_cocycle_receiver import (
    ClassThreeBCH, controls, coset_fixture, free_step_three, free_two_step_three, graph_branches,
    learn_normal_generator, partial_fourier_branch, potential_fixture,
)


def test_rejects_class_four_and_invalid_derived_presentation():
    vectors = [tuple(int(i == j) for i in range(5)) for j in range(5)]
    with pytest.raises(ValueError, match="exceeds three"):
        ClassThreeBCH(11, 2, 3, {(0, 1): vectors[2], (0, 2): vectors[3], (0, 3): vectors[4]})
    with pytest.raises(ValueError, match="adapted"):
        ClassThreeBCH(11, 2, 3, {(0, 1): vectors[0]})
    with pytest.raises(ValueError, match="exactly"):
        ClassThreeBCH(11, 2, 3, {(0, 1): vectors[2]})


def test_bch_against_truncated_free_associative_algebra():
    group, rng = free_two_step_three(47), random.Random(4)
    p = group.p

    def add(*words):
        keys = set().union(*words)
        return {key: sum(w.get(key, 0) for w in words) % p for key in keys}

    def scale(c, words):
        return {key: c * value % p for key, value in words.items()}

    def multiply(left, right):
        result = {}
        for a, av in left.items():
            for b, bv in right.items():
                if len(a+b) <= 3:
                    result[a+b] = (result.get(a+b, 0) + av*bv) % p
        return result

    def commutator(left, right):
        return add(multiply(left, right), scale(-1, multiply(right, left)))

    x, y = {(0,): 1}, {(1,): 1}
    z = commutator(x, y)
    basis = [x, y, z, commutator(x, z), commutator(y, z)]

    def exponential(coefficients):
        a = add(*(scale(c, word) for c, word in zip(coefficients, basis)))
        aa = multiply(a, a)
        return {key: value for key, value in add({(): 1}, a, scale(pow(2, -1, p), aa),
                scale(pow(6, -1, p), multiply(aa, a))).items() if value}

    for _ in range(80):
        a, b = [tuple(rng.randrange(p) for _ in group.zero) for _ in range(2)]
        exact_product = {key: value for key, value in multiply(exponential(a), exponential(b)).items() if value}
        assert exact_product == exponential(group.bch(a, b))


@pytest.mark.parametrize("rank", [1, 2])
def test_public_chart_and_extension_group_law(rank):
    group, rng = free_two_step_three(11, rank), random.Random(88 + rank)
    for _ in range(80):
        a, b, c = [tuple(rng.randrange(11) for _ in group.zero) for _ in range(3)]
        q, n = group.to_chart(a)
        r, v = group.to_chart(b)
        assert group.from_chart(q, n) == a
        assert group.chart_product(q, n, r, v) == group.to_chart(group.bch(a, b))
        assert group.bch(group.bch(a, b), c) == group.bch(a, group.bch(b, c))
        assert group.bch(a, group.scale(-1, a)) == group.zero


def test_extension_is_genuinely_nonsplit_over_derived_ideal():
    group = free_two_step_three(5)
    # Every pair of lifts of the two quotient basis vectors still has a
    # nonzero z component in its bracket, regardless of ideal corrections.
    for a in product(range(5), repeat=3):
        for b in product(range(5), repeat=3):
            x = (1, 0) + a
            y = (0, 1) + b
            assert group.bracket(x, y)[2] == 1
    assert any(group.cocycle((1, 0), (0, 1)))


def test_cocycle_associativity_identity():
    group, rng = free_two_step_three(5), random.Random(2)
    points = list(product(range(5), repeat=2))
    for q in points:
        for r in points:
            actual = group.to_chart(group.bch(group.lift(q), group.lift(r)))[1]
            assert group.cocycle(q, r) == actual
            s = rng.choice(points)
            left = group.add(group.cocycle(q, r), group.cocycle(group.add(q, r), s))
            right = group.add(group.action(q, group.cocycle(r, s)), group.cocycle(q, group.add(r, s)))
            assert left == right


def test_expanded_potential_increment_exact_rational_coefficients():
    tau, t = symbols("tau t")
    # Ordered Lie words: a, [v,a], [q,a], [q,v], [q,[q,v]], [v,[q,v]].
    coefficients = Matrix([tau, -tau**2/2, tau, tau/2, tau/3, -tau**2/6])
    translation = Matrix.eye(6)
    translation[1, 2] = t
    translation[5, 4] = t
    increment = translation * coefficients.subs(tau, tau+t) - coefficients
    expected = Matrix([t, t**2/2, t, t/2, t/3, t**2/6])
    assert all(expand(entry) == 0 for entry in increment - expected)
    # Omitting the cubic correction must fail this identity.
    wrong = coefficients.copy()
    wrong[5] = Rational(0)
    assert any(expand(entry) != 0 for entry in
               translation * wrong.subs(tau, tau+t) - wrong - expected)


@pytest.mark.parametrize("p", [5, 7, 11])
def test_expanded_potential_arbitrary_functional_and_gauge(p):
    group, rng = free_step_three(p, generators=3), random.Random(201 + p)

    def expanded_potential(h, q, ell):
        v, a, lifted = group.lift(h[:group.m]), group.ideal(h[group.m:]), group.lift(q)
        tau = sum(x*y for x, y in zip(ell, q)) % p
        qv = group.bracket(lifted, v)
        terms = (
            (tau, a),
            (-tau*tau*pow(2, -1, p), group.bracket(v, a)),
            (tau, group.bracket(lifted, a)),
            (tau*pow(2, -1, p), qv),
            (tau*pow(3, -1, p), group.bracket(lifted, qv)),
            (-tau*tau*pow(6, -1, p), group.bracket(v, qv)),
        )
        result = group.zero
        for coefficient, word in terms:
            result = group.add(result, group.scale(coefficient, word))
        assert not any(result[:group.m])
        return result[group.m:]

    for _ in range(3):
        h = (1,) + tuple(rng.randrange(p) for _ in range(group.dimension-1))
        v = h[:group.m]
        ell0 = (1, 0, 0)
        tail = tuple(rng.randrange(p) for _ in range(group.m-1))
        ell1 = ((1-sum(x*y for x, y in zip(tail, v[1:]))) % p,) + tail
        for _ in range(4):
            q = tuple(rng.randrange(p) for _ in range(group.m))
            values = [expanded_potential(h, q, ell) for ell in (ell0, ell1)]
            assert values[0] == potential_fixture(group, h, q)
            gauge = group.add(values[1], group.scale(-1, values[0]))
            for t in (0, 1, p-1):
                shifted = group.add(q, group.scale(t, v))
                outputs = [expanded_potential(h, shifted, ell) for ell in (ell0, ell1)]
                _, orbit = group.to_chart(group.scale(t, h))
                expected = group.add(group.action(q, orbit),
                                     group.cocycle(q, group.scale(t, v)))
                for base, output in zip(values, outputs):
                    assert group.add(output, group.scale(-1, base)) == expected
                assert group.add(outputs[1], group.scale(-1, outputs[0])) == gauge


def test_free_class_three_group_is_not_uniformly_poly_near_hamiltonian():
    group = free_two_step_three(5)
    generators = [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0)]
    lines = [{group.scale(t, v) for t in range(5)} for v in generators]
    normalizer_intersection, center = set(), set()
    for x in product(range(5), repeat=group.dimension):
        if all(group.bracket(x, v) == group.zero for v in generators):
            center.add(x)
        if all(group.bch(group.bch(x, v), group.scale(-1, x)) in line
               for v, line in zip(generators, lines)):
            normalizer_intersection.add(x)
    # The Baer norm lies between the center and this normalizer intersection.
    assert normalizer_intersection == center
    assert len(center) == 5**2
    assert 5**group.dimension // len(center) == 5**3


def test_three_generator_free_lie_case_is_not_a_product_of_two_generator_fixtures():
    group = free_step_three()
    assert group.dimension == 14 and group.m == 3 and group.n == 11
    h = tuple((i+1) % 5 for i in range(group.dimension))
    v, _ = group.to_chart(h)
    points = list(product(range(5), repeat=3))
    basis = [a for a in monomials(3, 3) if any(a)]
    rows = [[int(np.prod([pow(x, a, 5) for x, a in zip(q, alpha)], dtype=object)) % 5
             for alpha in basis] for q in points]
    values = [potential_fixture(group, h, q) for q in points]
    for q, base in zip(points, values):
        for t in range(5):
            shifted = group.add(q, group.scale(t, v))
            _, orbit = group.to_chart(group.scale(t, h))
            assert group.add(potential_fixture(group, h, shifted), group.scale(-1, base)) == group.add(
                group.action(q, orbit), group.cocycle(q, group.scale(t, v)))
    for j in range(group.n):
        assert affine_solution(5, rows, [value[j] for value in values], len(basis)) is not None


@pytest.mark.parametrize("rank", [1, 2])
def test_one_fixed_cubic_potential_not_independent_coset_polynomials(rank):
    group, rng = free_two_step_three(5, rank), random.Random(rank)
    h = tuple((i+1) % 5 for i in range(group.dimension))
    v, _ = group.to_chart(h)
    points = list(product(range(5), repeat=group.m))
    basis = [a for a in monomials(group.m, 3) if any(a)]
    values = [potential_fixture(group, h, q) for q in points]
    for q, base in zip(points, values):
        for t in range(5):
            _, orbit = group.to_chart(group.scale(t, h))
            shift = group.add(q, group.scale(t, v))
            expected = group.add(group.action(q, orbit), group.cocycle(q, group.scale(t, v)))
            assert group.add(potential_fixture(group, h, shift), group.scale(-1, base)) == expected
    rows = [[int(np.prod([pow(x, a, 5) for x, a in zip(q, alpha)], dtype=object)) % 5
             for alpha in basis] for q in points]
    coefficients = []
    for j in range(group.n):
        solution = affine_solution(5, rows, [row[j] for row in values], len(basis))
        assert solution is not None and not solution["basis"]
        coefficients.append(solution["offset"])
    parameters = tuple(coefficients[j][i] for i in range(len(basis)) for j in range(group.n))
    for _ in range(12):
        a = tuple(rng.randrange(5) for _ in group.zero)
        label = tuple(rng.randrange(5) for _ in range(group.n))
        state, probability = partial_fourier_branch(group, coset_fixture(group, h, a), label)
        assert probability == pytest.approx(5**(-group.n))
        packet = initial_packet(5, group.m, label)
        phases = [amplitude*np.exp(-2j*np.pi*packet.evaluate_fixture(q, parameters)/5)
                  for q, amplitude in state.items()]
        assert max(abs(value - phases[0]) for value in phases) < 1e-12


@pytest.mark.parametrize("rank", [1, 2])
def test_cocycle_corrected_graph_relabel_and_omission_falsifier(rank):
    group, rng = free_two_step_three(11, rank), random.Random(30 + rank)
    h = tuple((i+1) % 11 for i in range(group.dimension))
    v = group.scale(3, group.to_chart(h)[0])
    normalized = group.scale(3, h)
    omission_failed = False
    for _ in range(30):
        a = tuple(rng.randrange(11) for _ in group.zero)
        source = coset_fixture(group, h, a)
        for omit in (False, True):
            branches = graph_branches(group, source, v, omit_cocycle=omit)
            assert len(branches) == 1
            state = next(iter(branches.values()))
            offsets = {group.add(key[1:], group.scale(-1, group.to_chart(
                group.scale(key[0], normalized))[1])) for key in state}
            if omit:
                omission_failed |= len(offsets) > 1
            else:
                assert len(offsets) == 1
    assert omission_failed


@pytest.mark.parametrize("seed", [1, 2, 3, 4, 5, 6])
def test_known_hpgp_recovers_normal_coordinate_without_secret_advice(seed):
    group, rng = free_two_step_three(23), random.Random(seed)
    h = (2, 4, 1, 3, 4)
    direction = (1, 2)
    calls = 0

    def source():
        nonlocal calls
        calls += 1
        return coset_fixture(group, h, tuple(rng.randrange(23) for _ in group.zero))

    normal, ledger = learn_normal_generator(group, source, direction, rng)
    recovered = group.from_chart(direction, normal)
    assert recovered == group.scale(pow(2, -1, 23), h)
    assert calls == ledger["source_copies"]
    assert [row["remaining_dimension_before"] for row in ledger["equations"]] == [3, 2, 1]


def test_wrong_direction_rejected_by_actual_graph_support():
    group, rng = free_two_step_three(23), random.Random(81)
    h = (1, 2, 3, 4, 5)
    with pytest.raises(ValueError, match="full graph"):
        learn_normal_generator(group, lambda: coset_fixture(group, h, group.zero), (1, 0), rng)


def test_complete_finite_hidden_generator_recovery():
    report = controls()
    assert report["recovered_same_hidden_subgroup"]
    assert report["full_finite_generator_recovery_executed"]
    assert not report["compiled_quantum_algorithm_executed"]
    assert not report["novelty_established"]
    assert not report["hidden_data_supplied_to_controllers"]
    assert report["original_coset_copies"] == report["quotient_erasure"]["source_copies"] + report["known_quadratic_hpgp"]["source_copies"]
    assert report["quotient_erasure"]["source_copies"] % 7600 == 0
    assert report["quotient_erasure"]["max_final_phase_error"] < 1e-9
    assert report["quotient_erasure"]["zero_fourier_labels"] == 0
    assert report["quotient_erasure"]["single_active_merges"] == {"3": 0, "2": 0, "1": 0}
    assert report["known_quadratic_hpgp"]["quadratic_merges"] > 0
