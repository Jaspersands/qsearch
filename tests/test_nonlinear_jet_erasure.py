"""Exact public algebra and finite channel falsifiers, not an HSP execution."""
from itertools import product
from fractions import Fraction
from math import comb, prod, sqrt
import random

import numpy as np
import pytest
from scipy.sparse import csr_matrix, kron

from theorems.affine_phase_erasure import monomials
from theorems.nonlinear_jet_erasure import (
    TaylorJetChart, compile_higher_scalar_packet, fourier_curve_packet,
    higher_jet_maps, pullback_phase, rank_schedule,
    verify_weighted_witness, weighted_degree, weighted_merge,
)
from theorems.ut5_matrix_phase_alignment import (
    _product, _rank, align_jet_maps, verify_alignment,
)
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket


def _mv(A, x, p):
    return [sum(a*b for a, b in zip(row, x)) % p for row in A]


def _potential(chart, coefficients, q):
    return [sum(c*prod(pow(x, e, chart.p) for x, e in zip(q, nu))
                for (a, nu), c in coefficients.items() if a == b) % chart.p
            for b in range(chart.noncentral_width)]


def _jet(chart, coefficients, q):
    # Independent definition from the coefficients of Q, not transport_matrix.
    return [sum(c*prod(comb(n, e)*pow(x, n-e, chart.p)
                       for n, e, x in zip(nu, alpha, q))
                for (a, nu), c in coefficients.items()
                if a == b and sum(nu)-sum(alpha) == k and
                all(n >= e for n, e in zip(nu, alpha))) % chart.p
            for alpha, k, b in chart.indices]


@pytest.mark.parametrize("p,D,m", [(7, 3, 1), (11, 4, 2), (2**127-1, 3, 2)])
def test_taylor_expansion_closure_and_affine_composition(p, D, m):
    chart = TaylorJetChart(p, m, 2, D)
    assert chart.jet_width == 2*(comb(m+D, m+1)-1)
    rng = random.Random(901)
    coefficients = {(a, nu): rng.randrange(p) for a in range(2) for nu in monomials(m, D)}
    for _ in range(10):
        q, y, y2 = [[rng.randrange(p) for _ in range(m)] for _ in range(3)]
        s, s2 = rng.randrange(1, p), rng.randrange(1, p)
        shifted = [(a+s*b) % p for a, b in zip(y, q)]
        J = _jet(chart, coefficients, q)
        actual = _jet(chart, coefficients, shifted)
        expected = [(a+b) % p for a, b in zip(_jet(chart, coefficients, y),
                                             _mv(chart.transport_matrix(y, s), J, p))]
        assert actual == expected
        top = _potential(chart, {key: value for key, value in coefficients.items()
                                 if sum(key[1]) == D}, q)
        total = _potential(chart, coefficients, y)
        for (alpha, k, a), value in zip(chart.indices, J):
            total[a] += pow(s, k, p)*prod(pow(x, e, p) for x, e in zip(y, alpha))*value
        assert _potential(chart, coefficients, shifted) == [
            (a+pow(s, D, p)*b) % p for a, b in zip(total, top)]
        combined_y = [(a+s2*b) % p for a, b in zip(y2, y)]
        combined = chart.transport_matrix(combined_y, s*s2 % p)
        assert _product(chart.transport_matrix(y2, s2), chart.transport_matrix(y, s), p) == list(map(list, combined))
        A = chart.transport_matrix(y, s)
        assert _rank(A, p) == chart.jet_width
        for i, row in enumerate(A):
            assert row[i] == pow(s, chart.indices[i][1], p)
            assert all(not value or i == j or chart.indices[j][1] < chart.indices[i][1]
                       for j, value in enumerate(row))


def test_quadratic_chart_is_linear_but_cubic_chart_requires_lower_weight_cross_terms():
    quadratic = TaylorJetChart(7, 2, 3, 2)
    assert set(quadratic.weights) == {1}
    assert quadratic.transport_matrix([2, 4], 3) == tuple(
        tuple(3*int(i == j) for j in range(quadratic.jet_width)) for i in range(quadratic.jet_width))
    cubic = TaylorJetChart(7, 1, 1, 3)
    A = cubic.transport_matrix([2], 3)
    assert any(A[i][j] for i in range(cubic.jet_width) for j in range(i))
    with pytest.raises(ValueError, match="nonzero scale"):
        cubic.transport_matrix([2], 0)


