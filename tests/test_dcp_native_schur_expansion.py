from fractions import Fraction
import itertools
import random

import pytest

from dcp_native_schur_expansion import (
    _code_components, identity_pencil_middle_source_mass, native_adaptive_pool_bound, native_low_variation_source_bound,
    selected_schur_subcode_certificate, signature_capacity, universal_signature_gate,
)
from dcp_physical_phase_noise import read
from dcp_pivot_span_obstructions import _columns_value, _nullspace, _row_basis


def _systematic(n, tail):
    return tuple((1 << l) | sum(((column >> l) & 1) << (n + j) for j, column in enumerate(tail)) for l in range(n))


def _physical_kernel_basis(n, tail):
    return tuple((1 << (n + j)) | column for j, column in enumerate(tail))


def test_product_stabilizer_components_are_actual_disjoint_code_summands():
    R = (0b0011, 0b1100)
    assert set(_code_components(R, 4)) == {0b0011, 0b1100}
    assert _code_components((0b101, 0b110), 3) == (0b111,)
    assert _code_components((0b101, 0b110), 5) == (0b111,)


def test_positive_rank_one_family_is_preserved_at_growing_dimension():
    for n in (2, 3, 4, 8, 16):
        width = 2 * n + 1
        R = tuple((1 << j) | (1 << (n + j)) | (1 << (2 * n)) for j in range(n))
        W = tuple((1 << j) | (1 << (n + j)) for j in range(n))
        row = selected_schur_subcode_certificate(R, width, W)
        assert row["extension_rank"] == 1
        assert row["product_stabilizer_component_count"] == n + 1
        assert row["signature_gate_at_actual_extension_rank"]["distinct_nonzero_binary_column_signatures"] == n + 1
        assert not row["signature_gate_at_actual_extension_rank"]["every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded"]
        assert not row["nonsingular_pencil_inverse_or_decoder_implemented"]


def test_zero_binary_columns_are_punctured_and_do_not_create_false_all_span_no_go():
    n, width = 3, 10
    R = tuple(sum(((column >> l) & 1) << (column - 1) for column in range(1, 8)) for l in range(n))
    W = (1 << 7, 1 << 8, 1 << 9)
    row = selected_schur_subcode_certificate(R, width, W)
    assert row["extension_rank"] == 0
    gate = row["signature_gate_at_actual_extension_rank"]
    assert gate["zero_binary_columns"] == 3
    assert gate["active_projection_dimension_lower_bound"] == 0
    assert not gate["every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded"]


def test_unit_membership_changes_the_correct_augmentation_floor():
    # Every row has even weight, so the all-one vector genuinely belongs to C.
    R = (0b0011, 0b1100)
    W = (0b0011, 0b1100)
    row = selected_schur_subcode_certificate(R, 4, W)
    assert row["extension_rank"] == 0
    gate = row["signature_gate_at_actual_extension_rank"]
    assert gate["all_one_physical_vector_in_kernel"]
    assert gate["unit_augmented_subcode_dimension_lower_bound"] == 2
    assert not gate["every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded"]


def test_every_small_systematic_kernel_subspace_survives_gate_at_its_actual_rank():
    spans = {_row_basis((u, v), 3) for u in range(1, 8) for v in range(u + 1, 8)}
    assert len(spans) == 7
    checked = 0
    for tail in itertools.product(range(4), repeat=3):
        R = _systematic(2, tail)
        K = _physical_kernel_basis(2, tail)
        for coordinates in spans:
            W = tuple(_columns_value(K, w) for w in coordinates)
            row = selected_schur_subcode_certificate(R, 5, W)
            assert row["kneser_dimension_slack"] >= 0
            for r in range(3):
                gate = universal_signature_gate(R, 5, 2, r)
                if gate["every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded"]:
                    assert row["extension_rank"] > r
            checked += 1
    assert checked == 448


