"""Controls for cross-batch support, not new oracle problems or quantum runs."""
from itertools import product
import random

import pytest

from tests.test_class_four_matrix_source import forms3, mv
from theorems.class_four_matrix_source import align_variable_jets
from theorems.symbolic_scalar_phase_erasure import (
    pin_symbolic_packet, sparse_leading_columns, verify_diagonal_witness,
)
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket


def _batch(p, extra):
    forms = forms3(p)+[[[0]*3 for _ in range(3)]]
    labels, scales, outcomes = [], [], []
    for j in range(3):
        labels += [[c*int(i == j) % p for i in range(4)] for c in (1, 1, -2)]
        scales += [j+1]*3
        outcomes += [[0, 0], [1, 0], [0, 1]]
    labels += [[0, 0, 0, 1], [0, 0, 0, p-1]]
    scales += [4, 4]
    outcomes += [[0, 0], [1, 1]]
    for _ in range(extra):
        labels += [[1, 1, 1, 0], [p-1, p-1, p-1, 0]]
        scales += [2, 2]
        outcomes += [[2, 3], [3, 1]]
    outcomes = [[(y+extra) % p for y in row] for row in outcomes]
    alignment = align_variable_jets(p, forms, labels, scales, outcomes)
    return alignment, scales, outcomes


def _aligned_displacement(alignment, scales, outcomes, q, potential):
    maps = alignment.maps
    R, p = maps.carrier_width, maps.p
    raw, start = [0]*(2*R), 0
    for i, rep in zip(maps.active_indices, maps.representations):
        point = [(y+scales[i]*x) % p for y, x in zip(outcomes[i], q)]
        v = mv(rep.weyl, potential(*point), p)
        r = rep.qudits
        raw[start:start+r], raw[R+start:R+start+r] = v[:r], v[r:]
        start += r
    return mv(alignment.symplectic, raw, p)[:R]


def _potential(x, y):
    return [2+x+x*y, 3-x+y*y, 4+y+x*x]


def _common_jet(x, y):
    # Lq, polarization(e_1,q), polarization(e_2,q), in the public J order.
    return [x, -x, y, y, 0, 2*x, x, 2*y, 0]


@pytest.mark.parametrize("p", [7, 2**127-1])
def test_different_multivariate_batches_retain_identical_hidden_jet(p):
    rng = random.Random(19)
    points = list(product(range(p), repeat=2)) if p == 7 else [
        (rng.randrange(p), rng.randrange(p)) for _ in range(16)]
    widths, physical_widths = set(), set()
    for extra in (0, 1, 3):
        alignment, scales, outcomes = _batch(p, extra)
        R, D = alignment.maps.carrier_width, alignment.maps.jet_width
        widths.add(R)
        physical_widths.add(alignment.maps.source_carrier_width)
        origin = _aligned_displacement(alignment, scales, outcomes, (0, 0), _potential)
        for q in points:
            actual = _aligned_displacement(alignment, scales, outcomes, q, _potential)
            delta = [(a-b) % p for a, b in zip(actual, origin)]
            assert delta == [x % p for x in _common_jet(*q)]+[0]*(R-D)
    assert len(widths) > 1 and len(physical_widths) == 3


def test_same_transcript_different_hidden_chart_does_not_keep_same_support():
    p = 7
    alignment, scales, outcomes = _batch(p, 0)
    changed = lambda x, y: _potential(y, x)
    results = []
    for potential in (_potential, changed):
        zero = _aligned_displacement(alignment, scales, outcomes, (0, 0), potential)
        one = _aligned_displacement(alignment, scales, outcomes, (1, 0), potential)
        results.append([(a-b) % p for a, b in zip(one, zero)])
    # A line with q=(t,0) maps to different graph supports. A matching
    # field, schema and even identical public transcript cannot fix this.
    assert results[0] != results[1]


def test_truth_specific_cancellation_is_not_a_public_parameter_identity():
    p, basis = 11, ((0, (1,)), (0, (2,)))
    batch = [pin_symbolic_packet(
        SymbolicScalarPacket(p, 1, 0, basis, {((3,), (i,)): 1}),
        instance_id="same", chart_id="same") for i in (0, 1)]
    columns, _ = sparse_leading_columns(batch, 3)
    # At theta=(1,1), 1^3 + (-1)^3 = 0. At theta=(1,2), it is nonzero.
    weights = [1, p-1]
    with pytest.raises(ArithmeticError, match="cancellation failed"):
        verify_diagonal_witness(p, columns, weights, 3)
    for theta, expected in (([1, 1], 0), ([1, 2], p-1)):
        value = sum(pkt.packet.evaluate_fixture([s], theta) for pkt, s in zip(batch, weights)) % p
        assert value == expected
