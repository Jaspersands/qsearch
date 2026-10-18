"""Tests for dcp_prefix_peeling_error_propagation_union_bridge."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from theorems.dcp_prefix_peeling_error_propagation_union_bridge import (
    DEFAULT_ARTIFACT_PATH,
    build_dcp_prefix_peeling_error_propagation_union_bridge_report,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_correct_prefix_phase_reduction_and_uniformity() -> None:
    report = build_dcp_prefix_peeling_error_propagation_union_bridge_report()
    assert report["summary"]["theorem1_correct_prefix_reduction_passed"] is True
    assert report["summary"]["max_correct_prefix_state_error"] <= 1e-12
    for inst in report["instances"]:
        pa = inst["peeling_channel_audit"]
        assert pa["theorem1_passed"] is True
        assert pa["truncation_uniform"] is True
        assert pa["truncation_fiber_multiplicity"] == inst["q_prefix"]
        assert pa["correct_prefix_pairs_checked"] == inst["q"]


def test_theorem2_incorrect_prefix_character_depolarization() -> None:
    report = build_dcp_prefix_peeling_error_propagation_union_bridge_report()
    assert report["summary"]["theorem2_wrong_prefix_depolarization_passed"] is True
    assert report["summary"]["max_wrong_prefix_depolarized_error"] <= 1e-12
    for inst in report["instances"]:
        pa = inst["peeling_channel_audit"]
        assert pa["theorem2_passed"] is True
        assert pa["wrong_prefix_pairs_checked"] == inst["q"] * (
            inst["q_prefix"] - 1
        )
        assert pa["max_wrong_prefix_depolarized_error"] <= 1e-12


def test_theorem3_binomial_majority_tail_and_verifier_orthogonality() -> None:
    report = build_dcp_prefix_peeling_error_propagation_union_bridge_report()
    assert report["summary"]["theorem3_majority_and_verifier_passed"] is True
    assert report["summary"]["max_verifier_single_shot_prob_error"] <= 1e-12
    for inst in report["instances"]:
        mv = inst["majority_and_verifier_audit"]
        assert mv["theorem3_passed"] is True
        assert mv["majority_error_float"] <= mv["bhattacharyya_upper_bound"] + 1e-12
        assert mv["bhattacharyya_upper_bound"] <= mv["hoeffding_upper_bound"] + 1e-12
        assert mv["true_candidate_pairs_checked"] == inst["q"]
        assert mv["false_candidate_pairs_checked"] == inst["q"] * (inst["q"] - 1)
        assert Fraction(mv["false_candidate_L_shot_survival_exact"]) == Fraction(
            1, 1 << inst["L_verifier"]
        )


def test_artifact_and_honesty_guardrails() -> None:
    report = build_dcp_prefix_peeling_error_propagation_union_bridge_report()
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
                / "dcp_prefix_peeling_error_propagation_union_bridge.py"
            ),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True
