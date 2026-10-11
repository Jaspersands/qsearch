"""Tests for Wreath Product Sign-Orbit Plancherel Mass Extinction Barrier & Racah Cumulant Collapse.

Verifies:
1. Exact Euler partition numbers p(n) and bijection with distinct odd parts.
2. Exact wreath product W_n dimension sums and Plancherel measure factorization.
3. Sign-swap self-duality mass law on W_{2m}.
4. Multi-copy collision probability bounds.
5. Empirical orientation-syndrome channel collapse from S_6 to S_7.
6. Report generation, registry negative result registration, and claim gating.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from theorems.self_dual_wreath_plancherel_mass_extinction_barrier import (
    partition_count_euler,
    integer_partitions,
    hook_length_dimension,
    transpose_partition,
    is_self_conjugate,
    distinct_odd_partitions,
    verify_euler_bijection,
    symmetric_group_plancherel_spectrum,
    wreath_product_plancherel_spectrum,
    wreath_sign_swap_self_dual_law,
    multi_copy_plancherel_collision_law,
    audit_empirical_orientation_cross_check,
    evaluate_asymptotic_mass_information_trilemma,
    build_report,
    write_report,
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
)


def test_euler_partition_count():
    """Verify exact partition numbers p(n) for small n."""
    known = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]
    for n, expected in enumerate(known):
        assert partition_count_euler(n) == expected


def test_euler_self_conjugate_bijection():
    """Verify Euler's theorem that |SC_n| == |DistinctOdd_n|."""
    res = verify_euler_bijection(12)
    assert res["all_matched"]
    for rec in res["records"]:
        assert rec["matched"]
        assert rec["self_conjugate_count_q_n"] == rec["distinct_odd_count"]


def test_wreath_spectrum_factorization():
    """Verify exact dimension squared sum and Plancherel factorization on W_n."""
    for n in (1, 2, 3, 4):
        res = wreath_product_plancherel_spectrum(n)
        assert res["exact_dimension_sum_verified"]
        assert res["factorization_exact"]
        assert res["factorization_max_residual"] < 1e-14
        expected_order = (2 ** n) * (1 if n == 0 else [1, 1, 2, 6, 24][n])
        assert res["group_order"] == expected_order


def test_sign_swap_self_dual_law():
    """Verify sign-swap self-dual mass formula and asymptotic bounds."""
    law = wreath_sign_swap_self_dual_law(8)
    assert len(law) == 8
    for row in law:
        assert row["bound_satisfied"]
        assert row["sign_swap_self_dual_mass"] > 0
        assert row["sm_collision_probability"] <= row["max_sm_plancherel_weight"] + 1e-14
        if row["m"] >= 2:
            assert row["sign_swap_self_dual_mass"] < law[row["m"] - 2]["sign_swap_self_dual_mass"]


def test_multi_copy_collision_law():
    """Verify multi-copy collision bounds sum [M_n]^k <= [M_max]^{k-1}."""
    law = multi_copy_plancherel_collision_law(8)
    for row in law:
        for k in (2, 3, 4, 5, 6):
            assert row[f"k_{k}_bound_satisfied"]
            assert row[f"k_{k}_collision"] <= row[f"k_{k}_upper_bound"] + 1e-14


def test_empirical_orientation_collapse():
    """Verify empirical orientation channel CMI collapse from S_6 to S_7."""
    res = audit_empirical_orientation_cross_check()
    assert res["spike_is_isolated_finite_resonance"]
    assert abs(res["s6_spike"]["cmi_bits"] - 1.0) < 1e-6
    assert res["s7_typical_haar_collapse"]["cmi_bits"] < 1e-4
    assert res["typical_cmi_collapse_ratio"] < 1e-4
    assert res["weighted_cmi_collapse_ratio"] < 0.005


def test_asymptotic_mass_information_trilemma():
    """Verify universal mass-information trilemma scaling."""
    scaling = evaluate_asymptotic_mass_information_trilemma([4, 8, 16, 32, 64])
    for row in scaling:
        assert not row["advantage_possible"]
        assert row["repeated_6tuple_orbit_mass_bound"] > 0
        assert row["typical_cmi_bits_bound"] > 0
        assert row["total_physical_information_ceiling_bits"] > 0
    # Strict decay
    assert scaling[-1]["total_physical_information_ceiling_bits"] < scaling[0]["total_physical_information_ceiling_bits"]


def test_report_and_registry_integration():
    """Verify report generation, claim gate, and negative results registry update."""
    out_path = write_report(write_registry=True)
    assert out_path.exists()

    report = json.loads(out_path.read_text())
    assert report["status"] == "SELF_DUAL_WREATH_PLANCHEREL_MASS_EXTINCTION_BARRIER_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["asymptotic_quantum_speedup_falsified"] is True

    # Registry check
    registry = json.loads(REGISTRY.read_text())
    entry = next((e for e in registry if e["id"] == NEGATIVE_RESULT_ID), None)
    assert entry is not None
    assert "CODE-EQUIVALENCE-HARD-FAMILY-SEARCH" in entry["applies_to"]
    assert "WREATH-ORIENTATION-PROJECTOR" in entry["applies_to"]
    assert len(entry["lesson"]) > 20
    assert len(entry["reason_invalid"]) > 20
