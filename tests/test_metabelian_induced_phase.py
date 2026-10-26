"""Exact coefficient falsifiers for the public induced-source compiler."""
from dataclasses import replace
from itertools import product
from math import prod
import random

import pytest
import sympy as sp

from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.metabelian_induced_phase import (
    InducedPhasePacket, MetabelianLieChart, _multiply, align_induced_jet,
    cocycle_template, lie_word_cocycle_template, compile_induced_phase, induced_leading_columns,
    merge_induced_phases, pullback_induced_phase,
)
from theorems.right_abelian_induced_source import (
    FiliformNormal, derived_length_three_witness, symbolic_filiform_cocycle,
)
from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates
from theorems.ut5_matrix_phase_alignment import _identity, _product, _rank
from theorems.ut5_scalar_phase_compiler import _multiply as quadratic_multiply


def filiform_chart(p, k):
    n = k+1
    brackets = [[[0]*n for _ in range(n)] for _ in range(n)]
    for i in range(1, k):
        brackets[0][i][i+1], brackets[i][0][i+1] = 1, p-1
    return MetabelianLieChart(p, 2, tuple(tuple(map(tuple, rows)) for rows in brackets))


def coefficients(expression, coordinates, parameters, p):
    result = {}
    for exponents, coefficient in sp.Poly(sp.expand(expression), *coordinates, *parameters).terms():
        a, b = sp.fraction(coefficient)
        value = int(a)*pow(int(b), -1, p) % p
        if value:
            alpha, powers = exponents[:len(coordinates)], exponents[len(coordinates):]
            result[(alpha, tuple(i for i, power in enumerate(powers) for _ in range(power)))] = value
    return result


def design(chart, st):
    rows, scales, ys = [], [], []
    for s, y in product(range(1, chart.degree+1), product(range(chart.degree), repeat=chart.quotient_width)):
        row = [pow(s, k, chart.p)*prod(pow(v, e, chart.p) for v, e in zip(y, alpha)) % chart.p
               for alpha, k, a in chart.indices if a == 0]
        if _rank(rows+[row], chart.p) > len(rows):
            rows.append(row)
            scales.append(s)
            ys.append(y)
    assert len(rows) == chart.jet_width//chart.noncentral_width
    scales.append(1)
    ys.append((1,)*chart.quotient_width)
    labels = [tuple((i*j+j+i) % st.p for j in range(st.ideal_width)) for i in range(len(scales))]
    labels[0] = (0,)*st.ideal_width
    return labels, scales, ys


@pytest.mark.parametrize("p,k", [(17, 2), (17, 3), (17, 4), (17, 5), (17, 7), (2**127-1, 4)])
def test_entire_universal_cocycle_matches_independent_semidirect_coefficients(p, k):
    st = filiform_chart(p, k)
    g, x, independent = symbolic_filiform_cocycle(k)
    actual = cocycle_template(st)
    assert st.nilpotency_class == k
    assert [dict(row) for row in actual] == [coefficients(value, x, g, p) for value in independent]
    assert max(sum(alpha)+len(params) for row in actual for (alpha, params), _ in row) == k
    if k >= 4:
        assert max(len(params) for row in actual for (_, params), _ in row) > 2
        assert max(sum(alpha) for row in actual for (alpha, _), _ in row) > 2


def test_non_lie_nonabelian_ideal_and_nonnilpotent_data_rejected():
    st = filiform_chart(17, 4)
    bad = [[list(v) for v in row] for row in st.brackets]
    bad[0][0][2] = 1
    with pytest.raises(ValueError, match="alternating"):
        replace(st, brackets=tuple(tuple(map(tuple, row)) for row in bad))
    bad = [[list(v) for v in row] for row in st.brackets]
    bad[2][3][4], bad[3][2][4] = 1, 16
    with pytest.raises(ValueError, match="I must be abelian"):
        replace(st, brackets=tuple(tuple(map(tuple, row)) for row in bad))
    bad = [[list(v) for v in row] for row in st.brackets]
    bad[1][2][2], bad[2][1][2] = 1, 16
    with pytest.raises(ValueError, match="Jacobi"):
        replace(st, brackets=tuple(tuple(map(tuple, row)) for row in bad))
    bad = [[[0]*2 for _ in range(2)] for _ in range(2)]
    bad[0][1][1], bad[1][0][1] = 1, 16
    with pytest.raises(ValueError, match="not nilpotent"):
        MetabelianLieChart(17, 1, tuple(tuple(map(tuple, row)) for row in bad))


