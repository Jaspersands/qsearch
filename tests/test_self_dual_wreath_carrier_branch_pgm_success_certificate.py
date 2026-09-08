from coset_natural_multicopy_pgm_benchmark import _source_data
from self_dual_wreath_carrier_branch_pgm_success_certificate import (
    adaptive_pinching_success_lower_bound,
    audit_carrier_branch_pgm_source,
    audit_natural_pair_carrier_angle_dilution,
    audit_natural_carrier_branch_pgm_certificate,
    disjoint_pair_certificate_denominator_upper,
    disjoint_pair_threshold_success_lower_bound,
    equal_overlap_certificate_denominator,
    jensen_flagged_success_lower_bound,
    natural_one_copy_rank_normalized_overlap,
    run_carrier_branch_pgm_success_certificate,
    symmetric_group_threshold_retention_lower_bound,
    write_carrier_branch_pgm_success_certificate_report,
)


def test_every_branch_holder_certificate_lower_bounds_exact_pgm_success() -> None:
    partitions, _, _ = _source_data(4, 2)
    standard = partitions.index((3, 1))
    control = audit_carrier_branch_pgm_source(
        4,
        2,
        (standard, standard),
        standard,
        natural_source_probability=1.0,
    )
    assert len(control.branches) > 1
    assert control.flagged_holder_success_lower_bound <= (
        control.exact_flagged_pgm_native_success + 1e-10
    )
    for branch in control.branches:
        assert branch.carrier_angle_dilution >= 1 - 1e-10
        assert branch.compressed_average_frame_purity > 0
        assert branch.frame_denominator_identity_residual <= 1e-8
        assert branch.self_purity_inflation >= 1 - 1e-10
        assert branch.distinct_overlap_collision_term >= -1e-10
        assert branch.holder_success_lower_bound <= (
            branch.exact_branch_pgm_native_success + 1e-10
        )
        assert branch.certificate_verified is True
    assert control.exact_certificate_verified is True


def test_natural_s5_certificate_beats_product_and_young_bayes_baselines() -> None:
    aggregate, controls = audit_natural_carrier_branch_pgm_certificate()
    assert len(controls) == 196
    assert abs(aggregate.total_natural_source_probability - 1.0) <= 1e-10
    assert 0.25 < aggregate.natural_holder_success_lower_bound < 0.26
    assert 0.30 < aggregate.natural_exact_flagged_pgm_native_success < 0.31
    assert aggregate.certified_advantage_over_product_pgm > 0.07
    assert aggregate.certified_advantage_over_separate_young > 0.05
    assert aggregate.certificate_to_exact_success_ratio > 0.82
    assert 1.1 < aggregate.branch_probability_weighted_self_purity_inflation < 1.2
    assert 3.2 < aggregate.branch_probability_weighted_collision_term < 3.4
    assert 4.4 < aggregate.branch_probability_weighted_certificate_denominator < 4.5
    assert aggregate.unpinched_equal_overlap_certificate_denominator == 2.75
    assert 1.6 < aggregate.effective_carrier_frame_inflation < 1.7
    assert 0.22 < aggregate.natural_jensen_success_lower_bound < 0.23
    assert aggregate.natural_jensen_success_lower_bound <= (
        aggregate.natural_holder_success_lower_bound
    )
    assert aggregate.jensen_certified_advantage_over_product_pgm > 0.04
    assert aggregate.jensen_certified_advantage_over_separate_young > 0.03
    assert aggregate.all_certificates_verified is True


def test_jensen_and_adaptive_pinching_bounds_are_operational() -> None:
    probabilities = (0.2, 0.3, 0.5)
    denominators = (1.0, 2.0, 5.0)
    direct = sum(
        probability / denominator
        for probability, denominator in zip(probabilities, denominators, strict=True)
    )
    jensen = jensen_flagged_success_lower_bound(probabilities, denominators)
    assert abs(jensen - 1.0 / 3.3) <= 1e-12
    assert jensen <= direct
    assert adaptive_pinching_success_lower_bound(0.75, (3, 5)) == 0.05
    assert equal_overlap_certificate_denominator(15, 3) == 2.75
    assert disjoint_pair_certificate_denominator_upper(15, 3, 1) == 32.0
    assert disjoint_pair_threshold_success_lower_bound(1) == 0.05
    assert disjoint_pair_threshold_success_lower_bound(2) == 1.0 / 272.0
    assert natural_one_copy_rank_normalized_overlap(5, 2, 0, 0) == 1.0
    assert abs(natural_one_copy_rank_normalized_overlap(5, 2, 0, 1) - 0.5) <= 1e-10
    assert 0 < symmetric_group_threshold_retention_lower_bound(100, 2, 3) < 0.01


