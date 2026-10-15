"""Pytest suite for `theorems/dcp_truncated_qft_tree_merge_joint_channel_audit.py`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.dcp_truncated_qft_tree_merge_joint_channel_audit import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    audit_two_copy_cnot_phase_defect_addition_and_sine_cancellation,
    build_dcp_truncated_qft_tree_merge_joint_channel_audit_report,
)


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = (
    ROOT
    / "research"
    / "certificates"
    / "dcp_truncated_qft_tree_merge_joint_channel_audit_crosscheck.js"
)


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "dcp-truncated-qft-tree-merge-joint-channel-audit-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


def test_cnot_phase_defect_addition_and_sine_cancellation_factorization() -> None:
    rows = audit_two_copy_cnot_phase_defect_addition_and_sine_cancellation()
    assert len(rows) == 7
    for row in rows:
        assert row["max_cnot_merged_density_error"] < 1e-14
        assert row["exact_factorization_error_at_d1"] < 1e-14
        assert row["matches_theorems_1_2_3"] is True


def test_report_and_nodejs_crosscheck() -> None:
    report = build_dcp_truncated_qft_tree_merge_joint_channel_audit_report()
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
    assert payload["joint_channel_configs_verified"] == 7


def test_cli_execution() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "theorems.dcp_truncated_qft_tree_merge_joint_channel_audit",
            "--no-write",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "dcp_truncated_qft_tree_merge_joint_channel_audit"
    assert all(out["verification"].values())
