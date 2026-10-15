"""Pytest suite for `theorems/planted_qary_cdkm_adder_sparsity_bridge.py`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.planted_qary_cdkm_adder_sparsity_bridge import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    analyze_qary_cube_circuit_sparsity,
    audit_modulus_scaling_at_fixed_geometry,
    build_planted_qary_cdkm_adder_sparsity_bridge_report,
)


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = ROOT / "research" / "certificates" / "planted_qary_cdkm_adder_sparsity_bridge_crosscheck.js"


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "planted-qary-cdkm-adder-sparsity-bridge-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    ("n", "m", "q", "support", "seed", "m_box", "width"),
    [
        (4, 2, 257, 3, 11, 8, 4),
        (6, 3, 1009, 4, 17, 16, 4),
        (8, 4, 65537, 5, 23, 16, 8),
        (10, 5, 1000003, 6, 29, 32, 8),
        (12, 6, 1000003, 8, 37, 32, 8),
    ],
)
def test_centered_rref_cdkm_addition_compression_and_free_bounds(
    n: int, m: int, q: int, support: int, seed: int, m_box: int, width: int
) -> None:
    rec = analyze_qary_cube_circuit_sparsity(
        n=n,
        m=m,
        q=q,
        support=support,
        seed=seed,
        m_box=m_box,
        width=width,
        compile_circuit=(n == 4),
    )
    assert rec["free_col_nnz_all_equal_1"] is True
    assert rec["piv_col_nnz_matches_formula"] is True
    assert rec["theorem_1_addition_count_matches"] is True
    assert rec["theorem_2_free_bounds_and_widths_match"] is True
    assert rec["theorem_3_nonsplit_free_popcount_matches"] is True
    assert rec["saved_constant_additions_vs_dense"] >= rec["min_guaranteed_saved_additions"]


def test_modulus_independence_of_free_column_cell_widths_past_2_pow_80() -> None:
    mod_audit = audit_modulus_scaling_at_fixed_geometry()
    assert mod_audit["split_free_cell_bits_constant_across_all_q"] is True
    assert mod_audit["nonsplit_free_cell_bits_constant_across_all_q"] is True
    assert mod_audit["total_free_column_cell_qubits_constant_across_all_q"] is True


def test_report_and_nodejs_crosscheck() -> None:
    report = build_planted_qary_cdkm_adder_sparsity_bridge_report()
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
    assert payload["modulus_scaling_configs_verified"] == 5
    assert payload["dimension_family_configs_verified"] == 5


def test_cli_execution() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "theorems.planted_qary_cdkm_adder_sparsity_bridge", "--no-write"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "planted_qary_cdkm_adder_sparsity_bridge"
    assert all(out["verification"].values())
