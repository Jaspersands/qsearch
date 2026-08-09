from self_dual_wreath_marked_relation_topology import (
    _substitute_word_images,
    canonical_relator,
)
from self_dual_wreath_relative_surface_factorization import (
    EXPECTED_CANONICAL_RELATION,
    EXPECTED_TRANSFORMED_TARGET,
    GENERATORS,
    NEW_TO_OLD,
    OLD_TO_NEW,
    SOURCE_RELATION,
    SOURCE_TARGET,
    relative_surface_factorization_control,
    run_relative_surface_factorization,
)


def test_basis_change_is_an_exact_two_sided_free_group_automorphism():
    for generator in GENERATORS:
        old_round_trip = _substitute_word_images(
            _substitute_word_images((generator,), OLD_TO_NEW),
            NEW_TO_OLD,
        )
        new_round_trip = _substitute_word_images(
            _substitute_word_images((generator,), NEW_TO_OLD),
            OLD_TO_NEW,
        )
        assert old_round_trip == (generator,)
        assert new_round_trip == (generator,)


def test_relation_and_target_factor_into_disjoint_commutators():
    control = relative_surface_factorization_control()
    assert canonical_relator(
        _substitute_word_images(SOURCE_RELATION, OLD_TO_NEW)
    ) == EXPECTED_CANONICAL_RELATION
    assert (
        _substitute_word_images(SOURCE_TARGET, OLD_TO_NEW)
        == EXPECTED_TRANSFORMED_TARGET
    )
    assert control.relation_generator_pair == (6, 7)
    assert control.target_generator_pair == (4, 5)
    assert control.disjoint_generator_pairs
    assert control.exact_relative_surface_factorization_verified


def test_exact_S3_control_matches_the_all_group_formula():
    control = relative_surface_factorization_control()
    assert control.exact_solution_count == 648
    assert control.predicted_solution_count == 648
    assert control.standard_normalized_character_average == "1/4"
    assert control.predicted_standard_normalized_character_average == "1/4"
    assert control.exact_finite_control_verified


def test_report_resolves_only_the_certified_profile():
    report = run_relative_surface_factorization()
    assert report.claim_gate["leading_relative_surface_factorization_proved"]
    assert not report.claim_gate[
        "all_positive_genus_support_profiles_classified"
    ]
    assert not report.claim_gate[
        "growing_degree_relative_surface_theorem_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
