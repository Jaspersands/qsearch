"""Tests for dcp_multi_packet_product_twirl_sq_dimension_audit."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_multi_packet_product_twirl_sq_dimension_audit import (
    generate_dcp_multi_packet_product_twirl_sq_dimension_certificate,
    verify_cosine_character_orthogonality_and_sq_dimension,
    verify_known_basis_header_constructive_control,
)


def test_cosine_character_orthogonality_and_sq_dimension() -> None:
    res_even = verify_cosine_character_orthogonality_and_sq_dimension(q=4, n=2, gamma=0.5)
    assert res_even["exact_orthogonality_and_chi_square_verified"] is True
    assert res_even["unordered_nonzero_pair_count"] == 9

    res_odd = verify_cosine_character_orthogonality_and_sq_dimension(q=5, n=2, gamma=0.4)
    assert res_odd["exact_orthogonality_and_chi_square_verified"] is True
    assert res_odd["unordered_nonzero_pair_count"] == 12


def test_known_basis_header_constructive_control() -> None:
    ctrl = verify_known_basis_header_constructive_control(q=8, s_vec=[1, 3, 4], gamma=0.5)
    assert ctrl["constructive_basis_readout_exact"] is True


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_multi_packet_product_twirl_sq_dimension_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_multi_packet_product_twirl_sq_dimension_audit.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_multi_packet_product_twirl_sq_dimension_audit_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
