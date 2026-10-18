"""Tests for dcp_cnot_conjugated_schur_weyl_clifford_twirl_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_cnot_conjugated_schur_weyl_clifford_twirl_bridge import (
    generate_dcp_cnot_conjugated_schur_weyl_clifford_twirl_certificate,
    verify_complement_weight_shift_and_degree_r_exclusion,
    verify_r3_cnot_conjugated_sym_closed_form_and_ghz_escape,
)


def test_complement_weight_shift_and_degree_r_exclusion() -> None:
    for r in (2, 3, 4, 5):
        res = verify_complement_weight_shift_and_degree_r_exclusion(r_copies=r)
        assert res["complement_weight_shift_plus_minus_1_verified"] is True
        assert res["degree_r_harmonic_strictly_excluded"] is True
        if (r % 2) == 1:
            assert res["odd_r_strictly_even_harmonics"] is True


def test_r3_cnot_conjugated_sym_closed_form() -> None:
    res = verify_r3_cnot_conjugated_sym_closed_form_and_ghz_escape(
        thetas=[0.35, 1.15, 2.25],
        gammas=[0.9, 0.8, 0.7],
    )
    assert res["exact_two_body_law_verified"] is True
    assert res["formula_error"] < 1e-12


def test_input_validation_rejects_invalid_r() -> None:
    try:
        verify_complement_weight_shift_and_degree_r_exclusion(r_copies=1)
        raise AssertionError("Expected ValueError for r_copies=1")
    except ValueError as exc:
        assert "r_copies" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_cnot_conjugated_schur_weyl_clifford_twirl_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_cnot_conjugated_schur_weyl_clifford_twirl_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_cnot_conjugated_schur_weyl_clifford_twirl_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
