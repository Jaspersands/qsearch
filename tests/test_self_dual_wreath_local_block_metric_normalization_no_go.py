from pathlib import Path

import proof_tracker

from self_dual_wreath_local_block_metric_normalization_no_go import (
    audit_pair_carrier_natural_marginal,
    local_block_normalization_scaling_record,
    run_local_block_metric_normalization_no_go,
    write_local_block_metric_normalization_no_go_report,
)


def test_pair_carrier_target_marginal_is_exactly_natural() -> None:
    control = audit_pair_carrier_natural_marginal(5, 2)
    assert control.exact_joint_probability_mass == "1"
    assert control.exact_target_marginal_probability_mass == "1"
    assert control.maximum_regular_dimension_identity_residual == 0
    assert control.maximum_source_character_cancellation_residual == 0
    assert control.exact_target_marginal_violation_count == 0
    assert control.exact_natural_target_marginal_verified is True


def test_every_local_pairing_schedule_has_exponential_threshold_normalization() -> None:
    schedules = (
        "all-singletons",
        "fixed-two-pairs",
        "logarithmic-pairs",
        "maximal-pairing",
    )
    records = [
        local_block_normalization_scaling_record(20, schedule=schedule)
        for schedule in schedules
    ]
    for record in records:
        assert record.singleton_block_count + 2 * record.pair_block_count == (
            record.information_threshold_copy_count
        )
        assert record.relevant_natural_label_count == (
            record.information_threshold_copy_count + record.pair_block_count
        )
        assert record.local_product_normalization_log2_lower_bound >= (
            record.information_threshold_copy_count / 2
        )
        assert record.local_product_normalization_log2_lower_bound >= (
            record.universal_threshold_log2_lower_bound
        )
        assert record.asymptotic_superpolynomial_no_go_applies is True
        assert record.inverse_polynomial_normalization_possible is False


def test_pairing_changes_constants_not_the_per_copy_normalization_barrier() -> None:
    singleton = local_block_normalization_scaling_record(
        64,
        schedule="all-singletons",
    )
    maximal = local_block_normalization_scaling_record(
        64,
        schedule="maximal-pairing",
    )
    assert maximal.local_product_normalization_log2_lower_bound < (
        singleton.local_product_normalization_log2_lower_bound
    )
    assert maximal.local_product_normalization_log2_lower_bound >= (
        maximal.information_threshold_copy_count / 2
    )
    assert maximal.envelope_failure_probability_upper_bound < 64**-3


def test_report_scopes_no_go_to_local_composition() -> None:
    report = run_local_block_metric_normalization_no_go()
    assert report.theorem.exact_pair_carrier_natural_marginal_proved is True
    assert (
        report.theorem.local_singleton_pair_product_normalization_no_go_proved
        is True
    )
    assert report.theorem.all_local_pairing_schedules_covered is True
    assert report.theorem.global_shared_label_metric_access_ruled_out is False
    assert report.theorem.full_threshold_metric_block_encoding_compiled is False
    assert report.claim_gate["speedup_claim_allowed"] is False
    assert report.headline_metrics["asymptotic_no_go_scaling_row_count"] == 20


def test_writer_emits_artifact_without_registry(tmp_path: Path) -> None:
    output = tmp_path / "local-block-no-go.json"
    payload = write_local_block_metric_normalization_no_go_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "local-threshold-lcu-composition-falsified-global-metric-access-open"
    )
    assert payload["headline_metrics"][
        "local_singleton_pair_product_normalization_no_go_count"
    ] == 1
    assert payload["headline_metrics"][
        "full_threshold_metric_block_encoding_compiler_count"
    ] == 0


def test_proof_tracker_closes_local_route_and_keeps_global_access_open(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output = tmp_path / "local-block-no-go.json"
    write_local_block_metric_normalization_no_go_report(
        output,
        write_registry=False,
    )
    monkeypatch.setattr(
        proof_tracker,
        "LOCAL_BLOCK_METRIC_NORMALIZATION_NO_GO_PATH",
        output,
    )
    local_lemmas = {
        lemma.id: lemma
        for lemma in proof_tracker._local_block_metric_normalization_no_go_lemmas(
            "CODE-COSET-COLLECTIVE"
        )
    }
    assert local_lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-PAIR-CARRIER-NATURAL-MARGINAL"
    ].status.startswith("proved-")
    assert local_lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-LOCAL-BLOCK-THRESHOLD-METRIC-NORMALIZATION-NO-GO"
    ].status.startswith("proved-")

    full_access = {
        lemma.id: lemma
        for lemma in proof_tracker._dimensionless_pgm_truncation_lemmas(
            "CODE-COSET-COLLECTIVE"
        )
    }[
        "LEMMA-CODE-COSET-COLLECTIVE-FULL-THRESHOLD-RANK-SCALED-METRIC-ACCESS"
    ]
    assert full_access.status == (
        "blocked-local-products-falsified-global-shared-label-access-open"
    )
