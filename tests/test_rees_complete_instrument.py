"""Cross-check sparse regular-operator emulation and the complete finite lift."""
from itertools import product
import random

import numpy as np
import pytest

from theorems.central_character_descent import controlled_discard
from theorems.rees_complete_instrument import (
    ReesFiliformFixture, central_descent_packet, conditioned_coefficients,
    operator_product, report, source_multiply,
)
from theorems.rees_hsp_reduction import _units, make_rees_cover
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra


class _Cyclic:
    stage = 2
    p = 5

    def __init__(self, width=2):
        self.width = width
        self.identity = (0,)*width
        self.elements = tuple(product(range(5), repeat=width))
        self.index = {g: i for i, g in enumerate(self.elements)}
        self.order = len(self.elements)

    def mul(self, a, b):
        return tuple((x+y) % 5 for x, y in zip(a, b))

    def inv(self, a):
        return tuple(-x % 5 for x in a)

    def dilate(self, a, s):
        return tuple(x*pow(s, j+1, 5) % 5 for j, x in enumerate(a))

    @property
    def center_points(self):
        return tuple(((t,), (0, t)) for t in range(5))

    @property
    def quotient(self):
        return _Cyclic(1)

    def project(self, a):
        return a[:1]

    def right(self, a):
        return np.array([self.index[self.mul(x, self.inv(a))] for x in self.elements])


def _dense(group, coefficients):
    out = np.zeros((group.order, group.order), dtype=complex)
    columns = np.arange(group.order)
    for g, value in coefficients.items():
        out[group.right(g), columns] += value
    return out


def test_regular_operator_products_and_projectors_match_literal_dense_matrices():
    group = _Cyclic()
    coefficients = {(t, t): 1+0j for t in range(5)}
    rho = _dense(group, coefficients)/25
    states = {}
    for label in range(5):
        projector = {(0, t): np.exp(-2j*np.pi*label*t/5)/5 for t in range(5)}
        P = _dense(group, projector)
        np.testing.assert_allclose(_dense(group, operator_product(group, projector, coefficients)),
                                   P @ _dense(group, coefficients), atol=1e-13)
        actual = P @ rho @ P.conj().T
        mass, sparse = conditioned_coefficients(group, coefficients, (label,))
        np.testing.assert_allclose(mass, np.trace(actual), atol=1e-13)
        np.testing.assert_allclose(_dense(group, sparse)/25, actual/mass, atol=1e-13)
        states[label] = sparse
    # A slanted H with degree-(1,2) action has a residual phase. The sparse
    # implementation must retain it, not manufacture the desired coset state.
    records, weights = (((1,), states[1]), ((1,), states[1])), (1, 2)
    actual = central_descent_packet(group, records, weights)
    controls = [np.array([group.right(group.dilate((x, 0), s)) for x in range(5)]) for s in weights]
    dense_source = _dense(group, states[1])/25
    dense_output = 5*controlled_discard(dense_source, controls[0])*controlled_discard(dense_source, controls[1])
    np.testing.assert_allclose(_dense(group.quotient, actual)/5, dense_output, atol=1e-13)
    assert max(abs(value.imag) for value in actual.values()) > 0.5
    assert np.linalg.norm(dense_output-np.ones((5, 5))/5) > 1
    full = {g: 1+0j for g in group.elements}
    assert conditioned_coefficients(group, full, (1,)) == (0.0, None)
    with pytest.raises(ValueError, match="moment"):
        central_descent_packet(group, records, (1, 1))
    for bad in ((), (5,), (True,), (1.0,)):
        with pytest.raises(ValueError, match="canonical"):
            conditioned_coefficients(group, coefficients, bad)


