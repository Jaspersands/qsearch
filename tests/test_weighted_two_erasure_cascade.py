"""Tests for the Bezout exponent-reduced higher-degree SDE solver and two-stage weighted-to-ordinary phase-erasure cascade."""
from __future__ import annotations

import random

import pytest

from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.nonlinear_jet_erasure import TaylorJetChart
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket
from theorems.weighted_two_erasure_cascade import (
    PinnedWeightedPacket,
    bezout_reduced_exponent,
    build_weighted_two_erasure_cascade_report,
    ordinary_higher_degree_erasure_stage,
    required_bezout_arity,
    solve_bezout_sde_weights,
    transition_to_fourier_residual,
    verify_general_degree_witness,
    weighted_cancellation_weights,
    weighted_erasure_stage,
)


@pytest.mark.parametrize("p,degree,expected_g", [
    (23, 1, 1),
    (23, 2, 2),
    (23, 3, 1),
    (23, 4, 2),
    (23, 5, 1),
    (23, 6, 2),
    (2**127 - 1, 4, 2),
    (2**127 - 1, 5, 1),
])
def test_bezout_reduced_exponent_and_sde_solver(p: int, degree: int, expected_g: int) -> None:
    g, u = bezout_reduced_exponent(p, degree)
    assert g == expected_g
    rng = random.Random(2026 + degree)
    for _ in range(10):
        y = rng.randrange(p)
        assert pow(pow(y, u, p), degree, p) == pow(y, g, p)

    rank_target = 2
    arity = required_bezout_arity(p, degree, rank_target)
    columns = [[(i + 1) * (j + 2) + (i * i % 7) for j in range(rank_target)] for i in range(arity)]
    columns = [[x % p for x in col] for col in columns]
    weights, rank, g_out, _ = solve_bezout_sde_weights(p, columns, degree, rng=rng)
    assert g_out == expected_g
    assert rank <= rank_target
    assert any(weights)
    verify_general_degree_witness(p, columns, weights, degree)


def test_weighted_controller_never_calls_evaluate_fixture(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("hidden truth accessed inside weighted cascade")

    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    p = 23
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=3)
    basis = ((0, (1,)), (0, (2,)), (0, (3,)))
    rng = random.Random(42)

    packets = []
    for i in range(3):
        exp = [0] * chart.width
        exp[0] = 5
        pkt = SymbolicScalarPacket(p, 1, chart.jet_width, basis, {(tuple(exp), (0, 1)): i + 1})
        packets.append(PinnedWeightedPacket("inst-p23", "chart-0", chart, pkt))

    outcomes = [
        ([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)])
        for _ in packets
    ]
    merged, weights, rank, eqs = weighted_erasure_stage(packets, 5, outcomes, rng=rng)
    assert any(weights)
    assert rank == 1 and eqs == 1
    assert merged.weighted_degree <= 4
    assert all(pkt.consumed for pkt in packets)


def test_weighted_provenance_pinning_and_premature_fourier_rejection() -> None:
    p = 23
    chart = TaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=3)
    basis = ((0, (1,)), (0, (2,)))
    exp = (3,) + (0,) * chart.jet_width
    raw = SymbolicScalarPacket(p, 1, chart.jet_width, basis, {(exp, (0,)): 2})
    pkt1 = PinnedWeightedPacket("inst-A", "chart-0", chart, raw)
    pkt_wrong_inst = PinnedWeightedPacket("inst-B", "chart-0", chart, raw)

    # Duplicate wrapper instance rejected
    with pytest.raises(ValueError, match="distinct"):
        weighted_cancellation_weights([pkt1, pkt1], 3)

    # Mismatched instance_id rejected
    with pytest.raises(ValueError, match="pinned"):
        weighted_cancellation_weights([pkt1, pkt_wrong_inst], 3)

    # Premature Fourier readout rejected while weighted_degree > 0
    with pytest.raises(ValueError, match="erased to degree 0"):
        transition_to_fourier_residual(pkt1, [1] * chart.jet_width)
    assert not pkt1.consumed


def test_two_stage_weighted_to_ordinary_cascade_reaches_zero_degree() -> None:
    p = 23
    rng = random.Random(99)
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=3)
    basis = tuple((0, (k,)) for k in range(1, 4))

    # Build 2 weighted-erased roots (starting from weighted degree 1)
    residual_packets = []
    for r_idx in range(3):
        exp1 = (1,) + (0,) * chart.jet_width
        b1 = [
            PinnedWeightedPacket(
                "inst-2stage",
                "c0",
                chart,
                SymbolicScalarPacket(p, 1, chart.jet_width, basis, {(exp1, (0,)): i + 1}),
            )
            for i in range(2)
        ]
        o1 = [([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)]) for _ in b1]
        w_root, _, _, _ = weighted_erasure_stage(b1, 1, o1, rng=rng)
        assert w_root.weighted_degree == 0
        eta = [(r_idx + j + 1) % p for j in range(chart.jet_width)]
        res = transition_to_fourier_residual(w_root, eta)
        assert w_root.consumed
        assert res.degree == 3
        residual_packets.append(res)

    # Erase ordinary degree 3 -> <= 2
    after_d3, w3, _, _ = ordinary_higher_degree_erasure_stage(
        residual_packets,
        3,
        outcomes=[[rng.randrange(p)] for _ in residual_packets],
        rng=rng,
    )
    assert any(w3)
    assert after_d3.degree <= 2

    # Also test ordinary degree-4 erasure at p = 23 (g = gcd(4, 22) = 2)
    deg4_packets = [
        SymbolicScalarPacket(p, 1, 0, basis, {((4,), (0,)): (i + 1) % p, ((2,), (1,)): (2 * i + 1) % p})
        for i in range(4)
    ]
    after_d4, w4, r4, eq4 = ordinary_higher_degree_erasure_stage(
        deg4_packets,
        4,
        outcomes=[[i % p] for i in range(4)],
        rng=rng,
    )
    assert any(w4)
    assert r4 == 1 and eq4 == 1
    assert after_d4.degree <= 3


def test_report_builder_invariants() -> None:
    report = build_weighted_two_erasure_cascade_report()
    assert report["schema_version"] == "weighted_two_erasure_cascade_v1"
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    assert report["scope"]["supported_reduced_exponents"] == [1, 2, 3]
    assert report["scope"]["quadratic_requires_p_mod4_3"]
    assert report["scope"]["cubic_three_coset_collision"]
    assert not report["scope"]["general_coset_collision_sde_for_g_gt_3"]
    assert report["stage1_weighted_erasure_p23"][-1]["output_weighted_degree"] == 0
    assert report["fourier_transition_and_stage2_ordinary_p23"]["after_stage_D_ordinary_degree"] <= 2
    assert report["large_prime_127bit_higher_degree_controls"]["degree_4"]["verified_nonzero_witness"] is True
    assert report["large_prime_127bit_higher_degree_controls"]["degree_5"]["verified_nonzero_witness"] is True
