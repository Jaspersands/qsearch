from fractions import Fraction

from self_dual_wreath_alternating_even_collision_core_reduction import (
    audit_even_class_asymptotics,
    audit_even_collision_support,
    even_class_power_sum,
    even_reciprocal_support_expansion,
    even_support_centralizer_power_sum,
    run_alternating_even_collision_core_reduction,
    write_alternating_even_collision_core_reduction_report,
)


def test_even_support_coefficients_start_with_three_cycles_and_double_transpositions() -> None:
    assert even_support_centralizer_power_sum(2, 1) == 0
    assert even_support_centralizer_power_sum(3, 1) == 3
    assert even_support_centralizer_power_sum(4, 1) == 8
    assert even_support_centralizer_power_sum(5, 1) == 5
    assert even_support_centralizer_power_sum(3, 2) == 9


def test_even_support_expansion_exactly_recovers_class_sums() -> None:
    for n in range(3, 13):
        for power in (1, 2):
            assert even_reciprocal_support_expansion(n, power) == even_class_power_sum(
                n, power
            )


def test_exact_even_collision_has_only_one_unresolved_full_mask() -> None:
    for n in (3, 4, 5):
        row = audit_even_collision_support(n)
        assert row.size_three_mask_count == 4
        assert row.size_four_mask_count == 3
        assert row.size_five_mask_count == 6
        assert row.size_six_mask_count == (0 if n == 3 else 1)
        assert row.exact_decomposition_residual == "0"
        assert row.support_coefficients_verified
        assert row.exact_support_decomposition_verified


def test_even_lower_support_scales_are_smaller_and_energy_is_dominated() -> None:
    rows = [audit_even_class_asymptotics(n) for n in (5, 8, 12, 16)]

    assert all(row.even_energy_dominated_by_full for row in rows)
    assert rows[-1].n_cubed_scaled_even_reciprocal_sum < 4.6
    assert rows[-1].n_sixth_scaled_even_inverse_square_sum < 14.1
    assert [row.exact_even_character_energy_second_moment for row in rows] == sorted(
        (row.exact_even_character_energy_second_moment for row in rows),
        reverse=True,
    )


def test_report_closes_lower_support_but_not_fully_nonidentity_core(tmp_path) -> None:
    report = run_alternating_even_collision_core_reduction()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["even_collision_support_decomposition_proved"]
    assert report.claim_gate["all_lower_support_even_terms_vanish_proved"]
    assert report.claim_gate[
        "fully_nonidentity_even_core_is_only_renyi_obstruction"
    ]
    assert not report.claim_gate[
        "fully_nonidentity_even_core_subpolynomial_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "even-core.json"
    payload = write_alternating_even_collision_core_reduction_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
