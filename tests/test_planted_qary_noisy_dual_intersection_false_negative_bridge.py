from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.planted_qary_noisy_dual_intersection_false_negative_bridge import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_planted_qary_noisy_dual_intersection_false_negative_bridge,
    evaluate_noisy_dual_intersection_case,
    load_contract,
    write_planted_qary_noisy_dual_intersection_false_negative_bridge,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert (
        contract["contract_id"]
        == "planted-qary-noisy-dual-intersection-false-negative-bridge-contract"
    )
    assert len(contract["theorems"]) == 3


def test_all_theorems_across_cases() -> None:
    payload = build_planted_qary_noisy_dual_intersection_false_negative_bridge()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert (
        payload["status"]
        == "VERIFIED_EXACT_NOISY_DUAL_INTERSECTION_FALSE_NEGATIVE_LAWS"
    )
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True


def test_spurious_invariance_across_noise_rates() -> None:
    payload = build_planted_qary_noisy_dual_intersection_false_negative_bridge()
    c0 = payload["cases"][0]
    assert c0["spurious_single_sample_survival_exact"] == "1/3"
    assert c0["spurious_m_sample_survival_exact"] == "1/9"


def test_custom_noisy_dual_intersection_evaluation() -> None:
    res = evaluate_noisy_dual_intersection_case(
        case_id="custom_q2_n3_d1",
        q=2,
        n=3,
        generator_matrix=[[1, 1, 1]],
        gamma_num=1,
        gamma_den=3,
        m_samples=2,
    )
    assert res["all_theorems_verified"] is True
    assert res["primal_minimum_distance_d_min"] == 3


def test_guardrails_preserved() -> None:
    payload = build_planted_qary_noisy_dual_intersection_false_negative_bridge()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "noisy_dual_inter.json"
    written = write_planted_qary_noisy_dual_intersection_false_negative_bridge(
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
            / "planted_qary_noisy_dual_intersection_false_negative_bridge_crosscheck.js"
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