def test_natural_pair_angle_mean_is_bounded_but_s6_worst_sector_is_large() -> None:
    control = audit_natural_pair_carrier_angle_dilution(6, 3)
    assert abs(control.total_natural_outcome_probability - 1.0) <= 1e-9
    assert 1.8 < control.natural_outcome_weighted_angle_dilution < 1.9
    assert control.all_n_natural_outcome_first_moment_upper <= 4.0
    assert control.maximum_angle_dilution > 19.9
    assert control.maximum_angle_exceeds_n_minus_one is True
    assert control.natural_first_moment_bound_verified is True


def test_report_proves_disjoint_pair_anti_locking_and_keeps_compiler_open() -> None:
    report = run_carrier_branch_pgm_success_certificate()
    assert report.theorem.branch_success_certificate_proved is True
    assert report.theorem.flagged_pgm_success_certificate_proved is True
    assert report.theorem.finite_collective_success_certified is True
    assert report.theorem.aggregate_jensen_certificate_proved is True
    assert report.theorem.all_n_operational_anti_locking_proved is True
    assert report.theorem.all_n_natural_outcome_angle_first_moment_proved is True
    assert report.theorem.all_n_natural_average_self_purity_bound_proved is True
    assert report.theorem.all_n_uniform_branch_self_purity_bound_proved is False
    assert report.theorem.collision_biased_angle_moment_bounded is True
    assert report.theorem.disjoint_pair_all_n_collision_bound_proved is True
    assert report.theorem.fixed_depth_constant_success_proved is True
    assert report.theorem.logarithmic_depth_inverse_polynomial_success_proved is True
    assert report.theorem.polynomial_success_retention_proved is True
    assert report.theorem.all_n_collision_control_proved is False
    assert report.claim_gate["holevo_retention_only_argument_required"] is False
    assert report.claim_gate["all_n_self_purity_inflation_control_proved"] is True
    assert report.claim_gate["all_n_distinct_collision_control_proved"] is False
    assert report.claim_gate["all_n_operational_pinching_anti_locking_proved"] is True
    assert report.claim_gate[
        "all_n_natural_outcome_angle_first_moment_proved"
    ] is True
    assert report.claim_gate[
        "all_n_natural_average_self_purity_inflation_control_proved"
    ] is True
    assert report.claim_gate["all_n_uniform_branch_self_purity_control_proved"] is False
    assert report.claim_gate["collision_biased_angle_moment_bounded"] is False
    assert report.claim_gate[
        "disjoint_pair_collision_biased_angle_moment_bounded"
    ] is True
    assert report.claim_gate["subexponential_threshold_success_retention_proved"] is True
    assert report.claim_gate["polynomial_threshold_success_retention_proved"] is False
    assert report.claim_gate[
        "disjoint_pair_polynomial_threshold_success_retention_proved"
    ] is True
    assert report.claim_gate["overlapping_adaptive_collision_control_proved"] is False
    assert report.claim_gate[
        "constant_success_at_information_threshold_after_carrier_pinching"
    ] is False
    assert report.claim_gate[
        "constant_success_at_threshold_after_disjoint_pair_pinching"
    ] is True
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_certificate_artifact_without_registry(tmp_path) -> None:
    output = tmp_path / "carrier-branch-pgm-certificate.json"
    payload = write_carrier_branch_pgm_success_certificate_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "disjoint-pair-carrier-all-n-accessible-success-compiler-open"
    )
    assert payload["headline_metrics"]["all_n_collision_control_theorem_count"] == 0
    assert payload["headline_metrics"]["disjoint_pair_all_n_collision_theorem_count"] == 1
