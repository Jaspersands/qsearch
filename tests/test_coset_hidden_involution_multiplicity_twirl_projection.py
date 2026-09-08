from pathlib import Path

import proof_tracker

from coset_hidden_involution_multiplicity_twirl_projection import (
    audit_multiplicity_twirl_projection,
    hermitian_bounded_support_orbit_representatives,
    run_multiplicity_twirl_projection,
    validate_signed_weight_projection_against_full_twirl,
    write_multiplicity_twirl_projection_report,
)


def test_generator_bfs_compresses_bounded_support_orbits() -> None:
    rank_six = hermitian_bounded_support_orbit_representatives(6, 5)
    rank_seven = hermitian_bounded_support_orbit_representatives(7, 6)
    assert len(rank_six) == 28
    assert len(rank_seven) == 82


def test_rank_six_repeated_block_requires_support_six() -> None:
    control = audit_multiplicity_twirl_projection(
        6,
        (8, 4),
        (4, 2),
        6,
    )
    steps = {
        step.maximum_moved_point_support: step for step in control.support_steps
    }
    assert control.exact_branching_multiplicity == 2
    assert control.expected_isotypic_dimension == 18
    assert control.observed_isotypic_dimension == 18
    assert control.symmetric_commutant_dimension == 3
    assert control.full_copy_algebra_dimension == 4
    assert steps[5].generated_copy_algebra_dimension == 2
    assert steps[6].generated_copy_algebra_dimension == 4
    assert control.minimum_full_copy_algebra_support == 6
    assert control.first_full_support_witness is not None
    assert control.compressed_twirl_projection_verified is True


def test_rank_seven_continuation_closes_at_support_six() -> None:
    control = audit_multiplicity_twirl_projection(
        7,
        (10, 4),
        (5, 2),
        6,
    )
    steps = {
        step.maximum_moved_point_support: step for step in control.support_steps
    }
    assert control.symmetric_irrep_dimension == 637
    assert control.observed_isotypic_dimension == 28
    assert steps[5].generated_copy_algebra_dimension == 2
    assert steps[6].generated_copy_algebra_dimension == 4
    assert control.minimum_full_copy_algebra_support == 6
    assert control.maximum_symmetric_commutant_K_commutator_residual <= 1e-9
    assert control.maximum_sparse_representation_action_residual <= 1e-9


def test_rank_seven_multiplicity_three_block_closes_at_support_five() -> None:
    control = audit_multiplicity_twirl_projection(
        7,
        (9, 4, 1),
        (4, 2, 1),
        6,
    )
    assert control.symmetric_irrep_dimension == 4368
    assert control.pair_flip_fixed_space_dimension == 294
    assert control.exact_branching_multiplicity == 3
    assert control.observed_isotypic_dimension == 105
    assert control.full_copy_algebra_dimension == 9
    assert control.minimum_full_copy_algebra_support == 5
    assert control.compressed_twirl_projection_verified is True


def test_nontrivial_beta_sector_closes_at_support_four() -> None:
    control = audit_multiplicity_twirl_projection(
        7,
        (10, 2, 2),
        (4, 1),
        6,
        negative_hyperoctahedral_partition=(2,),
    )
    assert control.negative_hyperoctahedral_partition == (2,)
    assert control.selected_character_negative_pair_count == 2
    assert control.exact_branching_multiplicity == 2
    assert control.observed_isotypic_dimension == 8
    assert control.minimum_full_copy_algebra_support == 4
    assert control.compressed_twirl_projection_verified is True


def test_signed_sector_projection_matches_explicit_full_twirl() -> None:
    validation = validate_signed_weight_projection_against_full_twirl()
    assert validation.hyperoctahedral_group_order == 384
    assert validation.validation_passed is True
    assert validation.projected_restriction_residual <= 1e-12


def test_report_falsifies_only_strict_growth_extrapolation() -> None:
    report = run_multiplicity_twirl_projection(
        include_rank_seven_portfolio=False,
    )
    assert report.theorem.hilbert_schmidt_twirl_projection_proved is True
    assert report.theorem.rank_five_six_thresholds_reproduced is True
    assert report.theorem.strict_rank_tracking_support_growth_falsified is True
    assert report.theorem.universal_support_six_generation_proved is False
    assert report.theorem.unbounded_support_requirement_proved is False
    assert report.theorem.coherent_commutant_transform_compiled is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_artifact_without_registry(tmp_path: Path) -> None:
    output = tmp_path / "multiplicity-twirl.json"
    payload = write_multiplicity_twirl_projection_report(
        output,
        write_registry=False,
        include_rank_seven_portfolio=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "strict-support-growth-extrapolation-falsified-support-six-uniformity-open"
    )
    assert payload["headline_metrics"][
        "strict_rank_tracking_support_growth_falsifier_count"
    ] == 1
    assert payload["headline_metrics"][
        "universal_support_six_generation_theorem_count"
    ] == 0


def test_proof_tracker_records_falsifier_but_keeps_uniformity_open(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output = tmp_path / "multiplicity-twirl.json"
    write_multiplicity_twirl_projection_report(
        output,
        write_registry=False,
    )
    monkeypatch.setattr(
        proof_tracker,
        "MULTIPLICITY_TWIRL_PROJECTION_PATH",
        output,
    )
    monkeypatch.setattr(
        proof_tracker,
        "NATURAL_SUPPORT_SIX_MASS_AUDIT_PATH",
        tmp_path / "missing-natural-mass-audit.json",
    )
    lemmas = {
        lemma.id: lemma
        for lemma in proof_tracker._multiplicity_twirl_projection_lemmas(
            "CODE-COSET-COLLECTIVE"
        )
    }
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-MULTIPLICITY-TWIRL-PROJECTION-DIAGNOSTIC"
    ].status.startswith("proved-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-SIGNED-WEIGHT-TWIRL-PROJECTION"
    ].status.startswith("proved-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-MULTIPLICITY-THREE-SUPPORT-FIVE-CONTROL"
    ].status.startswith("proved-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-UNIFORM-SUPPORT-SIX-NATURAL-COMMUTANT"
    ].status == (
        "blocked-strict-growth-falsified-support-six-uniformity-gap-and-access-open"
    )
