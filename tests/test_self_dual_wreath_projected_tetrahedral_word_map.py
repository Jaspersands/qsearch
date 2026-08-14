from __future__ import annotations

import math

from self_dual_wreath_projected_tetrahedral_word_map import (
    audit_projected_tetrahedral_word_map,
    projected_kernel_subprobability_chi_square,
    projected_mean_and_kernel,
    run_projected_tetrahedral_word_map,
    write_projected_tetrahedral_word_map_report,
)


def test_full_projected_kernel_recovers_untrimmed_chi_square() -> None:
    expected = {2: 7.0, 3: 12.5, 4: 3581 / 162}
    for n, chi_square in expected.items():
        value = projected_kernel_subprobability_chi_square(n, 0)

        assert float(value) == chi_square


def test_projected_mean_and_kernel_have_correct_full_limits() -> None:
    for n in range(2, 5):
        retained, mass, mean, kernel = projected_mean_and_kernel(n, 0)
        identity = (1,) * n

        assert len(retained) > 0
        assert mass == 1
        assert mean[identity] == 1
        assert all(
            value == (1 if cycle_type == identity else 0)
            for cycle_type, value in mean.items()
        )
        assert kernel[identity, identity] == 1


def test_label_and_projected_kernel_chi_square_agree_after_trims() -> None:
    for n, threshold in ((3, 0), (3, 1), (4, 0), (4, 1), (4, 2)):
        row = audit_projected_tetrahedral_word_map(
            n,
            threshold,
            validate_projected_kernel=True,
        )

        assert row.exact_projected_kernel_identity_verified
        assert row.projected_kernel_identity_residual is not None
        assert row.projected_kernel_identity_residual < 1e-9
        assert row.retained_unnormalized_total_variation <= (
            row.chi_square_total_variation_upper_bound + 1e-9
        )


def test_one_dimensional_trim_removes_raw_s5_chi_square_tail() -> None:
    full = audit_projected_tetrahedral_word_map(5, 0)
    trimmed = audit_projected_tetrahedral_word_map(5, 1)

    assert trimmed.retained_plancherel_mass < 1
    assert trimmed.label_space_subprobability_chi_square < 1
    assert trimmed.label_space_subprobability_chi_square < (
        full.label_space_subprobability_chi_square / 10
    )
    assert trimmed.retained_unnormalized_total_variation > 0
    assert trimmed.retained_positive_kl_contribution_bits > 0


def test_retained_product_mass_is_sixth_power_of_retained_plancherel_mass() -> None:
    for n, threshold in ((3, 1), (4, 1), (5, 1), (5, 4)):
        row = audit_projected_tetrahedral_word_map(n, threshold)

        assert math.isclose(
            row.retained_product_mass,
            row.retained_plancherel_mass**6,
            rel_tol=1e-10,
            abs_tol=1e-10,
        )


def test_report_keeps_projected_asymptotic_and_coherent_routes_open(tmp_path) -> None:
    report = run_projected_tetrahedral_word_map()

    assert report.claim_gate["high_dimension_projected_word_map_identity_proved"]
    assert report.claim_gate["raw_parity_chi_square_tail_excluded_by_projection"]
    assert not report.claim_gate[
        "canonical_projected_collision_norm_vanishes_proved"
    ]
    assert not report.claim_gate[
        "canonical_projected_collision_norm_survives_proved"
    ]
    assert not report.claim_gate["retained_positive_kl_survives_proved"]
    assert not report.claim_gate["classical_baseline_separated"]
    assert not report.claim_gate["coherent_multiplicity_transform_compiled"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "projected-word-map.json"
    payload = write_projected_tetrahedral_word_map_report(path)
    assert path.exists()
    assert payload["headline_metrics"][
        "canonical_projected_collision_asymptotic_theorem_count"
    ] == 0
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