@pytest.mark.parametrize("p", [17, 2**127-1])
def test_larger_abelian_fiber_really_requires_the_full_quartic_parameter_lift(p):
    st = replace(filiform_chart(p, 4), a_width=1)
    a, x = sp.symbols("a x")
    b = sp.symbols("b0:4")
    # I=span(Y0,...,Y3), section exp(xX): kappa=exp(-(a+x)J)*F(a)*B.
    independent = [sum((-(a+x))**u/sp.factorial(u)*a**v/sp.factorial(v+1)*b[j-u-v]
                       for u in range(j+1) for v in range(j-u+1)) for j in range(4)]
    actual = cocycle_template(st)
    assert [dict(row) for row in actual] == [coefficients(v, (x,), (a,)+b, p) for v in independent]
    assert max(len(params) for row in actual for (_, params), _ in row) == 4
    ch = FullTaylorJetChart(p, 1, 1, 2)
    alignment = align_induced_jet(ch, st, *design(ch, st))
    packet = compile_induced_phase(alignment, (5,))
    assert max(len(params) for _, params in packet.terms) == 4
    assert packet.supported_parameter_count < packet.lifted_parameter_count
    assert all(sum(packet.parameter_basis[i][0] >= 1 for i in params) <= 1 for _, params in packet.terms)
    pulled = pullback_induced_phase(packet, (2,), (3, 4, 5), 3)
    assert max(len(params) for _, params in pulled.terms) == 4


def test_alignment_includes_zero_labels_and_rejects_forged_or_rank_deficient_data():
    st, ch = filiform_chart(17, 4), FullTaylorJetChart(17, 1, 2, 2)
    labels, scales, ys = design(ch, st)
    a = align_induced_jet(ch, st, labels, scales, ys)
    assert _product(a.forward, a.inverse, 17) == _identity(a.carrier_width)
    assert _product(a.forward, a.displacement_map, 17) == [row[:ch.jet_width] for row in _identity(a.carrier_width)]
    zero = align_induced_jet(ch, st, [(0,)*st.ideal_width]*len(labels), scales, ys)
    assert zero.forward == a.forward
    assert not compile_induced_phase(zero, (3, 7)).terms
    with pytest.raises(ValueError, match="rank deficient"):
        align_induced_jet(ch, st, labels, [1]*len(labels), [(0,)]*len(labels))
    with pytest.raises(ValueError, match="nonzero"):
        align_induced_jet(ch, st, labels, [0]+scales[1:], ys)
    with pytest.raises(ValueError, match="verified"):
        compile_induced_phase(replace(a, inverse=tuple(reversed(a.inverse))), (3, 7))
    with pytest.raises(ValueError):
        compile_induced_phase(a, ())


