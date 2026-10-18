from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_multi_harmonic_weighted_fisher_decoder_audit import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_dcp_multi_harmonic_weighted_fisher_decoder_audit,
    evaluate_multi_harmonic_case,
    load_contract,
    write_dcp_multi_harmonic_weighted_fisher_decoder_audit,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert (
        contract["contract_id"]
        == "dcp-multi-harmonic-weighted-fisher-decoder-audit-contract"
    )
    assert len(contract["theorems"]) == 3


def test_all_theorems_across_cases() -> None:
    payload = build_dcp_multi_harmonic_weighted_fisher_decoder_audit()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert (
        payload["status"]
        == "VERIFIED_EXACT_MULTI_HARMONIC_PARSEVAL_AND_MATCHED_FILTER_LAWS"
    )
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True


def test_depolarizing_zero_gap_vs_structured_positive_gap() -> None:
    payload = build_dcp_multi_harmonic_weighted_fisher_decoder_audit()
    nn_case = payload["cases"][0]
    dep_case = payload["cases"][4]
    assert nn_case["snr_gap_float"] > 0.0
    assert dep_case["snr_gap_matched_minus_uniform_exact"] == "0/1"


def test_custom_multi_harmonic_evaluation() -> None:
    res = evaluate_multi_harmonic_case(
        case_id="custom_q10_nn",
        q=10,
        kernel_kind="nearest_neighbor",
        p_num=1,
        p_den=5,
    )
    assert res["all_theorems_verified"] is True


def test_guardrails_preserved() -> None:
    payload = build_dcp_multi_harmonic_weighted_fisher_decoder_audit()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "multi_harmonic.json"
    written = write_dcp_multi_harmonic_weighted_fisher_decoder_audit(
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
            / "dcp_multi_harmonic_weighted_fisher_decoder_audit_crosscheck.js"
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
