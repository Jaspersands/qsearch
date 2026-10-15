from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.native_higher_call_weighted_fourier_pinching_audit import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DOC_PATH,
    SCHEMA_VERSION,
    bilinear_fourier_phase,
    build_native_higher_call_weighted_fourier_pinching_audit,
    evaluate_schedule_case,
    load_contract,
    signed_net_error_phase,
    signed_net_frequency,
    write_native_higher_call_weighted_fourier_pinching_audit,
)


def test_contract_and_doc_exist() -> None:
    assert DEFAULT_CONTRACT_PATH.exists()
    assert DEFAULT_DOC_PATH.exists()
    contract = load_contract()
    assert contract["contract_id"] == "native-higher-call-weighted-fourier-pinching-audit-contract"
    assert len(contract["theorems"]) == 3


def test_signed_frequency_and_bilinear_phase_primitives() -> None:
    freq_table = [(1, 0), (0, 1), (1, 1)]
    error_table = [0, 1, 2]
    assert signed_net_frequency((0, 1), freq_table, (1, -1), 3) == (1, 2)
    assert signed_net_error_phase((0, 2), error_table, (1, -1), 3) == 1
    assert bilinear_fourier_phase((1, 2), (1, -1), x=2, D=3) == (1 * 2 * 1 - 1 * 2 * 2) % 3


def test_theorem1_secret_average_equals_pinched_variety_sum() -> None:
    payload = build_native_higher_call_weighted_fourier_pinching_audit()
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["status"] == "VERIFIED_EXACT_K_CALL_WEIGHTED_FOURIER_PINCHING_IDENTITIES"
    assert payload["summary"]["all_cases_verified"] is True
    assert payload["summary"]["max_theorem1_pinching_residual"] <= 1e-12


def test_theorem2_diagonal_floor_and_zero_mean_off_diagonal_surplus() -> None:
    payload = build_native_higher_call_weighted_fourier_pinching_audit()
    for case in payload["cases"]:
        D = case["D"]
        assert case["diagonal_floor_exact"] == f"1/{D}"
        assert case["theorem2_floor_plus_offdiag_residual"] <= 1e-12
        assert abs(case["off_diagonal_surplus_sum"]) <= 1e-12
        assert case["probability_normalization_residual"] <= 1e-12


def test_theorem3_balanced_signed_vs_unsigned_k2_contrast() -> None:
    payload = build_native_higher_call_weighted_fourier_pinching_audit()
    assert payload["summary"]["theorem3_unsigned_vs_balanced_contrast_verified"] is True
    unsigned = payload["cases"][0]
    balanced = payload["cases"][1]
    assert unsigned["k2_transpose_off_diagonal_collisions"] == 6
    assert balanced["k2_self_difference_zero_fiber_count"] == 3
    assert balanced["zero_fiber_multiplicity"] >= 3


def test_custom_k3_schedule_evaluation() -> None:
    res = evaluate_schedule_case(
        case_id="custom_k3_test",
        D=3,
        q=3,
        n=2,
        freq_table=[(1, 2), (2, 0), (0, 1)],
        error_table=[1, 0, 2],
        epsilon=(-1, 1, -1),
        sigma=(-1, 1, 1),
    )
    assert res["exact_verification_passed"] is True
    assert res["diagonal_trajectory_count"] == 27


def test_guardrails_preserved() -> None:
    payload = build_native_higher_call_weighted_fourier_pinching_audit()
    g = payload["guardrails"]
    assert g["accepted_speedup_candidate"] is False
    assert g["new_active_negative_result_created"] is False
    assert g["novelty_claim"] is False


def test_artifact_matches_builder_and_js_crosscheck(tmp_path: Path) -> None:
    out_file = tmp_path / "pinching_audit.json"
    written = write_native_higher_call_weighted_fourier_pinching_audit(output_path=out_file)
    assert out_file.exists()
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["certificate_sha256"] == written["certificate_sha256"]
        js_script = (
            ROOT
            / "research"
            / "certificates"
            / "native_higher_call_weighted_fourier_pinching_audit_crosscheck.js"
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
