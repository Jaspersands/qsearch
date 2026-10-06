from fractions import Fraction

import pytest

from dcp_relation_walk_stationarity import (
    _actual_swap_control, _laplacian_controls, _source_controls,
    signed_relation_dictionary_certificate, signed_relation_swap,
)
from dcp_physical_phase_noise import read


def test_known_signed_relation_swap_is_a_physical_involution_and_fixes_all_secret_states():
    row = _actual_swap_control()
    assert row["touched_physical_words"] == 16
    assert max(row["all_fixed_secret_state_residuals"]) < 1e-10
    assert not row["implemented_swap_is_a_new_hidden_secret_decoder"]


def test_actual_nonzero_complete_fiber_laplacians_have_no_secret_dependent_dynamics():
    rows = _laplacian_controls()
    assert len(rows) == 3
    for row in rows:
        assert row["explicit_fiber_edges"]
        assert row["maximum_actual_Laplacian_state_residual"] < 1e-9
        assert row["maximum_positive_eigenvalue_phase_estimation_mass"] < 1e-9
        assert row["unknown_phase_state_is_already_stationary_in_every_fiber"]
        assert not row["laplacian_is_zero_operator"]
        assert row["non_Laplacian_adjacency_source_energy_variance"] > 0
        assert not row["all_fiber_preserving_Hamiltonians_leave_state_unchanged"]


def test_complete_source_control_matches_one_unit_coefficient_uniformity():
    rows = _source_controls()
    assert [r["all_canonical_signed_relations"] for r in rows] == [4, 16]
    assert all(r["exact_one_fixed_relation_source_hits"] == 64 for r in rows)


def test_label_adaptive_long_move_dictionary_charges_physical_applicability():
    row = signed_relation_dictionary_certificate(16, 65, 1056, 211, 1056**4)
    assert row["label_adaptive_choice_of_the_entire_dictionary_allowed"]
    assert read(row["on_no_short_relation_event_uniform_word_dictionary_applicability_upper_bound"]) == Fraction(1056**4, 1 << 211)
    assert row["conservative_short_relation_failure_dyadic_exponent"] > 50
    assert not row["implicit_word_adaptive_neighbor_finders_ruled_out"]
    assert read(row["unconditional_native_applicability_probability_upper_bound"]) == min(
        1, read(row["any_short_relation_native_probability_union_upper_bound"])+Fraction(1056**4,1 << 211))


def test_vacuous_and_empty_thresholds_do_not_create_false_source_claims():
    empty = signed_relation_dictionary_certificate(1, 2, 4, 0, 0)
    assert read(empty["any_short_relation_native_probability_union_upper_bound"]) == 0
    assert read(empty["on_no_short_relation_event_uniform_word_dictionary_applicability_upper_bound"]) == 0
    full = signed_relation_dictionary_certificate(1, 2, 4, 4, 100)
    assert read(full["any_short_relation_native_probability_union_upper_bound"]) == 1
    assert read(full["on_no_short_relation_event_uniform_word_dictionary_applicability_upper_bound"]) == 1


def test_invalid_relation_or_modulus_fails_before_permutation():
    for delta in ((1, 1), (0, 0), (True, -1), (2, -2), (1,)):
        with pytest.raises(ValueError):
            signed_relation_swap(((1, 1),), 4, delta, 0)
    with pytest.raises(ValueError):
        signed_relation_swap(((1, 1),), 4, (1, -1), 4)
    with pytest.raises(ValueError):
        signed_relation_dictionary_certificate(1, 1, 4, 1, 2)
    with pytest.raises(ValueError):
        signed_relation_dictionary_certificate(1, 2, 4, 5, 2)


def test_postselection_is_not_free_even_for_a_perfect_relation():
    A, q, delta = ((1, 1, 3, 3),), 4, (1, 1, 1, 1)
    permutation = [signed_relation_swap(A, q, delta, x) for x in range(16)]
    assert sum(x != y for x, y in enumerate(permutation)) == 2
    assert Fraction(2, 16) == Fraction(1, 8)