@pytest.mark.parametrize("p", [7, 2**127-1])
def test_public_alignment_removes_cubic_top_and_preserves_same_nonlinear_jet(p):
    chart, rng = TaylorJetChart(p, 1, 2, 3), random.Random(2)
    forms = [[[0, p-1], [1, 0]]]
    coefficients = {(a, nu): rng.randrange(p) for a in range(2) for nu in monomials(1, 3)}
    for batch in range(2):
        scales, labels, outcomes = [], [], []
        for _ in range(10+batch):
            s = rng.randrange(1, p)
            scales += [s, s]
            labels += [[1], [p-1]]
            outcomes += [[rng.randrange(p)], [rng.randrange(p)]]
        maps = higher_jet_maps(chart, forms, labels, scales, outcomes)
        alignment = align_jet_maps(maps)
        assert verify_alignment(alignment)
        R = maps.carrier_width
        spectator = [rng.randrange(p) for _ in range(R-chart.jet_width)]
        packet = compile_higher_scalar_packet(alignment, forms, labels, scales, outcomes,
                                             [[] for _ in labels], spectator, 5)
        assert weighted_degree(chart, packet) <= 5
        theta = [coefficients[a, nu] if a < 2 else rng.randrange(p) for a, nu in packet.parameter_basis]
        all_coefficients = dict(zip(packet.parameter_basis, theta))

        def displacement(q):
            raw, start = [0]*(2*R), 0
            for i, rep in zip(maps.active_indices, maps.representations):
                point = [(outcomes[i][0]+scales[i]*q) % p]
                v = _mv(rep.weyl, _potential(chart, coefficients, point), p)
                r = rep.qudits
                raw[start:start+r], raw[R+start:R+start+r] = v[:r], v[r:]
                start += r
            return _mv(alignment.symplectic, raw, p)

        origin = displacement(0)
        for q in (1, 2, p-1):
            actual = [(a-b) % p for a, b in zip(displacement(q), origin)][:R]
            assert actual == _jet(chart, coefficients, [q])+[0]*(R-chart.jet_width)
            t = [rng.randrange(p) for _ in chart.indices]
            vector = displacement(q)
            psi = sum(label[0]*sum(value*pow((y[0]+s*q) % p, nu[0], p)
                                  for (a, nu), value in all_coefficients.items() if a == 2)
                      for label, y, s in zip(labels, outcomes, scales))
            expected_phase = -psi-pow(2, -1, p)*sum(a*b for a, b in zip(vector[:R], vector[R:]))
            expected_phase -= sum(a*b for a, b in zip(vector[R:], t+spectator))
            assert packet.evaluate_fixture([q]+t, theta) == expected_phase % p
        eta = [rng.randrange(p) for _ in chart.indices]
        reduced = fourier_curve_packet(chart, packet.parameter_basis, eta)
        assert reduced.degree <= 2
        for q in (0, 1, 3):
            assert reduced.evaluate_fixture([q], theta) == sum(
                a*b for a, b in zip(eta, _jet(chart, coefficients, [q]))) % p
        labels[-1] = [2]
        with pytest.raises(ValueError, match="degree-2D"):
            higher_jet_maps(chart, forms, labels, scales, outcomes)


def test_rank_schedule_and_distinct_feature_monomials():
    for p, D, m in ((7, 3, 1), (11, 4, 2), (2**127-1, 3, 1)):
        chart = TaylorJetChart(p, m, 2, D)
        count, bound = rank_schedule(chart)
        assert count > chart.jet_width and bound <= Fraction(1, 4*p)
        # After dividing a row by s: top=s^(D-1), jet=s^(k-1)*Y^alpha.
        features = {(D-1,)+(0,)*m}
        features.update((k-1,)+alpha for alpha, k, a in chart.indices if a == 0)
        assert len(features) == 1+chart.jet_width//2
        assert max(map(sum, features)) == D-1
    with pytest.raises(ValueError, match="p > 2D"):
        rank_schedule(TaylorJetChart(5, 1, 1, 3))


def _packet(chart, terms, basis=None):
    basis = basis or ((0, (1,)), (0, (2,)))
    return SymbolicScalarPacket(chart.p, chart.quotient_width, chart.jet_width, basis, terms)


