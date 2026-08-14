import pytest

from self_dual_wreath_alternating_parity_coset_channel import (
    audit_alternating_parity_coset_channel,
    parity_coset_word_likelihood_arrays,
    run_alternating_parity_coset_channel,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import sign_frequency


def test_seven_nonzero_parity_cosets_have_two_tetrahedral_types():
    _orbits, arrays = parity_coset_word_likelihood_arrays(3)
    nonzero = [parity for parity in arrays if parity != (0, 0, 0)]
    assert sum(sum(sign_frequency(parity)) == 3 for parity in nonzero) == 4
    assert sum(sum(sign_frequency(parity)) == 4 for parity in nonzero) == 3


def test_exact_fourier_reconstruction_and_conditional_channel_through_S5():
    rows = [audit_alternating_parity_coset_channel(n) for n in range(2, 6)]
    assert all(row.exact_parity_coset_channel_verified for row in rows)
    assert all(row.maximum_orientation_fourier_reconstruction_residual < 2e-8 for row in rows)
    assert all(row.maximum_base_likelihood_residual < 2e-8 for row in rows)
    assert all(row.maximum_conditional_probability_sum_residual < 2e-8 for row in rows)
    assert all(row.minimum_conditional_syndrome_probability >= -2e-8 for row in rows)


def test_coset_conditional_kl_matches_lossless_chain():
    for n in range(2, 6):
        row = audit_alternating_parity_coset_channel(n)
        assert row.expected_conditional_syndrome_kl_bits == pytest.approx(
            row.kl_chain_conditional_syndrome_kl_bits,
            abs=2e-8,
        )
        assert row.conditional_kl_residual < 2e-8


def test_tetrahedral_symmetry_equalizes_annealed_ratio_moments_within_types():
    rows = [audit_alternating_parity_coset_channel(n) for n in range(2, 6)]
    assert all(row.maximum_face_type_annealed_ratio_moment_residual < 2e-8 for row in rows)
    assert all(row.maximum_opposite_type_annealed_ratio_moment_residual < 2e-8 for row in rows)
    assert rows[-1].face_type_annealed_ratio_moment > 0
    assert rows[-1].opposite_type_annealed_ratio_moment > 0


def test_report_keeps_both_trimmed_twist_gates_open():
    report = run_alternating_parity_coset_channel()
    assert report.headline_metrics["alternating_parity_coset_channel_theorem_count"] == 1
    assert report.claim_gate["adaptive_syndrome_equals_parity_coset_imbalance_proved"]
    assert report.claim_gate["seven_twists_reduce_to_two_tetrahedral_types_proved"]
    assert not report.claim_gate["trimmed_face_twist_ratio_vanishes_proved"]
    assert not report.claim_gate["trimmed_opposite_twist_ratio_vanishes_proved"]
    assert not report.claim_gate["orbit_adaptive_syndrome_survives_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
