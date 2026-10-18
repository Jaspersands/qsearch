"""Tests for dcp_product_sine_source_coordinate_marginal_obstruction."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from theorems.dcp_product_sine_source_coordinate_marginal_obstruction import (
    DEFAULT_ARTIFACT_PATH,
    build_dcp_product_sine_source_coordinate_marginal_obstruction_report,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_single_coordinate_marginal_dephasing() -> None:
    report = build_dcp_product_sine_source_coordinate_marginal_obstruction_report()
    assert report["summary"]["theorem1_marginal_dephasing_passed"] is True
    assert report["summary"]["max_marginal_formula_error"] <= 1e-12
    for inst in report["instances"]:
        ma = inst["marginal_audit"]
        assert ma["theorem1_passed"] is True
        assert ma["zero_aux_shift_count"] == inst["q"]
        assert ma["nonzero_aux_shift_count"] == (inst["q"] ** inst["n"] - inst["q"])
        assert ma["max_nonzero_aux_trace_distance_from_maximally_mixed"] <= 1e-12


def test_theorem2_k_copy_parity_density_and_threshold_invariance() -> None:
    report = build_dcp_product_sine_source_coordinate_marginal_obstruction_report()
    assert report["summary"]["theorem2_k_copy_threshold_invariance_passed"] is True
    assert report["summary"]["max_k_copy_density_difference_error"] <= 1e-12
    for inst in report["instances"]:
        ka = inst["k_copy_parity_audit"]
        assert ka["theorem2_passed"] is True
        assert ka["cyclic_k_min_for_adv_1_16"] == ka["product_k_min_for_adv_1_16"]
        assert (
            ka["full_vector_target_ordered_pairs"]
            + ka["killed_by_auxiliary_averaging_pairs"]
            == ka["coord1_only_target_ordered_pairs"]
        )


def test_theorem3_auxiliary_zero_postselection_sample_blowup() -> None:
    report = build_dcp_product_sine_source_coordinate_marginal_obstruction_report()
    assert report["summary"]["theorem3_postselection_blowup_passed"] is True
    for inst in report["instances"]:
        pa = inst["postselection_audit"]
        assert pa["theorem3_passed"] is True
        assert pa["aux_zero_accepted_outcomes"] == inst["q"]
        assert Fraction(pa["acceptance_probability_exact"]) == Fraction(
            1, inst["q"] ** (inst["n"] - 1)
        )


def test_asymptotic_scaling_and_honesty_guardrails() -> None:
    report = build_dcp_product_sine_source_coordinate_marginal_obstruction_report()
    assert report["summary"]["all_theorems_passed"] is True
    for row in report["asymptotic_scaling"]:
        assert row["cyclic_equals_product_minimum_copies"] is True
        assert row["product_qft_controlled_phases"] < row["cyclic_qft_controlled_phases"]
        assert row["aux_zero_postselection_acceptance_neg_log2"] == (
            row["n"] - 1
        ) * row["coordinate_bits_L"]
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
                / "dcp_product_sine_source_coordinate_marginal_obstruction.py"
            ),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True
