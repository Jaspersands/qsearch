import itertools

import numpy as np

from representation_obstruction import integer_partitions
from self_dual_wreath_plancherel_carrier_contextuality import (
    _triple_isotypic_projectors,
)
from self_dual_wreath_plancherel_carrier_racah_access_boundary import (
    _global_diagonal_actions,
    _path_dimensions,
    annealed_racah_mass_control,
    audit_racah_block_access,
    run_plancherel_carrier_racah_access_boundary,
    write_plancherel_carrier_racah_access_boundary_report,
)


def test_left_and_right_racah_path_dimensions_match_for_every_s3_source() -> None:
    partitions = tuple(integer_partitions(3))
    for sources in itertools.product(partitions, repeat=3):
        for total in partitions:
            left = sum(value for _, value in _path_dimensions(sources, total, side="left"))
            right = sum(value for _, value in _path_dimensions(sources, total, side="right"))
            assert left == right


def test_dense_controls_localize_commutator_to_multiplicity_blocks() -> None:
    standard = audit_racah_block_access(
        "S3-STANDARD-CUBED", ((2, 1),) * 3
    )
    commuting = audit_racah_block_access(
        "S3-COMMUTING", ((2, 1), (2, 1), (3,))
    )
    assert standard.exact_racah_block_decomposition_verified is True
    assert standard.aggregate_commutator > 0.8
    assert standard.minimum_active_multiplicity_dimension == 3
    assert standard.active_racah_physical_dimension_fraction == 0.75
    assert standard.commutator_to_active_mass_bound_slack > 0
    assert commuting.exact_racah_block_decomposition_verified is True
    assert commuting.aggregate_commutator == 0
    assert commuting.active_racah_physical_dimension_fraction == 0


def test_lueders_return_probability_is_exact_commutator_witness() -> None:
    for sources in (((2, 1),) * 3, ((3, 1),) * 3, ((2, 2),) * 3):
        control = audit_racah_block_access("CONTROL", sources)
        assert control.disturbance_identity_residual <= 1e-12
        assert abs(
            control.aggregate_commutator
            - 2 * (1 - control.lueders_same_left_label_return_probability)
        ) <= 1e-12


def test_every_carrier_word_remains_globally_conjugation_invariant() -> None:
    sources = ((2, 1),) * 3
    left = _triple_isotypic_projectors(sources, "left")
    right = _triple_isotypic_projectors(sources, "right")
    actions = _global_diagonal_actions(sources)
    words = [
        left[0],
        right[0],
        left[0] @ right[1] @ left[0],
        right[1] @ left[2] @ right[1] @ left[0],
    ]
    assert max(
        np.linalg.norm(action @ word - word @ action, ord="fro")
        for action in actions
        for word in words
    ) <= 1e-12


def test_annealed_dense_control_matches_character_law_and_active_mass_bound() -> None:
    control = annealed_racah_mass_control()
    assert control.plancherel_weight_normalization_residual <= 1e-12
    assert control.dense_to_character_formula_residual <= 1e-12
    assert control.return_probability_to_weighted_commuting_residual <= 1e-12
    assert control.active_mass_bound_verified is True
    assert (
        control.dense_annealed_active_racah_dimension_fraction
        >= control.active_mass_lower_bound_from_commutator
    )


def test_report_advances_access_but_rejects_carrier_only_decoder() -> None:
    report = run_plancherel_carrier_racah_access_boundary()
    assert report.theorem.minimum_racah_block_theorem_proved is True
    assert report.theorem.constant_query_disturbance_compiled is True
    assert report.theorem.asymptotically_full_active_racah_mass_proved is True
    assert report.theorem.carrier_pvm_only_hidden_involution_decoder_possible is False
    assert report.claim_gate[
        "carrier_contextuality_operationally_accessible_by_pair_gpe"
    ] is True
    assert report.claim_gate[
        "carrier_only_adaptive_effects_conjugation_invariant"
    ] is True
    assert report.claim_gate[
        "carrier_only_protocol_can_identify_hidden_involution"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_access_boundary_artifact_without_registry(tmp_path) -> None:
    payload = write_plancherel_carrier_racah_access_boundary_report(
        path=tmp_path / "racah-access.json",
        write_registry=False,
    )
    assert payload["headline_metrics"][
        "minimum_total_irrep_racah_block_theorem_count"
    ] == 1
    assert payload["headline_metrics"][
        "carrier_pvm_conjugation_invariance_no_go_theorem_count"
    ] == 1
    assert payload["headline_metrics"]["hidden_involution_decoder_count"] == 0
    assert len(payload["falsifiers_triggered"]) >= 5
