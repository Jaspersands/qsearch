"""Pytest suite for `theorems/planted_qary_offset_pair_mass_frontier_audit.py`."""

from __future__ import annotations

from fractions import Fraction
import json
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.planted_qary_offset_pair_mass_frontier_audit import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    audit_planted_instance_offset_pair_mass_frontier,
    build_planted_qary_offset_pair_mass_frontier_audit_report,
    compute_dyadic_f1_schedule,
    conditional_geometry_obligation,
    same_colour_collision_counterexample,
    worst_case_box_l1_ceiling,
    worst_case_multiplicative_box_survival,
)


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = ROOT / "research" / "certificates" / "planted_qary_offset_pair_mass_frontier_audit_crosscheck.js"


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "planted-qary-offset-pair-mass-frontier-audit-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    ("n", "m", "s", "s_F"),
    [
        (4, 2, 3, 2),
        (6, 3, 4, 2),
        (8, 4, 6, 3),
        (12, 6, 8, 4),
        (16, 8, 10, 5),
        (32, 16, 18, 9),
    ],
)
def test_dyadic_f1_schedule_certifies_multiplicative_and_additive_bounds(
    n: int, m: int, s: int, s_F: int
) -> None:
    sched = compute_dyadic_f1_schedule(n=n, m=m, s=s, s_F=s_F)
    assert sched["multiplicative_bound_within_f1_budget"] is True
    assert sched["additive_bound_within_f1_budget"] is True
    m_box = sched["M_box"]
    l_box = worst_case_box_l1_ceiling(m, s_F)
    p_box_min = worst_case_multiplicative_box_survival(m_box, m, s_F)
    assert p_box_min >= Fraction(m_box - l_box, m_box)


def test_planted_instance_frontier_holds_across_dimensions_and_moduli() -> None:
    rows = audit_planted_instance_offset_pair_mass_frontier()
    assert len(rows) == 8
    for row in rows:
        assert row["theorem_1_cube_survival_enclosure_holds"] is True
        assert row["theorem_2_box_survival_lower_bound_holds"] is True
        assert row["theorem_3_partner_failure_budget_bound_verified"] is True
        assert row["source_bad_register_rate_certified"] is False
        assert row["source_bad_register_rate"] is None
        assert row["geometry_obligation"]["conditional_geometry_inequalities_satisfied"] is False
        assert row["schedule_and_hitting_trial_selected_with_private_witness"] is True


def test_partner_budget_does_not_imply_valid_dcp_source() -> None:
    row = same_colour_collision_counterexample()
    assert row["partner_budget_inequality_passes"] is True
    assert row["two_point_source_promise_falsified"] is True
    assert row["same_colour_collision_verified"] is True
    assert row["distinct_positions"][0] != row["distinct_positions"][1]
    assert row["cells"][0] == row["cells"][1] == [-1, -1, 0]
    assert row["schedule"]["source_bad_register_rate_certified"] is False


def test_geometry_gate_is_strict_and_does_not_certify_supplied_promise() -> None:
    assert conditional_geometry_obligation(3, 4, 5, 27)["conditional_geometry_inequalities_satisfied"] is False
    conditional = conditional_geometry_obligation(3, 4, 5, 28)
    assert conditional["conditional_geometry_inequalities_satisfied"] is True
    assert conditional["source_geometry_certified"] is False
    assert conditional["nonparallel_norm_lower_bound_verified"] is False
    assert conditional_geometry_obligation(3, 4, 3, 28)["collinear_exclusion_inequality_satisfied"] is False


@pytest.mark.parametrize("value", [True, 3.0, "3"])
def test_schedule_rejects_implicit_numeric_coercions(value) -> None:
    with pytest.raises(ValueError):
        compute_dyadic_f1_schedule(value, 1, 3, 2)


@pytest.mark.parametrize("tamper", ["geometry", "rate", "collision", "guardrail"])
def test_crosscheck_rejects_false_source_promotion_or_collision(tmp_path, tamper: str) -> None:
    report = json.loads(ARTIFACT_PATH.read_text())
    if tamper == "geometry":
        report["planted_instance_frontier_audit"][0]["geometry_obligation"]["source_geometry_certified"] = True
    elif tamper == "rate":
        report["planted_instance_frontier_audit"][0]["source_bad_register_rate"] = "0/1"
    elif tamper == "collision":
        report["source_geometry_counterexample"]["distinct_positions"][1] = [0, 0, 2]
    else:
        report["guardrails"]["unconditional_dcp_bad_register_budget_certified"] = True
    path = tmp_path / "tampered.json"
    path.write_text(json.dumps(report))
    proc = subprocess.run(["node", str(CROSSCHECK_JS), str(path)], capture_output=True, text=True)
    assert proc.returncode != 0


def test_report_and_nodejs_crosscheck() -> None:
    report = build_planted_qary_offset_pair_mass_frontier_audit_report()
    assert all(report["verification"].values())
    assert ARTIFACT_PATH.exists()
    saved = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert saved == report

    proc = subprocess.run(
        ["node", str(CROSSCHECK_JS)],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["status"] == "ok"
    assert payload["instances_verified"] == 8


def test_cli_execution() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "theorems.planted_qary_offset_pair_mass_frontier_audit", "--no-write"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "planted_qary_offset_pair_mass_frontier_audit"
    assert all(out["verification"].values())
