from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.native_higher_call_prime_power_divisibility_hierarchy_audit import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_native_higher_call_prime_power_divisibility_hierarchy_audit,
    evaluate_divisibility_hierarchy_case,
    load_contract,
    padic_valuation_int,
    padic_valuation_vec,
    write_native_higher_call_prime_power_divisibility_hierarchy_audit,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert (
        contract["contract_id"]
        == "native-higher-call-prime-power-divisibility-hierarchy-audit-contract"
    )
    assert len(contract["theorems"]) == 3


def test_padic_valuation_primitives() -> None:
    assert padic_valuation_int(0, 3, 3) == 3
    assert padic_valuation_int(9, 3, 3) == 2
    assert padic_valuation_int(6, 3, 3) == 1
    assert padic_valuation_int(5, 3, 3) == 0
    assert padic_valuation_vec((9, 6), 3, 3) == 1


def test_all_theorems_across_cases() -> None:
    payload = build_native_higher_call_prime_power_divisibility_hierarchy_audit()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["status"] == "VERIFIED_EXACT_PRIME_POWER_DIVISIBILITY_PINCHING_HIERARCHY"
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True


def test_custom_divisibility_hierarchy_evaluation() -> None:
    res = evaluate_divisibility_hierarchy_case(
        case_id="custom_p3_r2_k2",
        p=3,
        r=2,
        D=3,
        n=1,
        freq_table=[(2,), (5,), (8,)],
        error_table=[1, 2, 0],
        epsilon=(1, -1),
        sigma=(-1, 1),
    )
    assert res["all_theorems_verified"] is True


def test_guardrails_preserved() -> None:
    payload = build_native_higher_call_prime_power_divisibility_hierarchy_audit()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "div_hierarchy.json"
    written = write_native_higher_call_prime_power_divisibility_hierarchy_audit(
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
            / "native_higher_call_prime_power_divisibility_hierarchy_audit_crosscheck.js"
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
