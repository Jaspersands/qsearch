from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_two_copy_cnot_difference_alignment_audit import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_dcp_two_copy_cnot_difference_alignment_audit,
    evaluate_cnot_alignment_case,
    load_contract,
    write_dcp_two_copy_cnot_difference_alignment_audit,
    apply_cnot_and_project_target,
)
from theorems.dcp_quadrature_conjugate_pair_holevo_audit import build_qubit_pair_state


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert (
        contract["contract_id"]
        == "dcp-two-copy-cnot-difference-alignment-audit-contract"
    )
    assert len(contract["theorems"]) == 3


def test_all_theorems_across_cases() -> None:
    payload = build_dcp_two_copy_cnot_difference_alignment_audit()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert (
        payload["status"]
        == "VERIFIED_EXACT_TWO_COPY_CNOT_BIFURCATION_AND_YIELD_LAWS"
    )
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True


def test_custom_cnot_alignment_evaluation() -> None:
    res = evaluate_cnot_alignment_case(
        case_id="custom_q9_p015",
        q=9,
        p_err=0.15,
        test_secret_s=2,
    )
    assert res["all_theorems_verified"] is True


def test_guardrails_preserved() -> None:
    payload = build_dcp_two_copy_cnot_difference_alignment_audit()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_nonzero_effective_label_with_zero_visibility_has_no_secret_information():
    # q4 nearest-neighbor noise at rate1/2 has lambda_2=0, lambda_1=1/2.
    # The sum branch has nonzero label3 but identical density for every secret.
    for secret in range(4):
        rho1 = build_qubit_pair_state(2*np.pi*2*secret/4, 0.0)
        rho2 = build_qubit_pair_state(2*np.pi*secret/4, 0.5)
        for outcome in (0,1):
            probability, density = apply_cnot_and_project_target(rho1,rho2,outcome)
            assert abs(probability-0.5) < 1e-13
            np.testing.assert_allclose(density,np.eye(2)/2,atol=1e-13)


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "cnot_align.json"
    written = write_dcp_two_copy_cnot_difference_alignment_audit(
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
            / "dcp_two_copy_cnot_difference_alignment_audit_crosscheck.js"
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
