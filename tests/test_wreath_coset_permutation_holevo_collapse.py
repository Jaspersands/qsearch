"""Tests for Wreath Coset Permutation Decoder Gap & Factorial Holevo Information Collapse.

Verifies:
1. Exact Euler partition numbers p(n).
2. Conjugacy class inversion overlap law and purity for S_3, S_4, and S_5.
3. Asymptotic scaling Holevo bounds, Fano success bounds, and copy complexity barriers.
4. Report generation and registry integration.
"""
import json
from pathlib import Path

import pytest

from theorems.wreath_coset_permutation_holevo_collapse import (
    partition_count,
    cycle_type,
    verify_finite_symmetric_group,
    evaluate_scaling_holevo_collapse,
    build_report,
    write_report,
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
)


def test_partition_count_pentagonal():
    """Verify exact partition numbers for small n."""
    known_partitions = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]
    for n, expected in enumerate(known_partitions):
        assert partition_count(n) == expected


def test_cycle_type_computation():
    """Verify cycle type extraction from permutation tuples."""
    assert cycle_type((0, 1, 2)) == (1, 1, 1)
    assert cycle_type((1, 0, 2)) == (2, 1)
    assert cycle_type((1, 2, 0)) == (3,)
    assert cycle_type((1, 0, 3, 2)) == (2, 2)
    assert cycle_type((1, 2, 3, 0)) == (4,)


def test_finite_symmetric_group_s3():
    """Verify exact S_3 representation overlap law and purity."""
    res = verify_finite_symmetric_group(3)
    assert res["group_order"] == 6
    assert res["partition_count"] == 3
    assert res["identity_overlap_exact_one"]
    assert abs(res["purity_float"] - 1.0 / 6) < 1e-12
    assert abs(res["average_1copy_overlap_float"] - 0.5) < 1e-12
    assert res["exact_class_overlap_law_satisfied"]


def test_finite_symmetric_group_s4():
    """Verify exact S_4 representation overlap law and purity."""
    res = verify_finite_symmetric_group(4)
    assert res["group_order"] == 24
    assert res["partition_count"] == 5
    assert res["identity_overlap_exact_one"]
    assert abs(res["purity_float"] - 1.0 / 24) < 1e-12
    assert abs(res["average_1copy_overlap_float"] - 5.0 / 24) < 1e-12
    assert res["exact_class_overlap_law_satisfied"]


def test_finite_symmetric_group_s5():
    """Verify exact S_5 representation overlap law and purity."""
    res = verify_finite_symmetric_group(5)
    assert res["group_order"] == 120
    assert res["partition_count"] == 7
    assert res["identity_overlap_exact_one"]
    assert abs(res["purity_float"] - 1.0 / 120) < 1e-12
    assert abs(res["average_1copy_overlap_float"] - 7.0 / 120) < 1e-12
    assert res["exact_class_overlap_law_satisfied"]


def test_scaling_holevo_profiles():
    """Verify asymptotic Holevo capacity collapse and Fano bound across dimensions."""
    dims = [3, 4, 6, 8, 16, 32, 64]
    for n in dims:
        p = evaluate_scaling_holevo_collapse(n, k=4)
        assert p["dimension_n"] == n
        assert p["secret_entropy_bits"] > 0
        assert p["holevo_mutual_information_upper_bound_bits"] <= 16.0 / n + 1e-8
        assert p["copy_barrier_confirmed"]

        if n >= 6:
            assert p["fano_identification_success_upper_bound"] < 0.5
        if n >= 16:
            assert p["fano_identification_success_upper_bound"] < 0.05
        if n >= 32:
            assert p["average_kcopy_overlap_float"] < 1e-30


def test_report_building_and_integrity():
    """Verify that the generated report meets all theorem requirements."""
    report = build_report()
    assert report["status"] == "WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE_PROVED"
    assert report["speedup_claim_allowed"] is False
    assert report["accepted_speedup_candidate"] is False
    assert len(report["theorems_proved"]) == 5
    assert all(t["verified"] for t in report["theorems_proved"])
    assert len(report["finite_instance_verifications"]) == 3
    assert len(report["scaling_profiles"]) == 8


def test_registry_integration():
    """Verify negative result registration in negative_results.json."""
    write_report(write_registry=True)
    assert REPORT.exists()
    assert REGISTRY.exists()

    data = json.loads(REGISTRY.read_text())
    entry = next((e for e in data if e.get("id") == NEGATIVE_RESULT_ID), None)
    assert entry is not None
    assert entry["id"] == NEGATIVE_RESULT_ID
    assert "CODE-EQUIVALENCE" in entry["applies_to"]
    assert "WREATH-PRODUCT-HSP" in entry["applies_to"]
    assert entry["source"] == "research/representation/wreath_coset_permutation_holevo_collapse.json"
