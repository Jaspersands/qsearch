"""Tests for dcp_cyclic_group_qft_dihedral_coset_interference_bridge."""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

from theorems.dcp_cyclic_group_qft_dihedral_coset_interference_bridge import (
    generate_dcp_cyclic_group_qft_dihedral_coset_interference_certificate,
    verify_cyclic_qft_product_identity_and_peak_criterion,
)


def test_cyclic_qft_product_identity() -> None:
    dyadic = [2.0 * math.pi * ((1 << j) * 5) / 8.0 for j in range(3)]
    res = verify_cyclic_qft_product_identity_and_peak_criterion(dyadic)
    assert res["exact_product_formula_verified"] is True
    assert res["argmax_K"] == 5
    assert abs(res["max_outcome_probability"] - 1.0) < 1e-12


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_cyclic_group_qft_dihedral_coset_interference_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_cyclic_group_qft_dihedral_coset_interference_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_cyclic_group_qft_dihedral_coset_interference_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
