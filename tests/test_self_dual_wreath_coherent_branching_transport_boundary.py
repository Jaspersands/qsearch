import math

from self_dual_wreath_coherent_branching_transport_boundary import (
    audit_tensor_branching_identity,
    coherent_independent_transport_countermodel,
    ordered_tuple_permutation_character,
    run_coherent_branching_transport_boundary,
)


def test_ordered_tuple_character_counts_fixed_injective_tuples() -> None:
    assert ordered_tuple_permutation_character((3, 1, 1, 1), 1) == 3
    assert ordered_tuple_permutation_character((3, 1, 1, 1), 2) == 6
    assert ordered_tuple_permutation_character((2, 2, 1, 1), 3) == 0


def test_tensor_product_chain_equals_remove_regrow_branching() -> None:
    row = audit_tensor_branching_identity(8, 2)
    assert row.permutation_module_dimension == 56
    assert row.maximum_transition_formula_residual < 1e-11
    assert row.maximum_tensor_multiplicity_integrality_residual == 0.0
    assert row.maximum_tensor_multiplicity_negativity == 0
    assert row.exact_tensor_branching_identity_verified


def test_shared_noise_can_hide_maximal_independent_noise_energy() -> None:
    row = coherent_independent_transport_countermodel(16)
    assert row.coherent_shared_shift_dirichlet_energy == 0.0
    assert math.isclose(row.independent_shift_dirichlet_energy, 15.0, abs_tol=1e-12)
    assert math.isclose(row.identity_coupling_mutual_information_bits, 4.0)
    assert row.independent_smoothed_likelihood_residual_to_one == 0.0
    assert row.exact_coherent_independent_separation_verified


def test_report_requires_new_transport_theorem() -> None:
    report = run_coherent_branching_transport_boundary()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["down_up_tensor_product_identity_proved"] is True
    assert report.claim_gate["coherent_branching_implies_independent_smoothing"] is False
    assert report.claim_gate["natural_racah_transport_inequality_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
