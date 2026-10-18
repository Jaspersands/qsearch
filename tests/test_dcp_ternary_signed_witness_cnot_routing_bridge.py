"""Tests for dcp_ternary_signed_witness_cnot_routing_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_ternary_signed_witness_cnot_routing_bridge import (
    evaluate_binary_vs_ternary_zero_sum_witnesses,
    generate_dcp_ternary_signed_witness_cnot_routing_certificate,
)


def test_binary_empty_vs_ternary_rich_witnesses() -> None:
    res = evaluate_binary_vs_ternary_zero_sum_witnesses([[1, 1, 1]], q_mod=5)
    assert res["cnot_syndrome_bijection_verified"] is True
    assert res["binary_zero_sum_witness_count"] == 0
    assert res["oriented_ternary_zero_sum_witness_count"] == 3


def test_input_validation_rejects_invalid_q() -> None:
    try:
        evaluate_binary_vs_ternary_zero_sum_witnesses([[1, 1]], q_mod=1)
        raise AssertionError("Expected ValueError for q_mod=1")
    except ValueError as exc:
        assert "q_mod" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_ternary_signed_witness_cnot_routing_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_ternary_signed_witness_cnot_routing_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_ternary_signed_witness_cnot_routing_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
