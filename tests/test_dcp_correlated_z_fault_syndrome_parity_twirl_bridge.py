"""Tests for dcp_correlated_z_fault_syndrome_parity_twirl_bridge."""

from __future__ import annotations

import itertools
import json
import subprocess
from pathlib import Path

from theorems.dcp_correlated_z_fault_syndrome_parity_twirl_bridge import (
    generate_dcp_correlated_z_fault_syndrome_parity_twirl_certificate,
    verify_cnot_packet_density_walsh_parity_law,
)


def test_even_weight_immunity_and_single_fault_collapse() -> None:
    thetas = [0.4, 1.1, 2.3]
    even_dist = {
        e: (0.25 if (sum(e) % 2) == 0 else 0.0)
        for e in itertools.product((0, 1), repeat=3)
    }
    res_even = verify_cnot_packet_density_walsh_parity_law(thetas, even_dist)
    assert res_even["exact_walsh_parity_law_verified"] is True
    assert abs(res_even["walsh_global_parity_visibility"] - 1.0) < 1e-12
    assert abs(res_even["naive_product_of_marginals"] - 0.0) < 1e-12


def test_input_validation_rejects_unnormalized_dist() -> None:
    try:
        verify_cnot_packet_density_walsh_parity_law([0.1, 0.2], {(0, 0): 0.5})
        raise AssertionError("Expected ValueError for unnormalized distribution")
    except ValueError as exc:
        assert "sum to 1.0" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_correlated_z_fault_syndrome_parity_twirl_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_correlated_z_fault_syndrome_parity_twirl_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_correlated_z_fault_syndrome_parity_twirl_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
