from coset_hidden_involution_rank_tracking_commutant_witness import (
    REPORT_PATH,
    SUPPORT_FIVE_REPRESENTATIVE,
    SUPPORT_SIX_REPRESENTATIVE,
    audit_rank_tracking_commutant,
    bounded_support_permutations,
    build_rank_tracking_commutant_report,
    hermitian_bounded_support_orbits_fast,
    permutation_cycles,
    write_rank_tracking_commutant_report,
)


def test_fast_bounded_support_inventory_is_complete() -> None:
    assert sum(1 for _ in bounded_support_permutations(12, 5)) == 39_810
    orbits = hermitian_bounded_support_orbits_fast(6, 5)
    assert len(orbits) == 28
    assert sum(len(orbit) for orbit in orbits) == 39_810


def test_explicit_witness_cycle_patterns_are_stable() -> None:
    assert permutation_cycles(SUPPORT_FIVE_REPRESENTATIVE) == ((3, 4, 6, 8, 10),)
    assert permutation_cycles(SUPPORT_SIX_REPRESENTATIVE) == (
        (5, 6, 8),
        (7, 9, 10),
    )


def test_rank_six_target_has_one_repeated_block() -> None:
    control = audit_rank_tracking_commutant()
    assert control.symmetric_irrep_dimension == 275
    assert control.occupied_K_block_count == 12
    assert control.repeated_K_block_count == 1
    assert control.maximum_branching_multiplicity == 2
    assert control.exact_commutant_dimension == 15
    assert control.full_commutant_generic_cyclic_capacity == 15


def test_every_orbit_through_support_five_still_fails() -> None:
    control = audit_rank_tracking_commutant()
    assert control.support_two_cyclic_reaches == (5, 5, 5)
    assert control.support_three_cyclic_reaches == (5, 5, 5)
    assert control.support_four_cyclic_reaches == (13, 13, 13)
    assert control.support_five_cyclic_reaches == (13, 13, 13)
    assert control.support_five_plus_K_center_cyclic_reaches == (13, 13, 13)
    assert not control.support_at_most_five_generates_full_commutant
    assert control.support_five_deficit_survives_K_center


def test_two_explicit_orbits_close_the_full_commutant() -> None:
    control = audit_rank_tracking_commutant()
    assert control.support_five_witness_orbit_size == 4_608
    assert control.support_six_witness_orbit_size == 2_880
    assert control.support_five_witness_cyclic_reaches == (10, 10, 10)
    assert control.support_six_witness_cyclic_reaches == (11, 11, 11)
    assert control.witness_pair_cyclic_reaches == (15, 15, 15)
    assert control.witness_pair_generates_full_commutant
    assert control.maximum_witness_K_commutator_residual < 1e-8


def test_report_falsifies_cutoffs_only_through_five() -> None:
    report = build_rank_tracking_commutant_report()
    assert report.claim_gate[
        "universal_support_cutoff_at_most_five_falsified"
    ] is True
    assert report.claim_gate[
        "explicit_support_six_pair_generates_target"
    ] is True
    assert report.claim_gate["universal_support_six_generation_proved"] is False
    assert report.claim_gate["unbounded_support_requirement_proved"] is False
    assert report.claim_gate["inverse_polynomial_spectral_gap_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_report_writer_materializes_research_artifact(tmp_path) -> None:
    output = tmp_path / REPORT_PATH.name
    payload = write_rank_tracking_commutant_report(output)
    assert output.exists()
    assert payload["status"] == (
        "universal-support-at-most-five-falsified-support-six-uniformity-open"
    )
