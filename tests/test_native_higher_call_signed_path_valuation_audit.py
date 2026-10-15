"""Pytest suite for `theorems/native_higher_call_signed_path_valuation_audit.py`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.native_higher_call_signed_path_valuation_audit import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    audit_paired_difference_sign_invariance,
    audit_single_path_coset_and_zero_sum_theorem,
    audit_universal_one_third_valuation_law,
    build_native_higher_call_signed_path_valuation_audit_report,
    closed_form_zero_sum_single_path_count,
    signed_paired_difference_counts,
    signed_single_path_sum_counts,
)
from theorems.native_response_path_valuation import local_difference_counts


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = ROOT / "research" / "certificates" / "native_higher_call_signed_path_valuation_audit_crosscheck.js"


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "native-higher-call-signed-path-valuation-audit-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    "signs",
    [
        (1,),
        (-1,),
        (1, 1),
        (1, -1),
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1, -1),
        (1, 1, 1, -1),
        (1, -1, 1, -1, 1, -1),
        (1, 1, 1, 1, 1, 1),
    ],
)
def test_single_path_z3_coset_and_zero_sum_formula(signs: tuple[int, ...]) -> None:
    sums = signed_single_path_sum_counts(signs)
    net_s = sum(signs)
    assert sum(sums.values()) == 3 ** len(signs)
    assert all(((x - y) - net_s) % 3 == 0 for (x, y) in sums)
    mod3_zero = sum(m for (x, y), m in sums.items() if x % 3 == 0 and y % 3 == 0)
    expected_mod3_zero = (3 ** (len(signs) - 1)) if (net_s % 3 == 0) else 0
    assert mod3_zero == expected_mod3_zero
    assert sums.get((0, 0), 0) == closed_form_zero_sum_single_path_count(signs)


@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_paired_difference_sign_schedule_invariance(k: int) -> None:
    ref = local_difference_counts(k)
    alt_signs = tuple(1 if i % 2 == 0 else -1 for i in range(k))
    assert signed_paired_difference_counts(alt_signs) == ref


def test_universal_one_third_valuation_law() -> None:
    rows = audit_universal_one_third_valuation_law()
    assert len(rows) == 8
    for row in rows:
        assert row["matches_theorem_3"] is True
        assert row["local_nonunit_fraction"] == "1/3"


def test_report_and_nodejs_crosscheck() -> None:
    report = build_native_higher_call_signed_path_valuation_audit_report()
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
    assert payload["valuation_call_counts_verified"] == 8


def test_cli_execution() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "theorems.native_higher_call_signed_path_valuation_audit", "--no-write"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "native_higher_call_signed_path_valuation_audit"
    assert all(out["verification"].values())
