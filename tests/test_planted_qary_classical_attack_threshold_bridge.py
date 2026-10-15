"""Pytest suite for `theorems/planted_qary_classical_attack_threshold_bridge.py`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.planted_qary_classical_attack_threshold_bridge import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    audit_free_support_and_classical_attacks,
    build_planted_qary_classical_attack_threshold_bridge_report,
    projective_free_coordinate_rref_search,
)
from theorems.planted_qary_usvp_source import canonical_sign, generate_source


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = (
    ROOT
    / "research"
    / "certificates"
    / "planted_qary_classical_attack_threshold_bridge_crosscheck.js"
)


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "planted-qary-classical-attack-threshold-bridge-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    ("n", "m", "q", "support", "seed"),
    [
        (4, 2, 257, 3, 11),
        (6, 3, 1009, 4, 17),
        (8, 4, 65537, 6, 23),
        (10, 6, 1000003, 8, 29),
    ],
)
def test_projective_free_coordinate_rref_search_recovers_plant_with_exact_state_count(
    n: int, m: int, q: int, support: int, seed: int
) -> None:
    gen = generate_source(
        n=n,
        m=m,
        q=q,
        gap=2,
        support=support,
        plant_seed=seed,
        matrix_seed=seed + 400,
    )
    res = projective_free_coordinate_rref_search(gen.problem)
    assert res["projective_free_states_checked"] == (3 ** (n - m) - 1) // 2
    assert res["projective_free_states_checked"] < res["ambient_mitm_states"]
    assert tuple(res["recovered_vector"]) == canonical_sign(gen.private.plant)


def test_classical_attack_thresholds_and_free_support_bounds() -> None:
    rows = audit_free_support_and_classical_attacks()
    assert len(rows) == 6
    for row in rows:
        assert row["free_support_within_sharp_bounds"] is True
        assert row["sparse_column_immune_at_s_ge_3"] is True
        assert row["public_lll_recovered_planted_vector"] is True
        assert row["projective_rref_recovered_planted_vector"] is True


def test_report_and_nodejs_crosscheck() -> None:
    report = build_planted_qary_classical_attack_threshold_bridge_report()
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
    assert payload["instances_verified"] == 6


def test_cli_execution() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "theorems.planted_qary_classical_attack_threshold_bridge",
            "--no-write",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "planted_qary_classical_attack_threshold_bridge"
    assert all(out["verification"].values())
