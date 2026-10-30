from fractions import Fraction as F

import numpy as np
import pytest

import spectral_mixture as s


@pytest.fixture(scope="module")
def report():
    return s.audit()


def test_actual_representation_and_all_rees_evaluations(report):
    assert report["representation_homomorphism_error"] < 1e-12
    assert report["actual_cover_elements_checked"] == 81
    assert report["matched_packet_maximum_overlap_error"] < 1e-12
    assert report["mixed_conjugation_hidden_order"] == 9
    assert report["old_scalar_support_hidden_order"] == 3


def test_marginals_do_not_replace_the_matched_spectral_packet(report):
    assert report["independent_marginals_wrong_hidden_overlap_error"] > .9


def test_degenerate_spectrum_invalidates_the_reduction(report):
    assert report["degenerate_conjugation_distance"] < 1e-12
    assert report["degenerate_packet_overlap"] < 1e-12


def test_aggregate_gap_does_not_require_individual_eigenstate_gaps(report):
    assert report["purification_gap_trials"] == 64
    assert report["maximum_gap_inequality_excess"] < 1e-12


def test_individual_eigenstate_gap_can_be_tiny_while_mixed_gap_is_constant(report):
    row = report["individual_eigenstate_gap_countercontrol"]
    assert row["finite_order_three_error"] < 1e-12
    assert 0 < row["one_eigenstate_overlap_gap"] < 1e-6
    assert row["mixed_conjugation_distance"] > .08


def test_principal_eigenstate_is_not_the_full_mixed_target(report):
    assert report["principal_only_fixed_vector_error"] == 0
    assert report["principal_only_false_symmetry_distance"] > .08


def test_normalizing_capped_packet_success_biases_the_eigenvalue_law():
    weights = (F(2, 3), F(1, 3))
    # One attempt per extra member in a six-copy packet.
    accepted = tuple(weight**6 for weight in weights)
    mass = sum(accepted)
    conditional = tuple(weight/mass for weight in accepted)
    assert 1 - mass == F(664, 729)
    assert conditional[0] == F(64, 65)
    assert abs(conditional[0] - weights[0]) > F(3, 10)


def test_controlled_dme_bound_including_reference(report):
    rows = report["controlled_dme_with_reference"]
    for row in rows:
        assert row["distance"] < row["bound"]
    assert all(a["distance"] > b["distance"] for a, b in zip(rows, rows[1:]))


def budget(**changes):
    values = dict(receiver_leaves=7, design_size=6, cover_order_bits=31,
                  minimum_weight=F(1, 10), spectral_gap=F(1, 100),
                  orbit_trace_gap=F(1, 4), error=F(1, 20))
    return s.packet_budget(**(values | changes))


def test_full_budget_pays_every_spectral_attempt_and_program_copy():
    plan = budget()
    packets = plan["spectral_packets"]
    attempts = plan["matching_attempts_per_required_copy_cap"]
    measurements = plan["spectral_measurement_cap"]
    assert measurements == packets * (1 + 5 * attempts)
    assert int(plan["total_raw_copy_cap"]) == measurements * (1 + int(plan["program_copies_per_spectral_measurement_cap"]))
    assert F(plan["overlap_gap_lower_bound"]) == F(1, 32)
    assert measurements * F(plan["per_estimate_bad_value_budget"]) == F(1, 160)
    implementation = measurements * (F(plan["per_measurement_dme_channel_budget"]) + F(plan["per_measurement_public_gate_budget"]))
    assert implementation == F(plan["spectral_implementation_error_budget"]) == F(1, 160)
    assert sum(F(plan[key]) for key in ("source_amplification_error_budget", "matching_abort_budget",
                                      "spectral_bad_value_budget", "spectral_implementation_error_budget",
                                      "address_and_receiver_budget")) == F(1, 20)


def test_bad_spectral_values_have_a_paid_grid_not_free_phase_oracle():
    plan = budget()
    assert int(plan["phase_grid"]) >= 128 / (F(1, 100) * F(plan["per_estimate_bad_value_budget"]))
    assert plan["unknown_state_inverse_calls"] == plan["conjugate_copy_calls"] == 0
    assert not plan["all_promises_certified"]


@pytest.mark.parametrize("change", [{"minimum_weight": F(1, 100)}, {"spectral_gap": F(1, 1000)},
                                   {"orbit_trace_gap": F(1, 8)}, {"error": F(1, 100)}])
def test_weakening_promises_increases_charged_raw_cost(change):
    assert int(budget(**change)["total_raw_copy_cap"]) > int(budget()["total_raw_copy_cap"])


@pytest.mark.parametrize("change", [{"minimum_weight": 0}, {"spectral_gap": 0}, {"orbit_trace_gap": 0},
                                   {"error": .1}, {"design_size": 0}, {"receiver_leaves": True}])
def test_unpaid_or_malformed_contracts_rejected(change):
    with pytest.raises(ValueError):
        budget(**change)


def test_scope_does_not_promote_the_conditional_reduction(report):
    scope = report["scope"]
    assert scope["conditional_reduction_for_nondegenerate_positive_spectrum"]
    assert not any(value for key, value in scope.items() if key != "conditional_reduction_for_nondegenerate_positive_spectrum")
