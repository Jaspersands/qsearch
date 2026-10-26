"""Tests for theorems/composed_full_jet_erasure_and_section_pullback_audit.py (Milestone 21)."""
from __future__ import annotations

import json
import pytest

from theorems.composed_full_jet_erasure_and_section_pullback_audit import (
    JSON_PATH,
    MD_PATH,
    audit_adaptive_recursion_resource_composition,
    build_composed_full_jet_erasure_and_section_pullback_report,
    render_markdown,
    verify_composed_degree_reduced_branch_and_terminal_kernel,
    verify_non_homomorphic_section_pullback_invariance,
    verify_twisted_section_character_covariance,
)


def test_composed_degree_reduced_branch_and_terminal_kernel() -> None:
    res = verify_composed_degree_reduced_branch_and_terminal_kernel(p=5, degree=2)
    assert res["hilbert_dim_V_times_J"] == 625
    assert res["degree_reduced_branch_frobenius_error"] < 1e-14
    assert res["merged_weighted_degree_after_stage2"] == 1
    assert res["terminal_weighted_degree_after_stage1"] == 0
    assert res["terminal_constant_residual_value_mod_p"] != 0
    assert res["terminal_kernel_unit_character_frobenius_error"] < 1e-14
    assert res["terminal_kernel_nonunit_character_frobenius_error"] > 0.1


def test_non_homomorphic_section_pullback_invariance_and_false_k_failure() -> None:
    res = verify_non_homomorphic_section_pullback_invariance(p=11)
    assert res["non_homomorphic_section_pairs_out_of_25"] > 20
    assert res["valid_k_in_h_right_invariance_checks"] == 30
    assert res["violated_k_not_in_h_mismatches_out_of_30"] > 20


def test_twisted_section_character_covariance_and_mislearned_failure() -> None:
    res = verify_twisted_section_character_covariance(p=11)
    assert res["valid_character_covariance_trials"] == 25
    assert res["mislearned_character_mismatches_out_of_25"] == 25


def test_adaptive_recursion_resource_composition_ledger() -> None:
    res = audit_adaptive_recursion_resource_composition(p=19)
    assert len(res["per_step_tree_budgets"]) == 3
    assert (
        res["additive_across_steps_log2_queries_bound"]
        < res["forbid_across_step_product_log2_queries"]
    )
    assert res["total_reversible_lift_overhead_gates_per_b0_batch"] > 0


def test_written_artifacts_match_report_schema() -> None:
    report = build_composed_full_jet_erasure_and_section_pullback_report()
    assert report["schema_version"] == "composed_full_jet_erasure_and_section_pullback_audit_v1"
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Composed Full-Jet Erasure" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "composed_full_jet_erasure_and_section_pullback_audit_v1"
    if MD_PATH.exists():
        assert "accepted_speedup_candidate" in MD_PATH.read_text(encoding="utf-8")
