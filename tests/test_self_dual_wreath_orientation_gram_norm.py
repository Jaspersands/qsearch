"""Unit tests for Wreath Orientation Projector Gram Norm & Complementary Pairing Duality."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from theorems.self_dual_wreath_orientation_gram_norm import (
    audit_orientation_gram_sector,
    run_orientation_gram_norm_audit,
    write_report,
    REPORT_PATH,
)
from self_dual_wreath_orientation_fusion_moment import _w4_collision_free_labels
from representation_obstruction import integer_partitions


def test_w4_complementary_pairing_orthogonality():
    """Verify that all non-complementary orientation masks are strictly orthogonal: E_a E_b = 0."""
    labels = _w4_collision_free_labels()[0]
    for target in integer_partitions(4):
        record = audit_orientation_gram_sector(target, labels)
        if record is not None:
            assert record.non_complementary_orthogonality_verified is True
            assert record.maximum_non_complementary_overlap_norm < 1e-8


def test_uniform_operator_norm_bound():
    """Verify that the operator norm of F_nu is bounded by 2.0 across all sectors."""
    labels_list = _w4_collision_free_labels()
    for labels in labels_list[:3]:
        for target in integer_partitions(4):
            record = audit_orientation_gram_sector(target, labels)
            if record is not None:
                assert record.operator_norm <= 2.0 + 1e-8
                assert record.minimum_nonzero_eigenvalue >= 0.0


def test_exact_third_moment_conservation_identity():
    """Verify Tr(F^3) == 3 Tr(F^2) - 2 Tr(F) holds with exact zero residual."""
    labels_list = _w4_collision_free_labels()
    for labels in labels_list[:3]:
        for target in integer_partitions(4):
            record = audit_orientation_gram_sector(target, labels)
            if record is not None:
                assert record.third_moment_formula_residual < 1e-12
                # Also check trace ordering with floating point tolerance
                assert record.tr_f1 <= record.tr_f2 + 1e-12
                assert record.tr_f2 <= record.tr_f3 + 1e-12
                assert record.tr_f3 <= record.tr_f4 + 1e-12


def test_subpovm_conclusive_probability_lower_bound():
    """Verify that the whitening-free projector sub-POVM achieves conclusive rate q >= 50%."""
    labels_list = _w4_collision_free_labels()
    for labels in labels_list[:3]:
        for target in integer_partitions(4):
            record = audit_orientation_gram_sector(target, labels)
            if record is not None:
                assert record.subpovm_conclusive_probability_lower_bound >= 0.5 - 1e-8


def test_report_generation_and_negative_result(tmp_path):
    """Verify full report generation, claim gating, and negative result registration."""
    test_path = tmp_path / "test_report.json"
    report = write_report(output_path=test_path, write_registry=False)

    assert test_path.exists()
    assert report["status"] == "wreath-orientation-gram-norm-and-complementary-pairing-proved"
    assert report["claim_gate"]["operator_norm_bound_proved"] is True
    assert report["claim_gate"]["third_moment_identity_proved"] is True
    assert report["claim_gate"]["speedup_claim_allowed"] is False

    registry_path = Path("research/registry/negative_results.json")
    assert registry_path.exists()
    registry = json.loads(registry_path.read_text())
    entry = next(
        (item for item in registry if item.get("id") == "NEG-WREATH-ORIENTATION-SUBPOVM-DECODER-GAP"),
        None,
    )
    assert entry is not None
    assert "CODE-COSET-COLLECTIVE" in entry["applies_to"]
