from self_dual_wreath_alternating_block_operator_anova import (
    allowed_anova_masks,
    audit_block_operator_anova,
    run_alternating_block_operator_anova,
    write_alternating_block_operator_anova_report,
)


def test_dual_private_generator_intersection_has_fourteen_blocks() -> None:
    masks = allowed_anova_masks()

    assert len(masks) == 14
    counts = {size: sum(mask.bit_count() == size for mask in masks) for size in range(7)}
    assert counts == {0: 0, 1: 0, 2: 0, 3: 4, 4: 3, 5: 6, 6: 1}


def test_exact_channel_anova_has_no_forbidden_energy() -> None:
    for n in range(2, 6):
        control, _rows = audit_block_operator_anova(n)
        assert control.maximum_forbidden_anova_block_energy < 2e-9
        assert control.exact_anova_energy_decomposition_residual < 2e-9
        assert control.allowed_anova_block_count == 14
        assert control.exact_private_generator_sparsity_verified


def test_order_six_anova_is_not_mistaken_for_nonidentity_class_core() -> None:
    controls = [audit_block_operator_anova(n)[0] for n in (4, 5)]

    assert all(abs(row.order_six_anova_minus_z6_core) > 1e-6 for row in controls)
    assert all(0 <= row.maximum_nonconstant_singular_value <= 1 + 1e-10 for row in controls)


def test_anova_energies_reconstruct_centered_collision_norm() -> None:
    for n in (3, 4, 5):
        row, _blocks = audit_block_operator_anova(n)
        total = (
            row.order_three_total_energy
            + row.order_four_total_energy
            + row.order_five_total_energy
            + row.order_six_total_energy
        )
        assert abs(total - row.centered_operator_hilbert_schmidt_square) < 2e-9
        assert abs(
            row.normalized_operator_hilbert_schmidt_square
            - 1.0
            - row.centered_operator_hilbert_schmidt_square
        ) < 2e-9


def test_report_keeps_all_growing_support_norm_claims_open(tmp_path) -> None:
    report = run_alternating_block_operator_anova()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["normalized_conditional_collision_operator_proved"]
    assert report.claim_gate["dual_private_generator_sparsity_proved"]
    assert report.claim_gate["fourteen_block_anova_normal_form_proved"]
    assert not report.claim_gate["order_six_anova_equals_z6_core"]
    assert not report.claim_gate[
        "growing_support_allowed_blocks_subpolynomial_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "anova.json"
    payload = write_alternating_block_operator_anova_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
