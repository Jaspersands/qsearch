"""Tests for dcp_noisy_cascaded_dyadic_peeling_sample_complexity_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_noisy_cascaded_dyadic_peeling_sample_complexity_bridge import (
    evaluate_cumulative_peeling_budget,
    generate_dcp_noisy_cascaded_dyadic_peeling_sample_complexity_certificate,
)


def test_noiseless_and_noisy_peeling_budgets() -> None:
    b_clean = evaluate_cumulative_peeling_budget(t_bits=5, gamma_0=1.0)
    assert abs(b_clean["cumulative_raw_qubits_per_unit_fisher_pruned"] - 31.0) < 1e-12
    assert abs(b_clean["cumulative_raw_qubits_per_unit_fisher_unpruned"] - 31.0) < 1e-12

    b_noisy = evaluate_cumulative_peeling_budget(t_bits=6, gamma_0=0.85)
    assert b_noisy["all_singly_exponential_bounds_verified"] is True
    assert b_noisy["cumulative_savings_ratio_unpruned_over_pruned"] > 4800.0


def test_input_validation_rejects_invalid_gamma() -> None:
    try:
        evaluate_cumulative_peeling_budget(t_bits=3, gamma_0=0.0)
        raise AssertionError("Expected ValueError for gamma_0=0.0")
    except ValueError as exc:
        assert "gamma_0" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_noisy_cascaded_dyadic_peeling_sample_complexity_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_noisy_cascaded_dyadic_peeling_sample_complexity_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_noisy_cascaded_dyadic_peeling_sample_complexity_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
