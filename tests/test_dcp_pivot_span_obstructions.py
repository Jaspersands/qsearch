from fractions import Fraction
import itertools

import pytest

from dcp_carry_packets import compile_packet
from dcp_conditional_carry_features import packet_pivot_pencil_certificate
from dcp_lowbit_fiber_normalizer import _apply_rows, _columns_value
from dcp_physical_phase_noise import read
from dcp_pivot_span_obstructions import (
    PolarOperatorFamily, _flatten, _nullspace, _restriction, _row_basis,
    complete_row_block_certificate, packet_polar_operator_family,
    physical_schur_product_certificate, selected_pivot_span_certificate, weighted_radical_span_screen,
)


def _fraction(family, W):
    good = sum(len(_row_basis(_restriction(family.matrix(y), W), len(W))) == len(W)
               for y in range(1 << family.background_bits))
    return Fraction(good, 1 << family.background_bits)


def test_binary_nullspaces_and_canonical_span_are_exact():
    for rows in itertools.product(range(8), repeat=3):
        basis = _row_basis(rows, 3)
        null = _nullspace(rows, 3)
        assert len(basis) + len(null) == 3
        assert _row_basis(reversed(rows), 3) == basis
        assert all(all((r & x).bit_count() % 2 == 0 for r in rows) for x in null)
        assert len(_row_basis(null, 3)) == len(null)


def test_actual_full_packet_family_matches_every_background_and_input():
    packet = compile_packet([[1, 0, 3, 2, 1], [0, 1, 2, 1, 1]], 8)
    U = (1, 2)
    family, provenance = packet_polar_operator_family(packet, U)
    V = tuple(int(x, 16) for x in provenance["complement_directions_hex"])
    assert family.constant_rows == (2, 3)
    assert family.operators == ((1,), (2,))
    for y in range(1 << family.background_bits):
        background = _columns_value(V, y)
        c = sum((x & 1) << l for l, x in enumerate(packet.residual(background)))
        for u in range(1 << family.input_bits):
            z = background ^ _columns_value(U, u)
            value = sum((x & 1) << l for l, x in enumerate(packet.residual(z)))
            assert value == c ^ _apply_rows(family.matrix(y), u)
    old = packet_pivot_pencil_certificate(packet, U)
    assert old["constant_matrix_rows"] == family.constant_rows
    assert old["variation_generator_rows"] == family.variation_rows
    assert not provenance["input_assignments_or_secret_states_enumerated"]


def test_polar_variation_only_depends_on_binary_source_and_not_middle_or_high_bits():
    A = ((1, 0, 3, 2, 1), (0, 1, 2, 1, 1))
    family, _ = packet_polar_operator_family(compile_packet(A, 16), (1, 2))
    changed_middle, _ = packet_polar_operator_family(compile_packet([[x ^ (2 if l == 0 and i == 2 else 0)
                                                                  for i, x in enumerate(r)] for l, r in enumerate(A)], 16), (1, 2))
    changed_high, _ = packet_polar_operator_family(compile_packet([[x ^ 4 for x in r] for r in A], 16), (1, 2))
    assert family.variation_rows == changed_middle.variation_rows == changed_high.variation_rows
    assert family.constant_rows == changed_high.constant_rows
    assert family.constant_rows != changed_middle.constant_rows


def test_complete_block_has_actual_private_background_witnesses():
    family = PolarOperatorFamily(3, (1, 4), ((1, 0), (2, 0), (0, 1), (0, 2)))
    row = complete_row_block_certificate(family)
    assert row["complete_row_block_dimension"] == 2
    assert row["all_fixed_n_dimensional_spans_excluded_by_complete_block"]
    assert read(row["all_fixed_spans_uniform_background_invertibility_fraction_upper_bound"]) == Fraction(1, 2)
    flat = [_flatten(M, 3) for M in family.variation_rows]
    for e, witnesses in zip(row["complete_row_block_basis_hex"], row["complete_row_block_background_witnesses_hex"]):
        for l, y in enumerate(witnesses):
            assert _columns_value(flat, int(y, 16)) == int(e, 16) << (3 * l)


