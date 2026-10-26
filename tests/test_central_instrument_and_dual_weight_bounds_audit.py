"""Tests for theorems/central_instrument_and_dual_weight_bounds_audit.py (Milestone 22)."""
from __future__ import annotations

import json
import pytest

from theorems.central_instrument_and_dual_weight_bounds_audit import (
    JSON_PATH,
    MD_PATH,
    build_central_instrument_and_dual_weight_bounds_report,
    render_markdown,
    verify_central_regular_instrument_and_inversion_equivalence,
    verify_dual_weight_class_three_phase_bounds,
    verify_nontrivial_central_intersection_zero_mass_obstruction,
)
from theorems.class_three_monomial_jet import ClassThreeStructure


def test_central_regular_instrument_and_inversion_equivalence() -> None:
    res = verify_central_regular_instrument_and_inversion_equivalence(p=5)
    assert res["normal_group_size"] == 125
    assert res["carrier_size_T"] == 25
    assert res["center_size_C"] == 5
    assert res["group_model"] == "direct_product_Fp_times_Heisenberg"
    assert res["source_construction"] == "ordinary_gH_label_equality_after_public_chart"
    assert res["hidden_subgroup_closure_verified"] is True
    assert res["hidden_intersection_normal_trivial_verified"] is True
    assert res["nonlinear_public_section_verified"] is True
    assert res["ordinary_coset_label_count"] == 125
    assert res["ordinary_coset_fiber_size"] == 5
    assert res["public_chart_right_action_checks"] == 3125
    assert res["potential_is_group_homomorphism"] is False
    assert res["inversion_vs_neg_fourier_frobenius_error"] == 0.0
    assert res["instrument_completeness_frobenius_error"] < 1e-13
    assert res["max_regular_branch_frobenius_error"] < 1e-13
    assert res["max_oracle_source_frobenius_error"] < 1e-13
    assert res["sector_traces_all_labels_including_zero"] == pytest.approx([0.2] * 5)
    assert res["wrong_reducible_plancherel_d2_over_N"] == pytest.approx(5.0)


def test_nontrivial_central_intersection_zero_mass_obstruction() -> None:
    res = verify_nontrivial_central_intersection_zero_mass_obstruction(p=5)
    assert res["center_size_C"] == 25
    assert res["zero_mass_label_count"] == 20
    assert res["surviving_annihilator_label_count"] == 5
    assert res["max_zero_mass_label_probability"] < 1e-15
    assert res["surviving_label_probability"] == pytest.approx(0.2)


@pytest.mark.parametrize("p,degree", [(11, 2), (17, 3), ((1 << 127) - 1, 2)])
def test_dual_weight_class_three_phase_bounds(p: int, degree: int) -> None:
    res = verify_dual_weight_class_three_phase_bounds(p=p, degree=degree)
    assert res["attained_max_operational_weight"] == res["operational_weight_bound_max_c_3D"]
    assert res["operational_weight_bound_max_c_3D"] == 3 * degree
    assert res["attained_parameter_weights"] == [1, 2]
    assert res["central_parameters_appear_in_quadratic_parameter_lifts"] is False


def test_nonlinear_graph_is_not_subgroup_without_its_public_chart() -> None:
    p = 5
    st = ClassThreeStructure(p, (), (((0, 1), (4, 0)),), (((), ()),))
    def multiply(a, b):
        x, _, z = st.multiply_fixture((a[:2], (), a[2:]), (b[:2], (), b[2:]))
        return x+z
    def potential(q):
        return (q, q*q % p, q**3 % p)
    graph = {(q, potential(q)) for q in range(p)}
    assert (2, multiply(potential(1), potential(1))) not in graph

    # The same potential partition CAN be justified using an explicit
    # different public chart and the genuine subgroup {(q,identity)}.
    # This prevents the negative control from becoming an overbroad no-go.
    def public_section(q):
        return tuple(-a % p for a in potential(q))
    for q in range(p):
        for physical_n in [(0, 0, 0), (1, 2, 3), (4, 1, 2)]:
            chart_n = multiply(physical_n, potential(q))
            assert multiply(chart_n, public_section(q)) == physical_n


def test_written_artifacts_match_report_schema() -> None:
    report = build_central_instrument_and_dual_weight_bounds_report()
    assert report["schema_version"] == "central_instrument_and_dual_weight_bounds_audit_v2"
    assert report["scope"]["ordinary_hiding_source_and_public_chart_verified"] is True
    assert report["scope"]["full_jet_algorithm_input_premises_verified"] is False
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Complete Central Fourier Instrument" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "central_instrument_and_dual_weight_bounds_audit_v2"
        assert on_disk["central_regular_instrument_audit"]["source_construction"] == (
            "ordinary_gH_label_equality_after_public_chart")
    if MD_PATH.exists():
        assert "accepted_speedup_candidate" in MD_PATH.read_text(encoding="utf-8")
