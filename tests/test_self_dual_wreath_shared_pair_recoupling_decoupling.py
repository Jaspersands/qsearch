import json

from self_dual_wreath_shared_pair_recoupling_decoupling import (
    audit_shared_pair_recoupling_decoupling,
    inverse_class_square_sum,
    plancherel_weights,
    run_shared_pair_recoupling_decoupling,
    shared_pair_joint_law,
    shared_pair_recoupling_scaling_record,
    write_shared_pair_recoupling_decoupling_report,
)


def test_shared_pair_joint_law_normalizes_and_has_plancherel_marginals() -> None:
    for n in range(3, 10):
        weights = plancherel_weights(n)
        joint = shared_pair_joint_law(n)
        assert sum(joint.values()) == 1
        for left in weights:
            assert sum(
                probability
                for (row, _), probability in joint.items()
                if row == left
            ) == weights[left]


def test_multiplicity_and_character_kernels_agree() -> None:
    for n in range(3, 9):
        row = audit_shared_pair_recoupling_decoupling(
            n,
            validate_multiplicity_kernel=True,
        )
        assert row.maximum_multiplicity_character_kernel_residual == 0
        assert row.exact_shared_pair_decoupling_theorem_verified


def test_chi_square_is_exact_inverse_class_square_sum() -> None:
    for n in range(3, 11):
        row = audit_shared_pair_recoupling_decoupling(
            n,
            validate_multiplicity_kernel=False,
        )
        assert row.chi_square_identity_residual == "0"
        assert row.exact_chi_square_divergence == str(inverse_class_square_sum(n))
        assert row.total_variation_bound_violation == 0
        assert row.mutual_information_bound_violation == 0


def test_transposition_class_asymptotically_dominates_exact_sum() -> None:
    rows = [shared_pair_recoupling_scaling_record(n) for n in (16, 24, 32)]
    ratios = [
        row.exact_inverse_class_square_sum / row.transposition_leading_term
        for row in rows
    ]
    assert all(ratio >= 1 for ratio in ratios)
    assert ratios == sorted(ratios, reverse=True)
    assert ratios[-1] < 1.003


def test_scaling_keeps_coherent_path_escape_open() -> None:
    row = shared_pair_recoupling_scaling_record(32)
    assert row.asymptotic_total_variation == "O(n^-2)"
    assert row.asymptotic_mutual_information == "O(n^-4)"
    assert row.dephased_shared_pair_label_correlation_inverse_polynomial
    assert not row.coherent_multiplicity_racah_phases_ruled_out


def test_report_preserves_dephased_scope() -> None:
    report = run_shared_pair_recoupling_decoupling()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["dephased_shared_pair_outputs_asymptotically_decouple"]
    assert not report.claim_gate["coherent_multiplicity_racah_paths_dequantized"]
    assert not report.claim_gate["state_dependent_transition_filter_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_emits_valid_json(tmp_path) -> None:
    path = tmp_path / "shared_pair_recoupling_decoupling.json"
    payload = write_shared_pair_recoupling_decoupling_report(path)
    parsed = json.loads(path.read_text())
    assert parsed["status"] == payload["status"]
    assert parsed["headline_metrics"] == payload["headline_metrics"]
