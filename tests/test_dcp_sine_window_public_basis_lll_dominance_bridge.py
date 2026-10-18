"""Tests for dcp_sine_window_public_basis_lll_dominance_bridge."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from theorems.dcp_sine_window_public_basis_lll_dominance_bridge import (
    DEFAULT_ARTIFACT_PATH,
    build_dcp_sine_window_public_basis_lll_dominance_bridge_report,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_clean_budget_gap_lower_bound_and_lll_window() -> None:
    report = build_dcp_sine_window_public_basis_lll_dominance_bridge_report()
    assert report["summary"]["theorem1_gap_lower_bound_passed"] is True
    for inst in report["instances"]:
        ga = inst["gap_audit"]
        assert ga["theorem1_passed"] is True
        assert ga["within_lll_guaranteed_uniqueness_window"] is True
        assert Fraction(ga["required_gap_sq_actual"], 1) > Fraction(
            ga["strict_radius_sq_exact"]
        )
        assert Fraction(ga["strict_radius_sq_exact"]) >= Fraction(
            ga["algebraic_gap_sq_lower_bound_exact"]
        )


def test_theorem2_outer_trial_preparation_and_qubit_overhead() -> None:
    report = build_dcp_sine_window_public_basis_lll_dominance_bridge_report()
    assert report["summary"]["theorem2_outer_trial_overhead_passed"] is True
    for inst in report["instances"]:
        oa = inst["overhead_audit"]
        assert oa["theorem2_passed"] is True
        assert oa["outer_coordinate_residue_trials"] == inst["dimension"] * (
            oa["splitting_prime_p"] - 1
        )
        assert (
            oa["single_sweep_quantum_preparations"]
            >= oa["min_sweep_preparations_bound"]
        )
        assert oa["w_calls_per_prep"] == 3 * inst["dimension"]


def test_theorem3_public_basis_lll_recovery_zero_preparations() -> None:
    report = build_dcp_sine_window_public_basis_lll_dominance_bridge_report()
    assert report["summary"]["theorem3_public_lll_recovery_passed"] is True
    assert report["summary"]["classical_lll_quantum_preparations"] == 0
    for inst in report["instances"]:
        ca = inst["classical_lll_audit"]
        assert ca["theorem3_passed"] is True
        assert ca["in_public_lattice"] is True
        assert ca["is_primitive"] is True
        assert ca["quantum_preparations_used"] == 0
        lo, hi = inst["norm_sq_interval"]
        assert lo <= ca["recovered_norm_squared"] <= hi


def test_artifact_and_honesty_guardrails() -> None:
    report = build_dcp_sine_window_public_basis_lll_dominance_bridge_report()
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
                / "dcp_sine_window_public_basis_lll_dominance_bridge.py"
            ),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True