@pytest.mark.parametrize("p", [7, 2**127-1])
def test_weighted_leading_cancellation_precedes_outcomes_and_needs_no_hidden_parameters(p):
    chart, rng = TaylorJetChart(p, 1, 1, 3), random.Random(41)
    alpha = [0]*chart.width
    alpha[0], alpha[1+next(i for i, (_, k, _) in enumerate(chart.indices) if k == 2)] = 3, 1
    alpha = tuple(alpha)
    term = (alpha, (0, 1))
    first = _packet(chart, {term: 1})
    second = _packet(chart, {term: -pow(pow(2, 5, p), -1, p) % p})
    assert first.degree == 4 and weighted_degree(chart, first) == 5
    verify_weighted_witness(chart, [first, second], [1, 2], 5)
    for _ in range(8):
        outcomes = [([rng.randrange(p)], [rng.randrange(p) for _ in chart.indices]) for _ in range(2)]
        merged = weighted_merge(chart, [first, second], [1, 2], outcomes, 5)
        assert weighted_degree(chart, merged) <= 4
        x, theta = [rng.randrange(p) for _ in range(chart.width)], [2, 3]
        values = []
        for packet, s, (y, z) in zip([first, second], [1, 2], outcomes):
            offset, A = chart.affine_map(y, z, s)
            point = [(a+b) % p for a, b in zip(offset, _mv(A, x, p))]
            pullback = pullback_phase(chart, packet, y, z, s)
            assert pullback.evaluate_fixture(x, theta) == packet.evaluate_fixture(point, theta)
            values.append(packet.evaluate_fixture(point, theta))
        assert merged.evaluate_fixture(x, theta) == sum(values) % p
    wrong = _packet(chart, {term: -pow(pow(2, 4, p), -1, p) % p})
    with pytest.raises(ArithmeticError, match="weighted cancellation"):
        verify_weighted_witness(chart, [first, wrong], [1, 2], 5)


def test_truth_specific_witness_and_mismatched_parameter_chart_are_rejected():
    chart = TaylorJetChart(7, 1, 1, 3)
    alpha = (3,)+(0,)*chart.jet_width
    packets = [_packet(chart, {(alpha, (i,)): 1}) for i in (0, 1)]
    # At theta=(1,1), the two phases cancel. Their public maps do not.
    with pytest.raises(ArithmeticError, match="weighted cancellation"):
        verify_weighted_witness(chart, packets, [1, 6], 3)
    wrong = _packet(chart, packets[1].terms, tuple(reversed(packets[1].parameter_basis)))
    with pytest.raises(ValueError, match="ordered parameter basis"):
        verify_weighted_witness(chart, [packets[0], wrong], [1, 6], 3)


def test_public_weighted_controller_does_not_evaluate_hidden_parameters(monkeypatch):
    def forbidden(*args):
        raise AssertionError("hidden truth accessed")
    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    chart = TaylorJetChart(7, 1, 1, 3)
    alpha = (5,)+(0,)*chart.jet_width
    packets = [_packet(chart, {(alpha, (0,)): c}) for c in (1, 6)]
    result = weighted_merge(chart, packets, [1, 1], [([2], [1]*chart.jet_width),
                                                   ([3], [2]*chart.jet_width)], 5)
    assert weighted_degree(chart, result) <= 4


def test_higher_compiler_keeps_variable_radicals_zero_rank_and_zero_scale_inputs():
    p, rng = 11, random.Random(17)
    chart = TaylorJetChart(p, 1, 3, 3)
    forms = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        form = [[0]*3 for _ in range(3)]
        form[i][j], form[j][i] = 1, p-1
        forms.append(form)
    forms.append([[0]*3 for _ in range(3)])
    labels, scales, outcomes = [], [], []
    for _ in range(14):
        label = [rng.randrange(1, p) for _ in forms]
        labels += [label, [-a % p for a in label]]
        scales += [rng.randrange(1, p)]*2
        outcomes += [[rng.randrange(p)], [rng.randrange(p)]]
    labels += [[0, 0, 0, 1], [0, 0, 0, p-1], [1, 0, 0, 0]]
    scales += [1, 1, 0]
    outcomes += [[2], [3], [1]]
    maps = higher_jet_maps(chart, forms, labels, scales, outcomes)
    assert maps.representations[-1].qudits == maps.representations[-2].qudits == 0
    assert len(labels)-1 not in maps.active_indices
    alignment = align_jet_maps(maps)
    characters = [[rng.randrange(p) for _ in rep.radical] for rep in maps.representations]+[[1]]
    spectator = [rng.randrange(p) for _ in range(maps.carrier_width-chart.jet_width)]
    packet = compile_higher_scalar_packet(alignment, forms, labels, scales, outcomes,
                                         characters, spectator, 5)
    assert weighted_degree(chart, packet) <= 5
    theta = [rng.randrange(p) for _ in packet.parameter_basis]
    coefficients = dict(zip(packet.parameter_basis, theta))
    for q in (0, 2, 7):
        R, raw, psi, start = maps.carrier_width, [0]*(2*maps.carrier_width), 0, 0
        for i, rep in zip(maps.active_indices, maps.representations):
            point = (outcomes[i][0]+scales[i]*q) % p
            value = _potential(chart, coefficients, [point])
            displacement = _mv(rep.weyl, value, p)
            r = rep.qudits
            raw[start:start+r], raw[R+start:R+start+r] = displacement[:r], displacement[r:]
            psi += sum(a*b for a, b in zip(characters[i], _mv(rep.radical, value, p)))
            psi += sum(labels[i][a-3]*c*pow(point, nu[0], p)
                       for (a, nu), c in coefficients.items() if a >= 3)
            start += r
        transformed = _mv(alignment.symplectic, raw, p)
        t = [rng.randrange(p) for _ in chart.indices]
        phase = -psi-pow(2, -1, p)*sum(a*b for a, b in zip(transformed[:R], transformed[R:]))
        phase -= sum(a*b for a, b in zip(transformed[R:], t+spectator))
        assert packet.evaluate_fixture([q]+t, theta) == phase % p


