"""Tests for dcp_overlapping_cnot_dag_carry_fanout_obstruction."""

from __future__ import annotations

import json
import subprocess
from itertools import product
from pathlib import Path

import pytest

from theorems.dcp_overlapping_cnot_dag_carry_fanout_obstruction import (
    evaluate_overlapping_dag_cross_terms,
    generate_dcp_overlapping_cnot_dag_carry_fanout_certificate,
    all_anchor_linearity_conditions,
)


def test_overlapping_dag_cross_terms_iff() -> None:
    obs = evaluate_overlapping_dag_cross_terms([[3, 1, 5]], [[1, 0], [1, 1], [0, 1]], t_bits=3)
    assert obs["iff_criterion_verified"] is True
    assert obs["cross_terms_identically_zero"] is False

    ctrl = evaluate_overlapping_dag_cross_terms([[3, 4, 5]], [[1, 0], [1, 1], [0, 1]], t_bits=3)
    assert ctrl["iff_criterion_verified"] is True
    assert ctrl["cross_terms_identically_zero"] is True


def test_full_column_rank_cancellation_refutes_old_termwise_necessity():
    row = evaluate_overlapping_dag_cross_terms(
        [[1, 1, 3, 5]], [[1, 1], [1, 1], [1, 0], [0, 1]], 2)
    assert row["cross_terms_identically_zero"]
    assert row["iff_criterion_verified"]
    assert not row["analytic_conditions"]["old_termwise_sufficient_condition"]
    assert row["non_zero_cross_term_evaluations"] == 0


@pytest.mark.parametrize("t", [1, 2, 3])
def test_corrected_criterion_on_every_two_row_two_wire_matrix_and_coefficient(t):
    for bits in product((0, 1), repeat=4):
        v = [list(bits[:2]), list(bits[2:])]
        for a in product(range(1 << t), repeat=2):
            row = evaluate_overlapping_dag_cross_terms([a], v, t)
            assert row["max_multilinear_expansion_error"] == 0
            assert row["iff_criterion_verified"], (a, v, t)


def test_higher_order_terms_cancel_when_toggle_and_pair_conditions_hold():
    v = [[1, 1, 1], [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    row = evaluate_overlapping_dag_cross_terms([[2, 2, 1, 3, 5]], v, 3)
    assert row["cross_terms_identically_zero"]
    assert not row["analytic_conditions"]["old_termwise_sufficient_condition"]
    assert row["iff_criterion_verified"]
    # Same pair cancels at anchor zero, but a toggle prevents all-anchor cancellation.
    row = evaluate_overlapping_dag_cross_terms([[1, 3]], [[1, 1], [1, 1]], 3)
    assert row["analytic_conditions"]["aggregate_pair_condition"]
    assert not row["analytic_conditions"]["anchor_toggle_condition"]
    assert not row["cross_terms_identically_zero"]


@pytest.mark.parametrize("a,v,t", [([], [[1]], 2), ([[1]], [[2]], 2),
                                     ([[1, 2]], [[1]], 2), ([[1]], [[1]], 0)])
def test_invalid_linear_models_are_rejected(a, v, t):
    with pytest.raises(ValueError):
        all_anchor_linearity_conditions(a, v, t)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_overlapping_cnot_dag_carry_fanout_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_overlapping_cnot_dag_carry_fanout_obstruction.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_overlapping_cnot_dag_carry_fanout_obstruction_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