def test_three_dimensional_binary_controls_challenge_every_support_and_parity_guard():
    for tail in itertools.product(range(8), repeat=3):
        R = _systematic(3, tail)
        W = _physical_kernel_basis(3, tail)
        row = selected_schur_subcode_certificate(R, 6, W)
        for r in range(4):
            if universal_signature_gate(R, 6, 3, r)["every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded"]:
                assert row["extension_rank"] > r


def test_four_dimensional_adversarial_codes_include_all_even_row_and_support_degeneracies():
    rng = random.Random(20261005)
    hyperplanes = [_nullspace((h,), 5) for h in range(1, 32)]
    checks = 0
    for force_even_parity in (False, True):
        for _ in range(16):
            tail = [rng.randrange(16) for _ in range(5)]
            if force_even_parity:
                tail[-1] = 15
                for column in tail[:-1]:
                    tail[-1] ^= column
            R, K = _systematic(4, tail), _physical_kernel_basis(4, tail)
            if force_even_parity:
                assert all(row.bit_count() % 2 == 0 for row in R)
            for plane in hyperplanes:
                W = tuple(_columns_value(K, coordinate) for coordinate in plane)
                row = selected_schur_subcode_certificate(R, 9, W)
                for r in range(4):
                    if universal_signature_gate(R, 9, 4, r)["every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded"]:
                        assert row["extension_rank"] > r
                checks += 1
    assert checks == 992


def test_distinct_native_signatures_exclude_rank_one_without_any_pivot_enumeration():
    tail = (3, 5, 6, 7, 9, 10, 12)
    R = _systematic(4, tail)
    gate = universal_signature_gate(R, 11, 4, 1)
    assert gate["zero_binary_columns"] == 0
    assert not gate["all_one_physical_vector_in_kernel"]
    assert gate["distinct_nonzero_binary_column_signatures"] == 11
    assert gate["nonzero_signature_capacity_upper_bound_decimal"] == "6"
    assert gate["every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded"]
    assert not gate["higher_label_adaptive_subspace_selection_evades_this_gate"]


def test_signature_capacity_accounts_for_component_rank_concentration():
    assert signature_capacity(8, 1, 9) == (8, 10)
    assert signature_capacity(8, 2, 9) == (7, 21)
    assert signature_capacity(8, 0, 9) == (9, 0)
    assert signature_capacity(3, 1, 3) == (2, 7)


def test_middle_source_is_not_invented_as_an_exponential_failure():
    for n in (2, 3):
        good = 0
        for M in itertools.product(range(1 << n), repeat=n):
            good += len(_row_basis(M, n)) == n and len(_row_basis((row ^ (1 << l) for l, row in enumerate(M)), n)) == n
        row = identity_pencil_middle_source_mass(n)
        assert read(row["uniform_constant_matrix_all_background_invertibility_probability"]) == Fraction(good, 1 << (n * n))
        assert not row["middle_label_acceptance_is_exponentially_small"]
    for n in (4, 8, 16, 32):
        assert read(identity_pencil_middle_source_mass(n)["uniform_constant_matrix_all_background_invertibility_probability"]) >= Fraction(9, 112)