def test_all_span_block_fraction_bound_holds_for_all_seven_binary_two_planes():
    family = PolarOperatorFamily(3, (1, 4), ((1, 0), (2, 0), (0, 1), (0, 2)))
    spans = {_row_basis((u, v), 3) for u in range(1, 8) for v in range(u + 1, 8)}
    assert len(spans) == 7
    fractions = []
    for W in spans:
        certificate = selected_pivot_span_certificate(family, W)
        actual = _fraction(family, W)
        fractions.append(actual)
        assert actual <= read(certificate["uniform_background_invertibility_fraction_upper_bound"]) <= Fraction(1, 2)
        assert certificate["all_backgrounds_invertible_excluded"]
    assert max(fractions) == Fraction(1, 2)


def test_correlated_binary_positive_control_survives_every_obstruction():
    family = PolarOperatorFamily(2, (2, 3), ((1, 2),))
    certificate = selected_pivot_span_certificate(family, (1, 2))
    assert _fraction(family, (1, 2)) == 1
    assert not certificate["all_backgrounds_invertible_excluded"]
    assert certificate["complete_row_block"]["complete_row_block_dimension"] == 0
    assert not certificate["dimension_theorem_excludes_every_constant_part"]
    assert not certificate["no_obstruction_is_a_success_proof"]


def test_triangular_positive_control_is_not_killed_by_a_nonzero_variation_space():
    family = PolarOperatorFamily(2, (1, 2), ((2, 0),))
    certificate = selected_pivot_span_certificate(family, (1, 2))
    assert not certificate["all_backgrounds_invertible_excluded"]
    assert certificate["pencil_coverage"]["all_backgrounds_invertible_certified"]


def test_dimension_gate_kills_correlated_high_rank_with_zero_complete_core():
    family = PolarOperatorFamily(3, (1, 2, 4), ((3, 0, 0), (0, 6, 0), (0, 0, 5), (1, 2, 4)))
    certificate = selected_pivot_span_certificate(family, (1, 2, 4))
    assert certificate["dimension_theorem_excludes_every_constant_part"]
    assert certificate["complete_row_block"]["complete_row_block_dimension"] == 0
    assert certificate["all_backgrounds_invertible_excluded"]
    assert _fraction(family, (1, 2, 4)) <= read(certificate["uniform_background_invertibility_fraction_upper_bound"])


def test_rebasing_a_failed_span_preserves_actual_fraction_and_variation_rank():
    family = PolarOperatorFamily(3, (1, 4), ((1, 0), (2, 0), (0, 1), (0, 2)))
    left = selected_pivot_span_certificate(family, (1, 4))
    right = selected_pivot_span_certificate(family, (5, 4))
    assert _fraction(family, (1, 4)) == _fraction(family, (5, 4)) == Fraction(1, 2)
    assert left["complete_row_block"]["background_matrix_image_dimension"] == right["complete_row_block"]["background_matrix_image_dimension"]
    assert right["all_backgrounds_invertible_excluded"]


def test_weighted_radical_screen_is_only_a_necessary_span_gate():
    positive = PolarOperatorFamily(2, (2, 3), ((1, 2),))
    row = weighted_radical_span_screen(positive)
    assert row["eligible_direction_span_dimension"] == 2
    assert not row["all_fixed_spans_excluded"]
    assert not row["necessary_gate_pass_proves_an_eligible_n_dimensional_pivot_span_exists"]
    full = PolarOperatorFamily(2, (1, 2), ((1, 0), (2, 0), (0, 1), (0, 2)))
    assert weighted_radical_span_screen(full)["all_fixed_spans_excluded"]


