import json
import math

from self_dual_wreath_latent_master_polar_tradeoff import (
    audit_latent_master_tradeoff,
    latent_master_scaling_record,
    run_latent_master_polar_tradeoff,
    write_latent_master_polar_tradeoff_report,
)


TARGET = (2, 1)
LABELS = (((3,), (2, 1)), ((2, 1), (1, 1, 1)))


def test_zero_master_weight_places_all_cost_in_graph_polar() -> None:
    control = audit_latent_master_tradeoff(
        "ZERO-MASTER",
        TARGET,
        LABELS,
        0.0,
        1.0,
    )
    assert abs(control.minimum_orientation_branch_probability - 1.0) < 1e-12
    assert abs(control.spectral_flattening_gain - 1.0) < 1e-12
    assert abs(
        control.graph_polar_threshold_scale
        - control.direct_normalized_analyzer_polar_scale
    ) < 1e-12
    assert control.exact_latent_master_tradeoff_verified


def test_unit_master_weight_regularizes_graph_but_suppresses_output() -> None:
    control = audit_latent_master_tradeoff(
        "UNIT-MASTER",
        TARGET,
        LABELS,
        1.0,
        1.0,
    )
    assert control.graph_polar_threshold_scale < (
        control.direct_normalized_analyzer_polar_scale
    )
    assert control.minimum_orientation_branch_probability < 0.5
    assert control.spectral_flattening_gain > 1.0
    assert control.combined_graph_and_flattening_scale > (
        control.direct_normalized_analyzer_polar_scale
    )


def test_graph_polar_and_flattened_orientation_formulas_are_exact() -> None:
    control = audit_latent_master_tradeoff(
        "FORMULA",
        (2, 2),
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        0.125,
        1.0,
    )
    assert control.graph_polar_formula_residual < 3e-15
    assert control.flattened_orientation_polar_residual < 3e-15
    assert control.tradeoff_product_identity_residual < 2e-15
    assert control.exact_latent_master_tradeoff_verified


def test_combined_cost_ratio_depends_only_on_flag_weights() -> None:
    control = audit_latent_master_tradeoff(
        "WEIGHT-RATIO",
        TARGET,
        LABELS,
        0.75,
        1.25,
    )
    expected = math.hypot(0.75, 1.25) / 1.25
    observed = (
        control.combined_graph_and_flattening_scale
        / control.direct_normalized_analyzer_polar_scale
    )
    assert abs(observed - expected) < 1e-12
    assert observed >= 1.0


def test_flat_scaling_benchmark_retains_factorial_half_exponent() -> None:
    record = latent_master_scaling_record(16)
    assert abs(
        record.best_latent_master_scale_log2_lower_bound
        - record.direct_normalized_analyzer_scale_log2
    ) < 1e-12
    assert record.best_latent_master_scale_log2_lower_bound > 20
    assert not record.constant_graph_condition_and_constant_output_possible
    assert not record.master_weight_improves_generic_query_exponent
    assert record.representation_specific_direct_bypass_open
    assert not record.complete_orientation_polar_compiled


def test_report_preserves_access_model_scope_and_false_claim_gates() -> None:
    report = run_latent_master_polar_tradeoff()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_count"] == 9
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["minimum_combined_to_direct_scale_ratio"] == 1.0
    assert report.claim_gate["latent_graph_polar_formula_proved"]
    assert report.claim_gate["conditioning_postselection_product_tradeoff_proved"]
    assert not report.claim_gate["latent_master_improves_generic_analyzer_query_exponent"]
    assert not report.claim_gate["representation_specific_direct_bypass_rejected"]
    assert not report.claim_gate["direct_rectangular_cs_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_records_tradeoff_without_algorithm_claim(tmp_path) -> None:
    path = tmp_path / "latent_master_tradeoff.json"
    payload = write_latent_master_polar_tradeoff_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["status"] == "latent-master-polar-normalization-tradeoff-proved"
    assert stored["headline_metrics"]["latent_master_tradeoff_theorem_count"] == 1
    assert stored["headline_metrics"]["direct_rectangular_cs_compiler_count"] == 0
    assert stored["headline_metrics"]["new_quantum_algorithm_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
