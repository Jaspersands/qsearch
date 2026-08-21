from coset_hidden_involution_commutant_support_growth_boundary import (
    REPORT_PATH,
    audit_commutant_support_growth,
    build_commutant_support_growth_report,
    hyperoctahedral_conjugacy_classes,
    hyperoctahedral_conjugacy_type,
    write_commutant_support_growth_report,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    hyperoctahedral_group,
)


def test_signed_cycle_types_classify_the_expected_K5_classes() -> None:
    classes = hyperoctahedral_conjugacy_classes(5)
    assert len(classes) == 36
    assert sum(len(row) for row in classes) == len(hyperoctahedral_group(5))
    assert all(
        len({hyperoctahedral_conjugacy_type(element) for element in row}) == 1
        for row in classes
    )


def test_target_has_full_commutant_cyclic_capacity() -> None:
    control = audit_commutant_support_growth()
    assert control.symmetric_irrep_dimension == 315
    assert control.exact_commutant_dimension == 42
    assert control.full_commutant_generic_cyclic_capacity == 42
    assert control.all_occupied_carrier_dimensions_at_least_multiplicity


def test_support_threshold_inventory_grows_at_five() -> None:
    control = audit_commutant_support_growth()
    assert (
        control.support_two_hermitian_orbit_count,
        control.support_three_hermitian_orbit_count,
        control.support_four_hermitian_orbit_count,
        control.support_five_hermitian_orbit_count,
    ) == (3, 5, 15, 28)


def test_support_four_is_a_real_internal_copy_space_deficit() -> None:
    control = audit_commutant_support_growth()
    assert control.support_four_cyclic_reaches == (40, 40)
    assert control.support_four_plus_K_center_cyclic_reaches == (40, 40)
    assert not control.support_four_generates_full_commutant
    assert control.support_four_deficit_survives_K_center


def test_support_five_repairs_the_target_exactly() -> None:
    control = audit_commutant_support_growth()
    assert control.support_two_cyclic_reaches == (5, 5)
    assert control.support_three_cyclic_reaches == (14, 14)
    assert control.support_five_cyclic_reaches == (42, 42)
    assert control.support_five_generates_full_commutant
    assert control.maximum_orbit_sum_hermiticity_residual < 1e-10
    assert control.maximum_K_generator_commutator_residual < 1e-8


def test_report_falsifies_only_support_four() -> None:
    report = build_commutant_support_growth_report()
    assert report.claim_gate["uniform_support_four_generation_falsified"] is True
    assert report.claim_gate[
        "support_four_deficit_survives_full_K_center"
    ] is True
    assert report.claim_gate[
        "support_five_target_sector_generation_verified"
    ] is True
    assert report.claim_gate["uniform_support_five_generation_proved"] is False
    assert report.claim_gate["support_requirement_unbounded_proved"] is False
    assert report.claim_gate["inverse_polynomial_spectral_gap_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_report_writer_materializes_research_artifact(tmp_path) -> None:
    output = tmp_path / REPORT_PATH.name
    payload = write_commutant_support_growth_report(output)
    assert output.exists()
    assert payload["status"] == (
        "uniform-support-four-falsified-support-five-uniformity-open"
    )
