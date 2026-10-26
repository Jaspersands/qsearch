"""Filtered-source algebra and falsifiers, not a physical HSP receiver."""
from dataclasses import replace
from itertools import combinations_with_replacement, product
from math import comb, prod
import random

import pytest
import sympy as sp

from theorems.ambient_filtered_induced import (
    FilteredInducedPhasePacket, FilteredNormalChart, ambient_filtration_certificate,
    compile_filtered_induced_phase, filtered_equation_bounds, filtered_jet_chart,
    filtered_resource_report,
)
from theorems.ambient_section_potential import polynomial_section_fixture, section_word_certificate
from theorems.class_three_monomial_jet import FullTaylorJetChart, full_jet_rank_schedule
from theorems.metabelian_induced_phase import (
    align_induced_jet, cocycle_template, induced_leading_columns,
    lie_word_cocycle_template, merge_induced_phases, pullback_induced_phase,
)
from theorems.nonlinear_jet_erasure import _jet_terms
from theorems.right_abelian_induced_source import (
    derived_length_three_witness, symbolic_filiform_cocycle, upper_triangular_lie,
)
from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates
from theorems.ut5_matrix_phase_alignment import _identity, _product, _rank
from tests.test_metabelian_induced_phase import coefficients, filiform_chart


def design(ch, st):
    scalar = FullTaylorJetChart(ch.p, ch.quotient_width, 1, ch.degree)
    rows, scales, ys = [], [], []
    for s, y in product(range(1, ch.degree+1), product(range(ch.degree), repeat=ch.quotient_width)):
        row = [pow(s, k, ch.p)*prod(pow(v, e, ch.p) for v, e in zip(y, alpha)) % ch.p
               for alpha, k, _ in scalar.indices]
        if _rank(rows+[row], ch.p) > len(rows):
            rows.append(row)
            scales.append(s)
            ys.append(y)
        if len(rows) == scalar.jet_width:
            break
    assert len(rows) == ch.feature_count
    scales.append(1)
    ys.append((1,)*ch.quotient_width)
    labels = [(0,)*st.ideal_width for _ in scales]
    labels[-1] = tuple(range(1, st.ideal_width+1))
    return labels, scales, ys


@pytest.mark.parametrize("p", [19, 43, 2**127-1])
def test_actual_class_nine_filtration_and_all_template_coefficients(p):
    algebra, ambient, _ = derived_length_three_witness(p)
    certificate = ambient_filtration_certificate(algebra, ambient)
    f = certificate.filtered
    assert certificate.verify(algebra)
    assert f.coordinate_weights == (6, 5, 4, 4, 3, 3, 2, 9, 8, 8, 7, 7, 7, 6, 6, 5, 5)
    assert cocycle_template(f.structure) == lie_word_cocycle_template(f.structure)
    ch = filtered_jet_chart(f, 2)
    assert (ch.jet_width, ch.feature_count, ch.degree) == (155, 56, 6)
    batch, bound = full_jet_rank_schedule(ch)
    assert batch == 57*p.bit_length()+2 and bound <= 1/(4*p)
    # The improved algebra guard also works at p19; old p>kc means p>36.
    packet = FilteredInducedPhasePacket(ch, 17, 4, {}, f)
    assert len(packet.parameter_basis) == 456
    assert packet.supported_parameter_count == 352*comb(108, 3)
    assert len(f.coordinate_weights) == 17


def section_control():
    p = 17
    algebra, slots = upper_triangular_lie(5, p)
    basis = _identity(algebra.dimension)
    certificate = ambient_filtration_certificate(algebra, basis)
    x = tuple(int(j == i+1 and i >= 1) for i, j in slots)
    y = tuple(int((i, j) == (0, 1)) for i, j in slots)
    zero = (0,)*len(slots)
    polynomial = polynomial_section_fixture(section_word_certificate(4), algebra,
                                            ((x, zero), (zero, y), (zero, zero)))
    return algebra, certificate, polynomial


def test_actual_section_coefficients_obey_each_coordinate_degree_not_just_c():
    algebra, cert, polynomial = section_control()
    attained = set()
    for alpha, value in polynomial.items():
        coordinates = _fmpz_solve_coordinates(cert.normal_basis, value, algebra.p)
        for a, w in zip(coordinates, cert.filtered.coordinate_weights):
            if a:
                assert sum(alpha) <= w
                if sum(alpha) == w:
                    attained.add(w)
    assert {2, 3, 4} <= attained


