"""Tests for dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_bridge import (
    evaluate_three_stage_mod8_adaptive_cascade_1d,
    evaluate_upper_bit_ensemble_three_stage_mod8_cascade_1d,
    generate_dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_certificate,
    verify_all_level_dyadic_sign_invariance,
    verify_multistage_weight_and_visibility_recurrence,
)


def test_all_level_dyadic_sign_invariance() -> None:
    res = verify_all_level_dyadic_sign_invariance(t_bits=4, n_rows=2)
    assert res["all_levels_sign_invariant"] is True


def test_three_stage_mod8_adaptive_cascade_fixed_and_ensemble() -> None:
    res_all4 = evaluate_three_stage_mod8_adaptive_cascade_1d(
        a_row=[1, 3, 5, 7, 1, 5, 3, 7],
        t_bits=3,
        gamma_0=0.85,
    )
    assert res_all4["deterministic_mod8_elimination_verified"] is True
    assert abs(res_all4["adaptive_mod8_zero_fraction"] - 1.0) < 1e-12
    assert abs(res_all4["empirical_mean_pruned_weight"] - 4.4375) < 1e-12

    res_all0 = evaluate_three_stage_mod8_adaptive_cascade_1d(
        a_row=[1, 7, 3, 5, 1, 7, 3, 5],
        t_bits=3,
        gamma_0=0.85,
    )
    assert res_all0["deterministic_mod8_elimination_verified"] is True
    assert abs(res_all0["empirical_mean_pruned_weight"] - 2.375) < 1e-12

    ens = evaluate_upper_bit_ensemble_three_stage_mod8_cascade_1d(gamma_0=0.85)
    assert ens["exact_ensemble_recurrence_match"] is True
    assert abs(ens["ensemble_mean_pruned_weight"] - 3.125) < 1e-12


def test_multistage_weight_and_visibility_recurrence() -> None:
    res = verify_multistage_weight_and_visibility_recurrence(max_stages=6, gamma_0=0.85)
    assert res["exact_recurrence_verified"] is True


def test_input_validation_rejects_even_or_short_inputs() -> None:
    try:
        evaluate_three_stage_mod8_adaptive_cascade_1d(
            a_row=[1, 2, 3, 5, 1, 3, 5, 7],
            t_bits=3,
            gamma_0=0.85,
        )
        raise AssertionError("Expected ValueError for even entry in a_row")
    except ValueError as exc:
        assert "odd integers" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
    assert data["adaptiveMod8ZeroFraction"] == 1.0
