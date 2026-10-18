"""Tests for dcp_sine_vs_box_window_pair_difference_overlap_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_sine_vs_box_window_pair_difference_overlap_bridge import (
    generate_dcp_sine_vs_box_window_pair_difference_overlap_certificate,
    verify_sine_vs_box_autocorrelation_and_crossover,
)


def test_sine_vs_box_autocorrelation_and_crossover() -> None:
    res = verify_sine_vs_box_autocorrelation_and_crossover(p_window=32)
    assert res["exact_identities_and_crossover_verified"] is True
    assert res["delta_1_loss_reduction_ratio_box_over_sine"] > 6.0


def test_input_validation_rejects_small_p() -> None:
    try:
        verify_sine_vs_box_autocorrelation_and_crossover(p_window=2)
        raise AssertionError("Expected ValueError for p_window=2")
    except ValueError as exc:
        assert "p_window >= 4" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_sine_vs_box_window_pair_difference_overlap_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_sine_vs_box_window_pair_difference_overlap_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_sine_vs_box_window_pair_difference_overlap_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
