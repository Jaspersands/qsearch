from __future__ import annotations

import math
from fractions import Fraction

from self_dual_wreath_source_conditioned_channel_decoupling import (
    analytic_half_class_sum_upper_bound,
    character_ratio_energy,
    exact_direct_five_character_variance,
    exact_nonidentity_class_convolution_energy,
    half_reciprocal_class_sum,
    plancherel_character_energy_moments,
    run_source_conditioned_channel_decoupling,
    source_conditioned_channel_control,
    source_conditioned_channel_scaling_record,
    source_averaged_conditional_chi_square,
    write_source_conditioned_channel_decoupling_report,
)
from self_dual_wreath_plancherel_kronecker_positivity import (
    reciprocal_nonidentity_class_sum,
)


def test_exact_character_energy_moments_and_convolution_identity() -> None:
    for n in range(3, 7):
        first, second = plancherel_character_energy_moments(n)
        variance = reciprocal_nonidentity_class_sum(n)

        assert first == variance
        assert second == exact_nonidentity_class_convolution_energy(n)
        assert source_averaged_conditional_chi_square(n) == 2 * first + second

    for n in (3, 4):
        assert exact_direct_five_character_variance(n) == (
            source_averaged_conditional_chi_square(n)
        )


def test_young_contraction_controls_plancherel_fourth_moment() -> None:
    for n in range(3, 15):
        _, second = plancherel_character_energy_moments(n)
        half_sum = half_reciprocal_class_sum(n)

        assert float(second) <= half_sum**2 + 1e-12


def test_uniform_character_energy_route_is_falsified() -> None:
    assert character_ratio_energy((10,)) == 41
    assert character_ratio_energy((9, 1)) > 1

    row = source_conditioned_channel_control(10)
    assert row.uniform_character_energy_bound_falsified
    assert row.maximum_character_energy_partition == (10,)
    assert row.maximum_nonlinear_character_energy_partition == (9, 1)


def test_exact_controls_record_closed_variance_reduction() -> None:
    for n in range(3, 8):
        row = source_conditioned_channel_control(
            n,
            validate_convolution=n <= 6,
            validate_direct=n <= 4,
        )

        assert row.exact_first_moment_identity_verified
        assert row.exact_variance_decomposition_verified
        assert row.exact_convolution_identity_verified is not False
        assert row.exact_direct_five_character_identity_verified is not False
        assert row.source_averaged_chi_square_upper_bound + 1e-12 >= float(
            Fraction(row.exact_source_averaged_conditional_chi_square)
        )


def test_half_reciprocal_sum_and_information_bounds_decay() -> None:
    rows = [
        source_conditioned_channel_scaling_record(n)
        for n in (16, 20, 24, 30, 40, 50)
    ]

    assert [row.half_reciprocal_class_sum for row in rows] == sorted(
        (row.half_reciprocal_class_sum for row in rows),
        reverse=True,
    )
    assert rows[-1].source_averaged_chi_square_upper_bound < 0.004
    assert rows[-1].average_conditional_mutual_information_upper_bound_bits < 0.006


def test_explicit_asymptotic_majorant_is_valid_and_vanishing() -> None:
    rows = [
        analytic_half_class_sum_upper_bound(n)
        for n in (300, 1_000, 10_000, 100_000)
    ]

    assert all(row.geometric_majorants_valid for row in rows)
    assert [row.analytic_half_reciprocal_sum_upper_bound for row in rows] == sorted(
        (row.analytic_half_reciprocal_sum_upper_bound for row in rows),
        reverse=True,
    )
    assert rows[-1].analytic_source_averaged_chi_square_upper_bound < 0.01


def test_report_closes_only_the_pre_final_dephased_route(tmp_path) -> None:
    report = run_source_conditioned_channel_decoupling()

    assert report.claim_gate["exact_source_conditioned_channel_law_proved"]
    assert report.claim_gate[
        "source_averaged_channel_chi_square_vanishes_proved"
    ]
    assert report.claim_gate[
        "five_label_plancherel_product_law_in_total_variation_proved"
    ]
    assert report.claim_gate["dephased_channel_route_without_final_label_closed"]
    assert not report.claim_gate[
        "final_label_conditioned_channel_information_vanishes_proved"
    ]
    assert not report.claim_gate["full_six_label_product_law_proved"]
    assert not report.claim_gate["coherent_multiplicity_phase_signal_absent_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "source-conditioned-decoupling.json"
    payload = write_source_conditioned_channel_decoupling_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["final_label_necessity_reduction_count"] == 1
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0


def test_information_bound_is_consistent_with_pinsker_scale() -> None:
    row = source_conditioned_channel_control(14)
    chi = float(Fraction(row.exact_source_averaged_conditional_chi_square))

    assert row.average_total_variation_upper_bound == 0.5 * math.sqrt(chi)
    assert row.average_conditional_mutual_information_upper_bound_bits == math.log2(
        1 + chi
    )
