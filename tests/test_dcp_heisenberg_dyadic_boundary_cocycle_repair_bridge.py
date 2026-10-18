"""Tests for dcp_heisenberg_dyadic_boundary_cocycle_repair_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_heisenberg_dyadic_boundary_cocycle_repair_bridge import (
    generate_dcp_heisenberg_dyadic_boundary_cocycle_repair_certificate,
    verify_cocycle_repair_and_half_period_orthogonality,
)


def test_cocycle_repair_and_half_period_orthogonality() -> None:
    res_odd = verify_cocycle_repair_and_half_period_orthogonality(t_bits=3, s1=5, s2=3, y0=6)
    assert res_odd["exact_cocycle_repair_verified"] is True
    assert abs(res_odd["half_period_msb_x_minus_prob_for_odd_s1"] - 1.0) < 1e-12

    res_even = verify_cocycle_repair_and_half_period_orthogonality(t_bits=3, s1=6, s2=3, y0=5)
    assert res_even["exact_cocycle_repair_verified"] is True


def test_input_validation_rejects_invalid_t() -> None:
    try:
        verify_cocycle_repair_and_half_period_orthogonality(t_bits=1, s1=1, s2=0, y0=0)
        raise AssertionError("Expected ValueError for t_bits=1")
    except ValueError as exc:
        assert "t_bits" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_heisenberg_dyadic_boundary_cocycle_repair_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_heisenberg_dyadic_boundary_cocycle_repair_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_heisenberg_dyadic_boundary_cocycle_repair_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
