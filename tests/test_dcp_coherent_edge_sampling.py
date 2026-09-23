from fractions import Fraction
import json
from itertools import combinations, product
from math import asin, cos, sin, sqrt

import numpy as np
import pytest

from dcp_balanced_pairing import BalancedPairingProgram, balanced_certificate
from dcp_coherent_edge_sampling import (
    build_coherent_edge_audit, edge_predicate, explicit_grover_rows,
    finite_geometric_readout, geometric_kernel, marked_amplitude,
    natural_degree_control, physical_edge_readout, sample_iterations, sampler_certificate,
    schedule_certificate, support_from_index, unrank_support,
)


def test_unranking_is_exact_without_materializing_the_prefix_list():
    for width in range(1, 9):
        for weight in range(width+1):
            expected = [sum(1 << i for i in c) for c in combinations(range(width), weight)]
            assert [unrank_support(width, weight, r) for r in range(len(expected))] == expected
    # Large rank remains an arithmetic unranking operation, not list enumeration.
    assert unrank_support(256, 30, (1 << 128)-1).bit_count() == 30


def test_capped_family_index_and_padding_match_an_independent_graph():
    p = BalancedPairingProgram((1, 2, 3, 4, 5, 6), 3, 1, (3, 6), 1)
    masks = [support_from_index(p, j) for j in range(16)]
    assert masks[:9] == [1 << left | 1 << right for left in range(3) for right in range(3, 6)]
    assert masks[9:] == [None]*7
    for b in range(64):
        raw = p.evaluate_xor(b)["neighbor_count_before_source_mark"]
        assert sum(edge_predicate(p, b, j) for j in range(16)) == (raw if p.marked(b) else 0)


@pytest.mark.parametrize("labels", [(0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 0)])
def test_full_grover_evolution_matches_degree_formula_without_counting(labels):
    p = BalancedPairingProgram(labels, 2, 1, (), 0)
    for t in range(7):
        state, marked = explicit_grover_rows(p, t)
        assert np.max(abs(np.sum(state*state, axis=1)-1)) < 1e-12
        for b in range(16):
            degree = int(marked[b].sum())
            assert np.allclose(state[b, marked[b]], marked_amplitude(degree, 4, t))


def test_fixed_time_can_reverse_the_parity_signal_on_an_actual_dcp_graph():
    p = BalancedPairingProgram((0, 1, 1, 1), 2, 1, (), 0)
    _, marked = explicit_grover_rows(p, 0)
    assert marked[4].sum() == 1 and marked[14].sum() == 2
    assert edge_predicate(p, 4, 3)  # Support 10 connects 4 and 14.
    row = physical_edge_readout(p, 2, 0)
    assert row["observed_signal"] == pytest.approx(-.25)
    assert row["conditional_normalization_used"] is False


def test_exact_kernel_matches_independent_trigonometric_expression_and_time_sum():
    for padded in (2, 4, 8, 16):
        schedule = schedule_certificate(padded, 24)
        stop, rho = float(schedule["stop_probability"]), float(schedule["rho"])
        def f(x):
            return stop*stop*cos(x)/(stop*stop+4*rho*sin(x)**2)
        for d, e in product(range(1, padded+1), repeat=2):
            kernel = geometric_kernel(d, e, padded)
            assert kernel > 0
            a, b = asin(sqrt(d/padded)), asin(sqrt(e/padded))
            trig = (f(a-b)-f(a+b))/(2*sqrt(d*e))
            direct = sum(stop*rho**t*marked_amplitude(d, padded, t)*marked_amplitude(e, padded, t)
                         for t in range(schedule["cutoff"]))
            assert float(kernel) == pytest.approx(trig, abs=1e-12)
            assert abs(float(kernel)-direct) <= rho**schedule["cutoff"]+1e-12
        assert geometric_kernel(1, 1, padded) == schedule["singleton_kernel"]
        assert geometric_kernel(0, 1, padded) == 0


@pytest.mark.parametrize("labels,hash_rows,offset", [
    ((0, 1, 1, 1), (), 0), ((1, 1, 1, 1), (), 0),
    ((1, 0, 1, 0), (0,), 1), ((1, 2, 3, 0), (3,), 1),
])
def test_physical_postselection_orientation_and_noise_match_unconditional_signal(labels, hash_rows, offset):
    p = BalancedPairingProgram(labels, 2, 1, hash_rows, offset)
    for t, secret, eta in product((0, 1, 2, 3), range(4), (1., .75, 0.)):
        row = physical_edge_readout(p, t, secret, eta)
        assert row["signal_residual"] < 1e-12
        assert row["success_residual"] < 1e-12
        assert abs(row["observed_signal"]) <= row["heralded_probability"]+1e-12
    averaged = finite_geometric_readout(p)
    assert all(averaged["checks"].values())
    if offset == 1 and hash_rows == (0,):
        assert averaged["truncated_signal"] == 0
    elif labels == (0, 1, 1, 1):
        assert averaged["truncated_signal"] > 0


