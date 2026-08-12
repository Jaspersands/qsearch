import json

import numpy as np

from self_dual_wreath_point_pgm_coarse_graining import (
    aggregate_by_fibers,
    audit_point_pgm_coarse_graining,
    point_pgm_coarse_graining_scaling_record,
    pretty_good_effects,
    run_point_pgm_coarse_graining,
    write_point_pgm_coarse_graining_report,
)


def test_uniform_pgm_commutes_with_equal_fiber_coarse_graining() -> None:
    states = (
        np.diag([0.8, 0.2, 0.0]),
        np.diag([0.6, 0.3, 0.1]),
        np.diag([0.1, 0.2, 0.7]),
        np.diag([0.0, 0.4, 0.6]),
    )
    fibers = ((0, 1), (2, 3))
    fine_effects, _, _ = pretty_good_effects(states)
    coarse_states = aggregate_by_fibers(states, fibers, average=True)
    coarse_effects, _, _ = pretty_good_effects(coarse_states)
    aggregated_effects = aggregate_by_fibers(
        fine_effects,
        fibers,
        average=False,
    )
    assert max(
        np.linalg.norm(observed - predicted)
        for observed, predicted in zip(coarse_effects, aggregated_effects)
    ) < 1e-10


def test_retained_joint_character_point_pgm_is_exact_coarse_graining() -> None:
    control = audit_point_pgm_coarse_graining(
        3,
        (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        ),
        control_id="TEST-W3-THRESHOLD",
    )
    assert control.exact_point_pgm_coarse_graining_verified
    assert control.maximum_coarse_state_aggregation_residual < 1e-9
    assert control.maximum_coarse_effect_aggregation_residual < 1e-9
    assert control.maximum_mapped_confusion_residual < 1e-9
    assert abs(
        control.mapped_fine_pgm_point_success
        - control.direct_point_pgm_success
    ) < 1e-9


def test_mapping_fine_output_recovers_within_fiber_errors() -> None:
    control = audit_point_pgm_coarse_graining(
        3,
        (((3,), (2, 1)),),
        control_id="TEST-W3-SINGLE",
    )
    assert control.mapped_fine_pgm_point_success >= control.fine_pgm_success
    assert control.within_fiber_error_recovery_gain > 0


def test_scaling_record_keeps_inherited_and_direct_routes_distinct() -> None:
    row = point_pgm_coarse_graining_scaling_record(64)
    assert row.reversible_point_image_evaluation_polynomial
    assert not row.child_star_square_root_required_for_inherited_route
    assert row.full_covariant_multiplicity_inverse_required
    assert not row.full_covariant_multiplicity_inverse_compiled
    assert not row.direct_coarse_bypass_ruled_out
    assert not row.polynomial_point_pgm_circuit_proved


def test_report_preserves_claim_gates() -> None:
    report = run_point_pgm_coarse_graining()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["point_pgm_equals_coarse_grained_full_pgm"]
    assert not report.claim_gate["child_star_square_root_logically_required"]
    assert not report.claim_gate["full_covariant_multiplicity_inverse_compiled"]
    assert not report.claim_gate["direct_coarse_bypass_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_emits_valid_json(tmp_path) -> None:
    path = tmp_path / "point_pgm_coarse_graining.json"
    payload = write_point_pgm_coarse_graining_report(path)
    parsed = json.loads(path.read_text())
    assert parsed["status"] == payload["status"]
    assert parsed["headline_metrics"] == payload["headline_metrics"]
    assert payload["status"] == "point-pgm-exactly-coarse-grained-full-pgm"
