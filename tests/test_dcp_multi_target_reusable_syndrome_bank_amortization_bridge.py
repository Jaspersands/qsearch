"""Tests for dcp_multi_target_reusable_syndrome_bank_amortization_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_multi_target_reusable_syndrome_bank_amortization_bridge import (
    generate_dcp_multi_target_reusable_syndrome_bank_amortization_certificate,
    verify_exact_ensemble_bucket_pair_expectation,
)


def test_exact_ensemble_bucket_pair_expectation() -> None:
    res14 = verify_exact_ensemble_bucket_pair_expectation(n_rows=1, k_cols=4)
    assert res14["exact_expectation_verified"] is True
    assert abs(res14["empirical_mean_m_pair"] - 2.75) < 1e-12

    res24 = verify_exact_ensemble_bucket_pair_expectation(n_rows=2, k_cols=4)
    assert res24["exact_expectation_verified"] is True
    assert abs(res24["empirical_mean_m_pair"] - (115.0 / 64.0)) < 1e-12


def test_input_validation_rejects_invalid_dims() -> None:
    try:
        verify_exact_ensemble_bucket_pair_expectation(n_rows=0, k_cols=4)
        raise AssertionError("Expected ValueError for n_rows=0")
    except ValueError as exc:
        assert "positive" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_multi_target_reusable_syndrome_bank_amortization_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_multi_target_reusable_syndrome_bank_amortization_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_multi_target_reusable_syndrome_bank_amortization_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
