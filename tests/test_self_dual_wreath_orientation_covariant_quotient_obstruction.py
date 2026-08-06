from self_dual_wreath_orientation_covariant_quotient_obstruction import (
    orientation_parity_span_rank,
    run_orientation_covariant_quotient_obstruction,
    self_conjugate_plancherel_mass_record,
    validate_covariant_orbit_closure,
)


def test_all_orientation_parity_span_has_expected_rank() -> None:
    for block_size in range(1, 12):
        assert orientation_parity_span_rank(block_size) == block_size + 1


def test_common_vector_orbit_closes_to_full_finite_carrier() -> None:
    record = validate_covariant_orbit_closure()
    assert record.initial_common_range_dimension == 1
    assert record.orbit_closure_dimension == 400
    assert record.carrier_dimension == 400
    assert record.orbit_closure_is_full
    assert record.every_source_partition_non_self_conjugate
    assert record.algebraic_scalar_commutant_condition_holds
    assert record.exact_finite_orbit_closure_validation


def test_self_conjugate_natural_tuple_condition_is_not_promoted() -> None:
    record = self_conjugate_plancherel_mass_record(48)
    assert record.self_conjugate_plancherel_mass > 0
    assert record.probability_no_self_conjugate_source_draw < 0.1
    assert not record.asymptotic_tuple_absence_proved


def test_report_closes_only_branchwise_covariant_quotient() -> None:
    report = run_orientation_covariant_quotient_obstruction()
    assert report.headline_metrics[
        "finite_orbit_closure_validation_failure_count"
    ] == 0
    assert report.claim_gate[
        "non_self_conjugate_branchwise_scalar_commutant_proved"
    ]
    assert not report.claim_gate[
        "nontrivial_branchwise_covariant_local_quotient_exists"
    ]
    assert not report.claim_gate[
        "typical_natural_tuple_satisfies_non_self_conjugate_condition"
    ]
    assert not report.claim_gate[
        "coherent_orientation_branch_mixing_transform_ruled_out"
    ]
    assert not report.claim_gate["general_physical_quotient_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
