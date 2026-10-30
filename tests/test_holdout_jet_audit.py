"""Independent formal-expansion and exact-duality controls for public jets."""

from itertools import combinations, product
import json
import random
from unittest import mock

import numpy as np
import pytest

from theorems import holdout_jet_audit as audit


def rows_from_points(points):
    return [list(row) for row in zip(*points)]


def expansion_coefficient(monomial, point, derivative):
    # Expand prod_i (y_i + T_i) as a polynomial dictionary, without jet formulas.
    polynomial = {(): 1}
    for variable in monomial:
        result = {}
        for powers, coefficient in polynomial.items():
            result[powers] = result.get(powers, 0) + coefficient * point[variable]
            shifted = tuple(sorted((*powers, variable)))
            result[shifted] = result.get(shifted, 0) + coefficient
        polynomial = result
    return polynomial.get(tuple(derivative), 0) % 2


def check_witness(result):
    assert result["speedup_claim_allowed"] is False
    assert result["accepted_candidate"] is False
    columns, b = result["packed_training_columns"], result["packed_target"]
    witness = result["gf2"]["witness"]
    if result["gf2"]["member"]:
        assert witness["kind"] == "span_coefficients"
        assert len(witness["coefficients"]) == len(columns)
        image = 0
        for coefficient, column in zip(witness["coefficients"], columns):
            assert coefficient in (0, 1)
            if coefficient:
                image ^= column
        assert image == b
    else:
        assert witness["kind"] == "separating_annihilator"
        h = sum(bit << i for i, bit in enumerate(witness["annihilator"]))
        assert h == witness["packed_annihilator"]
        assert all((h & column).bit_count() % 2 == 0 for column in columns)
        assert (h & b).bit_count() % 2 == 1
    assert witness["verified"]
    if result["transpose_crosscheck"]["status"] == "checked":
        assert result["transpose_crosscheck"]["heldout_image_rank"] == result["gf2"]["delta"]


def test_independent_formal_expansion_every_binary_point_and_allowed_degree_small():
    for k in range(2, 5):
        points = list(product((0, 1), repeat=k))
        rows = rows_from_points(points)
        for d in range(2, k + 1):
            for s in range(1, d):
                result = audit.analyze(rows, d, s, len(points) - 1)
                for col, label in zip(result["packed_training_columns"], result["training_columns"]):
                    expected = sum(expansion_coefficient(B, points[label["point"]], label["derivative"]) << i
                                   for i, B in enumerate(result["monomials"]))
                    assert col == expected
                expected = sum(expansion_coefficient(B, points[-1], ()) << i
                               for i, B in enumerate(result["monomials"]))
                assert result["packed_target"] == expected
                check_witness(result)


def test_whole_heldout_block_omitted_but_only_evaluation_tested():
    rows = rows_from_points([(1, 0, 0), (0, 1, 0), (1, 1, 1)])
    result = audit.analyze(rows, 3, 2, 2)
    assert len(result["training_columns"]) == 2 * 4
    assert {label["point"] for label in result["training_columns"]} == {0, 1}
    assert result["dimensions"]["omitted_full_heldout_jets"] == 4
    assert result["test_operator"] == "evaluation_only"
    assert result["gf2"]["delta"] == 1
    check_witness(result)
    # All derivatives can carry information when the evaluation itself is zero.
    zero = audit.analyze(rows_from_points([(0, 0, 0), (1, 1, 0)]), 3, 2, 1)
    assert zero["gf2"]["rank"] == 0 and zero["gf2"]["delta"] == 0
    assert zero["gf2"]["target_zero"]
    assert expansion_coefficient((0, 1, 2), (1, 1, 0), (2,)) == 1
    check_witness(zero)


