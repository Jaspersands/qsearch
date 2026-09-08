from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_pair_carrier_label_contextuality import (
    audit_isotypic_compatibility,
    carrier_label_scaling_record,
    isotypic_projector_on_subset,
    run_pair_carrier_label_contextuality,
    write_pair_carrier_label_contextuality_report,
)


def test_isotypic_projector_rejects_invalid_subset_contract() -> None:
    with pytest.raises(ValueError):
        isotypic_projector_on_subset((2, 1), (2, 1), (), 3)
    with pytest.raises(ValueError):
        isotypic_projector_on_subset((2, 1), (2, 1), (0, 0), 3)
    with pytest.raises(ValueError):
        isotypic_projector_on_subset((2, 1), (2, 1), (0, 3), 3)
    with pytest.raises(ValueError):
        isotypic_projector_on_subset((2, 1), (4,), (0, 1), 3)


def test_overlapping_s3_pair_labels_are_exactly_contextual() -> None:
    row = audit_isotypic_compatibility(
        "overlap",
        (2, 1),
        (3,),
        (0, 1),
        (1, 2),
        3,
        expected_commutator=math.sqrt(3) / 4,
        expected_compression_eigenvalue=1 / 4,
    )

    assert row.exact_compatibility_audit_verified
    assert row.first_projector_rank == 2
    assert row.second_projector_rank == 2
    assert row.commutator_norm == pytest.approx(math.sqrt(3) / 4)
    assert row.nonzero_first_compression_eigenvalues == pytest.approx((0.25, 0.25))
    assert not row.sharp_nondemolition_joint_label_exists


def test_disjoint_s3_pair_labels_commute() -> None:
    row = audit_isotypic_compatibility(
        "disjoint",
        (2, 1),
        (3,),
        (0, 1),
        (2, 3),
        4,
        expected_commutator=0.0,
        expected_compression_eigenvalue=1.0,
    )

    assert row.exact_compatibility_audit_verified
    assert row.commutator_norm < 1e-12
    assert row.sharp_nondemolition_joint_label_exists
    assert row.nonzero_first_compression_eigenvalues == pytest.approx((1.0,))


def test_projector_formula_is_hermitian_and_idempotent() -> None:
    projector = isotypic_projector_on_subset((2, 1), (1, 1, 1), (0, 1), 3)

    assert np.linalg.norm(projector - projector.conj().T, ord=2) < 1e-12
    assert np.linalg.norm(projector @ projector - projector, ord=2) < 1e-12


def test_local_physical_carrier_labels_reproduce_dense_spectra() -> None:
    report = run_pair_carrier_label_contextuality()

    assert len(report.local_controls) == 3
    assert report.headline_metrics["selected_physical_star_channel_count"] == 3
    assert report.headline_metrics["maximum_local_dense_spectrum_residual"] < 1e-12
    assert all(row.local_label_compiler_verified for row in report.local_controls)
    assert all(row.local_carrier_label_query_polynomial for row in report.local_controls)
    assert all(row.multiplicity_registers_preserved for row in report.local_controls)
    assert all(not row.multiplicity_coordinates_exposed for row in report.local_controls)
    assert {
        denominator
        for row in report.local_controls
        for denominator in row.distinct_correlation_denominators
    } == {5, 9, 10}


def test_local_label_query_scales_polynomially_but_not_as_global_table() -> None:
    rows = [carrier_label_scaling_record(n) for n in (8, 32, 128, 512)]

    assert all(row.selected_triple_gpe_call_count == 7 for row in rows)
    assert all(row.selected_local_label_query_polynomial for row in rows)
    assert all(not row.all_incident_pair_labels_can_be_persistently_copied for row in rows)
    assert all(not row.global_channel_atom_label_compiled for row in rows)
    assert rows[-1].controlled_young_action_factor_count_upper_bound > rows[0].controlled_young_action_factor_count_upper_bound


def test_scaling_rejects_degree_below_the_carrier_theorem_scope() -> None:
    with pytest.raises(ValueError):
        carrier_label_scaling_record(4)


def test_report_separates_local_positive_result_from_global_claim() -> None:
    report = run_pair_carrier_label_contextuality()

    assert report.theorem.theorem_verified
    assert report.claim_gate["selected_triple_carrier_label_query_polynomial"]
    assert report.claim_gate[
        "selected_triple_gamma_computable_without_multiplicity_basis"
    ]
    assert report.claim_gate["pair_gpe_preserves_multiplicity_registers"]
    assert not report.claim_gate["overlapping_pair_labels_always_jointly_classical"]
    assert not report.claim_gate[
        "pairwise_gpe_label_accumulation_compiles_global_channel_atom"
    ]
    assert not report.claim_gate[
        "physical_occupied_multistar_projectors_commute_all_depth"
    ]
    assert not report.claim_gate["coherent_multistar_racah_resolver_compiled"]
    assert not report.claim_gate["physical_pgm_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_global_interface_lists_three_non_pairwise_routes() -> None:
    interface = run_pair_carrier_label_contextuality().global_interface

    assert "commute" in interface.sufficient_commuting_route.lower()
    assert "racah" in interface.sufficient_racah_route.lower()
    assert "without" in interface.label_free_route.lower()
    assert not interface.pairwise_accumulation_route_valid


def test_report_writer_round_trip_without_registry(tmp_path) -> None:
    path = tmp_path / "pair-carrier-label-contextuality.json"
    payload = write_pair_carrier_label_contextuality_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"][
        "coherent_local_pair_carrier_label_query_count"
    ] == 1
    assert payload["status"] == (
        "coherent-local-carrier-label-query-proved-global-contextuality-open"
    )
