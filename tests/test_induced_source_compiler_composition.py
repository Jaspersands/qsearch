"""Original hiding labels -> batch shear -> GL/spectator -> compiled phase.

Exact phase counts, no floating-point reconstruction and no potential
oracle. The finite direct-product source is a channel diagnostic; its
selected normal factor is not claimed to be the ambient derived group.
"""
from collections import Counter
from fractions import Fraction
from itertools import product

from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.metabelian_induced_phase import align_induced_jet, compile_induced_phase
from theorems.nonlinear_jet_erasure import _jet_terms
from theorems.right_abelian_induced_source import FiliformNormal
from tests.test_metabelian_induced_phase import design, filiform_chart


def test_actual_original_oracle_batch_matches_compiler_with_all_record_factors():
    p, k = 11, 4
    group, st = FiliformNormal(p, k), filiform_chart(p, k)
    chart = FullTaylorJetChart(p, 2, 2, 2)
    labels, scales, outcomes = design(chart, st)
    alignment = align_induced_jet(chart, st, labels, scales, outcomes)
    assert labels[0] == (0, 0, 0)
    spectator = (3, 7)
    packet = compile_induced_phase(alignment, spectator)
    r, J, batch = st.a_width, chart.jet_width, len(labels)
    assert alignment.carrier_width-J == len(spectator)

    # G=F_p^2 x N, H={(u,0,exp(uX))}; f is fixed before the potential.
    powers = [group.exp((u, 0, 0, 0, 0)) for u in range(p)]
    def section(q):
        return group.exp((0, q[1], 0, 0, 0))
    def original_label(q, n):
        return q[1], group.multiply(n, powers[-q[0] % p])
    def chart_label(q, n):
        return original_label(q, group.multiply(n, section(q)))

    # Only diagnostic truth: Q(q)=q0*X-q0*q1*Y1, from the group word.
    parameters = tuple(1 if (a, alpha) == (0, (1, 0)) else
                       p-1 if (a, alpha) == (2, (1, 1)) else 0
                       for a, alpha in packet.parameter_basis)
    def evaluate(terms, q):
        return sum(c*pow(q[0], alpha[0], p)*pow(q[1], alpha[1], p)*
                   parameters[indices[0]] for (alpha, indices), c in terms.items()) % p
    def curve(q):
        return tuple(evaluate(_jet_terms(chart, packet.parameter_basis, j, 2), q) for j in range(J))
    def old_carrier(t):
        return tuple(sum(c*v for c, v in zip(row, t+spectator)) % p for row in alignment.inverse)

    fibers = tuple(product(range(p), repeat=k-1))
    def actual_phase_counts(label, q, qprime, x, y):
        if q[1] != qprime[1]:
            return Counter()
        counts = Counter()
        for fiber in fibers:
            n = group.inverse(group.from_right_coordinates(x, fiber))
            # Invert the ORIGINAL output label at qprime. No W(g) kernel here.
            value = chart_label(q, n)
            other = group.multiply(group.multiply(value[1], powers[qprime[0]]),
                                   group.inverse(section(qprime)))
            assert chart_label(qprime, other) == value
            target, other_fiber = group.right_coordinates(group.inverse(other))
            if target == y:
                phase = sum(c*(a-b) for c, a, b in zip(label, fiber, other_fiber)) % p
                counts[phase] += 1
        return counts

    saw_nontrivial_phase = False
    for q, qprime in (((0, 1), (2, 1)), ((3, 2), (7, 2)), ((1, 4), (1, 4))):
        t = tuple((3*j+1) % p for j in range(J))
        tprime = tuple((a+b-c) % p for a, b, c in zip(t, curve(q), curve(qprime)))
        carrier, other_carrier = old_carrier(t), old_carrier(tprime)
        total_phase = 0
        for i, (label, scale, origin) in enumerate(zip(labels, scales, outcomes)):
            old_q = tuple((y+scale*x) % p for y, x in zip(origin, q))
            old_qprime = tuple((y+scale*x) % p for y, x in zip(origin, qprime))
            counts = actual_phase_counts(label, old_q, old_qprime,
                                         carrier[r*i:r*(i+1)], other_carrier[r*i:r*(i+1)])
            assert len(counts) == 1 and sum(counts.values()) == p**(k-1)
            total_phase = (total_phase+next(iter(counts))) % p
        expected_phase = (packet.evaluate_fixture(q+t, parameters)-
                          packet.evaluate_fixture(qprime+tprime, parameters)) % p
        assert total_phase == expected_phase
        saw_nontrivial_phase |= total_phase != 0 and total_phase != -total_phase % p
    assert saw_nontrivial_phase  # Conjugating the compiled phase would fail.

    # Per-source raw kernel is 1/|G|, with inversion/Fourier norm included.
    # Fresh quotient |+> adds 1/|V|. All lambda, Y and spectator records remain.
    quotient_order, ideal_order, carrier_order = p**2, p**(k-1), p**r
    group_order = quotient_order*ideal_order*carrier_order
    raw_coefficient = Fraction(1, quotient_order*group_order**batch)
    records_mass = Fraction(1, ideal_order**batch*quotient_order**batch*p**len(spectator))
    curve_coefficient = Fraction(1, quotient_order*p**J)
    assert raw_coefficient == records_mass*curve_coefficient
    assert raw_coefficient != records_mass*curve_coefficient*ideal_order
    assert raw_coefficient != records_mass*curve_coefficient*quotient_order**batch

    # A proper-U off-diagonal entry vanishes already at the original label.
    assert not actual_phase_counts(labels[1], (0, 0), (0, 1), (0, 0), (0, 0))

    # Violating a retained jet address, even one whose hidden value is zero,
    # must remove coherence rather than silently integrating that register out.
    q, qprime = (0, 1), (2, 1)
    t = (0,)*J
    tprime = tuple((a-b) % p for a, b in zip(curve(q), curve(qprime)))
    wrong_tprime = tprime[:-1]+((tprime[-1]+1) % p,)
    carrier, wrong_carrier = old_carrier(t), old_carrier(wrong_tprime)
    killed = False
    for i, (label, scale, origin) in enumerate(zip(labels, scales, outcomes)):
        old_q = tuple((y+scale*x) % p for y, x in zip(origin, q))
        old_qprime = tuple((y+scale*x) % p for y, x in zip(origin, qprime))
        killed |= not actual_phase_counts(label, old_q, old_qprime,
                                           carrier[r*i:r*(i+1)], wrong_carrier[r*i:r*(i+1)])
    assert killed
