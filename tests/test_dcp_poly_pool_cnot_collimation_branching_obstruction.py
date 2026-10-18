"""Tests for dcp_poly_pool_cnot_collimation_branching_obstruction."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from theorems.dcp_poly_pool_cnot_collimation_branching_obstruction import (
    DEFAULT_ARTIFACT_PATH,
    build_dcp_poly_pool_cnot_collimation_branching_obstruction_report,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_cnot_branching_law_and_subtraction_halving() -> None:
    report = build_dcp_poly_pool_cnot_collimation_branching_obstruction_report()
    assert report["summary"]["theorem1_cnot_branching_passed"] is True
    assert report["summary"]["max_branch_probability_error"] <= 1e-12
    assert report["summary"]["max_conditional_state_error"] <= 1e-12
    for inst in report["instances"]:
        ca = inst["cnot_branching_audit"]
        assert ca["theorem1_passed"] is True
        assert ca["total_triples_checked"] == inst["q"] ** (3 * inst["n"])
        assert (
            ca["non_2_torsion_same_bucket_residues"]
            == ca["z1_only_cancels_residues"]
        )


def test_theorem2_bucket_occupancy_disjoint_pairing_bound() -> None:
    report = build_dcp_poly_pool_cnot_collimation_branching_obstruction_report()
    assert report["summary"]["theorem2_bucket_occupancy_pairing_passed"] is True
    for inst in report["instances"]:
        ba = inst["bucket_pairing_audit"]
        assert ba["theorem2_passed"] is True
        assert (
            ba["parity_identity_verified_assignments"]
            == ba["total_bucket_assignments"]
        )
        assert ba["max_disjoint_pairs_observed"] == inst["M_pool"] // 2
        assert Fraction(ba["expected_subtraction_children_exact"]) == Fraction(
            1, 2
        ) * Fraction(ba["expected_disjoint_pairs_exact"])
        assert Fraction(ba["expected_subtraction_children_exact"]) <= Fraction(
            inst["M_pool"], 4
        )


def test_theorem3_superpolynomial_depth_and_sample_barrier() -> None:
    report = build_dcp_poly_pool_cnot_collimation_branching_obstruction_report()
    assert report["summary"]["theorem3_superpolynomial_depth_barrier_passed"] is True
    for row in report["asymptotic_scaling"]:
        assert row["theorem3_passed"] is True
        assert (
            row["poly_pool_initial_preparations_log2_lower"]
            == 2 * row["minimum_tree_depth_L"]
        )


def test_artifact_and_honesty_guardrails() -> None:
    report = build_dcp_poly_pool_cnot_collimation_branching_obstruction_report()
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
                / "dcp_poly_pool_cnot_collimation_branching_obstruction.py"
            ),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True
