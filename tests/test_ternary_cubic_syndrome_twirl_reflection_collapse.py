"""Tests for ternary_cubic_syndrome_twirl_reflection_collapse."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from theorems.ternary_cubic_syndrome_twirl_reflection_collapse import (
    DEFAULT_ARTIFACT_PATH,
    build_ternary_cubic_syndrome_twirl_reflection_collapse_report,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_arbitrary_function_block_convolution_equivalence() -> None:
    report = build_ternary_cubic_syndrome_twirl_reflection_collapse_report()
    assert report["summary"]["theorem1_block_convolution_passed"] is True
    assert report["summary"]["max_statevector_vs_classical_error"] <= 1e-12
    for inst in report["instances"]:
        ba = inst["block_convolution_audit"]
        assert ba["theorem1_passed"] is True
        assert ba["max_statevector_vs_classical_error"] <= 1e-12


def test_theorem2_fermat_cubic_reduction_and_single_point_pinching() -> None:
    report = build_ternary_cubic_syndrome_twirl_reflection_collapse_report()
    assert report["summary"]["theorem2_fermat_single_point_pinching_passed"] is True
    for inst in report["instances"]:
        ta = inst["twirl_pinching_audit"]
        assert ta["theorem2_passed"] is True
        assert ta["fermat_identity_verified_residues"] == 3
        assert ta["distinct_mixed_cubic_vectors"] == inst["N"]
        assert (
            ta["distinct_homogeneous_quadratic_vectors"]
            == 1 + (inst["N"] - 1) // 2
        )
        assert ta["all_v_match_pinched_formula"] is True
        assert Fraction(ta["common_pinched_point_mass_exact"]) == Fraction(
            1, inst["N"]
        )
        assert Fraction(ta["common_pinched_point_mass_exact"]) < Fraction(
            ta["quadratic_reflection_bound_2_over_N_exact"]
        )


def test_theorem3_full_syndrome_source_average_decay() -> None:
    report = build_ternary_cubic_syndrome_twirl_reflection_collapse_report()
    assert report["summary"]["theorem3_source_average_decay_passed"] is True
    for row in report["asymptotic_scaling"]:
        assert row["multi_trial_upper_bound_power_of_two_neg_exponent"] >= 15


def test_artifact_and_honesty_guardrails() -> None:
    report = build_ternary_cubic_syndrome_twirl_reflection_collapse_report()
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
                / "ternary_cubic_syndrome_twirl_reflection_collapse.py"
            ),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True
