"""Pytest suite for `theorems/dcp_adaptive_quadrature_tree_sieve_audit.py`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.dcp_adaptive_quadrature_tree_sieve_audit import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    audit_bitwise_dyadic_demodulation_identity,
    audit_equal_valuation_cnot_pairing_dichotomy,
    audit_sieve_depth_visibility_thresholds,
    build_dcp_adaptive_quadrature_tree_sieve_audit_report,
    two_adic_valuation,
)


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = ROOT / "research" / "certificates" / "dcp_adaptive_quadrature_tree_sieve_audit_crosscheck.js"


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "dcp-adaptive-quadrature-tree-sieve-audit-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


def test_bitwise_dyadic_identity_is_not_promoted_to_sampled_recovery() -> None:
    rows = audit_bitwise_dyadic_demodulation_identity()
    assert len(rows) == 3
    for row in rows:
        assert row["max_pointwise_mean_error"] < 1e-14
        assert row["max_pointwise_variance_error"] < 1e-14
        assert row["all_pointwise_signs_match_bit_s_r"] is True
        assert row["mean_identity_is_a_sampled_receiver"] is False
        assert row["prescribed_labels_or_exact_expectations_available_to_solver"] is False


def test_equal_valuation_cnot_pairing_dichotomy() -> None:
    rows = audit_equal_valuation_cnot_pairing_dichotomy()
    assert len(rows) == 14
    for row in rows:
        assert row["stratum_size"] == row["expected_stratum_size"]
        assert row["both_branches_always_advance_valuation"] is True
        assert row["mod_4_branch_dichotomy_holds_for_every_pair"] is True
        assert row["exact_h_plus_1_branch_fraction"] == "1/2"
        assert row["ge_h_plus_2_branch_fraction"] == "1/2"


def test_sieve_depth_visibility_thresholds() -> None:
    rows = audit_sieve_depth_visibility_thresholds()
    assert len(rows) == 4
    for row in rows:
        for dp in row["depth_profiles"]:
            assert dp["min_guaranteed_2_adic_valuation"] == dp["sieve_depth_d"]


@pytest.mark.parametrize(("k", "ell", "expected"), [(0, 4, 4), (1, 4, 0), (6, 4, 1), (12, 4, 2), (8, 4, 3)])
def test_two_adic_valuation(k: int, ell: int, expected: int) -> None:
    assert two_adic_valuation(k, ell) == expected


def test_report_and_nodejs_crosscheck() -> None:
    report = build_dcp_adaptive_quadrature_tree_sieve_audit_report()
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
    assert payload["cnot_dichotomy_strata_verified"] == 14


def test_cli_execution() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "theorems.dcp_adaptive_quadrature_tree_sieve_audit", "--no-write"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "dcp_adaptive_quadrature_tree_sieve_audit"
    assert all(out["verification"].values())
