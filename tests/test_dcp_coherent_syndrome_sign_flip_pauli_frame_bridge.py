"""Tests for dcp_coherent_syndrome_sign_flip_pauli_frame_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_coherent_syndrome_sign_flip_pauli_frame_bridge import (
    evaluate_mod8_sign_rectified_cnot_pairing,
    generate_dcp_coherent_syndrome_sign_flip_pauli_frame_certificate,
    verify_pauli_x_density_negation_identity,
)


def test_pauli_x_density_negation_and_mod8_rectification() -> None:
    neg = verify_pauli_x_density_negation_identity([0.1, 1.2], [0.8, 1.0])
    assert neg["exact_pauli_x_negation_verified"] is True

    rect = evaluate_mod8_sign_rectified_cnot_pairing(t_bits=3, s_secret=3, gamma_1=0.85, gamma_2=0.75)
    assert rect["exact_rectification_verified"] is True
    assert abs(rect["pauli_x_rectified_d0_mod8_zero_fraction"] - 1.0) < 1e-12


def test_input_validation_rejects_small_t() -> None:
    try:
        evaluate_mod8_sign_rectified_cnot_pairing(t_bits=2, s_secret=1, gamma_1=0.8, gamma_2=0.8)
        raise AssertionError("Expected ValueError for t_bits=2")
    except ValueError as exc:
        assert "t_bits >= 3" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_coherent_syndrome_sign_flip_pauli_frame_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_coherent_syndrome_sign_flip_pauli_frame_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_coherent_syndrome_sign_flip_pauli_frame_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
