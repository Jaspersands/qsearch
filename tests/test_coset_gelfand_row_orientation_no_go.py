import math

import numpy as np

from coset_gelfand_row_orientation_no_go import (
    gelfand_row_intertwiner,
    perfect_matching_orientation_scaling,
    row_orientation_control,
    run_gelfand_row_orientation_no_go,
    write_gelfand_row_orientation_no_go,
)


def test_block_intertwiner_has_the_expected_shape_and_norm():
    row = np.array([1.0, 2.0j, -3.0], dtype=np.complex128)
    block = gelfand_row_intertwiner(4, 3, 0.64, row)
    assert block.shape == (4, 12)
    singular = np.linalg.svd(block, compute_uv=False)
    assert np.allclose(singular, 0.8)


def test_orthogonal_rows_share_output_gram_and_singular_data():
    control = row_orientation_control("CONTROL", 3, 4, 0.73, 1123)
    assert control.orientation_blindness_verified
    assert control.shared_output_gram_residual < 1e-11
    assert control.shared_singular_spectrum_residual < 1e-11
    assert control.inverse_row_overlap < 1e-11
    assert control.carrier_algebra_observable_residual < 1e-11
    assert math.isclose(
        control.commutant_orientation_witness_gap,
        2.0,
        abs_tol=1e-11,
    )
    assert math.isclose(
        control.physical_support_operator_distance,
        control.singular_value_squared,
        abs_tol=1e-11,
    )


def test_perfect_matching_scaling_keeps_dimension_claim_nonalgorithmic():
    for degree in (8, 16, 32, 64):
        row = perfect_matching_orientation_scaling(degree)
        assert int(row.minimum_physical_multiplicity_decimal) == math.factorial(
            degree
        )
        assert not row.outcome_gram_determines_row_orientation
        assert not row.source_specific_row_constraint_derived
        assert not row.classically_checkable_row_observable_constructed
        assert not row.polynomial_hidden_involution_decoder_constructed


def test_report_preserves_the_pgm_specific_open_route():
    report = run_gelfand_row_orientation_no_go()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["orthogonal_row_counterexample_count"] == 3
    assert report.claim_gate["source_specific_pgm_row_structure_still_open"]
    assert not report.claim_gate[
        "group_action_algebra_can_verify_inverse_row_orientation"
    ]
    assert report.claim_gate["commutant_or_source_specific_operation_required"]
    assert not report.claim_gate["natural_pgm_row_orientation_classified"]


def test_report_keeps_all_algorithm_claims_closed():
    report = run_gelfand_row_orientation_no_go()
    assert not report.claim_gate["row_state_verifier_constructed"]
    assert not report.claim_gate["polynomial_hidden_involution_decoder_constructed"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writes_json_artifact(tmp_path):
    payload = write_gelfand_row_orientation_no_go(tmp_path / "report.json")
    assert payload["headline_metrics"]["finite_control_failure_count"] == 0
    assert (tmp_path / "report.json").is_file()
