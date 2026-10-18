"""Tests for dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_bridge import (
    generate_dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_certificate,
    verify_banded_qft_product_law_and_sublattice_criterion,
)


def test_banded_qft_product_law_and_sublattice_criterion() -> None:
    for b in (1, 2, 3, 4):
        res = verify_banded_qft_product_law_and_sublattice_criterion(m_wires=4, band_b=b)
        assert res["exact_product_and_sublattice_iff_verified"] is True


def test_input_validation_rejects_invalid_band() -> None:
    try:
        verify_banded_qft_product_law_and_sublattice_criterion(m_wires=4, band_b=0)
        raise AssertionError("Expected ValueError for band_b=0")
    except ValueError as exc:
        assert "band_b" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