def test_weighted_radical_cap_is_charged_not_mislabeled_as_no_go():
    family = PolarOperatorFamily(13, tuple(1 << j for j in range(13)), ())
    row = weighted_radical_span_screen(family)
    assert row["status"] == "SKIPPED_EXPONENTIAL_WEIGHTED_COMBINATION_MENU"
    assert not row["all_fixed_spans_excluded"]
    assert not row["skipped_is_a_mathematical_negative_result"]


def test_all_two_by_two_two_generator_certificates_have_no_false_no_go_or_fraction_bound():
    matrices = [(bits & 3, bits >> 2) for bits in range(16)]
    for M0, M1, M2 in itertools.product(matrices, repeat=3):
        family = PolarOperatorFamily(2, M0, (M1, M2))
        row = selected_pivot_span_certificate(family, (1, 2))
        actual = _fraction(family, (1, 2))
        assert actual <= read(row["uniform_background_invertibility_fraction_upper_bound"])
        if row["all_backgrounds_invertible_excluded"]:
            assert actual < 1
        if row["surjective_direction_background_witness"] is not None:
            witness = row["surjective_direction_background_witness"]
            assert _apply_rows(family.matrix(int(witness["background_mask_hex"], 16)), int(witness["input_direction_hex"], 16)) == 0
        if weighted_radical_span_screen(family)["all_fixed_spans_excluded"]:
            assert actual < 1


def test_zero_variation_and_singular_constant_have_exact_failure_not_fake_fraction():
    for M0, value in (((1, 2), 1), ((1, 1), 0)):
        row = selected_pivot_span_certificate(PolarOperatorFamily(2, M0, ()), (1, 2))
        assert read(row["uniform_background_invertibility_fraction_upper_bound"]) == value


def test_physical_schur_quotient_equals_actual_pencil_rank_and_keeps_correlations():
    packet = compile_packet([[1, 0, 3, 2, 1], [0, 1, 2, 1, 1]], 8)
    row = physical_schur_product_certificate(packet, (1, 2))
    assert row["polar_variation_dimension"] == 1
    assert row["individual_column_variation_dimensions"] == [1, 1]
    assert row["disjoint_physical_supports"]
    assert row["unused_physical_columns_binary_rank"] == 1
    assert not row["disjoint_support_and_unused_full_rank_certify_column_separability"]
    assert not row["all_constant_parts_excluded_by_disjoint_support_gate"]


def test_disjoint_short_relation_shortcut_is_column_separable_when_unused_columns_span():
    B = ((1, 0, 1, 1, 0, 0, 1, 0), (0, 1, 0, 0, 1, 1, 0, 1))
    packet = compile_packet(B, 8)
    W = (3, 12)
    family, _ = packet_polar_operator_family(packet, W)
    row = physical_schur_product_certificate(packet, W)
    assert row["disjoint_support_and_unused_full_rank_certify_column_separability"]
    assert row["all_constant_parts_excluded_by_disjoint_support_gate"]
    assert row["polar_variation_dimension"] == 2
    selected = selected_pivot_span_certificate(family, (1, 2))
    assert selected["pencil_coverage"]["background_image_is_cartesian_product_of_column_spaces"]
    assert selected["all_backgrounds_invertible_excluded"]


def test_invalid_operator_or_pivot_inputs_fail_explicitly():
    for d, constant, variations in ((1, (1, 1), ()), (2, (), ()), (2, (1, 4), ()), (2, (1, 2), ((1,),))):
        with pytest.raises(ValueError):
            PolarOperatorFamily(d, constant, variations)
    family = PolarOperatorFamily(2, (1, 2), ())
    for directions in ((), (1,), (1, 1), (1, 4), (True, 2)):
        with pytest.raises(ValueError):
            selected_pivot_span_certificate(family, directions)
    with pytest.raises(ValueError):
        family.matrix(1)
    with pytest.raises(ValueError):
        weighted_radical_span_screen(family, combination_cap=-1)
    with pytest.raises(ValueError):
        packet_polar_operator_family(compile_packet([[1, 1, 1]], 8, syndrome=1), (1,))
