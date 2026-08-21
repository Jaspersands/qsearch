from functools import lru_cache

import numpy as np
import pytest

from self_dual_wreath_component_polar_physical_pgm_closure import (
    _projector_analysis_system,
    audit_physical_pgm_closure,
    coherent_approximation_control,
    pgm_closure_scaling_record,
    physical_pgm_coisometry_normal_form,
    run_component_polar_physical_pgm_closure,
)


@lru_cache(maxsize=1)
def _report():
    return run_component_polar_physical_pgm_closure()


@pytest.mark.parametrize(
    ("seed", "carrier", "count", "rank", "extra"),
    [
        (5201, 4, 2, 1, 2),
        (5213, 5, 4, 2, 3),
        (5227, 6, 8, 3, 4),
    ],
)
def test_orientation_polar_exactly_closes_physical_pgm_coisometry(
    seed: int,
    carrier: int,
    count: int,
    rank: int,
    extra: int,
) -> None:
    analysis, row_copy = _projector_analysis_system(
        seed,
        carrier_dimension=carrier,
        orientation_count=count,
        projector_rank=rank,
        row_copy_extra_dimension=extra,
    )
    row = audit_physical_pgm_closure(
        f"CONTROL-{seed}",
        analysis,
        row_copy,
        count,
    )

    assert row.exact_orientation_polar_closes_physical_pgm_verified
    assert row.physical_analysis_gram_residual <= 1e-8
    assert row.exact_pgm_coisometry_identity_residual <= 1e-8


def test_physical_pgm_normal_form_returns_same_coisometry_two_ways() -> None:
    analysis, row_copy = _projector_analysis_system(
        5237,
        carrier_dimension=5,
        orientation_count=4,
        projector_rank=2,
        row_copy_extra_dimension=5,
    )
    physical, polar, pgm, transferred = physical_pgm_coisometry_normal_form(
        analysis,
        row_copy,
        4,
    )

    np.testing.assert_allclose(pgm, transferred, atol=1e-9)
    np.testing.assert_allclose(
        physical @ physical.conj().T,
        analysis.conj().T @ analysis / 4,
        atol=1e-9,
    )
    np.testing.assert_allclose(
        polar.conj().T @ polar,
        np.eye(analysis.shape[1]),
        atol=1e-9,
    )


def test_coherent_map_error_bounds_final_event_probability() -> None:
    control = coherent_approximation_control(0.31)

    assert control.event_difference_bound_verified
    assert control.exact_map_isometry_residual <= 1e-12
    assert control.approximate_map_isometry_residual <= 1e-12
    assert control.witness_event_probability_difference <= control.map_operator_error


def test_information_threshold_error_budget_preserves_constant_success() -> None:
    record = pgm_closure_scaling_record(64)

    assert record.ideal_pgm_success_lower_bound >= 0.5
    assert record.allowed_total_coherent_compiler_error == pytest.approx(1 / 8)
    assert record.robust_pgm_success_lower_bound >= 3 / 8
    assert record.uniform_per_level_error_budget == pytest.approx(
        1 / (8 * record.tree_level_count)
    )
    assert record.robust_constant_success_conditional_on_polar_compiler
    assert not record.complete_orientation_polar_compiled


def test_report_removes_only_the_separate_post_polar_decoder_gate() -> None:
    report = _report()

    assert report.headline_metrics[
        "orientation_polar_to_physical_pgm_closure_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "complete_orientation_polar_suffices_for_physical_pgm"
    ]
    assert report.claim_gate["physical_output_intertwiner_compiled_conditionally"]
    assert not report.claim_gate[
        "separate_post_polar_hidden_label_decoder_required"
    ]
    assert not report.claim_gate[
        "component_labels_may_be_measured_during_recursive_compilation"
    ]
    assert not report.claim_gate["complete_natural_orientation_polar_compiled"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
