"""Tests for dcp_tensor_power_k_moment_dihedral_twirl_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_tensor_power_k_moment_dihedral_twirl_bridge import (
    generate_dcp_tensor_power_k_moment_dihedral_twirl_certificate,
    verify_ensemble_mean_frobenius_identity,
    verify_single_instance_twirl_and_ternary_enumerator,
)


def test_single_instance_and_ensemble_ternary_twirl_laws() -> None:
    c_free = verify_single_instance_twirl_and_ternary_enumerator(
        a_cols=[[1], [3]], q_mod=8, gammas=[0.85, 0.75]
    )
    assert c_free["exact_ternary_twirl_law_verified"] is True
    assert abs(c_free["frob_sq_explicit_twirl"] - 0.0) < 1e-12

    ens = verify_ensemble_mean_frobenius_identity(q_mod=4, n_rows=1, gammas=[0.8, 0.7, 0.6])
    assert ens["exact_ensemble_identity_verified"] is True


def test_input_validation_rejects_invalid_q() -> None:
    try:
        verify_single_instance_twirl_and_ternary_enumerator([[1]], q_mod=1, gammas=[0.8])
        raise AssertionError("Expected ValueError for q_mod=1")
    except ValueError as exc:
        assert "q_mod >= 2" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_tensor_power_k_moment_dihedral_twirl_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_tensor_power_k_moment_dihedral_twirl_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_tensor_power_k_moment_dihedral_twirl_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
