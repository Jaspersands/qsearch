from fractions import Fraction

from self_dual_wreath_alternating_product_character_zeta import (
    audit_product_character_zeta_finite,
    coarse_product_character_energy,
    product_character_zeta_scaling_control,
    run_alternating_product_character_zeta,
    write_alternating_product_character_zeta_report,
)


def test_exact_product_character_energies_include_split_multiplicity() -> None:
    expected = {
        2: (Fraction(0), Fraction(0)),
        3: (Fraction(1, 2), Fraction(1, 4)),
        4: (Fraction(11, 18), Fraction(85, 324)),
        5: (Fraction(569, 3600), Fraction(111361, 12960000)),
    }

    for n, (order_three, order_four) in expected.items():
        assert coarse_product_character_energy(n, 2) == order_three
        assert coarse_product_character_energy(n, 3) == order_four


def test_formulas_match_every_order_three_and_order_four_anova_block() -> None:
    for n in range(2, 6):
        row = audit_product_character_zeta_finite(n)
        assert row.order_three_block_count == 4
        assert row.order_four_block_count == 3
        assert row.maximum_order_three_formula_residual < 2e-9
        assert row.maximum_order_four_formula_residual < 2e-9
        assert row.order_three_total_formula_residual < 2e-9
        assert row.order_four_total_formula_residual < 2e-9
        assert row.exact_product_character_formulas_verified


def test_witten_zeta_and_minimum_degree_dominate_exact_energies() -> None:
    for n in (5, 8, 12, 16, 20):
        row = product_character_zeta_scaling_control(n)
        assert row.minimum_nontrivial_nonsign_dimension >= n - 1
        assert row.one_order_three_energy <= row.order_three_zeta_upper + 2e-14
        assert row.one_order_four_energy <= row.order_four_zeta_upper + 2e-14
        assert row.witten_zeta_four_tail <= (
            row.order_four_minimum_degree_upper + 2e-14
        )
        assert row.zeta_domination_verified
        assert row.minimum_degree_transfer_verified


def test_report_closes_only_lower_product_blocks(tmp_path) -> None:
    report = run_alternating_product_character_zeta()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["coarse_product_character_formulas_proved"]
    assert report.claim_gate["order_three_anova_energy_vanishes_proved"]
    assert report.claim_gate["order_four_anova_energy_vanishes_proved"]
    assert not report.claim_gate[
        "order_five_anova_energy_vanishes_from_this_theorem"
    ]
    assert not report.claim_gate["canonical_trimmed_sixway_subpolynomial_proved"]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "product-character-zeta.json"
    payload = write_alternating_product_character_zeta_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
