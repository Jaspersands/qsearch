"""Tests for dcp_disjoint_tree_wire_capacity_tradeoff_obstruction."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from theorems.dcp_disjoint_tree_wire_capacity_tradeoff_obstruction import (
    DEFAULT_ARTIFACT_PATH,
    build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_disjoint_block_wire_capacity_inequality() -> None:
    report = build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report()
    assert report["summary"]["theorem1_wire_capacity_passed"] is True
    for inst in report["instances"]:
        assert inst["theorem1_wire_capacity_passed"] is True
        for rec in inst["depth_sweep"]:
            assert rec["m_leaf_min"] >= rec["b_bits_per_level"] + 1
            assert rec["K_wires_min"] == rec["k_leaves"] * rec["m_leaf_min"]


def test_theorem2_polynomial_wire_depth_ceiling_and_oblivious_bound() -> None:
    report = build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report()
    assert report["summary"]["theorem2_depth_ceiling_passed"] is True
    for inst in report["instances"]:
        assert inst["theorem2_depth_ceiling_passed"] is True
        assert inst["max_feasible_depth_a"] <= inst["log2_K_floor"]
        assert (
            inst["min_feasible_oblivious_record_exponent"]
            >= inst["theoretical_wire_constrained_oblivious_lower_exponent"]
        )
        assert (
            inst["min_feasible_cartesian_record_exponent"]
            > inst["min_feasible_oblivious_record_exponent"]
        )


def test_theorem3_unconstrained_am_gm_joint_list_width_frontier() -> None:
    report = build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report()
    assert report["summary"]["theorem3_am_gm_frontier_passed"] is True
    for inst in report["instances"]:
        assert inst["theorem3_am_gm_frontier_passed"] is True
        opt = inst["unconstrained_am_gm_optimum"]
        assert (
            opt["optimal_oblivious_record_exponent"]
            == opt["am_gm_lower_bound_exponent"]
        )
        for rec in inst["depth_sweep"]:
            assert (
                rec["oblivious_join_record_exponent"]
                >= opt["am_gm_lower_bound_exponent"]
            )


def test_artifact_and_honesty_guardrails() -> None:
    report = build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report()
    assert report["summary"]["all_theorems_passed"] is True
    hg = report["honesty_guardrails"]
    assert hg["accepted_speedup_candidate"] is False
    assert hg["new_active_negative_result_created"] is False
    assert hg["novelty_claim"] is False
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["sha256"] == report["sha256"]


def test_cli_execution() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(
                ROOT
                / "theorems"
                / "dcp_disjoint_tree_wire_capacity_tradeoff_obstruction.py"
            ),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True
