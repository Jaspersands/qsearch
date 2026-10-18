from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.native_higher_call_word_permutation_covariance_audit import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_native_higher_call_word_permutation_covariance_audit,
    evaluate_word_permutation_case,
    load_contract,
    write_native_higher_call_word_permutation_covariance_audit,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert (
        contract["contract_id"]
        == "native-higher-call-word-permutation-covariance-audit-contract"
    )
    assert len(contract["theorems"]) == 3


def test_all_theorems_across_cases() -> None:
    payload = build_native_higher_call_word_permutation_covariance_audit()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert (
        payload["status"]
        == "VERIFIED_EXACT_WORD_PERMUTATION_COVARIANCE_AND_ALTERNATING_RESCUE"
    )
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True


def test_involutive_vs_non_involutive_k2_behavior() -> None:
    payload = build_native_higher_call_word_permutation_covariance_audit()
    c_inv = payload["cases"][1]      # m = 4 mod 5 (4^2 == 1 mod 5)
    c_noninv = payload["cases"][2]   # m = 2 mod 5 (2^2 == 4 != 1 mod 5)
    assert c_inv["is_involutive_m_sq_eq_1"] is True
    assert c_inv["max_uniform_dilation_ordered_tv"] <= 1e-12
    assert c_noninv["is_involutive_m_sq_eq_1"] is False
    assert c_noninv["max_uniform_dilation_ordered_tv"] > 1e-4
    assert c_noninv["max_alternating_intertwine_residual"] <= 1e-12


def test_custom_word_permutation_evaluation() -> None:
    res = evaluate_word_permutation_case(
        case_id="custom_k2_D5_m4",
        D=5,
        q=3,
        n=1,
        m_unit=4,
        shift_b=2,
        freq_table=[(1,), (2,), (0,), (1,), (0,)],
        error_table=[0, 1, 2, 1, 0],
        epsilon=(1, -1),
        sigma=(1, -1),
    )
    assert res["all_theorems_verified"] is True
    assert res["is_involutive_m_sq_eq_1"] is True


def test_guardrails_preserved() -> None:
    payload = build_native_higher_call_word_permutation_covariance_audit()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "word_perm.json"
    written = write_native_higher_call_word_permutation_covariance_audit(
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
            / "native_higher_call_word_permutation_covariance_audit_crosscheck.js"
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
