import math

from coset_hidden_involution_matching_charge_conditional_diameter import (
    build_conditional_diameter_report,
    conditional_diameter_scaling_record,
    explicit_delta_lower_bound,
    explicit_diameter_lower_bound,
    explicit_good_mass_lower_bound,
    write_conditional_diameter_report,
)
from coset_hidden_involution_matching_charge_natural_independence import (
    normalized_independence_commutator_squared_norm,
)


def test_explicit_inverse_polynomial_bounds_follow_from_exact_delta():
    for half_degree in (5, 6, 7, 11, 32, 128, 512):
        delta = normalized_independence_commutator_squared_norm(half_degree)
        assert delta >= explicit_delta_lower_bound(half_degree)
        assert delta / (8.0 - delta) >= explicit_good_mass_lower_bound(
            half_degree
        )
        assert math.sqrt(delta / 2.0) >= explicit_diameter_lower_bound(
            half_degree
        )


def test_scaling_records_certify_physical_conditional_diameter():
    for half_degree in (11, 12, 13, 17, 32, 64):
        row = conditional_diameter_scaling_record(half_degree)
        assert row.physical_h_even_transfer_exact
        assert row.inverse_polynomial_bounds_verified
        assert row.good_block_source_mass_lower_bound > 0
        assert row.conditional_D_spectral_diameter_lower_bound > 0
        assert row.scalar_distance_squared_threshold > 0


def test_event_escapes_fixed_defect_four_from_rank_thirteen():
    assert conditional_diameter_scaling_record(
        12
    ).beyond_defect_four_good_mass_lower_bound == 0
    for half_degree in (13, 17, 32, 64):
        assert conditional_diameter_scaling_record(
            half_degree
        ).beyond_defect_four_good_mass_lower_bound > 0


def test_report_distinguishes_diameter_from_minimum_gap():
    report = build_conditional_diameter_report()
    theorem = report.theorem
    assert theorem.exact_common_block_reduction_proved
    assert theorem.inverse_polynomial_source_event_mass_proved
    assert theorem.conditional_two_eigenvalue_separation_proved
    assert theorem.repeated_copy_dimension_on_good_event_proved
    assert theorem.beyond_defect_four_event_proved
    assert not theorem.full_joint_minimum_gap_proved
    assert not theorem.residual_multiplicity_bounded
    assert not theorem.coherent_D_diagonalization_compiled
    assert not theorem.source_CS_likelihood_correlation_proved
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_adversarial_audit_keeps_algorithmic_gates_closed():
    report = build_conditional_diameter_report()
    assert report.claim_gate[
        "natural_conditional_two_eigenvalue_separation_proved"
    ]
    assert report.claim_gate["event_reaches_growing_defect_source_mass"]
    assert not report.claim_gate["full_joint_minimum_gap_proved"]
    assert not report.claim_gate["source_CS_likelihood_correlation_proved"]
    assert not report.claim_gate["hidden_involution_detector_constructed"]
    assert all(row["resolved"] for row in report.adversarial_audit)


def test_live_conditional_diameter_report_is_json_serializable(tmp_path):
    output = tmp_path / "conditional-diameter.json"
    payload = write_conditional_diameter_report(output)
    assert output.exists()
    assert payload["status"] == (
        "matching-charge-natural-conditional-diameter-proved"
    )
    assert payload["theorem"]["theorem_verified"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
