from fractions import Fraction

import pytest

from self_dual_wreath_parity_racah_toric_obstruction import (
    audit_kronecker_transpose_xor,
    audit_racah_toric_control,
    conditional_independence_minors,
    conditional_mutual_information_bits,
    cube_binomial_defect,
    exact_natural_syndrome_amplitudes,
    exact_rank_profile_amplitudes,
    run_parity_racah_toric_obstruction,
    write_parity_racah_toric_obstruction_report,
)


def test_kronecker_transpose_dependence_is_exactly_one_xor_bit() -> None:
    for n in (3, 4, 5):
        control = audit_kronecker_transpose_xor(n)
        assert control.tested_oriented_triple_count > 0
        assert control.mismatch_count == 0
        assert control.transpose_xor_law_verified


def test_rank_profile_factorization_obeys_exact_markov_toric_identities() -> None:
    rank, faces, totals, _base = exact_rank_profile_amplitudes(
        5, (1, 2, 1, 2, 2, 2)
    )

    assert faces == ((1, 1),) * 4
    assert totals == (4, 3)
    assert rank == (
        Fraction(1, 100),
        Fraction(1, 75),
        Fraction(1, 100),
        Fraction(1, 75),
        Fraction(1, 100),
        Fraction(1, 75),
        Fraction(1, 100),
        Fraction(1, 75),
    )
    assert conditional_independence_minors(rank) == (0, 0)
    assert cube_binomial_defect(rank) == 0
    assert conditional_mutual_information_bits(rank) == pytest.approx(0.0, abs=1e-14)


def test_exact_positive_s5_natural_channel_violates_rank_toric_model() -> None:
    natural = exact_natural_syndrome_amplitudes(5, (1, 2, 1, 2, 2, 2))

    assert natural == (
        Fraction(1, 64),
        Fraction(1, 64),
        Fraction(1, 64),
        Fraction(9, 1600),
        Fraction(1, 64),
        Fraction(9, 1600),
        Fraction(1, 14400),
        Fraction(1, 64),
    )
    assert all(value > 0 for value in natural)
    assert conditional_independence_minors(natural) == (
        Fraction(-7, 28800),
        Fraction(17, 80000),
    )
    assert cube_binomial_defect(natural) == Fraction(-61, 1024000000)
    assert conditional_mutual_information_bits(natural) > 0.2


def test_toric_audit_separates_finite_flat_and_arithmetic_witnesses() -> None:
    flat = audit_racah_toric_control("S4-FLAT", 4, (1,) * 6)
    witness = audit_racah_toric_control("S5-WITNESS", 5, (1, 2, 1, 2, 2, 2))

    assert flat.exact_rank_factorization_verified
    assert not flat.natural_channel_outside_rank_profile_toric_model
    assert not flat.exact_toric_obstruction_verified
    assert witness.exact_rank_factorization_verified
    assert witness.natural_channel_outside_rank_profile_toric_model
    assert witness.exact_toric_obstruction_verified
    assert witness.maximum_exact_to_projector_amplitude_residual < 1e-12
    assert witness.maximum_rank_factorization_residual < 1e-12
    assert witness.all_natural_amplitudes_positive
    assert witness.rank_conditional_mutual_information_bits == pytest.approx(0.0, abs=1e-14)
    assert witness.natural_conditional_mutual_information_bits > 0.2


def test_report_preserves_finite_scope_and_closed_speedup_gates(tmp_path) -> None:
    report = run_parity_racah_toric_obstruction()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["exact_natural_toric_counterexample_count"] == 1
    assert report.claim_gate["rank_profile_is_G_K_H_markov_channel_proved"]
    assert report.claim_gate[
        "rank_profile_has_zero_three_factor_log_interaction_proved"
    ]
    assert report.claim_gate["natural_racah_channel_can_escape_rank_toric_model_proved"]
    assert report.claim_gate["finite_witness_is_strictly_positive"]
    assert not report.claim_gate["asymptotic_toric_violation_survives_proved"]
    assert not report.claim_gate["canonical_source_mass_positive_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "toric.json"
    payload = write_parity_racah_toric_obstruction_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
