"""Pytest suite for `theorems/dcp_noisy_fourier_likelihood_decoder_audit.py`."""

from __future__ import annotations

from fractions import Fraction
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from theorems.dcp_noisy_fourier_likelihood_decoder_audit import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    audit_quadrature_orthogonality_and_moments,
    audit_tree_merge_visibility_law,
    build_dcp_noisy_fourier_likelihood_decoder_audit_report,
    exact_cnot_merge_blocks,
    phase_density_matrix,
)


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = ROOT / "research" / "certificates" / "dcp_noisy_fourier_likelihood_decoder_audit_crosscheck.js"


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "dcp-noisy-fourier-likelihood-decoder-audit-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    ("N", "k1", "k2", "s", "v1", "v2"),
    [
        (8, 3, 5, 2, Fraction(7, 8), Fraction(3, 4)),
        (16, 7, 11, 5, Fraction(4, 5), Fraction(4, 5)),
        (32, 9, 14, 13, Fraction(13, 16), Fraction(7, 8)),
    ],
)
def test_cnot_tree_merge_visibility_multiplication_law(
    N: int, k1: int, k2: int, s: int, v1: Fraction, v2: Fraction
) -> None:
    rho1 = phase_density_matrix(N, k1, s, float(v1))
    rho2 = phase_density_matrix(N, k2, s, float(v2))
    merged = exact_cnot_merge_blocks(rho1, rho2)
    assert abs(merged["p0"] - 0.5) < 1e-14
    assert abs(merged["p1"] - 0.5) < 1e-14
    v_out = float(v1 * v2)
    expected_0 = phase_density_matrix(N, (k1 + k2) % N, s, v_out)
    expected_1 = phase_density_matrix(N, (k1 - k2) % N, s, v_out)
    assert np.allclose(merged["rho_out_0"], expected_0, atol=1e-14)
    assert np.allclose(merged["rho_out_1"], expected_1, atol=1e-14)


def test_quadrature_orthogonality_and_moments() -> None:
    rows = audit_quadrature_orthogonality_and_moments()
    assert len(rows) == 3
    for row in rows:
        assert row["quadrature_uniquely_identifies_all_oriented_shifts"] is True
        assert row["max_quadrature_mean_error"] < 1e-13
        assert row["max_quadrature_variance_error"] < 1e-13


def test_tree_depth_snr_monotonic_degradation() -> None:
    rows = audit_tree_merge_visibility_law()
    for row in rows:
        for d_row in row["tree_depth_scaling"]:
            assert d_row["strictly_dominated_by_d0"] is True


def test_report_and_nodejs_crosscheck() -> None:
    report = build_dcp_noisy_fourier_likelihood_decoder_audit_report()
    assert all(report["verification"].values())
    assert ARTIFACT_PATH.exists()
    saved = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert saved == report

    proc = subprocess.run(
        ["node", str(CROSSCHECK_JS)],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["status"] == "ok"
    assert payload["live_sources_verified"] == len(report["live_opaque_phase_decoder_audit"])


def test_cli_execution() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "theorems.dcp_noisy_fourier_likelihood_decoder_audit", "--no-write"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "dcp_noisy_fourier_likelihood_decoder_audit"
    assert all(out["verification"].values())
