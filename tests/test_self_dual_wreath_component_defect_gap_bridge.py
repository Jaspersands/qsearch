import math

import numpy as np
import pytest

from self_dual_wreath_component_defect_gap_bridge import (
    audit_component_defect_gap,
    coordinate_component_defect_gap_lower_bound,
    jacobi_defect_gap_scaling_record,
    run_component_defect_gap_bridge,
)


def test_balanced_projective_povm_has_exact_full_rank_defect_gap() -> None:
    effects = tuple(
        np.diag([float(index == outcome) for index in range(4)]).astype(complex)
        for outcome in range(4)
    )
    control = audit_component_defect_gap("projective", effects)
    assert control.exact_defect_gap_bound_verified
    assert control.component_traces_balanced
    assert control.positive_full_rank_defect_certified
    assert control.minimum_positive_component_eigenvalue == pytest.approx(1.0)
    assert control.theorem_defect_gap_lower_bound == pytest.approx(0.75)
    assert control.observed_defect_minimum_eigenvalue == pytest.approx(0.75)
    assert control.observed_defect_maximum_eigenvalue == pytest.approx(0.75)


def test_noncommuting_trine_povm_saturates_balanced_gap_bound() -> None:
    effects = []
    for index in range(3):
        angle = 2 * math.pi * index / 3
        vector = np.asarray([[math.cos(angle)], [math.sin(angle)]], dtype=complex)
        effects.append((2 / 3) * vector @ vector.conj().T)
    control = audit_component_defect_gap("trine", tuple(effects))
    assert control.exact_defect_gap_bound_verified
    assert control.positive_full_rank_defect_certified
    assert control.theorem_defect_gap_lower_bound == pytest.approx(1 / 3)
    assert control.observed_defect_minimum_eigenvalue == pytest.approx(1 / 3)


def test_small_edge_control_respects_bound_without_false_certificate() -> None:
    epsilon = 1e-4
    first = np.diag([epsilon, 0.5]).astype(complex)
    control = audit_component_defect_gap(
        "small-edge",
        (first, np.eye(2) - first),
    )
    assert control.exact_defect_gap_bound_verified
    assert control.theorem_defect_gap_lower_bound < 0
    assert not control.positive_full_rank_defect_certified


def test_sparse_jacobi_bridge_predicts_constant_aggregate_gap() -> None:
    coarse = jacobi_defect_gap_scaling_record(0.625, 64)
    fine = jacobi_defect_gap_scaling_record(0.625, 65536)
    assert fine.positive_full_rank_defect_predicted
    assert fine.balanced_defect_gap_lower_bound > 0.61
    assert fine.balanced_defect_gap_lower_bound > coarse.balanced_defect_gap_lower_bound
    assert fine.coordinate_cauchy_defect_gap_lower_bound > 0.60
    assert not fine.natural_jacobi_edge_transfer_proved


def test_coordinate_block_rank_bound_removes_trace_balance_requirement() -> None:
    bound = coordinate_component_defect_gap_lower_bound(
        0.6,
        640,
        (10,) * 64,
    )
    assert bound == pytest.approx(0.6 - 2 / 64 + 1 / 64)
    assert bound > 0.58


def test_report_keeps_natural_premises_and_algorithm_gates_open() -> None:
    report = run_component_defect_gap_bridge()
    assert report.claim_gate[
        "positive_component_edge_implies_aggregate_defect_gap"
    ]
    assert not report.claim_gate[
        "balanced_many_outcome_trace_dilutes_aggregate_defect_gap"
    ]
    assert report.claim_gate[
        "coordinate_block_dimensions_replace_trace_balance_premise"
    ]
    assert report.claim_gate[
        "haar_jacobi_sparse_support_predicts_constant_defect_gap"
    ]
    assert not report.claim_gate["natural_component_positive_edge_proved"]
    assert not report.claim_gate[
        "natural_component_block_to_fiber_aspects_controlled"
    ]
    assert not report.claim_gate[
        "natural_component_defect_full_rank_on_positive_mass_proved"
    ]
    assert not report.claim_gate["regular_master_central_support_controlled"]
    assert not report.claim_gate["natural_component_support_select_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
