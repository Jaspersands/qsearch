"""Tests for theorems/arbitrary_h_recursive_oracle_and_resource_audit.py (Milestone 24)."""
from __future__ import annotations

from itertools import product
import json
import pytest

from theorems.arbitrary_h_recursive_oracle_and_resource_audit import (
    JSON_PATH,
    MD_PATH,
    audit_arbitrary_h_recursive_resource_and_tree_budget,
    build_arbitrary_h_recursive_oracle_and_resource_report,
    clean_oracle_step,
    render_markdown,
    solve_arbitrary_h_from_black_box_oracle,
    verify_representative_cleanup_vs_leaked_workspace,
)
from theorems.jet_oracle_homogenization import lie_bch
from theorems.right_abelian_induced_source import upper_triangular_lie
from theorems.ut5_matrix_phase_alignment import _identity


def test_representative_cleanup_vs_leaked_workspace() -> None:
    res = verify_representative_cleanup_vs_leaked_workspace(p=5)
    assert res["quotient_size_Q"] == 25
    assert res["section_labels_equal_across_distinct_sections"] is True
    assert res["cleaned_kernel_vs_target_frobenius_error"] == 0.0
    assert res["leaked_kernel_off_diagonal_frobenius_norm"] == 0.0
    assert res["leaked_kernel_vs_maximally_mixed_frobenius_error"] == 0.0
    assert res["leaked_kernel_vs_target_frobenius_error"] > 0.3


def test_clean_oracle_step_verifies_zero_residual_workspace() -> None:
    q_out, ws, label = clean_oracle_step(
        (2, 3),
        lambda q: (q[0], (q[0] + q[1]) % 5, q[1]),
        lambda w: ((w[0] + 1) % 5, w[2]),
        3,
        5,
    )
    assert q_out == (2, 3)
    assert ws == (0, 0, 0)
    assert label == (3, 3)


def test_advice_free_black_box_oracle_recovery_on_ut4() -> None:
    p = 5
    ut4, slots4 = upper_triangular_lie(4, p)
    std4 = _identity(len(slots4))
    e01 = tuple(std4[slots4.index((0, 1))])
    e02 = tuple(std4[slots4.index((0, 2))])
    h_elements = [
        tuple((c0 * e01[k] + c1 * e02[k]) % p for k in range(ut4.dimension))
        for c0, c1 in product(range(p), repeat=2)
    ]

    def black_box_oracle(log_g: tuple[int, ...]) -> tuple[int, ...]:
        return min(lie_bch(ut4, log_g, h_el, 3) for h_el in h_elements)

    trace = solve_arbitrary_h_from_black_box_oracle(ut4, std4, black_box_oracle)
    assert trace.status == "SUCCESS"
    assert trace.workspace_cleanup_failures == 0
    assert trace.rebuilt_tuple_oracle_steps == 1
    assert trace.abelian_base_steps == 2
    assert trace.max_nested_section_depth == 2
    assert list(trace.recovered_generators) == [e01, e02]


def test_arbitrary_h_recursive_resource_and_tree_budget() -> None:
    res = audit_arbitrary_h_recursive_resource_and_tree_budget()
    profs = res["recursion_profiles_by_prime"]
    assert len(profs) == 2
    assert profs[0]["sequential_image_steps"] == 5
    assert profs[0]["total_additive_recursion_queries_ceil_log2_bound"] == profs[0]["max_single_step_queries_ceil_log2"] + 3
    tb = res["sample_three_stage_tree_budget"]
    assert tb["source_leaves"] == 240
    assert tb["stage_calls"] == [24, 4, 1]
    assert tb["total_instrument_calls"] == 269


def test_written_artifacts_match_report_schema() -> None:
    report = build_arbitrary_h_recursive_oracle_and_resource_report()
    assert report["schema_version"] == "arbitrary_h_recursive_oracle_and_resource_audit_v1"
    assert report["scope"]["target_h_advice_passed_to_solver"] is False
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Arbitrary-$H$ Black-Box Oracle Pullback" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "arbitrary_h_recursive_oracle_and_resource_audit_v1"
    if MD_PATH.exists():
        assert "accepted_speedup_candidate" in MD_PATH.read_text(encoding="utf-8")
