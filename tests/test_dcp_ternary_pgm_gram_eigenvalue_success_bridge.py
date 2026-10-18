"""Tests for dcp_ternary_pgm_gram_eigenvalue_success_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_ternary_pgm_gram_eigenvalue_success_bridge import (
    evaluate_pgm_gram_spectrum_and_success_probability,
    generate_dcp_ternary_pgm_gram_eigenvalue_success_certificate,
)


def test_pgm_gram_spectrum_and_square_root_occupancy_law() -> None:
    res_flat = evaluate_pgm_gram_spectrum_and_success_probability([[1, 2, 4]], q_mod=8)
    assert res_flat["exact_spectrum_and_pgm_law_verified"] is True
    assert abs(res_flat["pgm_success_closed_form"] - 1.0) < 1e-12

    res_coll = evaluate_pgm_gram_spectrum_and_success_probability([[1, 1, 2]], q_mod=8)
    assert res_coll["exact_spectrum_and_pgm_law_verified"] is True


def test_input_validation_rejects_large_or_invalid_q() -> None:
    try:
        evaluate_pgm_gram_spectrum_and_success_probability([[1, 2]], q_mod=1)
        raise AssertionError("Expected ValueError for q_mod=1")
    except ValueError as exc:
        assert "q_mod" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_ternary_pgm_gram_eigenvalue_success_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_ternary_pgm_gram_eigenvalue_success_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_ternary_pgm_gram_eigenvalue_success_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
