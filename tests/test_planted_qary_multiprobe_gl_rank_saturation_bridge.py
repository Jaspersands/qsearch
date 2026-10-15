from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.planted_qary_multiprobe_gl_rank_saturation_bridge import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    build_planted_qary_multiprobe_gl_rank_saturation_bridge,
    evaluate_multiprobe_case,
    exact_projected_rank_probability,
    load_contract,
    q_binomial_exact,
    write_planted_qary_multiprobe_gl_rank_saturation_bridge,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert contract["contract_id"] == "planted-qary-multiprobe-gl-rank-saturation-bridge-contract"
    assert len(contract["theorems"]) == 3


def test_q_binomial_and_projected_rank_probabilities() -> None:
    assert q_binomial_exact(3, 0, 3) == 1
    assert q_binomial_exact(3, 1, 3) == 13
    assert q_binomial_exact(3, 2, 3) == 13
    assert q_binomial_exact(3, 3, 3) == 1
    probs = [exact_projected_rank_probability(5, 3, 4, r) for r in range(4)]
    assert sum(probs) == Fraction(1, 1)


def test_theorem1_and_theorem2_and_theorem3_across_cases() -> None:
    payload = build_planted_qary_multiprobe_gl_rank_saturation_bridge()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["status"] == "VERIFIED_EXACT_MULTIPROBE_GL_RANK_SATURATION_LAWS"
    assert payload["summary"]["all_cases_verified"] is True
    for c in payload["cases"]:
        assert c["theorem1_verified"] is True
        assert c["theorem2_verified"] is True
        assert c["theorem3_verified"] is True
        if not c["zero_in_window"]:
            assert c["normalized_mass_exact"] == c["unstructured_nonzero_normalized_mass_exact"]


def test_custom_multiprobe_evaluation() -> None:
    res = evaluate_multiprobe_case(
        case_id="custom_q2_d3_k2",
        q=2,
        d=3,
        k=2,
        window=[1],
    )
    assert res["all_theorems_verified"] is True
    assert res["expected_full_rank_acceptance_count"] == 2
    assert res["observed_full_rank_acceptance_values"] == [2]


def test_guardrails_preserved() -> None:
    payload = build_planted_qary_multiprobe_gl_rank_saturation_bridge()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "multiprobe_bridge.json"
    written = write_planted_qary_multiprobe_gl_rank_saturation_bridge(output_path=out_file)
    assert out_file.exists()
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["certificate_sha256"] == written["certificate_sha256"]
        js_script = (
            ROOT
            / "research"
            / "certificates"
            / "planted_qary_multiprobe_gl_rank_saturation_bridge_crosscheck.js"
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
