from coset_natural_multicopy_pgm_benchmark import _source_data
from self_dual_wreath_carrier_conditioned_pgm_boundary import (
    audit_carrier_conditioned_source,
    audit_natural_carrier_conditioned_pgm,
    run_carrier_conditioned_pgm_boundary,
    write_carrier_conditioned_pgm_boundary_report,
)


def test_carrier_branch_probabilities_are_hidden_independent_and_pgm_normalizes() -> None:
    partitions, _, _ = _source_data(4, 2)
    nontrivial = next(
        index for index, partition in enumerate(partitions) if partition == (3, 1)
    )
    control = audit_carrier_conditioned_source(
        4,
        2,
        (nontrivial, nontrivial),
        nontrivial,
        natural_source_probability=1.0,
    )
    assert control.active_pair_carrier_count > 1
    assert control.maximum_hidden_branch_probability_residual <= 1e-12
    assert control.conditioned_channel_normalization_residual <= 1e-12
    assert control.maximum_branch_pgm_completeness_residual <= 1e-10
    assert control.carrier_dephased_holevo_information_bits <= (
        control.full_holevo_information_bits + 1e-10
    )
    assert control.exact_branch_pgm_factorization_verified is True


def test_natural_s5_carrier_conditioning_retains_signal_and_improves_average_conditioning() -> None:
    aggregate, controls = audit_natural_carrier_conditioned_pgm()
    assert len(controls) == 196
    assert abs(aggregate.total_natural_source_probability - 1.0) <= 1e-10
    assert 0.75 < aggregate.holevo_retention_fraction < 0.78
    assert 0.50 < aggregate.pgm_information_retention_fraction < 0.53
    assert 0.30 < (
        aggregate.retained_collective_information_gain_fraction_over_product_pgm
    ) < 0.33
    assert aggregate.carrier_conditioned_pgm_mutual_information_bits > (
        aggregate.product_one_copy_pgm_mutual_information_bits
    )
    assert aggregate.carrier_conditioned_pgm_bayes_success_probability > (
        aggregate.product_one_copy_pgm_bayes_success_probability
    )
    assert aggregate.average_condition_number_reduction_factor > 2.4
    assert aggregate.natural_mass_with_at_least_80_percent_pgm_information_retention < 0.14
    assert aggregate.all_exact_controls_verified is True


def test_report_keeps_compressed_multiplicity_whitening_and_decoder_open() -> None:
    report = run_carrier_conditioned_pgm_boundary()
    assert report.theorem.hidden_independent_branch_law_proved is True
    assert report.theorem.exact_branch_pgm_factorization_proved is True
    assert report.theorem.multiplicity_whitening_compressed is True
    assert report.theorem.multiplicity_whitening_eliminated is False
    assert report.theorem.finite_collective_gain_retained is True
    assert report.claim_gate[
        "carrier_conditioning_improves_average_support_conditioning"
    ] is True
    assert report.claim_gate["polynomial_carrier_branch_pgm_compiled"] is False
    assert report.claim_gate["hidden_involution_decoder_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_boundary_artifact_without_registry(tmp_path) -> None:
    output = tmp_path / "carrier-conditioned-pgm.json"
    payload = write_carrier_conditioned_pgm_boundary_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "carrier-conditioned-pgm-retains-gain-row-whitening-open"
    )
    assert payload["headline_metrics"][
        "multiplicity_whitening_elimination_theorem_count"
    ] == 0
