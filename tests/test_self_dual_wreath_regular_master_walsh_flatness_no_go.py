import json

import numpy as np
import pytest

from self_dual_wreath_regular_master_walsh_flatness_no_go import (
    audit_regular_walsh_flatness,
    cyclic_regular_orientation_projectors,
    native_polar_walsh_probabilities,
    regular_walsh_flatness_theorem,
    regular_walsh_mode_energy_formula,
    run_regular_master_walsh_flatness_no_go,
    walsh_modes,
    walsh_truncation_scaling_record,
    write_regular_master_walsh_flatness_report,
)


def test_regular_orientation_projectors_are_exact() -> None:
    projectors = cyclic_regular_orientation_projectors(3, (0, 1), 2)
    assert len(projectors) == 4
    assert all(
        np.linalg.norm(projector @ projector - projector, ord=2) <= 1e-10
        for projector in projectors
    )
    with pytest.raises(ValueError):
        cyclic_regular_orientation_projectors(3, (0,), 0)


def test_every_nonzero_walsh_mode_has_the_same_exact_energy() -> None:
    control = audit_regular_walsh_flatness("C3-CONTROL", 3, (0, 1), 2)
    assert control.exact_regular_walsh_flatness_verified
    assert control.minimum_nonzero_mode_energy == pytest.approx(
        control.predicted_nonzero_mode_energy
    )
    assert control.maximum_nonzero_mode_energy == pytest.approx(
        control.predicted_nonzero_mode_energy
    )
    assert control.maximum_mode_energy_formula_residual <= 1e-9


def test_parseval_energy_formula_matches_projector_rank() -> None:
    projectors = cyclic_regular_orientation_projectors(2, (0, 1), 3)
    modes = walsh_modes(projectors)
    constant, nonzero, rank = regular_walsh_mode_energy_formula(2, 2, 3)
    energies = [np.linalg.norm(mode, ord="fro") ** 2 for mode in modes]
    assert energies[0] == pytest.approx(constant)
    assert energies[1:] == pytest.approx([nonzero] * 7)
    assert sum(energies) == pytest.approx(rank)


def test_native_exact_polar_output_equals_normalized_mode_energy() -> None:
    projectors = cyclic_regular_orientation_projectors(3, (1,), 2)
    modes = walsh_modes(projectors)
    probabilities = native_polar_walsh_probabilities(projectors)
    _, _, rank = regular_walsh_mode_energy_formula(3, 1, 2)
    expected = [np.linalg.norm(mode, ord="fro") ** 2 / rank for mode in modes]
    assert probabilities == pytest.approx(expected, abs=1e-10)
    assert sum(probabilities) == pytest.approx(1.0)


def test_factorial_schedule_rejects_fixed_sparse_and_low_degree_modes() -> None:
    small = walsh_truncation_scaling_record(16)
    large = walsh_truncation_scaling_record(128)
    assert large.best_fixed_polynomial_mode_retained_probability < (
        small.best_fixed_polynomial_mode_retained_probability
    )
    assert large.quarter_degree_retained_probability < small.quarter_degree_retained_probability
    assert large.minimum_mode_fraction_for_ninety_percent >= 0.899
    assert not large.fixed_polynomial_mode_truncation_retains_constant_mass
    assert not large.fixed_quarter_degree_truncation_retains_constant_mass
    assert not large.source_adaptive_sparse_mode_no_go_proved


def test_report_preserves_dense_and_adaptive_route_boundaries() -> None:
    theorem = regular_walsh_flatness_theorem()
    report = run_regular_master_walsh_flatness_no_go()
    assert theorem.theorem_verified
    assert report.claim_gate["regular_source_walsh_mode_energy_flatness_proved"]
    assert report.claim_gate["native_exact_polar_walsh_output_law_proved"]
    assert report.claim_gate["fixed_polynomial_walsh_mode_truncation_rejected"]
    assert not report.claim_gate["frame_F_requires_dense_walsh_storage"]
    assert not report.claim_gate["dense_walsh_transform_hardness_proved"]
    assert not report.claim_gate["source_label_adaptive_sparse_mode_router_rejected"]
    assert not report.claim_gate["complete_natural_orientation_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_preserves_claim_gates(tmp_path) -> None:
    path = tmp_path / "regular-walsh.json"
    payload = write_regular_master_walsh_flatness_report(path)
    loaded = json.loads(path.read_text())
    assert loaded == payload
    assert loaded["headline_metrics"]["finite_control_failure_count"] == 0
    assert loaded["headline_metrics"]["exact_regular_walsh_energy_theorem_count"] == 1
    assert loaded["headline_metrics"]["source_adaptive_sparse_mode_no_go_count"] == 0
    assert loaded["headline_metrics"]["complete_orientation_polar_compiler_count"] == 0
    assert loaded["headline_metrics"]["new_quantum_algorithm_count"] == 0
