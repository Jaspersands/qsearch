"""Tests for planted_qary_macwilliams_dual_weight_enumerator_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.planted_qary_macwilliams_dual_weight_enumerator_bridge import (
    generate_planted_qary_macwilliams_dual_weight_enumerator_certificate,
    rowspace_and_dual_weight_enumerators,
    verify_noisy_qft_valid_check_macwilliams_bridge,
    verify_secret_syndrome_controls,
)


def test_qary_macwilliams_identity() -> None:
    res = rowspace_and_dual_weight_enumerators([[1, 0, 1, 2], [0, 1, 1, 1]], q=3)
    assert res["macwilliams_identity_exact"] is True


def test_noisy_qft_valid_check_bridge() -> None:
    res = verify_noisy_qft_valid_check_macwilliams_bridge([[1, 0, 1, 2], [0, 1, 1, 1]], q=3, gamma=0.25)
    assert res["bridge_identity_exact"] is True


def test_secret_syndrome_controls() -> None:
    ctrl = verify_secret_syndrome_controls(
        b_matrix=[[1, 0, 1, 2], [0, 1, 1, 1]],
        q=3,
        s_off_dual=[1, 0, 0, 0],
        s_on_dual=[2, 2, 1, 0],
    )
    assert ctrl["off_dual_exact_one_over_q"] is True
    assert ctrl["on_dual_constructive_alignment_unit"] is True


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_planted_qary_macwilliams_dual_weight_enumerator_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "planted_qary_macwilliams_dual_weight_enumerator_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "planted_qary_macwilliams_dual_weight_enumerator_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
