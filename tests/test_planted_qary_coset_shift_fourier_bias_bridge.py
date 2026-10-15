from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.planted_qary_coset_shift_fourier_bias_bridge import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_planted_qary_coset_shift_fourier_bias_bridge,
    evaluate_coset_shift_case,
    load_contract,
    write_planted_qary_coset_shift_fourier_bias_bridge,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert contract["contract_id"] == "planted-qary-coset-shift-fourier-bias-bridge-contract"
    assert len(contract["theorems"]) == 3


def test_all_theorems_across_cases() -> None:
    payload = build_planted_qary_coset_shift_fourier_bias_bridge()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["status"] == "VERIFIED_EXACT_COSET_SHIFT_FOURIER_AND_PROBE_INVARIANCE"
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True


def test_nontrivial_coset_first_moment_equalization_with_and_without_zero() -> None:
    payload = build_planted_qary_coset_shift_fourier_bias_bridge()
    c_no_zero = payload["cases"][0]
    c_with_zero = payload["cases"][1]
    assert c_no_zero["shift_a_in_B"] is False
    assert c_with_zero["shift_a_in_B"] is False
    assert c_no_zero["coset_first_moment_exact"] == "6/1"
    assert c_with_zero["coset_first_moment_exact"] == "6/1"
    assert c_no_zero["homogeneous_first_moment_exact"] != c_with_zero["homogeneous_first_moment_exact"]


def test_custom_coset_shift_evaluation() -> None:
    res = evaluate_coset_shift_case(
        case_id="custom_q2_n3_d2",
        q=2,
        n=3,
        generator_matrix=[[1, 0, 1], [0, 1, 1]],
        shift_a=[0, 0, 1],
        window=[1],
    )
    assert res["all_theorems_verified"] is True
    assert res["coset_first_moment_exact"] == "2/1"


def test_guardrails_preserved() -> None:
    payload = build_planted_qary_coset_shift_fourier_bias_bridge()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "coset_shift.json"
    written = write_planted_qary_coset_shift_fourier_bias_bridge(output_path=out_file)
    assert out_file.exists()
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["certificate_sha256"] == written["certificate_sha256"]
        js_script = (
            ROOT
            / "research"
            / "certificates"
            / "planted_qary_coset_shift_fourier_bias_bridge_crosscheck.js"
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
