"""Exact structural falsifiers of particular HPGP interface shortcuts."""
from fractions import Fraction
from itertools import product
from collections import Counter
import random

import pytest

from theorems.hpgp_coset_interface import (
    chart_collision_relation, chart_coverage_bound, discarded_center_control,
    matrix_power, noncommuting_tail_witness,
    report, tail_commutator, tail_matrix, tail_product, transverse_curve,
)
from theorems.ut5_matrix_phase_alignment import _identity, _lists, _matrix, _rank


@pytest.mark.parametrize("p", [5, 43, 2**127-1])
def test_noncommuting_tail_certificate_includes_valid_transverse_subgroups(p):
    result = noncommuting_tail_witness(p)
    assert result["tail_ab"] != result["tail_ba"]
    assert result["all_transverse_generators_have_order_p"]
    assert result["integer_chart_equation_elimination_checked"]
    assert result["universal_injective_chart_impossible"]
    assert not result["quantum_lower_bound"]
    a = _matrix(tail_matrix(p, result["tail_a"]), p)
    b = _matrix(tail_matrix(p, result["tail_b"]), p)
    expected = _identity(4)
    expected[1][3] = 1
    assert _lists(a*b*a.inv()*b.inv()) == expected


def test_symbolic_chart_equations_do_not_invent_a_collision_for_commuting_rows():
    a, b = (1, 0, 0, 0, 0), (0, 1, 0, 0, 0)
    assert chart_collision_relation(5, a, b) == {}


@pytest.mark.parametrize("p", [5, 43, 2**127-1])
def test_cubic_curve_matches_binary_matrix_powers_without_enumerating_field(p):
    vector = (1, 2, 3, 4, 1)
    g = _matrix(tail_matrix(p, vector, 1), p)
    for t in (0, 1, 2, 3, p-1):
        assert _lists(matrix_power(p, g, t)) == [list(row) for row in tail_matrix(p, transverse_curve(p, vector, t), t)]


def test_tail_bracket_formula_and_maximum_abelian_projection_dimension():
    p = 5
    vectors = list(product(range(p), repeat=3))
    commuting_pairs = 0
    for u, v in product(vectors, repeat=2):
        bracket = tail_commutator(p, u, v)
        commuting_pairs += bracket == (0, 0)
        if u[2] and bracket == (0, 0):
            assert _rank((u, v), p) == 1
        if u[2] == v[2] == 0:
            assert bracket == (0, 0)
    # The c=0 plane has dimension2 and is abelian; adding a c direction
    # makes it nonabelian. The two-dimensional center gives max rank4.
    assert tail_commutator(p, (1, 0, 0), (0, 0, 1)) == (1, 0)
    assert tail_commutator(p, (0, 1, 0), (0, 0, 1)) == (0, 1)
    assert Fraction(commuting_pairs, len(vectors)**2) == Fraction(2*p*p-1, p**4)


def test_raw_chart_succeeds_on_a_maximal_abelian_tail_coset_and_fails_elsewhere():
    p = 5
    offsets = list(product(range(p), repeat=5))
    vector = (1, 2, 0, 3, 4)
    for t in range(p):
        curve = transverse_curve(p, vector, t)
        for offset in offsets:
            actual = tail_product(p, offset, curve)
            assert actual == tuple((a+b) % p for a, b in zip(offset, curve))
    bad = (1, 2, 1, 3, 4)
    curve = transverse_curve(p, bad, 1)
    assert tail_product(p, (1, 0, 0, 0, 0), curve) != tuple(
        (a+b) % p for a, b in zip((1, 0, 0, 0, 0), curve))


def test_coverage_counts_subgroups_not_polynomial_degree_or_measured_curve_fits():
    result = chart_coverage_bound(43, 8, 1000)
    assert result["lie_dimension"] == 41 and result["nilpotency_class"] == 3
    assert Fraction(result["uniform_hidden_parameter_coverage_upper"]) == Fraction(1000, 43**8)
    assert result["charts_required_for_complete_coverage"] == 43**8
    assert result["maximum_abelian_tail_order"]*43**8 == result["normal_tail_order"]
    assert not result["arbitrary_adaptive_reductions_excluded"]
    assert not result["collective_quantum_reductions_excluded"]
    cp = Fraction(2*43**2-1, 43**4)**8
    assert Fraction(result["normal_tail_commuting_probability"]) == cp
    assert Fraction(result["single_fixed_chart_mean_trace_distance_lower_bound"]) == Fraction(42, 43)*(1-cp)/8
    assert Fraction(chart_coverage_bound(5, 1, 100)["uniform_hidden_parameter_coverage_upper"]) == 1


def test_approximate_translation_lemma_on_independent_nonabelian_tables():
    # A separate D8 table checks the generic agreement lemma, not the UT4
    # commutator formula. Outputs are the additive group Z/8Z.
    group = list(product(range(4), range(2)))
    index = {g: i for i, g in enumerate(group)}
    table = [[index[((a+(-1)**b*c) % 4, (b+d) % 2)] for c, d in group] for a, b in group]
    cp = Fraction(sum(table[i][j] == table[j][i] for i, j in product(range(8), repeat=2)), 64)
    assert cp == Fraction(5, 8)
    rng = random.Random(29)
    for _ in range(100):
        phi0, phi1 = rng.sample(range(8), 8), rng.sample(range(8), 8)
        matches = sum(max(Counter((phi1[table[n][u]]-phi0[n]) % 8 for n in range(8)).values())
                      for u in range(8))
        assert 1-Fraction(matches, 64) >= (1-cp)/8
    # The obstruction must vanish on an abelian group with an additive chart.
    cyclic = [[(i+j) % 8 for j in range(8)] for i in range(8)]
    assert all(len({(cyclic[n][u]-n) % 8 for n in range(8)}) == 1 for u in range(8))


@pytest.mark.parametrize("p", [5, 7])
def test_literal_partial_trace_does_not_prepare_quotient_coset_state(p):
    result = discarded_center_control(p)
    assert result["actual_partial_trace_performed"]
    assert result["actual_trace"] == pytest.approx(1)
    expected = Fraction(2*p-1, p*p)
    assert Fraction(result["desired_fourier_support_mass_exact"]) == expected
    assert result["desired_fourier_support_mass"] == pytest.approx(float(expected))
    assert result["trace_distance"] >= float(1-expected)-1e-12
    assert not result["arbitrary_quotient_conversion_impossible"]


@pytest.mark.parametrize("args", [(3, 1), (6, 1), (True, 1), (5, 0), (5, True), (5, 1, 0)])
def test_invalid_analytic_promises_rejected(args):
    with pytest.raises(ValueError):
        chart_coverage_bound(*args)


def test_dense_control_has_a_cap_before_allocation():
    with pytest.raises(ValueError, match="capped"):
        discarded_center_control(43)


def test_no_new_algorithm_or_general_quantum_barrier_in_report():
    result = report()
    for flag in ("known_hpgp_solver_implemented", "rees_correctness_verified", "rees_novelty_established",
                 "quantum_speedup_claimed", "general_hpgp_reduction_ruled_out"):
        assert result[flag] is False
