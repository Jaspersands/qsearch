"""Tests for theorems/full_jet_complement_and_weighted_pullback_audit.py (Milestone 20)."""
from __future__ import annotations

import json
import pytest

from theorems.class_three_monomial_jet import ClassThreeStructure, FullTaylorJetChart, align_full_jet
from theorems.full_jet_complement_and_weighted_pullback_audit import (
    JSON_PATH,
    MD_PATH,
    build_full_jet_complement_and_weighted_pullback_report,
    construct_alternative_complement_alignment,
    render_markdown,
    verify_full_jet_complement_and_phase_pullback_law,
    verify_weighted_triangular_matrix_and_merged_character_law,
)


@pytest.mark.parametrize("p", [11, (1 << 127) - 1])
def test_full_jet_complement_and_phase_pullback_law(p: int) -> None:
    res = verify_full_jet_complement_and_phase_pullback_law(p=p, degree=2)
    assert res["carrier_width_R"] == 12
    assert res["jet_width_J"] == 6
    assert res["spectator_width_S"] == 6
    assert res["residual_kernel_checks_passed"] == 10
    assert res["pivot_complement_exact_matches"] == 16
    assert res["stale_complement_phase_mismatches"] > 0
    assert res["updated_complement_phase_matches"] == 16


def test_construct_alternative_complement_alignment_rejects_singular_shear() -> None:
    p = 11
    st = ClassThreeStructure(
        p,
        (((0, 1), (p - 1, 0)),),
        (((0, 0), (0, 0)),),
        (((1,), (0,)),),
    )
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=2, degree=2)
    align1 = align_full_jet(chart, st, [(1,), (2,), (3,), (4,)], [1, 1, 2, 2], [(0,), (1,), (0,), (2,)])
    singular_s = [[0] * 6 for _ in range(6)]
    with pytest.raises(ValueError, match="invertible"):
        construct_alternative_complement_alignment(align1, singular_s)


@pytest.mark.parametrize("p,degree", [(17, 2), ((1 << 127) - 1, 3)])
def test_weighted_triangular_matrix_and_merged_character_law(p: int, degree: int) -> None:
    res = verify_weighted_triangular_matrix_and_merged_character_law(p=p, degree=degree)
    assert res["hdiag_verified"] is True
    assert res["hupper_verified"] is True
    assert res["entry_on_or_above_verified"] is True
    assert res["merged_character_exponent_matches"] == 12
    assert res["constant_after_weight_one_verified"] is True
    assert res["equal_weight_perturbation_diagonal_matches"] is True
    assert res["equal_weight_perturbation_rejected_by_merge"] is True


def test_written_artifacts_match_report_schema() -> None:
    report = build_full_jet_complement_and_weighted_pullback_report()
    assert report["schema_version"] == "full_jet_complement_and_weighted_pullback_audit_v1"
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Public Full-Jet Complement Pullback" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "full_jet_complement_and_weighted_pullback_audit_v1"
    if MD_PATH.exists():
        assert "accepted_speedup_candidate" in MD_PATH.read_text(encoding="utf-8")
