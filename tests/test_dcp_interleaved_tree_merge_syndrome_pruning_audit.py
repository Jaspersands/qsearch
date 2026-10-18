from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_interleaved_tree_merge_syndrome_pruning_audit import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_dcp_interleaved_tree_merge_syndrome_pruning_audit,
    evaluate_syndrome_pruning_case,
    load_contract,
    write_dcp_interleaved_tree_merge_syndrome_pruning_audit,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert (
        contract["contract_id"]
        == "dcp-interleaved-tree-merge-syndrome-pruning-audit-contract"
    )
    assert len(contract["theorems"]) == 3


def test_all_theorems_across_cases() -> None:
    payload = build_dcp_interleaved_tree_merge_syndrome_pruning_audit()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert (
        payload["status"]
        == "CONDITIONAL_CLASSICAL_IDENTITIES_PHYSICAL_ACCESS_NOT_SUPPLIED"
    )
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True


def test_purification_regimes_below_at_and_above_two_thirds() -> None:
    payload = build_dcp_interleaved_tree_merge_syndrome_pruning_audit()
    c_below = payload["cases"][0]  # p = 1/4
    c_crit = payload["cases"][2]   # p = 2/3
    c_above = payload["cases"][3]  # p = 3/4
    assert c_below["expected_purification_regime"] == "PURIFYING"
    assert c_below["step1_visibility_gain"] > 0.0
    assert c_crit["expected_purification_regime"] == "CRITICAL_NEUTRAL"
    assert abs(c_crit["step1_visibility_gain"]) <= 1e-12
    assert c_above["expected_purification_regime"] == "DEGRADING"
    assert c_above["step1_visibility_gain"] < 0.0


def test_custom_syndrome_pruning_evaluation() -> None:
    res = evaluate_syndrome_pruning_case(
        case_id="custom_q12_p_1_over_5",
        q=12,
        p_err_num=1,
        p_err_den=5,
        max_depth=3,
    )
    assert res["all_theorems_verified"] is True


def test_guardrails_preserved() -> None:
    payload = build_dcp_interleaved_tree_merge_syndrome_pruning_audit()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "syndrome_pruning.json"
    written = write_dcp_interleaved_tree_merge_syndrome_pruning_audit(
        output_path=out_file
    )
    assert out_file.exists()
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["certificate_sha256"] == written["certificate_sha256"]
        js_script = (
            ROOT
            / "research"
            / "certificates"
            / "dcp_interleaved_tree_merge_syndrome_pruning_audit_crosscheck.js"
        )
        proc = subprocess.run(
            ["/usr/local/bin/node", str(js_script)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        out_json = json.loads(proc.stdout)
        assert out_json["status"] == "CROSSCHECK_PASSED"
