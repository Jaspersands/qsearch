"""Tests for dcp_coset_subspace_qft_concentration_and_leakage_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_coset_subspace_qft_concentration_and_leakage_bridge import (
    generate_dcp_coset_subspace_qft_concentration_and_leakage_certificate,
    verify_hadamard_product_law_and_tv_identity,
)


def test_hadamard_product_law_and_tv_identity() -> None:
    ctrl = verify_hadamard_product_law_and_tv_identity([[4], [0], [4]], [1], t_bits=3)
    assert ctrl["exact_product_and_tv_verified"] is True
    assert abs(ctrl["max_single_outcome_probability"] - 1.0) < 1e-12

    leak = verify_hadamard_product_law_and_tv_identity([[2], [1], [3]], [1], t_bits=3)
    assert leak["exact_product_and_tv_verified"] is True
    assert leak["max_single_outcome_probability"] < 0.45


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_coset_subspace_qft_concentration_and_leakage_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_coset_subspace_qft_concentration_and_leakage_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_coset_subspace_qft_concentration_and_leakage_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
