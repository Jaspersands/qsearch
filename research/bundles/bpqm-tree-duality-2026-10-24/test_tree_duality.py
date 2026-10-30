from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

import numpy as np
import pytest

import tree_duality as t


def raw_pair(a, b):
    law = defaultdict(F)
    for sign in (1, -1):
        d = 1+sign*a*b
        if d:
            law[abs(a+sign*b)/d] += d/2
    return dict(law)


def direct_bayes(reliabilities):
    law = defaultdict(F)
    for outcomes in product((-1, 1), repeat=len(reliabilities)):
        probabilities = []
        for x in (-1, 1):
            p = F(1, 2)
            for r, s in zip(reliabilities, outcomes):
                p *= (1+x*s*r)/2
            probabilities.append(p)
        mass = sum(probabilities)
        if mass:
            law[abs(probabilities[1]-probabilities[0])/mass] += mass
    return dict(law)


@pytest.mark.parametrize("a,b", [(F(0), F(0)), (F(1), F(1)), (F(0), F(1)),
                                 (F(1, 4), F(3, 4)), (F(7, 8), F(1, 8)),
                                 (F(1, 3), F(2, 3)), (F(13, 20), F(13, 20))])
def test_classical_parallel_law_independent_bayes(a, b):
    assert raw_pair(a, b) == direct_bayes((a, b))
    q = sum(p*r*r for r, p in raw_pair(a, b).items())
    assert q <= a*a+b*b
    if a*b != 1:
        assert q == (a*a+b*b-2*a*a*b*b)/(1-a*a*b*b)


@pytest.mark.parametrize("a,b", [(0., 0.), (1., 1.), (0., 1.), (.25, .75),
                                 (.875, .125), (.65, .65)])
def test_quantum_parity_blocks_independent_density_matrices(a, b):
    def state(r, x):
        return np.array([np.sqrt((1+r)/2), (-1)**x*np.sqrt((1-r)/2)])
    densities = []
    for parity in (0, 1):
        vectors = [np.kron(state(a, x), state(b, x ^ parity)) for x in (0, 1)]
        densities.append(sum(np.outer(v, v) for v in vectors)/2)
    for sector, indices in enumerate(((0, 3), (1, 2))):
        blocks = [rho[np.ix_(indices, indices)] for rho in densities]
        probability = (1+(1 if sector == 0 else -1)*a*b)/2
        assert all(np.trace(block) == pytest.approx(probability) for block in blocks)
        if probability == 0:
            assert all(np.linalg.norm(block) == 0 for block in blocks)
            continue
        normalized = [block/probability for block in blocks]
        assert all(np.trace(block@block) == pytest.approx(1) for block in normalized)
        actual_squared = np.trace(normalized[0]@normalized[1])
        expected = (a+b)/(1+a*b) if sector == 0 else (a-b)/(1-a*b)
        assert actual_squared == pytest.approx(expected*expected, abs=1e-12)
    # The odd-sector sign may be negative. Absolute overlap is a known
    # branchwise gauge convention, not deletion of a hidden phase record.
    if a < b and a*b < 1:
        assert (a-b)/(1-a*b) < 0


@pytest.mark.parametrize("direction", ["up", "down"])
@pytest.mark.parametrize("kind", ["product", "parallel"])
def test_directed_rounding_preserves_information_bound(kind, direction):
    a, b, grid = F(3, 8), F(7, 8), 8
    left, right = t.point(a, grid, 16), t.point(b, grid, 16)
    bound = t.combine(left, right, kind, direction)
    raw = {a*b: F(1)} if kind == "product" else raw_pair(a, b)
    # Binary symmetric Blackwell checks through symmetric convex stop losses.
    for threshold in (F(i, 64) for i in range(65)):
        exact = sum(p*max(r-threshold, 0) for r, p in raw.items())
        approximate = sum(F(w, 1 << bound.bits)*max(F(i, grid)-threshold, 0)
                          for i, w in enumerate(bound.weights))
        assert approximate >= exact if direction == "up" else approximate <= exact
    assert sum(bound.weights) == 1 << 16


