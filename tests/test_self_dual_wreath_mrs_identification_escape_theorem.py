import json
import math

import numpy as np
import pytest

from self_dual_wreath_mrs_identification_escape_theorem import (
    identification_transfer_control,
    mrs_identification_escape_theorem,
    mrs_pgm_scaling_record,
    run_mrs_identification_escape_theorem,
    total_variation,
    transcript_identification_success,
    transcript_identification_upper_bound,
    write_mrs_identification_escape_report,
)


def test_total_variation_and_validation() -> None:
    assert total_variation(np.array([0.7, 0.3]), np.array([0.5, 0.5])) == pytest.approx(0.2)
    with pytest.raises(ValueError):
        total_variation(np.array([0.5, 0.4]), np.array([0.5, 0.5]))
    with pytest.raises(ValueError):
        total_variation(np.array([1.0, 0.0]), np.array([1.0]))


def test_fixed_hidden_tv_identification_bound_is_tight() -> None:
    control = identification_transfer_control(hidden_label_count=7, tv_radius=0.03)
    assert control.identification_transfer_bound_verified
    assert control.maximum_fixed_label_tv_distance == pytest.approx(0.03)
    assert control.decoder_identification_success == pytest.approx(1.0 / 7.0 + 0.03)
    assert control.saturation_residual <= 1e-12


def test_randomized_transcript_decoder_obeys_transfer_bound() -> None:
    reference = np.array([0.2, 0.3, 0.5])
    laws = np.array(
        [
            [0.25, 0.25, 0.5],
            [0.18, 0.35, 0.47],
            [0.2, 0.28, 0.52],
        ]
    )
    decoder = np.array(
        [
            [0.7, 0.1, 0.2],
            [0.2, 0.6, 0.2],
            [0.1, 0.2, 0.5],
        ]
    )
    success = transcript_identification_success(laws, decoder)
    exact_bound, radius_bound, maximum = transcript_identification_upper_bound(
        reference,
        laws,
    )
    assert success <= exact_bound + 1e-12
    assert exact_bound <= radius_bound + 1e-12
    assert maximum == pytest.approx(0.05)


def test_decoder_rejects_illegal_postprocessing() -> None:
    laws = np.eye(2)
    with pytest.raises(ValueError):
        transcript_identification_success(laws, np.ones((2, 2)))
    with pytest.raises(ValueError):
        transcript_identification_success(laws, np.eye(3))


def test_pgm_schedule_has_constant_margin_and_subsqrt_exponent() -> None:
    small = mrs_pgm_scaling_record(16)
    large = mrs_pgm_scaling_record(1024)
    assert small.pgm_identification_success_lower_bound >= 0.8
    assert small.robust_compiled_identification_success_lower_bound >= 0.675
    assert large.log_copy_count_over_sqrt_n < small.log_copy_count_over_sqrt_n
    assert large.copy_schedule_is_exp_o_sqrt_n
    assert not large.explicit_mrs_crossover_certified
    assert not large.complete_orientation_polar_compiled


def test_theorem_report_closes_only_the_mrs_necessity_gate() -> None:
    theorem = mrs_identification_escape_theorem()
    report = run_mrs_identification_escape_theorem()
    assert theorem.theorem_verified
    assert report.claim_gate[
        "target_physical_pgm_outside_all_mrs_transcript_postprocessings_asymptotically"
    ]
    assert report.claim_gate[
        "uniformly_accurate_constant_success_pgm_compiler_automatically_escapes_mrs"
    ]
    assert not report.claim_gate[
        "explicit_transcript_zonotope_separation_required_for_model_escape"
    ]
    assert not report.claim_gate["current_executable_complete_pgm_circuit_exists"]
    assert not report.claim_gate["complete_natural_orientation_polar_compiled"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.status == (
        "target-pgm-mrs-identification-separation-proved-polar-compiler-open"
    )


def test_report_writer_preserves_claim_boundaries(tmp_path) -> None:
    path = tmp_path / "mrs-identification.json"
    payload = write_mrs_identification_escape_report(path)
    loaded = json.loads(path.read_text())
    assert loaded == payload
    assert loaded["headline_metrics"][
        "all_policy_target_pgm_mrs_separation_theorem_count"
    ] == 1
    assert loaded["headline_metrics"]["complete_orientation_polar_compiler_count"] == 0
    assert loaded["headline_metrics"]["classical_separation_theorem_count"] == 0
    assert loaded["headline_metrics"]["new_quantum_algorithm_count"] == 0
    assert math.isclose(
        loaded["headline_metrics"]["minimum_robust_compiled_success_lower_bound"],
        min(row["robust_compiled_identification_success_lower_bound"] for row in loaded["scaling_records"]),
    )