def test_independent_semidirect_coordinates_agree_with_actual_rees_compiler_and_bch():
    def bracket(a, b):
        return 0, 0, (a[0]*b[1]-a[1]*b[0]) % 5, (a[0]*b[2]-a[2]*b[0]) % 5
    cover = make_rees_cover(PublicLieAlgebra(5, 4, bracket), _units(4))
    assert cover.dimensions == (4, 2, 1)
    group, rng = ReesFiliformFixture(), random.Random(1903)
    def encode(logarithm):
        a, b, c = cover.coefficients(logarithm)
        x, y, z, w = a
        u, v, t = b[2], b[3], c[3]
        return x, y, z, w, (u+3*x*y) % 5, (v+3*x*z) % 5, (t+3*x*u+x*x*y) % 5
    def exp_source(v):
        x, y, z, w = v
        return x, y, (z+3*x*y) % 5, (w+3*x*z+x*x*y) % 5
    for _ in range(24):
        a, b = (tuple(rng.randrange(5) for _ in range(7)) for _ in range(2))
        aa, bb = encode(a), encode(b)
        assert encode(cover.multiply(a, b)) == group.mul(aa, bb)
        assert group.mul(aa, group.inv(aa)) == group.identity
        for s in range(1, 5):
            assert encode(cover.dilate(a, s)) == group.dilate(aa, s)
            assert group.evaluate(aa, s) == exp_source(cover.evaluate(a, s))
            assert group.evaluate(group.mul(aa, bb), s) == source_multiply(
                group.evaluate(aa, s), group.evaluate(bb, s))
        for stage in (3, 2):
            current = ReesFiliformFixture(stage)
            aaa, bbb = aa[:current.width], bb[:current.width]
            assert current.project(current.mul(aaa, bbb)) == current.quotient.mul(
                current.project(aaa), current.project(bbb))


@pytest.fixture(scope="module")
def completed_report():
    return report()


@pytest.mark.parametrize("kind,lift_order,fibers,second_labels,tuples,basis", [
    ("X+W", 5, 15625, 25, 57, [[1, 0, 0, 1]]),
    ("Z+W", 25, 3125, 5, 37, [[0, 0, 1, 1]]),
])
def test_complete_lift_two_central_instruments_and_original_subspace_recovery(
        completed_report, kind, lift_order, fibers, second_labels, tuples, basis):
    case = next(case for case in completed_report["cases"] if case["hidden_fixture"] == kind)
    assert case["cover_order"] == 78125 and case["cover_dimension"] == 7
    assert case["all_tuple_fibers_checked"]
    assert case["lifted_subgroup_order"] == lift_order
    assert case["tuple_fiber_count"] == fibers
    first, second = case["stages"]
    assert (first["center_rank"], second["center_rank"]) == (1, 2)
    assert first["tested_label_tuples"] == 25 and first["all_positive_label_tuples_checked"]
    assert second["positive_labels"] == second_labels
    assert second["tested_label_tuples"] == tuples and not second["all_positive_label_tuples_checked"]
    assert second_labels <= second["distinct_label_tuples"] <= tuples
    assert max(first["maximum_regular_coefficient_error"], second["maximum_regular_coefficient_error"]) < 1e-12
    assert case["full_original_subspace_recovered"]
    assert case["recovered_basis"] == basis
    assert case["final_fourier_support_size"] == 125
    assert case["twelve_sample_recoveries"] == case["sampling_trials"] == 32
    assert case["lifted_copies_per_final_packet"] == 10
    assert case["ideal_original_oracle_queries_per_final_packet"] == 30


def test_complete_finite_control_does_not_promote_theorem_or_implementation_status(completed_report):
    for flag in ("all_second_stage_label_tuples_checked", "independent_review", "formal_verification",
                 "asymptotic_runtime_tested", "quantum_receiver_implemented", "novelty_established",
                 "speedup_claim_allowed"):
        assert completed_report[flag] is False
    assert "exhaustive" in completed_report["tuple_source_emulation"]
    assert "fixture_only" in completed_report["quadratic_witness_search"]
    for bad in (0, 4, True):
        with pytest.raises(ValueError):
            ReesFiliformFixture(bad)
