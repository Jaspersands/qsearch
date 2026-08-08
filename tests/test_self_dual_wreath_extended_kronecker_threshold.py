from self_dual_wreath_extended_kronecker_threshold import (
    audit_extended_kronecker_variance,
    extended_kronecker_scaling_record,
    fixed_target_variance_formula,
    run_extended_kronecker_threshold,
)
from self_dual_wreath_plancherel_kronecker_positivity import (
    reciprocal_nonidentity_class_sum,
)


def test_trivial_target_q3_formula_recovers_reciprocal_class_sum() -> None:
    for n in range(3, 9):
        assert fixed_target_variance_formula(n, 3, (n,)) == (
            reciprocal_nonidentity_class_sum(n)
        )


def test_exact_fixed_target_variance_controls() -> None:
    controls = [
        audit_extended_kronecker_variance(5, 3),
        audit_extended_kronecker_variance(4, 4),
    ]
    assert all(
        record.exact_fixed_target_variance_identity_verified
        for record in controls
    )
    assert all(
        record.fixed_target_zero_probability_bound_verified
        for record in controls
    )
    assert all(record.maximum_exact_mean_residual == "0" for record in controls)
    assert all(
        record.maximum_exact_variance_formula_residual == "0"
        for record in controls
    )


def test_more_factors_strengthen_the_pointwise_support_bound() -> None:
    for n in (10, 20, 30, 40, 50):
        records = [extended_kronecker_scaling_record(n, q) for q in (3, 4, 5)]
        assert records[2].worst_target_variance_upper_bound < records[1].worst_target_variance_upper_bound
        assert records[1].worst_target_variance_upper_bound < records[0].worst_target_variance_upper_bound
        assert all(
            record.fixed_target_positivity_probability_tends_to_one
            for record in records
        )
        assert all(record.multiplicity_concentration_proved for record in records)
        assert all(not record.simultaneous_all_target_covering_proved for record in records)


def test_report_keeps_covering_multiplicity_and_edge_gates_closed() -> None:
    report = run_extended_kronecker_threshold()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "three_independent_plancherel_factors_contain_fixed_target_aas"
    ]
    assert report.claim_gate[
        "independent_natural_hamming_three_support_transition_proved"
    ]
    assert not report.claim_gate[
        "simultaneous_all_irrep_covering_with_three_factors_proved"
    ]
    assert report.claim_gate[
        "fixed_target_normalized_multiplicity_concentration_proved"
    ]
    assert report.claim_gate[
        "fixed_hamming_pair_common_rank_concentration_proved"
    ]
    assert not report.claim_gate[
        "simultaneous_all_pair_rank_concentration_proved"
    ]
    assert not report.claim_gate["higher_order_incidence_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
