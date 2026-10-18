"""Tests for dcp_iqp_bounded_degree_carry_orthogonality_obstruction."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from theorems.dcp_iqp_bounded_degree_carry_orthogonality_obstruction import (
    DEFAULT_ARTIFACT_PATH,
    build_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_iqp_directional_derivative_matrix_and_sparsity() -> None:
    report = build_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report()
    assert report["summary"]["theorem1_iqp_derivative_sparsity_passed"] is True
    assert report["summary"]["max_matrix_entry_error"] <= 1e-12
    assert report["summary"]["max_advantage_formula_error"] <= 1e-12
    for inst in report["instances"]:
        ia = inst["iqp_matrix_audit"]
        assert ia["theorem1_passed"] is True
        assert ia["all_rows_have_degree_one"] is True
        assert ia["degree_directional_derivative"] <= max(0, ia["degree_P"] - 1)


def test_theorem2_lucas_carry_degree_orthogonality() -> None:
    report = build_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report()
    assert report["summary"]["theorem2_lucas_carry_degree_passed"] is True
    for inst in report["instances"]:
        la = inst["lucas_carry_audit"]
        assert la["theorem2_passed"] is True
        assert la["carry_anf_degree"] == la["w_lucas_vars"]
        assert la["derivative_anf_degree"] < la["w_lucas_vars"]
        assert la["xor_anf_degree"] == la["w_lucas_vars"]
        assert la["derivative_truth_table_parity_mod2"] == 0
        assert la["signed_correlation_lhs"] == la["signed_correlation_rhs"]


def test_theorem3_source_average_and_adaptive_sparse_bounds() -> None:
    report = build_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report()
    assert (
        report["summary"]["theorem3_source_average_and_adaptive_bounds_passed"] is True
    )
    for inst in report["instances"]:
        sa = inst["source_average_audit"]
        assert sa["theorem3_passed"] is True
        assert all(c == 1 for c in sa["all_x_hit_counts_over_pivot_column"])
        assert Fraction(sa["pointwise_hit_probability_exact"]) == Fraction(
            1, inst["q"] ** inst["n"]
        )


def test_asymptotic_scaling_and_honesty_guardrails() -> None:
    report = build_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report()
    assert report["summary"]["all_theorems_passed"] is True
    for row in report["asymptotic_scaling"]:
        assert row["msb_carry_anf_degree_power_of_two_exponent"] == row["t"] - 1
        assert row["clean_nonadaptive_mean_advantage_upper_neg_log2"] >= 4
        if row["n"] >= 32:
            assert row["sparse_class_excluded_at_1_16"] is True
    hg = report["honesty_guardrails"]
    assert hg["accepted_speedup_candidate"] is False
    assert hg["new_active_negative_result_created"] is False
    assert hg["novelty_claim"] is False
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["sha256"] == report["sha256"]


def test_cli_execution() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(
                ROOT
                / "theorems"
                / "dcp_iqp_bounded_degree_carry_orthogonality_obstruction.py"
            ),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True
