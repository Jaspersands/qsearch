from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_subset_sum_modular_collision_entropy_audit import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_dcp_subset_sum_modular_collision_entropy_audit,
    cosine_product_collision_prob,
    evaluate_subset_sum_collision_case,
    load_contract,
    write_dcp_subset_sum_modular_collision_entropy_audit,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert (
        contract["contract_id"]
        == "dcp-subset-sum-modular-collision-entropy-audit-contract"
    )
    assert len(contract["theorems"]) == 3


def test_zero_weight_vector_collision_is_one() -> None:
    assert abs(cosine_product_collision_prob((0, 0, 0), 7) - 1.0) <= 1e-12


def test_all_theorems_across_cases() -> None:
    payload = build_dcp_subset_sum_modular_collision_entropy_audit()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert (
        payload["status"]
        == "VERIFIED_EXACT_SUBSET_SUM_COLLISION_AND_BOOLEAN_SURJECTIVITY_LAWS"
    )
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True


def test_custom_subset_sum_collision_evaluation() -> None:
    res = evaluate_subset_sum_collision_case(
        case_id="custom_q10_composite_m2",
        q=10,
        m=2,
        is_composite_q=True,
    )
    assert res["all_theorems_verified"] is True
    assert res["mean_collision_probability_exact"] == "13/40"


def test_guardrails_preserved() -> None:
    payload = build_dcp_subset_sum_modular_collision_entropy_audit()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "subset_sum_coll.json"
    written = write_dcp_subset_sum_modular_collision_entropy_audit(
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
            / "dcp_subset_sum_modular_collision_entropy_audit_crosscheck.js"
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
