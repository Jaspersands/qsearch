"""Tests for theorems/jet_tuple_oracle_central_descent_audit.py (Milestone 23)."""
from __future__ import annotations

import json
import pytest

from theorems.jet_tuple_oracle_central_descent_audit import (
    JSON_PATH,
    MD_PATH,
    build_jet_tuple_oracle_central_descent_report,
    render_markdown,
    unrolled_tuple_oracle_arbitrary_h_solve,
    verify_nondestructive_central_instrument_vs_dropped_phase,
    verify_tuple_oracle_to_abelian_recovery,
)
from theorems.nonabelian_jet_homogenization import PolynomialJetGroup
from theorems.right_abelian_induced_source import upper_triangular_lie
from theorems.ut5_matrix_phase_alignment import _identity


def test_nondestructive_central_instrument_vs_dropped_phase() -> None:
    res = verify_nondestructive_central_instrument_vs_dropped_phase(p=7, degree_d=2)
    assert res["group_size_G"] == 343
    assert res["quotient_size_Q"] == 49
    assert res["discarded_zero_scale_slots"] == 1
    assert res["nondestructive_vs_target_frobenius_error"] < 1e-13
    assert res["nondestructive_vs_twisted_quotient_frobenius_error"] < 1e-13
    assert res["dropped_phase_fallacy_frobenius_error"] > 0.1
    assert res["non_preserved_subgroup_surviving_support_size"] == 1
    assert res["preserved_subgroup_support_size"] == 7


def test_tuple_oracle_to_abelian_recovery_without_curve_fixture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _forbidden_curve(*args: object, **kwargs: object) -> None:
        raise AssertionError("normalized_curve_fixture must never be called")

    monkeypatch.setattr(PolynomialJetGroup, "normalized_curve_fixture", _forbidden_curve)
    res = verify_tuple_oracle_to_abelian_recovery(p=5)
    assert res["simplex_queries_ell"] == 4
    assert res["jet_dimension"] == 4
    assert res["terminal_abelian_dimension_m_plus_r1"] == 5
    assert res["hf_subgroup_size"] == 5
    assert res["dilation_invariant_all_nonzero_scales"] is True
    assert res["recovered_quotient_image_U_generator"] == [1, 2]


def test_unrolled_tuple_oracle_arbitrary_h_solve_and_lie_closure() -> None:
    report = build_jet_tuple_oracle_central_descent_report()
    u7 = report["unrolled_ut7_arbitrary_h_rebuild_trace"]
    assert u7["status"] == "SUCCESS"
    assert u7["rebuilt_tuple_oracle_calls"] == 5
    assert u7["abelian_base_calls"] == 3
    assert False in u7["n_in_normalizer_flags"]
    assert u7["recovered_generator_count"] == 2
    # Verify that rebuilt weights strictly shrink across the restriction steps
    weights_seq = [row["rebuilt_weights"] for row in u7["rebuilt_chart_log"]]
    assert len(weights_seq[0]) > len(weights_seq[1])


def test_unrolled_tuple_oracle_aborts_on_non_dropping_preimage() -> None:
    p = 11
    ut4, slots4 = upper_triangular_lie(4, p)
    std4 = _identity(len(slots4))
    # Return the full quotient section so preimage_T == S and class does not drop -> must ABORT!
    trace = unrolled_tuple_oracle_arbitrary_h_solve(
        ut4,
        std4,
        abelian_base_oracle=lambda alg, span, lift: [],
        transverse_tuple_image_oracle=lambda alg, plan, lift: list(plan.certificate.section_basis),
    )
    assert trace.status == "ABORT"
    assert trace.abort_reason == "PREIMAGE_CLASS_DID_NOT_DROP"


def test_written_artifacts_match_report_schema() -> None:
    report = build_jet_tuple_oracle_central_descent_report()
    assert report["schema_version"] == "jet_tuple_oracle_central_descent_audit_v1"
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Deterministic Tuple-Oracle to Nondestructive Central-Character Descent" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "jet_tuple_oracle_central_descent_audit_v1"
    if MD_PATH.exists():
        assert "accepted_speedup_candidate" in MD_PATH.read_text(encoding="utf-8")
