from fractions import Fraction

from self_dual_wreath_plancherel_carrier_contextuality import (
    audit_dense_plancherel_contextuality,
    character_squared_class_law,
    exact_carrier_contextuality_control,
    run_plancherel_carrier_contextuality,
    sample_weighted_commuting_probability,
    write_plancherel_carrier_contextuality_report,
)


def test_character_squared_law_normalizes_exactly() -> None:
    for n in range(2, 9):
        law = character_squared_class_law(n)
        assert sum(law.values(), start=Fraction()) == 1
        assert all(weight > 0 for weight in law.values())


def test_exact_contextuality_separates_abelian_and_nonabelian_controls() -> None:
    abelian = exact_carrier_contextuality_control(2)
    assert abelian.exact_weighted_commuting_probability == "1"
    assert abelian.exact_annealed_aggregate_commutator == "0"
    assert abelian.nonabelian_contextuality_positive is False

    s3 = exact_carrier_contextuality_control(3)
    assert s3.exact_weighted_commuting_probability == "47/54"
    assert s3.exact_annealed_aggregate_commutator == "7/27"
    assert s3.nonabelian_contextuality_positive is True
    assert s3.exact_character_moment_verified is True


def test_dense_plancherel_average_matches_character_formula() -> None:
    control = audit_dense_plancherel_contextuality(3)
    assert control.dense_plancherel_formula_verified is True
    assert control.source_tuple_count == 27
    assert control.carrier_label_pair_count == 243
    assert control.maximum_projector_idempotence_residual < 1e-12
    assert control.dense_to_formula_residual < 1e-12


def test_exact_contextuality_grows_across_selected_controls() -> None:
    rows = [exact_carrier_contextuality_control(n) for n in (3, 5, 8)]
    assert all(row.exact_character_moment_verified for row in rows)
    assert rows[0].annealed_aggregate_commutator < rows[1].annealed_aggregate_commutator
    assert rows[1].annealed_aggregate_commutator < rows[2].annealed_aggregate_commutator
    assert rows[-1].annealed_aggregate_commutator > 1.5


def test_sampled_query_uses_finite_confidence_not_asymptotic_claim() -> None:
    record = sample_weighted_commuting_probability(12, 4_000, seed=9012)
    assert record.finite_sample_only is True
    assert record.exact_distribution_normalization_residual < 1e-12
    assert record.commuting_probability_confidence_lower <= (
        record.estimated_weighted_commuting_probability
    )
    assert record.commuting_probability_confidence_upper >= (
        record.estimated_weighted_commuting_probability
    )
    assert record.aggregate_commutator_confidence_lower > 1.65


def test_report_keeps_asymptotic_and_compiler_claims_blocked() -> None:
    report = run_plancherel_carrier_contextuality(sample_count=2_000)
    assert report.claim_gate[
        "exact_natural_annealed_contextuality_formula_proved"
    ] is True
    assert report.claim_gate[
        "pairwise_carrier_spectra_determine_joint_sharp_labels"
    ] is False
    assert report.claim_gate[
        "weighted_commuting_probability_asymptotically_vanishes_proved"
    ] is False
    assert report.claim_gate[
        "collision_free_positive_constant_contextuality_proved"
    ] is False
    assert report.claim_gate["structured_multistar_racah_resolver_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_proof_gated_artifact(tmp_path) -> None:
    payload = write_plancherel_carrier_contextuality_report(
        path=tmp_path / "carrier-contextuality.json",
        write_registry=False,
        sample_count=1_000,
    )
    assert payload["headline_metrics"][
        "natural_carrier_contextuality_character_reduction_theorem_count"
    ] == 1
    assert payload["headline_metrics"][
        "asymptotic_constant_contextuality_theorem_count"
    ] == 0
    assert len(payload["falsifiers_triggered"]) >= 4
