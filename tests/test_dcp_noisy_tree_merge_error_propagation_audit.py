from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_noisy_tree_merge_error_propagation_audit import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_dcp_noisy_tree_merge_error_propagation_audit,
    cyclic_convolve_power,
    evaluate_noisy_tree_merge_case,
    fourier_cos_harmonics,
    load_contract,
    symmetric_nearest_neighbor_kernel,
    write_dcp_noisy_tree_merge_error_propagation_audit,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert contract["contract_id"] == "dcp-noisy-tree-merge-error-propagation-audit-contract"
    assert len(contract["theorems"]) == 3


def test_convolution_and_harmonic_power_law() -> None:
    kernel = symmetric_nearest_neighbor_kernel(8, 0.2)
    h1 = fourier_cos_harmonics(kernel)
    conv4 = cyclic_convolve_power(kernel, 4)
    h4 = fourier_cos_harmonics(conv4)
    for m in range(8):
        assert abs(float(h4[m]) - float(h1[m] ** 4)) <= 1e-12


def test_all_theorems_across_cases() -> None:
    payload = build_dcp_noisy_tree_merge_error_propagation_audit()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["status"] == "VERIFIED_EXACT_NOISY_TREE_MERGE_CONVOLUTION_AND_SNR_CROSSOVER"
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True
        for row in c["depth_rows"]:
            if row["depth_L"] >= 1:
                assert row["root_to_leaf_snr_ratio"] < 1.0


def test_custom_noisy_tree_merge_evaluation() -> None:
    res = evaluate_noisy_tree_merge_case(
        case_id="custom_q12_p03_d3",
        q=12,
        p_err=0.3,
        max_depth=3,
        target_tau=0.6,
    )
    assert res["all_theorems_verified"] is True


def test_guardrails_preserved() -> None:
    payload = build_dcp_noisy_tree_merge_error_propagation_audit()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "noisy_tree_merge.json"
    written = write_dcp_noisy_tree_merge_error_propagation_audit(output_path=out_file)
    assert out_file.exists()
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["certificate_sha256"] == written["certificate_sha256"]
        js_script = (
            ROOT
            / "research"
            / "certificates"
            / "dcp_noisy_tree_merge_error_propagation_audit_crosscheck.js"
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
