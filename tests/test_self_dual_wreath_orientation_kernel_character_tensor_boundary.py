from __future__ import annotations

import json

from self_dual_wreath_orientation_fourier_reduction import _w4_collision_free_labels
from self_dual_wreath_orientation_kernel_character_tensor_boundary import (
    audit_character_tensor_kernel,
    character_tensor_scaling,
    run_character_tensor_boundary,
    simultaneous_pair_orbit_count_direct,
    simultaneous_pair_orbit_count_formula,
    write_character_tensor_boundary_report,
)


THRESHOLD = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_character_tensor_formula_matches_projector_overlap_kernel() -> None:
    s3 = audit_character_tensor_kernel(
        3,
        (2, 1),
        THRESHOLD,
        control_id="s3",
    )
    assert s3.character_tensor_formula_residual < 1e-9
    assert s3.hermiticity_residual < 1e-9
    assert s3.minimum_kernel_eigenvalue >= -1e-9

    s4 = audit_character_tensor_kernel(
        4,
        (2, 2),
        _w4_collision_free_labels()[0],
        control_id="s4",
    )
    assert s4.character_tensor_formula_residual < 1e-9


def test_simultaneous_pair_orbit_burnside_formula_is_exact() -> None:
    assert simultaneous_pair_orbit_count_formula(3) == 11
    assert simultaneous_pair_orbit_count_formula(4) == 43
    assert simultaneous_pair_orbit_count_direct(3) == 11
    assert simultaneous_pair_orbit_count_direct(4) == 43


def test_boolean_walsh_diagonalization_is_not_universal() -> None:
    control = audit_character_tensor_kernel(
        3,
        (2, 1),
        THRESHOLD,
        control_id="walsh",
    )
    assert control.boolean_translation_invariance_residual > 0.1
    assert control.walsh_offdiagonal_frobenius_norm > 0.1
    assert not control.boolean_walsh_diagonalization_valid


def test_orientation_kernel_has_nonproduct_operator_schmidt_rank() -> None:
    control = audit_character_tensor_kernel(
        3,
        (2, 1),
        THRESHOLD,
        control_id="schmidt",
    )
    assert control.operator_schmidt_ranks == (4, 4)
    assert control.operator_schmidt_ranks == (
        control.operator_schmidt_maximum_possible_ranks
    )
    assert not control.product_orientation_kernel_valid


def test_local_character_factors_have_no_fixed_simultaneous_eigenbasis() -> None:
    control = audit_character_tensor_kernel(
        4,
        (2, 2),
        _w4_collision_free_labels()[0],
        control_id="local-basis",
    )
    assert control.maximum_local_character_factor_commutator_norm > 1
    assert not control.fixed_local_simultaneous_diagonalization_valid


def test_pair_orbit_enumeration_remains_factorial() -> None:
    row = character_tensor_scaling(512)
    assert row.log2_raw_character_pair_summand_count > 7000
    assert row.log2_simultaneous_pair_orbit_count_lower_bound > 3000
    assert not row.simultaneous_conjugacy_orbit_enumeration_polynomial
    assert not row.internal_kronecker_multiplicity_transform_compiled


def test_report_redirects_to_global_recoupling_without_overclaiming() -> None:
    report = run_character_tensor_boundary()
    assert report.theorem.theorem_verified
    assert report.claim_gate[
        "orientation_kernel_character_tensor_network_identified"
    ]
    assert not report.claim_gate["boolean_walsh_diagonalization_is_universal"]
    assert not report.claim_gate["product_orientation_transform_is_universal"]
    assert not report.claim_gate["fixed_local_diagonalizing_basis_exists"]
    assert not report.claim_gate["global_kronecker_racah_transform_compiled"]
    assert not report.claim_gate["actual_physical_pgm_rejected"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_character_tensor_artifact(tmp_path) -> None:
    path = tmp_path / "character-tensor-boundary.json"
    payload = write_character_tensor_boundary_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"][
        "exact_character_tensor_network_theorem_count"
    ] == 1
