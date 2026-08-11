import math

from diagram_multiplicity_source_mass_gate import (
    brauer_regular_mass_control,
    multiplicity_signal_scaling,
    run_diagram_multiplicity_source_mass_gate,
    write_diagram_multiplicity_source_mass_gate,
)


def test_brauer_regular_sector_masses_normalize_exactly():
    for diagram_order in (2, 4, 8, 12, 16):
        row = brauer_regular_mass_control(diagram_order)
        assert row.exact_regular_normalization_verified
        assert row.regular_mass_sum_residual < 1e-15
        assert math.isclose(row.regular_mass_sum, 1.0, abs_tol=1e-14)
        assert row.minimum_sector_dimension == 1
        assert row.one_dimensional_sector_count >= 2


def test_rarest_regular_sector_has_search_and_sampling_exponents():
    row = brauer_regular_mass_control(12)
    assert math.isclose(
        row.sample_copies_for_rarest_sector_log2,
        row.algebra_dimension_log2,
        abs_tol=1e-12,
    )
    assert math.isclose(
        row.coherent_queries_for_rarest_sector_log2,
        0.5 * row.algebra_dimension_log2,
        abs_tol=1e-12,
    )


def test_source_mass_gate_separates_polynomial_and_exponential_regimes():
    polynomial = multiplicity_signal_scaling(
        64,
        ambient_module_dimension_log2=30.0,
        target_irrep_dimension_log2=12.0,
    )
    exponential = multiplicity_signal_scaling(
        64,
        ambient_module_dimension_log2=4096.0,
        target_irrep_dimension_log2=12.0,
    )
    assert polynomial.polynomial_coherent_detection
    assert polynomial.polynomial_direct_sampling
    assert not exponential.polynomial_coherent_detection
    assert not exponential.polynomial_direct_sampling
    assert math.isclose(
        exponential.coherent_detection_query_log2,
        0.5 * exponential.direct_sample_copy_log2,
    )


def test_report_records_dequantization_and_counting_class_boundaries():
    report = run_diagram_multiplicity_source_mass_gate()
    assert report.headline_metrics["finite_brauer_control_failure_count"] == 0
    assert report.headline_metrics["rare_sector_coherent_obstruction_count"] > 0
    assert not report.claim_gate[
        "counting_class_membership_implies_bqp_algorithm"
    ]
    assert not report.claim_gate[
        "recent_classical_dequantization_baselines_passed"
    ]


def test_report_writes_and_keeps_candidate_rejected(tmp_path):
    payload = write_diagram_multiplicity_source_mass_gate(
        tmp_path / "report.json"
    )
    assert payload["headline_metrics"]["source_mass_query_gate_theorem_count"] == 1
    assert not payload["claim_gate"][
        "diagram_module_spectral_candidate_passes_proof_gate"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
