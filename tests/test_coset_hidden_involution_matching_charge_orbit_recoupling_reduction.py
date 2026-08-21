from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
)
from coset_hidden_involution_matching_charge_orbit_recoupling_reduction import (
    audit_charge_stabilizer,
    build_charge_orbit_recoupling_report,
    charge_orbit_scaling_record,
    conjugate_permutation,
    conjugated_matching_charge_term_from_index,
    cross_pair_transposition,
    reference_hidden_involution,
    write_charge_orbit_recoupling_report,
)
from coset_hidden_involution_matching_charge_coherent_label_compiler import (
    matching_charge_term_count,
    matching_charge_term_from_index,
)


def test_exact_K_stabilizer_controls_have_an_all_rank_noncentral_witness():
    for half_degree in (4, 5, 6):
        row = audit_charge_stabilizer(half_degree)
        assert row.charge_is_K_invariant
        assert not row.charge_is_G_central
        assert row.witness_coefficient_before_conjugation == 1
        assert row.witness_conjugate_coefficient == 0
        assert row.witness_pair_support_before == 4
        assert row.witness_pair_support_after == 3
        assert row.maximality_cross_transposition_count + half_degree == (
            row.maximality_total_transposition_count
        )
        assert row.exact_stabilizer_is_K_proved


def test_cross_transposition_changes_the_reference_hidden_matching():
    for half_degree in (4, 5, 8):
        hidden = reference_hidden_involution(half_degree)
        cross = cross_pair_transposition(half_degree)
        conjugated = conjugate_permutation(cross, hidden)
        assert conjugated != hidden
        assert conjugate_permutation(cross, conjugated) == hidden


def test_controlled_term_access_is_exact_conjugation_of_reference_access():
    for half_degree in (4, 5, 6):
        cross = cross_pair_transposition(half_degree)
        total = matching_charge_term_count(half_degree)
        for index in (0, 1, 191, total // 2, total - 1):
            expected = conjugate_permutation(
                cross,
                matching_charge_term_from_index(half_degree, index),
            )
            observed = conjugated_matching_charge_term_from_index(
                half_degree,
                cross,
                index,
            )
            assert observed == expected


def test_charge_orbit_size_equals_hidden_involution_class_size():
    for half_degree in (4, 8, 16, 32, 64):
        row = charge_orbit_scaling_record(half_degree)
        assert row.orbit_size_equals_hidden_matching_count
        assert row.hidden_matching_count > 1
        assert row.hidden_matching_label_bits > 0
        assert row.controlled_conjugated_block_encoding_normalization == 1.0


def test_report_reduces_detector_to_cross_charge_transition_without_overclaim():
    report = build_charge_orbit_recoupling_report()
    theorem = report.theorem
    assert theorem.exact_all_rank_charge_stabilizer_proved
    assert theorem.hidden_matching_to_charge_orbit_injective
    assert theorem.normalization_one_controlled_orbit_access_compiled
    assert theorem.charge_orbit_is_a_faithful_candidate_coordinate
    assert not theorem.useful_cross_charge_transition_gap_proved
    assert not theorem.source_aware_transition_mass_proved
    assert not theorem.all_copy_target_recoupling_compiled
    assert not theorem.hidden_involution_detector_constructed
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_live_charge_orbit_report_is_json_serializable(tmp_path):
    output = tmp_path / "charge-orbit.json"
    payload = write_charge_orbit_recoupling_report(output)
    assert output.exists()
    assert payload["status"] == (
        "faithful-matching-charge-orbit-proved-transition-kernel-open"
    )
    assert payload["claim_gate"]["charge_stabilizer_exactly_K_proved"]
    assert payload["claim_gate"]["hidden_matching_charge_orbit_injective"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
