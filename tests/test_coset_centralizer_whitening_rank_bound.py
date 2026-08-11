import pytest

from coset_centralizer_whitening_rank_bound import (
    build_coset_centralizer_whitening_rank_report,
    centralizer_rank_envelope,
    fixed_point_free_scaling_record,
    fixed_point_free_square_root_count,
    finite_centralizer_rank_control,
    involution_centralizer_order,
    square_root_character_control,
    write_coset_centralizer_whitening_rank_report,
)


def test_fixed_point_free_square_root_formula_and_character_identity():
    assert fixed_point_free_square_root_count(6) == 0
    assert fixed_point_free_square_root_count(8) == 12
    for n in (4, 6, 8, 10, 12):
        row = square_root_character_control(n, n // 2)
        assert row.frobenius_schur_square_root_identity_verified
        assert row.sum_irrep_characters == row.direct_fixed_point_free_square_root_count


def test_centralizer_order_and_small_envelopes():
    assert involution_centralizer_order(4, 2) == 8
    assert centralizer_rank_envelope(4, 2) == pytest.approx(1.5)
    assert centralizer_rank_envelope(5, 2) == pytest.approx(3.5)


def test_finite_actual_rank_obeys_copy_independent_centralizer_bound():
    for copy_count in (1, 2, 3):
        row = finite_centralizer_rank_control(5, 2, copy_count)
        assert row.finite_control_verified
        assert row.upper_bound_residual < 1e-10
        assert row.observed_average_multiplicity_rank_ratio <= (
            row.centralizer_restriction_upper_bound + 1e-10
        )


def test_fixed_point_free_envelope_is_exp_sqrt_not_factorial():
    row = fixed_point_free_scaling_record(256)
    assert row.lower_bound_below_exact
    assert row.exact_below_upper_bound
    assert row.envelope_is_exp_theta_sqrt_n
    assert row.log2_exact_centralizer_rank_envelope < 32
    assert row.constant_pgm_success_copy_count > 500


def test_report_preserves_actual_rank_and_algorithm_gates(tmp_path):
    report = build_coset_centralizer_whitening_rank_report()
    assert report.theorem.theorem_verified
    assert report.theorem.multiplicity_rank_as_restriction_map_rank_proved
    assert report.theorem.copy_independent_natural_upper_bound_proved
    assert report.theorem.fixed_point_free_exp_sqrt_envelope_proved
    assert not report.theorem.actual_rank_matches_envelope_proved
    assert not report.theorem.polynomial_actual_rank_proved
    assert not report.theorem.coherent_restriction_transform_constructed
    assert not report.theorem.polynomial_hidden_involution_algorithm_proved
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_centralizer_whitening_rank_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "centralizer-rank-envelope-sharp-image-rank-open"
    )