@pytest.mark.parametrize("p", [17, 2**127-1])
def test_full_aligned_phase_coefficients_and_actual_group_coordinates(p):
    st, ch = filiform_chart(p, 4), FullTaylorJetChart(p, 1, 2, 2)
    a = align_induced_jet(ch, st, *design(ch, st))
    spectator = (3, 7)
    packet = compile_induced_phase(a, spectator)
    g, x, independent = symbolic_filiform_cocycle(4)
    q = sp.symbols("q0:1")
    t = sp.symbols(f"t0:{ch.jet_width}")
    theta = sp.symbols(f"theta0:{len(packet.parameter_basis)}")
    carriers = [sum(c*v for c, v in zip(row, t+spectator)) for row in a.inverse]
    expected = 0
    for i, (label, s, y) in enumerate(zip(a.labels, a.scales, a.outcomes)):
        components = [sum(theta[j]*prod((origin+s*variable)**e for origin, variable, e in zip(y, q, alpha))
                          for j, (coordinate, alpha) in enumerate(packet.parameter_basis) if coordinate == b)
                      for b in range(st.width)]
        substitution = dict(zip(g, components)) | dict(zip(x, carriers[2*i:2*i+2]))
        expected -= sum(c*value.xreplace(substitution) for c, value in zip(label, independent))
    assert packet.terms == coefficients(expected, q+t, theta, p)
    assert max(len(params) for _, params in packet.terms) == 3
    assert packet.weighted_degree <= 8
    assert packet.lifted_parameter_count > len({params for _, params in packet.terms})
    # Independent semidirect group calculation, including nonzero spectators.
    group, rng = FiliformNormal(p, 4), random.Random(813)
    for _ in range(12):
        parameters = tuple(rng.randrange(p) for _ in theta)
        point = tuple(rng.randrange(p) for _ in range(ch.width))
        carrier = tuple(sum(c*v for c, v in zip(row, point[1:]+spectator)) % p for row in a.inverse)
        phase = 0
        for i, (label, s, y) in enumerate(zip(a.labels, a.scales, a.outcomes)):
            shifted = (y[0]+s*point[0]) % p
            logarithm = tuple(sum(parameters[j]*pow(shifted, alpha[0], p)
                                  for j, (coordinate, alpha) in enumerate(packet.parameter_basis) if coordinate == b) % p
                              for b in range(st.width))
            _, cocycle = group.induced_action(group.exp(logarithm), carrier[2*i:2*i+2])
            phase -= sum(c*v for c, v in zip(label, cocycle))
        assert packet.evaluate_fixture(point, parameters) == phase % p


def test_actual_higher_degree_pullback_and_coefficientwise_merge():
    st, ch = filiform_chart(17, 4), FullTaylorJetChart(17, 1, 2, 2)
    a = align_induced_jet(ch, st, *design(ch, st))
    packet = compile_induced_phase(a, (3, 7))
    y, z, s = (4,), tuple(range(ch.jet_width)), 3
    pulled = pullback_induced_phase(packet, y, z, s)
    offset, matrix = ch.affine_map(y, z, s)
    assert max(len(params) for _, params in pulled.terms) == 3
    variables = sp.symbols(f"v0:{ch.width}")
    parameters = sp.symbols(f"u0:{len(packet.parameter_basis)}")
    expression = sum(c*prod(v**e for v, e in zip(variables, alpha))*prod(parameters[j] for j in indices)
                     for (alpha, indices), c in packet.terms.items())
    substitution = {v: constant+sum(c*w for c, w in zip(row, variables))
                    for v, constant, row in zip(variables, offset, matrix)}
    assert pulled.terms == coefficients(expression.xreplace(substitution), variables, parameters, 17)
    rng = random.Random(91)
    for _ in range(12):
        point = tuple(rng.randrange(17) for _ in range(ch.width))
        theta = tuple(rng.randrange(17) for _ in packet.parameter_basis)
        transformed = tuple((c+sum(a*b for a, b in zip(row, point))) % 17 for c, row in zip(offset, matrix))
        assert pulled.evaluate_fixture(point, theta) == packet.evaluate_fixture(transformed, theta)
    opposite_labels = [tuple(-c % 17 for c in row) for row in a.labels]
    opposite = compile_induced_phase(align_induced_jet(ch, st, opposite_labels, a.scales, a.outcomes), (3, 7))
    assert opposite.terms == {key: -c % 17 for key, c in packet.terms.items()}
    columns, keys = induced_leading_columns([packet, opposite], packet.weighted_degree)
    assert keys and all((x+y) % 17 == 0 for x, y in zip(*columns))
    outcomes = [((0,), (0,)*ch.jet_width), (y, z), ((0,), (0,)*ch.jet_width)]
    merged = merge_induced_phases([packet, opposite, packet], [1, 1, 0], outcomes, packet.weighted_degree)
    assert merged.terms and merged.weighted_degree < packet.weighted_degree
    with pytest.raises(ArithmeticError, match="coefficientwise"):
        merge_induced_phases([packet, packet], [1, 1], outcomes[:2], packet.weighted_degree)


