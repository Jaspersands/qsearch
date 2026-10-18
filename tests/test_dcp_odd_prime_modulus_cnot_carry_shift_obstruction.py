"""Tests for dcp_odd_prime_modulus_cnot_carry_shift_obstruction."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_odd_prime_modulus_cnot_carry_shift_obstruction import (
    generate_dcp_odd_prime_modulus_cnot_carry_shift_certificate,
    verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law,
)


def test_odd_prime_anchor_invariance_and_minimal_zero_sum_law() -> None:
    res_min3 = verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law(
        a_matrix=[[1, 2, 4]],
        v_vec=[1, 1, 1],
        p_mod=7,
    )
    assert res_min3["invariance_iff_zero_columns_verified"] is True
    assert res_min3["anchor_invariant_mod_p"] is False
    assert res_min3["minimal_witness_exact_monochrome_fraction_verified"] is True
    assert abs(res_min3["zero_tilde_anchor_fraction"] - 0.25) < 1e-12


def test_input_validation_rejects_even_or_composite_p() -> None:
    try:
        verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law([[1, 3]], [1, 1], p_mod=4)
        raise AssertionError("Expected ValueError for even p_mod=4")
    except ValueError as exc:
        assert "odd integer" in str(exc)

    try:
        verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law([[1, 8]], [1, 1], p_mod=9)
        raise AssertionError("Expected ValueError for composite p_mod=9")
    except ValueError as exc:
        assert "prime" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_odd_prime_modulus_cnot_carry_shift_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_odd_prime_modulus_cnot_carry_shift_obstruction.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_odd_prime_modulus_cnot_carry_shift_obstruction_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
