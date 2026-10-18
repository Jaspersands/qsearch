"""Tests for dcp_coherent_fiber_support_erasure_inversion_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_coherent_fiber_support_erasure_inversion_bridge import (
    evaluate_pointer_dephasing_and_fiber_erasure_regimes,
    generate_dcp_coherent_fiber_support_erasure_inversion_certificate,
)


def test_pointer_dephasing_and_fiber_erasure_regimes() -> None:
    res = evaluate_pointer_dephasing_and_fiber_erasure_regimes(
        a_matrix=[[1, 1, 2, 2]],
        q_mod=4,
        s_test_1=[1],
        s_test_2=[3],
    )
    assert res["hierarchy_and_collision_free_iff_verified"] is True
    assert res["unerased_pointer_strictly_secret_blind"] is True
    assert abs(res["single_rep_unconditional_recovery_prob"] - 0.25) < 1e-12


def test_input_validation_rejects_invalid_q() -> None:
    try:
        evaluate_pointer_dephasing_and_fiber_erasure_regimes([[1]], q_mod=1, s_test_1=[0], s_test_2=[0])
        raise AssertionError("Expected ValueError for q_mod=1")
    except ValueError as exc:
        assert "q_mod >= 2" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_coherent_fiber_support_erasure_inversion_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_coherent_fiber_support_erasure_inversion_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_coherent_fiber_support_erasure_inversion_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