def test_empty_training_rank_deficiency_saturation_and_no_input_change():
    single = audit.analyze([[1], [1], [1]], 3, 2, 0, rational=True)
    assert single["training_columns"] == []
    assert not single["generator"]["full_row_rank"]
    assert single["gf2"]["delta"] == single["rational"]["delta"] == 1
    check_witness(single)
    rows = np.asarray(rows_from_points([(1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]))
    before = rows.copy()
    saturated = audit.analyze(rows, 2, 1, 3)
    assert np.array_equal(rows, before)
    assert saturated["generator"]["basis_changed"] is False
    assert saturated["gf2"]["saturated"] and saturated["gf2"]["member"]
    check_witness(saturated)


def test_counterexample_has_exact_field_disagreement_and_explicit_certificates():
    points = [tuple(int(i == j) for i in range(6)) for j in range(6)]
    points += [(0, 0, 1, 1, 1, 0), (1, 1, 0, 0, 1, 0), (1, 1, 1, 1, 0, 0)]
    result = audit.analyze(rows_from_points(points), 3, 2, 8, rational=True)
    assert (result["gf2"]["rank"], result["gf2"]["augmented_rank"]) == (8, 8)
    assert (result["rational"]["rank"], result["rational"]["augmented_rank"]) == (8, 9)
    assert result["field_membership_disagrees"]
    assert result["rational"]["operator"] == "full_hasse" and result["rational"]["exact"]
    nonunit = [column for column, label in zip(result["packed_training_columns"], result["training_columns"])
               if label["point"] in (6, 7)]
    assert len(nonunit) == 14
    assert nonunit[1] ^ nonunit[2] ^ nonunit[10] ^ nonunit[11] == result["packed_target"]
    coefficients = {(0, 2, 4): 1, (0, 2, 3): -1, (0, 1, 2): -1}
    h = [coefficients.get(tuple(B), 0) for B in result["monomials"]]
    assert all(sum(v * ((column >> i) & 1) for i, v in enumerate(h)) == 0
               for column in result["packed_training_columns"])
    assert sum(v * ((result["packed_target"] >> i) & 1) for i, v in enumerate(h)) == -2
    check_witness(result)


def test_reduced_orders_examples_and_general_lowbit_rule():
    assert audit.reduced_derivative_orders(7, 6) == [3, 5]
    assert audit.reduced_derivative_orders(8, 7) == [0, 4, 6]
    for d in range(2, 17):
        expected = sorted(d - 2**j for j in range(1, d.bit_length()) if d - 2**j >= 0)
        assert audit.reduced_derivative_orders(d, d - 1) == expected


def test_elementary_symmetric_e4_needs_retained_order_zero_not_only_top_order():
    point = (1,) * 6
    monomials = list(combinations(range(6), 4))
    for order in range(3):
        for derivative in combinations(range(6), order):
            value = sum(expansion_coefficient(B, point, derivative) for B in monomials) % 2
            assert value == int(order == 0)

    rows = rows_from_points([point, point])
    full = audit.analyze(rows, 4, 3, 1)
    reduced = audit.analyze(rows, 4, 3, 1, reduced=True)
    assert reduced["derivative_orders"] == [0, 2]
    assert full["gf2"]["member"] and reduced["gf2"]["member"]
    h = (1 << len(monomials)) - 1  # Coefficients of e4 are all one.
    positive_order_columns = [
        column for column, label in zip(full["packed_training_columns"], full["training_columns"])
        if label["derivative"]
    ]
    assert all((h & column).bit_count() % 2 == 0 for column in positive_order_columns)
    assert (h & full["packed_target"]).bit_count() % 2 == 1
    top_order_columns = [
        column for column, label in zip(full["packed_training_columns"], full["training_columns"])
        if len(label["derivative"]) == 2
    ]
    assert audit.gf2_bit_rank(top_order_columns + [full["packed_target"]]) == audit.gf2_bit_rank(top_order_columns) + 1
    check_witness(full)
    check_witness(reduced)


def test_full_reduced_same_span_kernels_and_membership_exhaustive_small_random_larger():
    rng = random.Random(1984)
    for k in range(2, 7):
        point_sets = [[point] for point in product((0, 1), repeat=k)] if k <= 4 else [
            [tuple(rng.randrange(2) for _ in range(k)) for _ in range(3)] for _ in range(4)]
        for points in point_sets:
            rows = rows_from_points(points + [tuple(rng.randrange(2) for _ in range(k))])
            for d in range(2, k + 1):
                for s in range(1, d):
                    full = audit.analyze(rows, d, s, len(points))
                    reduced = audit.analyze(rows, d, s, len(points), reduced=True)
                    full_columns, reduced_columns = full["packed_training_columns"], reduced["packed_training_columns"]
                    rank = full["gf2"]["rank"]
                    assert rank == reduced["gf2"]["rank"]
                    assert audit.gf2_bit_rank(full_columns + reduced_columns) == rank
                    assert full["gf2"]["delta"] == reduced["gf2"]["delta"]
                    assert full["transpose_crosscheck"]["annihilator_dimension"] == reduced["transpose_crosscheck"]["annihilator_dimension"]
                    check_witness(full)
                    check_witness(reduced)


@pytest.mark.parametrize("rows,d,s,held", [
    ([], 2, 1, 0), ([[0], []], 2, 1, 0), ([[], []], 2, 1, 0),
    ([[0, 1], [1]], 2, 1, 0), ([[0.0], [1]], 2, 1, 0),
    ([[True], [1]], 2, 1, 0), ([[2], [0]], 2, 1, 0),
    ([["0"], [1]], 2, 1, 0), ([[0], [1]], 2.0, 1, 0),
    ([[0], [1]], True, 1, 0), ([[0], [1]], 2, 0, 0),
    ([[0], [1]], 2, 2, 0), ([[0], [1]], 3, 1, 0),
    ([[0], [1]], 2, 1, -1), ([[0], [1]], 2, 1, 1),
    ([[0], [1]], 2, 1, True), ([[0], [1]], 2, 1, 0.0),
    (np.zeros((2, 2, 1), dtype=int), 2, 1, 0),
])
def test_invalid_inputs_rejected_before_expansion(rows, d, s, held):
    with mock.patch.object(audit, "combinations", side_effect=AssertionError("expanded too soon")):
        with pytest.raises((TypeError, ValueError)):
            audit.analyze(rows, d, s, held)


@pytest.mark.parametrize("kwargs", [
    {"max_monomials": 1}, {"max_entries": 1}, {"max_entries": True},
    {"max_monomials": 0}, {"max_entries": 1.5}, {"rational": 1},
    {"reduced": 1}, {"rational": True, "reduced": True},
])
def test_caps_and_options_before_expansion(kwargs):
    with mock.patch.object(audit, "combinations", side_effect=AssertionError("expanded too soon")):
        with pytest.raises((TypeError, ValueError)):
            audit.analyze([[1, 0], [0, 1], [1, 1]], 2, 1, 1, **kwargs)


def test_rational_smaller_caps_and_transpose_cap_status():
    with mock.patch.object(audit, "combinations", side_effect=AssertionError("expanded too soon")):
        with pytest.raises(ValueError, match="rational cap"):
            audit.analyze([[0, 1]] * 12, 4, 1, 1, rational=True)
        with pytest.raises(ValueError, match="rational cap"):
            audit.analyze([[0] * 300] * 6, 3, 2, 299, rational=True)
    with mock.patch.object(audit, "TRANSPOSE_MAX_ENTRIES", 1):
        result = audit.analyze([[1, 0], [0, 1], [1, 1]], 2, 1, 1)
    assert result["transpose_crosscheck"]["status"] == "skipped_cap"
    check_witness(result)


def test_report_is_deterministic_json_public_fixtures_and_bounded():
    result = audit.report()
    assert json.loads(json.dumps(result)) == result
    assert result == audit.report()
    assert not result["asymptotic_gijs_validated"] and not result["quantum_claim"]
    assert result["speedup_claim_allowed"] is False
    assert result["accepted_candidate"] is False
    records = {record["id"]: record for record in result["controls"]}
    goppa, random_control = records["binary_goppa_t2"], records["matched_random_public_matrix"]
    assert goppa["metadata"]["goppa_instance"]
    assert not goppa["metadata"]["sufficient_interpolation_holds"]
    assert goppa["full"]["gf2"]["saturated"]
    assert goppa["full"]["gf2"]["member"] and random_control["full"]["gf2"]["member"]
    assert goppa["full"]["generator"] == random_control["full"]["generator"]
    assert records["nonsaturated_duplicate"]["full"]["gf2"]["member"]
    assert not records["nonsaturated_duplicate"]["full"]["gf2"]["saturated"]
    actual = records["binary_membership_not_complex_membership"]
    assert not actual["metadata"]["goppa_instance"] and not actual["metadata"]["general_no_go"]
    assert actual["full"]["field_membership_disagrees"]
    for record in result["controls"]:
        assert record["full_reduced_gf2_agree"]
        check_witness(record["full"])
        check_witness(record["reduced"])
        for operator in (record["full"], record["reduced"]):
            assert operator["dimensions"]["monomials"] <= 4096
            assert operator["dimensions"]["entries_including_target"] <= 1000000
