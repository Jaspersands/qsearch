from functools import lru_cache

from self_dual_wreath_marked_pressure_obstruction_search import (
    PressureSearchConfig,
    PressureProfileKey,
    _assignments_to_support_mask,
    _known_adversarial_profiles,
    _lift_profile,
    _obstruction_record,
    _support_mask_to_assignments,
    audit_constant_zero_trailing_lift,
    residual_target_cancellation_control,
    run_marked_pressure_obstruction_search,
    run_pressure_search,
    strip_constant_zero_trailing_lifts,
)
from self_dual_wreath_marked_relation_topology import (
    _weak_compositions,
    free_reduce,
    inverse_word,
)


@lru_cache(maxsize=1)
def _report():
    return run_marked_pressure_obstruction_search()


def test_support_masks_round_trip_exactly():
    support = ((0, 0, 0), (0, 1, 1), (1, 1, 0))
    mask = _assignments_to_support_mask(3, support)
    assert _support_mask_to_assignments(3, mask) == support


def test_known_degree_three_obstructions_receive_exact_pressure_certificates():
    records = [
        _obstruction_record(key, index, maximum_nielsen_states=4_000)
        for index, key in enumerate(_known_adversarial_profiles(), start=1)
    ]
    assert all(row.status == "pressure-upper-bound-certified" for row in records)
    assert all(row.strong_pressure_excess <= 0 for row in records)
    assert all(row.symmetric_group_solution_count > 0 for row in records)
    assert all(row.target_character_symbolically_cancelled for row in records)
    assert all(row.finite_S3_maximum_nontrivial_character_bias == 1 for row in records)
    assert not any(row.asymptotic_counterexample_proved for row in records)


def test_small_best_first_search_is_deterministic():
    config = PressureSearchConfig(
        frame_position_count=3,
        crossing=True,
        random_seed=991,
        initial_random_profile_count=20,
        search_round_count=1,
        beam_width=8,
        mutations_per_state=3,
        strong_finalist_count=4,
        maximum_nielsen_states=1_000,
    )
    first = run_pressure_search(config)
    second = run_pressure_search(config)
    assert first.evaluated_profile_count == second.evaluated_profile_count
    assert [row.residual_relations for row in first.finalists] == [
        row.residual_relations for row in second.finalists
    ]
    assert [row.strong_certificate_source for row in first.finalists] == [
        row.strong_certificate_source for row in second.finalists
    ]


def test_constant_zero_trailing_lift_is_exact_for_every_profile_through_degree_two():
    for frame_count in range(3):
        support_limit = 1 << (1 << frame_count)
        for powers in _weak_compositions(frame_count, 4):
            for same_mask in range(1, support_limit):
                for different_mask in range(1, support_limit):
                    control = audit_constant_zero_trailing_lift(
                        PressureProfileKey(
                            frame_count,
                            powers,
                            True,
                            same_mask,
                            different_mask,
                        )
                    )
                    assert control.exact_relation_isomorphism_verified
                    assert control.lifted_free_generator_count_delta == 1
                    assert control.exact_pressure_invariance_verified


def test_repeated_constant_zero_lifts_strip_to_the_unique_original_core():
    original = _known_adversarial_profiles()[0]
    lifted_once = _lift_profile(original, 3, 0)
    lifted_twice = _lift_profile(lifted_once, 3, 0)
    core, depth = strip_constant_zero_trailing_lifts(lifted_twice)
    assert depth == 2
    assert core == original


def test_residual_target_has_an_exact_cyclic_relator_certificate():
    control = residual_target_cancellation_control()
    assert control.solution_counts == (66, 960, 11_040)
    assert control.nonidentity_target_counts == (0, 0, 0)
    assert control.exact_finite_search_verified
    assert control.matched_relation_index == 4
    assert control.matched_relation_orientation == "inverse"
    assert control.cyclic_shift == 6
    assert control.conjugating_prefix == (-5, -8, 7, 8, 4, 5)
    relation = control.residual_relations[control.matched_relation_index - 1]
    reconstructed = free_reduce(
        inverse_word(control.conjugating_prefix)
        + inverse_word(relation)
        + control.conjugating_prefix
    )
    assert reconstructed == control.residual_target_word
    assert reconstructed == control.normal_closure_certificate_word
    assert control.exact_cyclic_conjugacy_verified
    assert control.target_in_presented_group_normal_closure_proved
    assert control.all_group_target_identity_proved
    assert control.all_symmetric_group_target_identity_proved


def test_live_search_localizes_proof_debt_without_claiming_a_theorem():
    report = _report()
    metrics = report.headline_metrics
    assert metrics["searched_profile_count"] >= 3_000
    assert metrics["search_run_count"] == 8
    assert metrics["unresolved_finalist_count"] == 0
    assert metrics["maximum_strong_pressure_excess"] <= 0
    assert metrics["asymptotic_counterexample_count"] == 0
    assert metrics["constant_zero_trailing_lift_failure_count"] == 0
    assert metrics["constant_zero_trailing_lift_theorem_count"] == 1
    assert metrics["degree_five_reducible_finalist_count"] == 0
    assert metrics["degree_six_reducible_finalist_count"] == 0
    assert metrics["degree_six_positive_literal_pressure_profile_count"] == 0
    assert metrics["mixed_frame_positive_split_genus_finalist_count"] > 0
    assert metrics["mixed_frame_symbolically_cancelled_target_finalist_count"] == 0
    assert metrics["mixed_frame_symbolically_uncancelled_target_finalist_count"] > 0
    assert metrics["mixed_frame_maximum_strong_pressure_excess"] <= -1
    assert metrics["mixed_frame_full_exponent_margin_finalist_count"] == metrics[
        "mixed_frame_positive_split_genus_finalist_count"
    ]
    assert metrics["mixed_frame_nonzero_finite_character_bias_finalist_count"] > 0
    assert metrics["residual_target_cancellation_control_failure_count"] == 0
    assert metrics["cyclic_relator_target_cancellation_theorem_count"] == 1
    assert metrics["two_partition_ribbon_improved_finalist_count"] > 0
    assert any(
        row.strong_certificate_source == "single-whitehead-primitive"
        for run in report.search_runs
        for row in run.finalists
    )
    assert report.claim_gate["counterexample_directed_search_operational"]
    assert report.claim_gate["two_partition_ribbon_scoring_operational"]
    assert report.claim_gate["constant_zero_trailing_free_product_lift_proved"]
    assert report.claim_gate[
        "degree_five_search_quotients_constant_zero_lifts"
    ]
    assert report.claim_gate[
        "degree_six_search_quotients_constant_zero_lifts"
    ]
    assert report.claim_gate["mixed_frame_scalar_pressure_search_operational"]
    assert report.claim_gate[
        "positive_genus_support_uncancelled_search_operational"
    ]
    assert report.claim_gate[
        "mixed_frame_full_exponent_margin_on_all_finalists"
    ]
    assert report.claim_gate["mixed_frame_finite_character_control_operational"]
    assert not report.claim_gate[
        "visited_mixed_frame_symbolic_character_cancellation_complete"
    ]
    assert report.claim_gate["unresolved_profiles_are_proof_debt_only"]
    assert not report.claim_gate["asymptotic_pressure_counterexample_proved"]
    assert not report.claim_gate["growing_degree_pressure_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