def test_exact_public_coin_sampler_aborts_instead_of_postselecting_a_short_time():
    class Coins:
        def __init__(self, values):
            self.values = iter(values)
        def getrandbits(self, bits):
            assert bits == 1
            return next(self.values)
    assert sample_iterations(4, Coins([1, 1, 0]), 2) == 2
    assert sample_iterations(4, Coins([1]*4), 2) is None
    # The zero-truncated process sums to 1-tail; it is not renormalized.
    schedule = schedule_certificate(4, 2)
    stop, rho = schedule["stop_probability"], schedule["rho"]
    assert sum(stop*rho**t for t in range(schedule["cutoff"])) == 1-rho**schedule["cutoff"]


def test_correlated_fault_laws_are_not_replaced_by_product_attenuation():
    p = BalancedPairingProgram((0, 1, 1, 1), 2, 1, (), 0)
    all_or_none = {0: Fraction(3, 4), 15: Fraction(1, 4)}
    exactly_one = {1 << i: Fraction(1, 4) for i in range(4)}
    for t in range(4):
        clean = physical_edge_readout(p, t, 0)
        a = physical_edge_readout(p, t, 0, fault_law=all_or_none)
        b = physical_edge_readout(p, t, 0, fault_law=exactly_one)
        assert a["observed_signal"] == pytest.approx(.75*clean["observed_signal"])
        assert b["observed_signal"] == pytest.approx(.5*clean["observed_signal"])
        assert a["signal_residual"] < 1e-12 and b["signal_residual"] < 1e-12


def test_bounded_degree_oriented_edge_bound_on_every_small_label_tuple():
    # Exact graph counts, before taking natural-label expectations.
    for labels in product(range(4), repeat=4):
        p = BalancedPairingProgram(labels, 2, 1, (), 0)
        _, marked = explicit_grover_rows(p, 0)
        degrees = marked.sum(axis=1).tolist()
        for cap in (1, 2, 3):
            good = sum(degrees[b] <= cap and degrees[b ^ support_from_index(p, j)] <= cap
                       for b in range(16) for j in range(4) if marked[b, j])
            assert good >= sum(degrees)-Fraction(2, cap)*sum(d*d for d in degrees)


def test_unmarked_source_moments_are_checked_without_affine_hash_conditioning():
    row = natural_degree_control()
    assert row["mean_degree"] == 1
    assert row["second_moment"] == Fraction(7, 4)
    assert all(row["checks"].values())


def test_scalable_signal_bound_has_no_marking_counting_or_exponential_storage():
    for n in (6, 7, 8, 16, 31, 64, 128, 256, 512):
        row = sampler_certificate(n, 2*n)
        assert row["bounded_degree_oriented_mass_lower"] >= Fraction(1, 2)
        assert row["support_survival_lower"] >= Fraction(1, 3)
        assert row["bounded_degree_kernel_lower"] == Fraction(1, 4225)
        assert row["prelabel_fault_signal_lower"] >= Fraction(1, 25350)-Fraction(1, 65536) > 0
        for d, e in product(range(1, 9), repeat=2):
            assert geometric_kernel(d, e, row["padded_supports"]) >= row["bounded_degree_kernel_lower"]
        assert row["mean_reversible_predicate_calls_upper"] >= 1 << (n//2)
        assert not row["vertex_marking_used"]
        assert not row["quantum_counting_required"]
        assert not row["unique_neighbor_oracle_required"]
        assert not row["explicit_list_required"]
        assert not row["polynomial_time_claimed"]


def test_a_loose_time_cutoff_cannot_inherit_the_positive_signal_claim():
    row = sampler_certificate(16, 32, tail_bits=1)
    assert row["prelabel_fault_signal_lower"] < 0


@pytest.mark.parametrize("args", [(1, 16), (3, 16), (4, 0), (True, 16)])
def test_invalid_schedule_parameters_are_rejected(args):
    with pytest.raises(ValueError):
        schedule_certificate(*args)


def test_report_preserves_scope_and_never_calls_grover_a_new_speedup():
    row = build_coherent_edge_audit()
    assert row["control_failures"] == 0
    assert len(row["physical_controls"]) == 96
    assert row["contract"]["speedup_claim_allowed"] is False
    assert row["contract"]["unknown_input_state_reflection_used"] is False
    assert row["contract"]["no_quantum_counting_or_unique_partner_needed"] is True
    assert row["fixed_time_sign_counterexample"]["observed_signal"] == pytest.approx(-.25)
    assert len(row["correlated_noise_controls"]) == 24
    json.dumps(row)  # Native JSON booleans, not NumPy scalar checks.
