from fractions import Fraction
import cmath
import itertools
import math

import pytest

from dcp_carry_packets import compile_packet
from dcp_full_bell_source_moments import (
    _complete_q8_source_control, _independent_disjoint_count, _physical_full_probabilities,
    _quartet_controls, _systematic_control, fresh_native_verification_certificate,
    fresh_packet_verification_certificate, known_residue_high_bit_completion_bound,
    known_residue_phase_correction_plan,
    full_collision_source_certificate, systematic_source_mean,
)


def read(value):
    return Fraction(value["sign"] * int(value["numerator_hex"], 16),
                    1 << value["denominator_binary_exponent"])


def test_full_source_collision_identity_is_not_a_product_of_marginals():
    packets = [compile_packet(A, 8) for A in ([[1, 1, 1]], [[1, 1, 0]])]
    row = full_collision_source_certificate(*packets)
    count = _independent_disjoint_count(*packets)
    assert row["ordered_disjoint_physical_direction_pairs"] == count
    assert read(row["high_label_mean_relative_full_collision"]) == Fraction(count, 4)
    assert not row["statistic_is_mutual_information"]
    assert not row["source_tail_concentration_proved"]


def test_complete_native_high_label_average_and_real_readout_sign_ambiguity():
    row = _complete_q8_source_control()
    assert row["complete_higher_label_tables"] == 4096
    assert row["all_tables_obey_secret_negation_invariance"]
    assert row["source_mean_relative_collisions"]["0"] == row["source_mean_relative_collisions"]["3"]


def test_quartet_identity_survives_growing_moduli():
    rows = _quartet_controls()
    assert [r["modulus"] for r in rows] == [8, 16, 32, 128]
    assert len({r["physical_source_surviving_quartets"] for r in rows}) == 1


def test_systematic_native_mean_has_exact_small_complete_control():
    row = _systematic_control()
    assert row["complete_systematic_pair_tables"] == 16
    assert read(row["mean_relative_collision"]) == Fraction(65, 32)
    assert read(row["full_source_formula"]["two_public_prefix_invertibility_probability"]) == Fraction(1, 4)


def test_large_full_collision_mean_does_not_promote_itself_to_decoder():
    row = systematic_source_mean(128)
    assert read(row["conditional_mean_relative_full_collision"]) > 2**40
    assert read(row["two_public_prefix_invertibility_probability"]) > Fraction(1, 20)
    assert row["conditions_on_prefix_success_not_unconditional_claim"]
    assert row["mean_does_not_prove_typical_instance_signal"]
    assert not row["speedup_claim_allowed"]


def test_lower_modulus_and_exponential_enumeration_are_guarded():
    packet = compile_packet([[1, 1, 1]], 4)
    with pytest.raises(ValueError, match="at least eight"):
        full_collision_source_certificate(packet, packet)
    packet = compile_packet([[1] * 17], 8)
    with pytest.raises(ValueError, match="exponential"):
        full_collision_source_certificate(packet, packet)


def test_even_secret_exception_cannot_use_odd_secret_source_identity():
    packet = compile_packet([[1, 1, 1]], 8)
    probabilities = _physical_full_probabilities(packet, packet, [0], 0)
    assert probabilities == [1, 0, 0, 0]
    row = full_collision_source_certificate(packet, packet)
    assert row["requires_nonzero_secret_parity"]
    assert read(row["high_label_mean_relative_full_collision"]) < 4


def test_fresh_known_candidate_verification_has_native_soundness_not_chosen_labels():
    for q, delta in ((8, [2]), (8, [4]), (16, [2, 4]), (8, [0, 0])):
        values = []
        for label in itertools.product(range(q), repeat=len(delta)):
            angle = 2 * math.pi * sum(a * d for a, d in zip(label, delta)) / q
            values.append((1 + cmath.exp(1j * angle).real) / 2)
        row = fresh_native_verification_certificate(q, delta, 40)
        assert sum(values) / len(values) == pytest.approx(float(read(row["one_test_high_source_average_acceptance"])))
        assert read(row["all_tests_high_source_average_acceptance"]) == (1 if not any(delta) else Fraction(1, 2**40))
        assert row["candidate_committed_before_verification_labels"]
        assert row["requires_fresh_original_native_phase_states"]
        assert not row["decoder_implemented"]
    row = fresh_native_verification_certificate(2**64, [2, 0], 100)
    assert row["difference_character_image_order"] == 2**63
    assert read(row["all_tests_high_source_average_acceptance"]) == Fraction(1, 2**100)


def test_verification_certificate_refuses_invalid_source_parameters():
    for q, delta, tests in ((3, [1], 1), (8, [], 1), (8, [1], 0)):
        with pytest.raises(ValueError):
            fresh_native_verification_certificate(q, delta, tests)


def test_packet_residue_verification_uses_fresh_source_and_handles_even_differences():
    packet = compile_packet([[1, 1, 1]], 8)
    for delta in range(4):
        total = Fraction(0)
        for high in itertools.product(range(4), repeat=3):
            fresh = compile_packet([[1 + 2 * h for h in high]], 8)
            roots = [0] * 4
            for z in range(4):
                roots[(delta * fresh.residual(z)[0]) % 4] += 1
            total += Fraction((roots[0] - roots[2])**2 + (roots[1] - roots[3])**2, 16)
        row = fresh_packet_verification_certificate(packet, [delta], 3)
        assert total / 64 == read(row["one_test_conditional_high_source_mean_acceptance"])
        assert read(row["all_tests_conditional_high_source_mean_acceptance"]) == (1 if delta == 0 else Fraction(1, 64))
        assert row["fresh_original_phase_states_consumed"] == 9
        assert row["does_not_recover_lost_original_high_bit"]


def test_known_residue_completion_counts_the_lost_bit_stage():
    row = known_residue_high_bit_completion_bound(128, 40)
    assert row["fresh_original_phase_states_consumed"] == 168
    assert read(row["highest_bit_vector_binary_rank_failure_upper_bound"]) < Fraction(1, 2**40)
    assert row["incorrect_residue_not_covered"]
    assert not row["residue_decoder_implemented"]
    with pytest.raises(ValueError):
        known_residue_high_bit_completion_bound(0)


def test_candidate_correction_is_a_public_affine_plan_not_a_hidden_inverse():
    for q in (8, 16, 128):
        packet = compile_packet([[1, 3, 5, 7]], q, 1)
        for candidate in (0, 1, q // 2 - 1):
            plan = known_residue_phase_correction_plan(packet, [candidate])
            constants = set()
            for z in range(8):
                value = sum(int(step["known_phase_exponent_mod_q_hex"], 16) *
                            (step["affine_origin"] ^ ((int(step["logical_parity_mask_hex"], 16) & z).bit_count() & 1))
                            for step in plan["steps_compute_phase_uncompute"])
                constants.add((value + 2 * candidate * packet.residual(z)[0]) % q)
            assert len(constants) == 1
            assert plan["reusable_clean_ancillas"] == 1
            assert not plan["unknown_secret_or_phase_evaluator_required"]
            assert not plan["physical_backend_execution_verified"]
    packet = compile_packet([[1] * 65], 128)
    plan = known_residue_phase_correction_plan(packet, [1])
    assert plan["logical_width"] == 64
    assert max(int(s["logical_parity_mask_hex"], 16) for s in plan["steps_compute_phase_uncompute"]) > 2**53
    with pytest.raises(ValueError):
        known_residue_phase_correction_plan(packet, [])
