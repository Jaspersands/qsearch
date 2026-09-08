from coset_natural_multicopy_pgm_benchmark import _source_data
from self_dual_wreath_carrier_holevo_budget_theorem import (
    analytic_log2_partition_upper_bound,
    audit_carrier_pinching_holevo_control,
    carrier_holevo_scaling_record,
    partition_number,
    run_carrier_holevo_budget_theorem,
    write_carrier_holevo_budget_theorem_report,
)


def test_partition_number_and_generating_function_bound() -> None:
    known = {1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 10: 42, 20: 627}
    for n, expected in known.items():
        assert partition_number(n) == expected
        assert partition_number(n).bit_length() - 1 <= (
            analytic_log2_partition_upper_bound(n)
        )


def test_noncommuting_carrier_pinching_losses_obey_telescope_budget() -> None:
    partitions, _, _ = _source_data(4, 2)
    standard = partitions.index((3, 1))
    control = audit_carrier_pinching_holevo_control(
        "S4-STANDARD-CUBED",
        4,
        2,
        (standard, standard, standard),
    )
    assert control.initial_holevo_information_bits > 1.0
    assert control.left_holevo_loss_bits >= -1e-12
    assert control.second_holevo_loss_bits >= -1e-12
    assert control.left_holevo_loss_bits <= control.left_log_outcome_bound_bits
    assert control.total_holevo_loss_bits <= control.two_round_log_outcome_bound_bits
    assert control.left_coherence_difference_identity_residual <= 1e-12
    assert control.two_round_telescope_residual <= 1e-12
    assert control.entropy_budget_verified is True


def test_threshold_scaling_retains_extensive_holevo_for_shallow_hierarchy() -> None:
    records = [carrier_holevo_scaling_record(n) for n in (64, 256, 1024)]
    assert all(record.pgm_success_lower_bound >= 0.8 for record in records)
    assert all(
        record.exact_log2_partition_count
        <= record.analytic_log2_partition_upper_bound
        for record in records
    )
    assert all(record.extensive_holevo_lower_bound_survives for record in records)
    assert records[-1].post_pinching_holevo_lower_bound_bits > 1000
    assert records[-1].post_pinching_fraction_of_fano_lower_bound > 0.7
    assert all(not record.accessible_information_lower_bound_proved for record in records)


def test_report_proves_holevo_budget_but_keeps_access_and_decoder_open() -> None:
    report = run_carrier_holevo_budget_theorem()
    assert report.theorem.single_pinching_holevo_bound_proved is True
    assert report.theorem.adaptive_holevo_budget_proved is True
    assert report.theorem.partition_label_sqrt_n_bound_proved is True
    assert report.theorem.threshold_extensive_input_holevo_proved is True
    assert report.theorem.shallow_hierarchy_extensive_holevo_retention_proved is True
    assert report.theorem.accessible_information_retention_proved is False
    assert report.claim_gate["full_linear_depth_carrier_tree_certified"] is False
    assert report.claim_gate[
        "carrier_hierarchy_accessible_information_retained"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_theorem_artifact_without_registry(tmp_path) -> None:
    output = tmp_path / "carrier-holevo-budget.json"
    payload = write_carrier_holevo_budget_theorem_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "shallow-carrier-extensive-holevo-retained-accessible-decoder-open"
    )
    assert payload["headline_metrics"][
        "accessible_information_retention_theorem_count"
    ] == 0