def test_valid_weighted_normal_tensor_is_insufficient_without_actual_ambient_flag():
    algebra, cert, polynomial = section_control()
    f, st = cert.filtered, cert.filtered.structure
    center = [i for i in range(st.a_width) if not any(any(row) for row in st.brackets[i])]
    high = next(i for i in center if f.coordinate_weights[i] == 3)
    low = next(i for i in center if f.coordinate_weights[i] == 2)
    bad_basis = list(cert.normal_basis)
    bad_basis[high] = tuple((a+b) % algebra.p for a, b in zip(bad_basis[high], bad_basis[low]))
    # Both vectors centralize N: its bracket tensor and abstract weight test still pass.
    assert f.verify_cocycle_support()
    with pytest.raises(ValueError, match="actual ambient filtration"):
        replace(cert, normal_basis=tuple(bad_basis)).verify(algebra)
    violations = []
    for alpha, value in polynomial.items():
        coords = _fmpz_solve_coordinates(bad_basis, value, algebra.p)
        violations.extend((sum(alpha), w) for a, w in zip(coords, f.coordinate_weights) if a and sum(alpha) > w)
    assert (3, 2) in violations


@pytest.mark.parametrize("m", [1, 2])
def test_heterogeneous_full_jet_transport_and_composition(m):
    f = FilteredNormalChart(filiform_chart(17, 3), 7, (2, 3, 5, 7))
    ch = filtered_jet_chart(f, m)
    packet = FilteredInducedPhasePacket(ch, 4, 3, {}, f)
    rng = random.Random(71)
    theta = [rng.randrange(17) for _ in packet.parameter_basis]
    def curve(q):
        return tuple(sum(v*theta[params[0]]*prod(pow(x, e, 17) for x, e in zip(q, alpha))
                         for (alpha, params), v in _jet_terms(ch, packet.parameter_basis, i, m).items()) % 17
                     for i in range(ch.jet_width))
    for _ in range(5):
        q, y, z = [tuple(rng.randrange(17) for _ in range(m)) for _ in range(3)]
        s, t = rng.randrange(1, 17), rng.randrange(1, 17)
        transport = ch.transport_matrix(y, s)
        assert curve(tuple((a+s*b) % 17 for a, b in zip(y, q))) == tuple(
            (a+sum(c*b for c, b in zip(row, curve(q)))) % 17 for a, row in zip(curve(y), transport))
        assert _product(transport, ch.transport_matrix(z, t), 17) == list(map(list,
            ch.transport_matrix(tuple((a+s*b) % 17 for a, b in zip(y, z)), s*t % 17)))
        for i, row in enumerate(transport):
            assert row[i] == pow(s, ch.weights[m+i], 17)
            assert all(not v or ch.indices[j][2] == ch.indices[i][2] for j, v in enumerate(row))


def compiled_control():
    f = FilteredNormalChart(filiform_chart(17, 3), 7, (2, 3, 5, 7))
    ch = filtered_jet_chart(f, 1)
    labels, scales, ys = design(ch, f.structure)
    alignment = align_induced_jet(ch, f.structure, labels, scales, ys)
    spectator = tuple((2*i+3) % 17 for i in range(alignment.carrier_width-ch.jet_width))
    packet = compile_filtered_induced_phase(alignment, spectator, f)
    return f, alignment, spectator, packet


def test_filtered_compiler_matches_independent_full_semidirect_expression():
    f, a, spectator, packet = compiled_control()
    ch, p = packet.chart, packet.chart.p
    variables = sp.symbols(f"v0:{ch.width}")
    theta = sp.symbols(f"t0:{len(packet.parameter_basis)}")
    g, x, cocycle = symbolic_filiform_cocycle(3)
    old_carriers = [sum(c*v for c, v in zip(row, (*variables[1:], *spectator))) for row in a.inverse]
    expression = 0
    for i, (label, s, y) in enumerate(zip(a.labels, a.scales, a.outcomes)):
        components = [sum(theta[j]*(y[0]+s*variables[0])**alpha[0]
                          for j, (component, alpha) in enumerate(packet.parameter_basis) if component == k)
                      for k in range(4)]
        substitution = dict(zip((*g, *x), (*components, *old_carriers[2*i:2*i+2])))
        expression -= sum(c*value.xreplace(substitution) for c, value in zip(label, cocycle))
    assert packet.terms == coefficients(expression, variables, theta, p)
    assert packet.weighted_degree == f.ambient_class == 7
    assert packet.weighted_degree < packet.parameter_cap*ch.degree == 9


