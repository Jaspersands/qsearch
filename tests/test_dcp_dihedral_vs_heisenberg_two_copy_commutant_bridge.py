"""Tests for dcp_dihedral_vs_heisenberg_two_copy_commutant_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_dihedral_vs_heisenberg_two_copy_commutant_bridge import (
    generate_dcp_dihedral_vs_heisenberg_two_copy_commutant_certificate,
    verify_dyadic_heisenberg_boundary_cocycle_law,
    verify_odd_prime_heisenberg_unit_concentration,
)


def test_odd_prime_and_dyadic_heisenberg_laws() -> None:
    p7 = verify_odd_prime_heisenberg_unit_concentration(p_mod=7, s1=5, s2=3, y0=4)
    assert p7["exact_odd_prime_law_verified"] is True

    d_odd = verify_dyadic_heisenberg_boundary_cocycle_law(t_bits=3, s1=5, s2=3, y0=6)
    assert d_odd["exact_boundary_cocycle_law_verified"] is True
    assert abs(d_odd["delta_1_peak_prob"] - 0.5625) < 1e-12
    assert abs(d_odd["half_period_delta_peak_prob"] - 0.0) < 1e-12

    d_even = verify_dyadic_heisenberg_boundary_cocycle_law(t_bits=3, s1=6, s2=3, y0=5)
    assert d_even["exact_boundary_cocycle_law_verified"] is True
    assert abs(d_even["half_period_delta_peak_prob"] - 1.0) < 1e-12


def test_input_validation_rejects_invalid_t() -> None:
    try:
        verify_dyadic_heisenberg_boundary_cocycle_law(t_bits=1, s1=1, s2=0, y0=0)
        raise AssertionError("Expected ValueError for t_bits=1")
    except ValueError as exc:
        assert "t_bits" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_dihedral_vs_heisenberg_two_copy_commutant_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_dihedral_vs_heisenberg_two_copy_commutant_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_dihedral_vs_heisenberg_two_copy_commutant_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