@pytest.mark.parametrize("arity,degree", [(3, 6), (4, 7), (3, 3)])
@pytest.mark.parametrize("direction", ["up", "down"])
def test_ab_ba_intertwining(arity, degree, direction):
    c, v = F(3, 5), t.point(1, 16, 32, direction)
    u = t.point(c, 16, 32, direction)
    for _ in range(3):
        # Separately compute the V -> A(B(V)) and U -> B(A(U)) streams.
        v = t.A(t.B(v, c, arity, direction), degree, direction)
        u = t.B(t.A(u, degree, direction), c, arity, direction)
        assert u == t.B(v, c, arity, direction)


def test_nishimori_and_first_level_tree_information():
    c = F(13, 20)
    reference = direct_bayes((c,)*5)
    q = sum(p*r*r for r, p in reference.items())
    # Conditional on the true input +1, posterior sign is correct with
    # probability (1+r)/2. Thus E[m]=E[m^2], not E[|m|].
    signed_mean = sum(p*((1+r)/2*r-(1-r)/2*r) for r, p in reference.items())
    assert signed_mean == q
    upper = t.bounded_tree(levels=1)["history"][0]
    assert q <= F(upper["q_classical_upper"])
    assert q < sum(p*r for r, p in reference.items())


def test_canonical_mixture_metrics_cannot_be_interchanged():
    weights = (128, 0, 0, 0, 128)
    erasure = t.Law(4, 8, weights)
    bsc = t.point(F(1, 2), 4, 8)
    assert erasure.moment(1) == bsc.moment(1) == F(1, 2)
    assert erasure.moment(2) == F(1, 2)
    assert bsc.moment(2) == F(1, 4)


def test_native_factor_tree_from_gibbs_weights():
    c, branches = F(13, 20), 3
    law = defaultdict(F)
    total = F(0)
    # Root plus six revealed leaves; each factor contains root and two leaves.
    for boundary in product((-1, 1), repeat=2*branches):
        masses = []
        for root in (-1, 1):
            weight = F(1, 2**(1+2*branches))
            for j in range(branches):
                weight *= 1+c*root*boundary[2*j]*boundary[2*j+1]
            masses.append(weight)
        mass = sum(masses)
        total += mass
        law[abs(masses[1]-masses[0])/mass] += mass
    assert total == 1
    assert dict(law) == direct_bayes((c,)*branches)


def test_original_quantum_certificate_replayed_and_classical_basin_entered():
    reference = json.loads((Path(__file__).parent/"reference_frontier.json").read_text())
    result = t.bounded_tree()
    actual = [r["mean_quantum_overlap_upper"] for r in result["history"][:12]]
    assert actual == reference["upper_fidelity_history"]
    assert result["nonreconstruction_certificate"]["level"] == 8
    q12 = F(result["history"][11]["q_classical_upper"])
    assert q12 < F(9, 200)
    assert F(169, 80)*F(9, 200) < F(1, 10)
    for extra in range(5):
        assert t.basin_bound(q12, F(13, 20), 3, 6, extra) <= \
            F(80, 169)*F(1, 10)**(2**extra)
    assert result["finite_graph_mixing_proved"] is False
    assert result["all_quantum_decoders_ruled_out"] is False


def test_nonreconstruction_does_not_imply_worst_boundary_uniqueness():
    assert t.all_plus_boundary_update(F(99, 100), F(13, 20)) > F(99, 100)
    assert t.all_plus_boundary_update(F(1), F(13, 20)) > F(99, 100)


def test_endpoints_have_opposite_information_meanings():
    perfect_boundary = t.point(1, 16, 32)
    zero = t.B(perfect_boundary, 0, 3)
    one = t.B(perfect_boundary, 1, 3)
    assert zero.moment(1) == t.A(zero, 6).moment(2) == 0
    assert one.moment(1) == t.A(one, 6).moment(2) == 1


@pytest.mark.parametrize("kwargs", [{"c": 0.65}, {"c": 1}, {"grid": 7},
                                    {"levels": 0}, {"arity": 2}, {"degree": 2}])
def test_bad_contracts_fail_closed(kwargs):
    with pytest.raises(ValueError):
        t.bounded_tree(**kwargs)


def test_no_unjustified_basin_or_mass_admission():
    with pytest.raises(ValueError):
        t.basin_bound(1, F(13, 20), 3, 6, 1)
    with pytest.raises(ValueError):
        t.Law(4, 8, (0, 0, 0, 0, 255))
    with pytest.raises(ValueError):
        t.combine(t.point(1, 8), t.point(1, 16), "parallel")
