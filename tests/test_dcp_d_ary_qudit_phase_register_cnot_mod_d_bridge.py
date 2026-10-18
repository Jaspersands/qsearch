"""Tests for dcp_d_ary_qudit_phase_register_cnot_mod_d_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_d_ary_qudit_phase_register_cnot_mod_d_bridge import (
    generate_dcp_d_ary_qudit_phase_register_cnot_mod_d_certificate,
    verify_d_ary_qudit_sum_carry_and_linearity_criterion,
)


def test_d_ary_qudit_sum_carry_and_linearity_criterion() -> None:
    res_qutrit = verify_d_ary_qudit_sum_carry_and_linearity_criterion(
        a_matrix=[[1, 2]],
        v_vec=[1, 1],
        d_radix=3,
        t_exp=2,
    )
    assert res_qutrit["linearity_characterization_verified"] is True
    assert res_qutrit["universal_mod_d_descent_verified"] is True
    assert abs(res_qutrit["linear_anchor_fraction"] - (1.0 / 3.0)) < 1e-12


def test_input_validation_rejects_invalid_radix() -> None:
    try:
        verify_d_ary_qudit_sum_carry_and_linearity_criterion([[1, 1]], [1, 1], d_radix=1, t_exp=2)
        raise AssertionError("Expected ValueError for d_radix=1")
    except ValueError as exc:
        assert "d_radix >= 2" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_d_ary_qudit_phase_register_cnot_mod_d_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_d_ary_qudit_phase_register_cnot_mod_d_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_d_ary_qudit_phase_register_cnot_mod_d_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