def test_native_probability_ledger_charges_zeros_parity_and_actual_pair_collisions():
    n, k = 32, 4 * 32 * 32 + 16
    row = native_low_variation_source_bound(n, k, 6)
    assert read(row["expected_equal_signature_pair_count"]) == Fraction(k * (k - 1) // 2 + n * k, 1 << n)
    assert row["distinct_signature_deficit_if_capacity_below_packet_width"] == 23
    assert read(row["signature_cover_event_upper_bound"]) == 1
    bound = read(row["exists_any_n_dimensional_kernel_subcode_with_extension_rank_at_most_r_probability_upper_bound"])
    assert 0 < bound < Fraction(1, 10000)
    zero = native_low_variation_source_bound(n, k, 0)
    assert read(zero["signature_event_upper_bound"]) == 0
    assert read(zero["exists_any_n_dimensional_kernel_subcode_with_extension_rank_at_most_r_probability_upper_bound"]) == Fraction(k + 1, 1 << n)


def test_coverage_bound_is_rounded_up_not_down_and_small_n_can_be_vacuous():
    row = native_low_variation_source_bound(32, 4 * 32 * 32 + 16, 1)
    assert row["signature_cover_dyadic_exponent_before_conservative_rounding"] > 32
    assert read(row["signature_cover_event_upper_bound"]) == Fraction(1, 1 << 32)
    tiny = native_low_variation_source_bound(2, 32, 1)
    assert read(tiny["exists_any_n_dimensional_kernel_subcode_with_extension_rank_at_most_r_probability_upper_bound"]) == 1


def test_higher_public_label_selection_cannot_evade_an_all_subcode_binary_obstruction():
    row = native_low_variation_source_bound(64, 4 * 64 * 64 + 16, 7)
    assert row["subcode_search_may_use_all_public_higher_labels"]
    assert not row["all_code_subspaces_enumerated"]
    assert not row["general_nonsingular_pencils_or_full_quantum_algorithms_excluded"]
    assert read(row["exists_any_n_dimensional_kernel_subcode_with_extension_rank_at_most_r_probability_upper_bound"]) < Fraction(1, 10 ** 12)


def test_subspace_envelopes_strengthen_logarithmic_to_linear_variation_rank_barrier():
    for n in range(16, 129):
        k, r = 4 * n * n + 16, n // 2 - 1
        row = native_low_variation_source_bound(n, k, r)
        envelope = row["parity_free_subspace_envelope"]
        assert envelope["envelope_probability_dyadic_exponent_before_rounding"] >= n
        assert not envelope["all_one_kernel_vector_exception_needed"]
        bound = read(row["exists_any_n_dimensional_kernel_subcode_with_extension_rank_at_most_r_probability_upper_bound"])
        assert bound <= Fraction(k + 1, 1 << n)
        assert not row["general_nonsingular_pencils_or_full_quantum_algorithms_excluded"]


def test_three_quarter_tail_bound_is_an_exact_integer_inequality():
    assert Fraction(3, 4) ** 5 < Fraction(1, 4)
    row = native_low_variation_source_bound(32, 4112, 15)
    envelope = row["parity_free_subspace_envelope"]
    assert envelope["tail_coverage_decay_binary_exponent_lower_bound"] == 2 * (4112 // 5)
    assert int(envelope["parity_free_signature_capacity_decimal"]) * 4 <= 3 * (1 << 32)


def test_adaptive_pool_selection_charges_all_menus_without_multiplying_global_zero_exception():
    n, pool, r = 64, 64 ** 4, 16
    k = 4 * n * n + 16
    row = native_adaptive_pool_bound(n, k, r, pool)
    assert row["ordered_packet_menu_count_binary_exponent_upper_bound"] == (n + k) * 24
    assert row["envelope_mass_exponent_after_charging_all_ordered_packet_menus"] > n
    assert row["arbitrary_public_label_adaptive_grouping_permitted"]
    assert row["zero_label_exception_is_charged_once_on_entire_pool_not_once_per_menu"]
    assert read(row["existence_probability_upper_bound_including_global_zero_label_exception"]) <= Fraction(pool + 1, 1 << n)
    vacuous = native_adaptive_pool_bound(32, 4112, 15, 32 ** 4)
    assert read(vacuous["existence_probability_upper_bound_including_global_zero_label_exception"]) == 1


def test_invalid_rank_domains_and_non_kernel_directions_rejected():
    for rows, width, t, r in (((1, 1), 4, 2, 1), ((1, 2), 4, 3, 1), ((1, 2), 4, 2, -1)):
        with pytest.raises(ValueError):
            universal_signature_gate(rows, width, t, r)
    with pytest.raises(ValueError):
        selected_schur_subcode_certificate((1, 2), 4, (1, 4))
    with pytest.raises(ValueError):
        selected_schur_subcode_certificate((1, 2), 4, (4, 4))
    with pytest.raises(ValueError):
        native_low_variation_source_bound(2, 1, 1)
    with pytest.raises(ValueError):
        identity_pencil_middle_source_mass(1)
    with pytest.raises(ValueError):
        native_adaptive_pool_bound(4, 4, 1, 7)
