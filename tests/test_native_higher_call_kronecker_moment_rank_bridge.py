from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.native_higher_call_kronecker_moment_rank_bridge import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_native_higher_call_kronecker_moment_rank_bridge,
    evaluate_kronecker_moment_case,
    load_contract,
    write_native_higher_call_kronecker_moment_rank_bridge,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert (
        contract["contract_id"]
        == "native-higher-call-kronecker-moment-rank-bridge-contract"
    )
    assert len(contract["theorems"]) == 3


def test_all_theorems_across_cases() -> None:
    payload = build_native_higher_call_kronecker_moment_rank_bridge()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["status"] == "VERIFIED_EXACT_KRONECKER_SECOND_MOMENT_PARSEVAL_IDENTITIES"
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True
        assert c["total_l2_signal_energy"] <= c["kronecker_l2_upper_bound_float"] + 1e-12


def test_custom_kronecker_moment_evaluation() -> None:
    res = evaluate_kronecker_moment_case(
        case_id="custom_k2_D3_q3_n1",
        D=3,
        q=3,
        n=1,
        freq_table=[(1,), (2,), (0,)],
        error_table=[1, 0, 2],
        epsilon=(1, -1),
        sigma=(-1, 1),
    )
    assert res["all_theorems_verified"] is True


def test_guardrails_preserved() -> None:
    payload = build_native_higher_call_kronecker_moment_rank_bridge()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "kronecker_moment.json"
    written = write_native_higher_call_kronecker_moment_rank_bridge(output_path=out_file)
    assert out_file.exists()
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["certificate_sha256"] == written["certificate_sha256"]
        js_script = (
            ROOT
            / "research"
            / "certificates"
            / "native_higher_call_kronecker_moment_rank_bridge_crosscheck.js"
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