def test_filtered_schema_survives_pullback_and_weighted_merge():
    f, a, spectator, packet = compiled_control()
    ch, d, p = packet.chart, packet.weighted_degree, packet.chart.p
    y, z, s = (2,), tuple((i+1) % p for i in range(ch.jet_width)), 3
    pulled = pullback_induced_phase(packet, y, z, s)
    assert type(pulled) is FilteredInducedPhasePacket and pulled.schema == packet.schema
    for key, value in packet.terms.items():
        if ch.weighted_degree(key[0]) == d:
            assert pulled.terms[key] == value*pow(s, d, p) % p
    opposite = replace(packet, terms={key: -value % p for key, value in packet.terms.items()})
    outcomes = [((0,), (0,)*ch.jet_width), (y, z), ((0,), (0,)*ch.jet_width)]
    merged = merge_induced_phases([packet, opposite, packet], [1, 1, 0], outcomes, d)
    assert type(merged) is FilteredInducedPhasePacket and merged.weighted_degree < d
    assert merged.terms and merged.schema == packet.schema
    with pytest.raises(ValueError, match="schemas"):
        induced_leading_columns([packet, replace(packet, filtered=replace(f, ambient_class=8))], d)


def test_filtered_guards_reject_forbidden_carrier_budget_and_basis_mix():
    f, a, spectator, packet = compiled_control()
    with pytest.raises(ValueError, match="bracket violates"):
        replace(f, coordinate_weights=(3, 3, 5, 7))
    high_parameter = next(i for i, (a, _) in enumerate(packet.parameter_basis) if a == 3)
    exponent = (0, 1)+(0,)*(packet.chart.jet_width-1)
    with pytest.raises(ValueError, match="filtered q/jet"):
        replace(packet, terms={(exponent, (high_parameter,)): 1})
    bad = [list(row) for row in a.inverse]
    j = next(i for i, (_, _, component) in enumerate(packet.chart.indices) if component == 1)
    bad[0][j] = 1
    with pytest.raises(ValueError, match="carrier filtration"):
        compile_filtered_induced_phase(replace(a, inverse=tuple(map(tuple, bad))), spectator, f)


def test_equation_dp_matches_independent_direct_support_enumeration():
    f = FilteredNormalChart(filiform_chart(11, 2), 4, (2, 2, 4))
    ch = filtered_jet_chart(f, 1)
    packet = FilteredInducedPhasePacket(ch, 3, 2, {}, f)
    expected = {d: 0 for d in range(1, 5)}
    for h in (1, 2):
        for indices in combinations_with_replacement(range(len(packet.parameter_basis)), h):
            ideal_count = sum(packet.parameter_basis[i][0] >= 2 for i in indices)
            if ideal_count > 1 or (ideal_count == 0 and h >= 2):
                continue
            cost = sum(f.coordinate_weights[packet.parameter_basis[i][0]] for i in indices)
            for t in range(3-h):
                for jets in combinations_with_replacement(range(ch.jet_width), t):
                    total = cost+sum(f.a_degrees[ch.indices[i][2]] for i in jets)
                    if total > 4:
                        continue
                    for qdegree in range(cost+1):
                        d = qdegree+sum(ch.indices[i][1] for i in jets)
                        if 1 <= d <= 4:
                            expected[d] += 1
    weighted, ordinary = filtered_equation_bounds(f, 1)
    assert weighted == expected
    assert ordinary == {1: 6, 2: 6}


def test_resource_improvement_is_an_exact_upper_envelope_not_a_timing():
    algebra, basis, _ = derived_length_three_witness(43)
    f = ambient_filtration_certificate(algebra, basis).filtered
    report = filtered_resource_report(f, 2)
    assert (report["weighted_degree"], report["ordinary_degree"], report["jet_width"]) == (9, 6, 155)
    assert report["counts_upper_power_of_two_exponents"]["queries"] == 4496
    assert len(report["stages"]) == 15 and report["joint_failure_upper_bound"] == "3/32"
    assert report["receiver_executed"] is False
    with pytest.raises(ValueError, match="exact error budget"):
        filtered_resource_report(f, 2, 0.125)
