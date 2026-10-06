from fractions import Fraction

import pytest

from dcp_carry_packets import compile_packet
from dcp_carry_throughput_gate import (
    calibration_product_on_background,
    fixed_direction_conductor_gate,
    native_fixed_yield_bound,
    q8_postselection_ledger,
    run_controls,
)


def test_q4_isotropy_and_zero_background_cannot_certify_q8_throughput():
    directions = (7, 25)
    labels = [[1, 3, 1, 3, 1, 3]]
    q4 = compile_packet(labels, 4)
    assert all(calibration_product_on_background(q4, directions, z) for z in range(32))
    q8 = compile_packet(labels, 8)
    assert calibration_product_on_background(q8, directions, 0)
    assert not all(calibration_product_on_background(q8, directions, z) for z in range(32))
    assert not fixed_direction_conductor_gate(q8, directions)["necessary_gate_passed"]
    with pytest.raises(ValueError, match=">=8"):
        fixed_direction_conductor_gate(q4, directions)


def test_disjoint_zero_sum_blocks_remain_a_real_positive_baseline():
    for q in (8, 16, 256):
        packet = compile_packet([[1, 3, 5, 7, 9, 11]], q)
        # Physical directions {0,1} and {2,3}; both have even parity sum.
        directions = (1, 6)
        assert fixed_direction_conductor_gate(packet, directions)["necessary_gate_passed"]
        assert all(calibration_product_on_background(packet, directions, z) for z in range(32))


def test_conductor_gate_is_necessary_not_sufficient():
    packet = compile_packet([[2, 2, 2]], 8)
    gate = fixed_direction_conductor_gate(packet, (3, 5))
    assert gate["necessary_gate_passed"]
    assert not gate["sufficient_product_output_certificate"]
    assert not calibration_product_on_background(packet, (3, 5), 0)
    with pytest.raises(ValueError, match="independent"):
        fixed_direction_conductor_gate(packet, (1, 1))


def test_postselection_rate_is_exact_not_free_conditional_sampling():
    packet = compile_packet([[1, 3, 1, 3, 1, 3]], 8)
    directions = (7, 25)
    ledger = q8_postselection_ledger(packet, directions)
    assert ledger["constraint_rank"] == 1
    assert ledger["success_probability"] == {"numerator": "1", "denominator": "2"}
    for background in range(32):
        predicted = all((row & background).bit_count() % 2 == target
                        for row, target in zip(ledger["logical_constraint_rows"], ledger["constraint_targets"]))
        assert predicted == calibration_product_on_background(packet, directions, background)
    assert not ledger["free_postselection"]
    assert not ledger["conditioned_output_labels_proved_iid"]


def test_cubic_obstruction_cannot_be_fixed_by_selecting_backgrounds():
    packet = compile_packet([[1, 1, 1, 1, 1, 1, 1, 1]], 8)
    # Even pair overlaps but odd triple overlap in the physical cube.
    physical = (0b00001111, 0b00110011, 0b01010101)
    directions = tuple(u >> 1 for u in physical)
    ledger = q8_postselection_ledger(packet, directions)
    assert not ledger["possible"]
    assert ledger["reason"] == "cubic interaction on retained subspace"
    assert not any(calibration_product_on_background(packet, directions, z) for z in range(128))


def test_three_overlapping_outputs_can_survive_costed_postselection():
    packet = compile_packet([[1] * 8], 8)
    directions = (7, 25, 97)
    ledger = q8_postselection_ledger(packet, directions)
    assert ledger["possible"]
    assert ledger["constraint_rank"] == 1
    successes = 0
    for z in range(128):
        accepted = all((row & z).bit_count() % 2 == target
                       for row, target in zip(ledger["logical_constraint_rows"], ledger["constraint_targets"]))
        assert accepted == calibration_product_on_background(packet, directions, z)
        successes += accepted
    assert successes == 64
    assert not fixed_direction_conductor_gate(packet, directions)["necessary_gate_passed"]


def test_nonproduct_branch_has_a_constant_pure_product_fidelity_gap():
    import numpy as np
    from dcp_carry_packets import calibration_packet_state

    ceiling = (1 + 1 / np.sqrt(2)) / 2
    for q in (8, 16, 256):
        packet = compile_packet([[1, 1, 1]], q)
        state = calibration_packet_state(packet, [q // 8]).reshape(2, 2)
        eigenvalue = np.linalg.eigvalsh(state @ state.conj().T)[-1]
        assert eigenvalue == pytest.approx(ceiling)
        assert np.sqrt(1 - eigenvalue) == pytest.approx(np.sin(np.pi / 8))


def test_native_cap_bound_is_exact_and_preserves_adaptive_escape():
    row = native_fixed_yield_bound(128)
    value = row["cap_failure_probability_upper_bound"]
    probability = Fraction(int(value["numerator_hex"], 16), 1 << value["denominator_binary_exponent"])
    assert probability < Fraction(1, 10**10)
    assert row["fixed_all_outcome_product_output_cap"] <= 31
    assert not row["outcome_adaptive_direction_selection_covered"]
    assert not row["general_quantum_measurements_covered"]
    with pytest.raises(ValueError):
        native_fixed_yield_bound(0)


def test_exhaustive_affine_controls_never_violate_conductor_necessity():
    report = run_controls()
    assert report["exhaustive_implication_checks"] > 1000
    assert report["exhaustive_postselection_probability_checks"] == report["exhaustive_implication_checks"]
    assert report["all_outcome_product_pairs_retained"] > 0
    assert report["zero_background_false_positive"]["failing_backgrounds"]
    assert not report["outcome_adaptive_or_correlated_decoder_excluded"]
    assert not report["speedup_claim_allowed"]