# A closed two-coordinate quotient of the full degree-three jet, with
# F(q)=theta*(q_1,q_1^2), suffices to contract physical channels without
# allocating the full p^(m+J) space. These are not HSP input families.
def _curve(q, p, theta=2):
    return (theta*q[0] % p, theta*q[0]**2 % p)


def _curve_map(address, y, z, s, p, wrong=False):
    q, t = address[:-2], address[-2:]
    image = tuple((a+s*b) % p for a, b in zip(y, q))
    jet = ((z[0]+s*t[0]) % p,
           (z[1]+s*s*t[1]+(0 if wrong else 2*y[0]*s*t[0])) % p)
    return image+jet


def _curve_source(p, m, support, phase, theta=2):
    points = list(product(range(p), repeat=m+2))
    omega = np.exp(2j*np.pi/p)
    rho = np.zeros((len(points), len(points)), complex)
    for i, x in enumerate(points):
        q, t = x[:-2], x[-2:]
        for j, other in enumerate(points):
            r, v = other[:-2], other[-2:]
            if tuple((b-a) % p for a, b in zip(q, r)) not in support:
                continue
            if any((b+y-a-x) % p for a, x, b, y in zip(t, _curve(q, p, theta), v, _curve(r, p, theta))):
                continue
            rho[i, j] = omega**((phase(x)-phase(other)) % p)/len(points)
    return points, rho


def _branch_operator(points, outcomes, scales, p, wrong=False):
    index = {x: i for i, x in enumerate(points)}
    N = len(points)
    columns = []
    for x in points:
        i = index[_curve_map(x, *outcomes[0], scales[0], p, wrong)]
        j = index[_curve_map(x, *outcomes[1], scales[1], p, wrong)]
        columns.append(i*N+j)
    return csr_matrix(([1/sqrt(N)]*N, (range(N), columns)), shape=(N, N*N))


@pytest.mark.parametrize("p,m", [(3, 1), (3, 2), (5, 1)])
def test_physical_two_step_merge_preserves_curve_and_uniform_outcomes(p, m):
    support = {tuple([u]*m) for u in range(p)}
    phases = [lambda x: x[0]**3*x[-1]+x[0]**4, lambda x: 2*x[0]*x[-2]+x[-1]**2]
    points, first = _curve_source(p, m, support, phases[0])
    _, second = _curve_source(p, m, support, phases[1])
    assert np.linalg.eigvalsh(first).min() > -1e-12
    joint = kron(csr_matrix(first), csr_matrix(second), format="csr")
    N, scales, wrong_detected = len(points), [1, 2], False
    rng = random.Random(31)
    for _ in range(4):
        outcomes = [(tuple(rng.randrange(p) for _ in range(m)),
                     tuple(rng.randrange(p) for _ in range(2))) for _ in range(2)]
        K = _branch_operator(points, outcomes, scales, p)
        actual = (K @ joint @ K.conj().T).toarray()
        phase = lambda x: sum(f(_curve_map(x, *o, s, p)) for f, o, s in zip(phases, outcomes, scales))
        _, expected = _curve_source(p, m, support, phase)
        assert np.trace(actual) == pytest.approx(N**-2)
        np.testing.assert_allclose(actual*N*N, expected, atol=1e-12)
        wrong = _branch_operator(points, outcomes, scales, p, wrong=True)
        damaged = (wrong @ joint @ wrong.conj().T).toarray()*N*N
        assert np.trace(damaged) == pytest.approx(1)
        wrong_detected |= np.linalg.norm(damaged-expected) > 0.01
    assert wrong_detected


