import itertools

from self_dual_wreath_alternating_cycle_type_block_dependence import (
    audit_cycle_type_block_dependence,
    inverse_output_word_map,
    output_word_map,
    run_alternating_cycle_type_block_dependence,
    write_alternating_cycle_type_block_dependence_report,
)


def test_output_word_map_inverse_is_exact_on_small_symmetric_groups() -> None:
    for n in (2, 3):
        group = tuple(itertools.permutations(range(n)))
        for triple in itertools.product(group, repeat=3):
            assert inverse_output_word_map(*output_word_map(*triple)) == triple


def test_all_cycle_type_coordinates_are_pairwise_independent() -> None:
    for n in range(2, 6):
        row = audit_cycle_type_block_dependence(n)
        assert row.maximum_one_coordinate_marginal_residual == "0"
        assert row.maximum_pairwise_independence_residual == "0"
        assert row.collision_duality_residual == "0"
        assert row.exact_block_dependence_structure_verified


def test_shannon_information_is_not_preserved_by_character_transform() -> None:
    rows = [audit_cycle_type_block_dependence(n) for n in (3, 4, 5)]

    assert any(row.shannon_duality_residual_bits > 1e-6 for row in rows)
    assert rows[0].shannon_information_preserved_by_fourier_transform
    assert all(
        not row.shannon_information_preserved_by_fourier_transform
        for row in rows[1:]
    )


def test_report_rejects_marginal_mixing_as_joint_evidence(tmp_path) -> None:
    report = run_alternating_cycle_type_block_dependence()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["input_output_word_map_bijection_proved"]
    assert report.claim_gate["all_scalar_cycle_type_pairs_independent_proved"]
    assert report.claim_gate[
        "even_collision_is_joint_block_renyi_dependence_proved"
    ]
    assert not report.claim_gate["single_product_mixing_sufficient"]
    assert not report.claim_gate["pairwise_mixing_sufficient"]
    assert not report.claim_gate[
        "shannon_cycle_type_information_equals_label_kl"
    ]
    assert not report.claim_gate["joint_block_collision_subpolynomial_proved"]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "block-dependence.json"
    payload = write_alternating_cycle_type_block_dependence_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