def test_hidden_truth_cancellation_does_not_pass_public_gate_or_legacy_quadratic_gate():
    ch = FullTaylorJetChart(17, 1, 2, 2)
    exponent = (1,)+(0,)*(ch.width-1)
    a = InducedPhasePacket(ch, 5, 4, {(exponent, (0, 0, 0)): 1})
    b = InducedPhasePacket(ch, 5, 4, {(exponent, (1, 1, 1)): 16})
    point, theta = (1,)*ch.width, (1,)*len(a.parameter_basis)
    assert (a.evaluate_fixture(point, theta)+b.evaluate_fixture(point, theta)) % 17 == 0
    with pytest.raises(ArithmeticError, match="coefficientwise"):
        merge_induced_phases([a, b], [1, 1], [((0,), (0,)*ch.jet_width)]*2, 1)
    zero = (0,)*ch.width
    with pytest.raises(ArithmeticError, match="quadratic"):
        quadratic_multiply({(zero, (0, 0)): 1}, {(zero, (0,)): 1}, 17)
    with pytest.raises(ArithmeticError, match="declared"):
        _multiply({(zero, (0, 0, 0, 0)): 1}, {(zero, (0,)): 1}, 17, 4)
    with pytest.raises(ValueError, match="bounded"):
        replace(a, terms={(exponent, (0,)*5): 1})
    with pytest.raises(ValueError, match="abelian-fiber"):
        replace(a, terms={(exponent, (6, 6)): 1})
    with pytest.raises(ValueError, match="abelian-fiber"):
        replace(a, terms={(exponent, (0,)*4): 1})
    with pytest.raises(ValueError, match="schemas"):
        induced_leading_columns([a, replace(a, normal_width=6)], 1)
    with pytest.raises(ValueError, match="p>kD"):
        replace(a, chart=FullTaylorJetChart(7, 1, 2, 2))


@pytest.mark.parametrize("p", [43, 2**127-1])
def test_template_inside_actual_class_nine_ambient_derived_algebra(p):
    from tests.test_metabelian_phase_extension import finite_matrix_exp_log

    algebra, ambient, _ = derived_length_three_witness(p)
    normal = algebra.lower_central_series(ambient)[1]
    ideal = algebra.lower_central_series(normal)[1]
    complement = algebra.span(ideal+normal)[len(ideal):]
    basis = complement+ideal
    table = tuple(tuple(_fmpz_solve_coordinates(basis, algebra.bracket(a, b), p) for b in basis) for a in basis)
    st = MetabelianLieChart(p, len(complement), table)
    assert (st.width, st.a_width, st.ideal_width, st.nilpotency_class) == (17, 7, 10, 4)
    template = cocycle_template(st)
    assert template == lie_word_cocycle_template(st)
    slots = tuple((i, j) for i in range(10) for j in range(i+1, 10))
    import numpy as np
    def matrix(coordinates):
        vector = [sum(c*b[j] for c, b in zip(coordinates, basis)) % p for j in range(algebra.dimension)]
        out = np.zeros((10, 10), dtype=object)
        for ij, c in zip(slots, vector):
            out[ij] = c
        return out
    rng = random.Random(182)
    for _ in range(4):
        q = tuple(rng.randrange(p) for _ in basis)
        x = tuple(rng.randrange(p) for _ in complement)
        A, X, Q = matrix(q[:st.a_width]+(0,)*st.ideal_width), matrix(x+(0,)*st.ideal_width), matrix(q)
        # All factors lie in N, with superdiagonal degree >=2; fifth powers vanish.
        left = finite_matrix_exp_log((-A-X) % p, p)
        middle = finite_matrix_exp_log(Q, p)
        right = finite_matrix_exp_log(X, p)
        actual = finite_matrix_exp_log(left @ middle % p @ right % p, p, logarithm=True)
        predicted = tuple(sum(c*prod(pow(v, e, p) for v, e in zip(x, alpha))*prod(q[i] for i in params)
                              for (alpha, params), c in component) % p for component in template)
        assert np.array_equal(actual, matrix((0,)*st.a_width+predicted))