def test_every_branch_is_complete_without_postselecting_translation_outcomes():
    p, points = 3, list(product(range(3), repeat=3))
    N, diagonal = len(points), np.zeros(len(points)**2)
    for x, y in product(points, repeat=2):
        K = _branch_operator(points, [(x[:1], x[1:]), (y[:1], y[1:])], [1, 2], p)
        # Each row has one entry and distinct columns, so K^dag K is diagonal.
        assert len(set(K.indices)) == N
        diagonal[K.indices] += 1/N
    np.testing.assert_allclose(diagonal, np.ones(N*N), atol=1e-12)


def test_same_public_chart_does_not_certify_the_same_hidden_curve():
    p, support = 3, {(u,) for u in range(3)}
    points, first = _curve_source(p, 1, support, lambda x: 0, theta=1)
    _, second = _curve_source(p, 1, support, lambda x: 0, theta=2)
    K = _branch_operator(points, [((1,), (0, 2)), ((2,), (1, 1))], [1, 2], p)
    actual = (K @ kron(csr_matrix(first), csr_matrix(second), format="csr") @ K.conj().T).toarray()
    assert np.trace(actual) == pytest.approx(len(points)**-2)
    assert np.linalg.norm(actual*len(points)**2-first) > 0.1


def test_fourier_removes_curve_but_leaves_nonconstant_phase_for_every_nonzero_useful_label():
    p, support = 5, {(u,) for u in range(5)}
    points, rho = _curve_source(p, 1, support, lambda x: 0)
    omega = np.exp(2j*np.pi/p)
    summed_probability = 0
    phases_seen = []
    for eta in product(range(p), repeat=2):
        K = np.zeros((p, len(points)), complex)
        for i, x in enumerate(points):
            K[x[0], i] = omega**(-sum(a*b for a, b in zip(eta, x[-2:])) % p)/p
        actual = K @ rho @ K.conj().T
        probability = np.trace(actual).real
        assert probability == pytest.approx(p**-2)
        phase = [sum(a*b for a, b in zip(eta, _curve((q,), p))) % p for q in range(p)]
        expected = np.array([[omega**((a-b) % p)/p for b in phase] for a in phase])
        np.testing.assert_allclose(actual/probability, expected, atol=1e-12)
        phases_seen.append(phase)
        summed_probability += probability
    assert summed_probability == pytest.approx(1)
    assert sum(len(set(phase)) == 1 for phase in phases_seen) == 1


def test_fourier_before_weighted_phase_erasure_does_not_give_the_claimed_source():
    p, support = 5, {(u,) for u in range(5)}
    points, rho = _curve_source(p, 1, support, lambda x: x[0]*x[-1])
    K = np.zeros((p, len(points)), complex)
    for i, x in enumerate(points):
        K[x[0], i] = 1/p  # Even eta=0 cannot remove a q-dependent t phase.
    actual = K @ rho @ K.conj().T
    assert np.trace(actual) == pytest.approx(p**-2)
    assert np.linalg.norm(actual*p*p-np.ones((p, p))/p) > 0.1


def test_actual_weyl_spectator_instrument_has_nonlinear_graph_and_weighted_phase():
    p, omega = 5, np.exp(2j*np.pi/5)
    carriers = list(product(range(p), repeat=3))
    lookup = {x: i for i, x in enumerate(carriers)}
    gauges, offsets, frequencies = [], [], []
    for q in range(p):
        A = ((_curve((q,), p)[0]+1) % p, (_curve((q,), p)[1]+2) % p, 3)
        B = (q*q % p, q**3 % p, (q+1) % p)
        V = np.zeros((p**3, p**3), complex)
        for i, t in enumerate(carriers):
            out = tuple((a+b) % p for a, b in zip(A, t))
            exponent = q**4+sum(b*(x+pow(2, -1, p)*a) for a, b, x in zip(A, B, t))
            V[lookup[out], i] = omega**(exponent % p)
        gauges.append(V)
        offsets.append(A)
        frequencies.append(B)
    source = np.block([[a.conj().T @ b for b in gauges] for a in gauges])/p**4
    for spectator in range(p):
        addresses = [q*p**3+lookup[(a, b, spectator)] for q, a, b in product(range(p), repeat=3)]
        measured = source[np.ix_(addresses, addresses)]
        assert np.trace(measured) == pytest.approx(1/p)

        def phase(x):
            q, a, b = x
            A, B = offsets[q], frequencies[q]
            return -q**4-pow(2, -1, p)*sum(v*w for v, w in zip(A, B))-sum(
                v*w for v, w in zip(B, (a, b, spectator)))

        _, expected = _curve_source(p, 1, {(q,) for q in range(p)}, phase)
        np.testing.assert_allclose(measured*p, expected, atol=1e-12)
