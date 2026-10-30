from fractions import Fraction as F
from itertools import product

import pytest

import class_three as c


@pytest.fixture(scope="module")
def hidden():
    return c.span(c.lifted_hidden_basis(), 10)


@pytest.fixture(scope="module")
def result():
    return c.run()


def test_cyclotomic_multiplication_and_vanishing_sum():
    total = c.CZERO
    for i in range(7):
        total = c.cadd(total, c.root(i))
        for j in range(7):
            assert c.cmul(c.root(i), c.root(j)) == c.root(i + j)
    assert total == c.CZERO


def test_bch_has_nonzero_cubic_term():
    x, y = c.unit(5, 0), c.unit(5, 1)
    actual = c.bch(x, y, c.BASE_BRACKETS)
    assert actual == (1, 1, 4, 3, 4)
    assert c.associative_exp(c.lie_words(actual)) == c.associative_product(
        c.associative_exp(c.lie_words(x)), c.associative_exp(c.lie_words(y)))


def test_original_tilted_subgroup_survives_cover(hidden):
    assert hidden == {(a, 0, 0, a, 0, 0, 0, 0, 0, 0) for a in range(7)}
    assert len(c.lifted_hidden_basis((1, 2))) > 1
    assert len(c.lifted_hidden_basis((1, 1, 1))) > 1


def test_zero_dilation_is_forbidden():
    with pytest.raises(ValueError, match="not an automorphism"):
        c.dilation(0, c.unit(10, 0))


def test_empty_witness_is_forbidden():
    with pytest.raises(ValueError, match="nonempty"):
        c.merge({}, (0, 0), (0, 0))


@pytest.mark.parametrize("degree", (2, 3))
def test_all_scalar_label_tuples_have_verified_witness(degree):
    for labels in product(range(7), repeat=degree + 1):
        scales = c.witness(labels, degree)
        assert any(scales)
        assert sum(lam * pow(s, degree, 7) for lam, s in zip(labels, scales)) % 7 == 0


def test_insufficient_arity_fails_instead_of_using_zero():
    with pytest.raises(ValueError, match="No nonzero"):
        c.witness((1,), 3)


def test_full_two_sided_projection_not_normalized_forbidden_branch(hidden):
    containing = {c.add(h, c.scale(c.unit(10, 9), z)) for h in hidden for z in range(7)}
    moments, masses = c.branch_moments(containing, 9)
    assert set(moments) == {0}
    assert masses == {i: F(int(i == 0)) for i in range(7)}


def test_sparse_moments_include_exact_zero_off_support(hidden):
    moments, masses = c.branch_moments(hidden, 9)
    assert set(masses.values()) == {F(1, 7)}
    assert all(len(table) == 49 for table in moments.values())
    assert all(c.unit(10, 1) not in table for table in moments.values())
    assert moments[1][c.unit(10, 9)] == 1


def test_linear_cancellation_does_not_pass_cubic_gate(hidden):
    moments, _ = c.branch_moments(hidden, 9)
    actual = c.merge(c.transformed_moments(moments), (1, 2), (1, 3))
    assert actual[c.unit(10, 9)] == 6


def test_algebra_and_full_descent_counts(result):
    assert result["algebra"]["base_class"] == 3
    assert result["algebra"]["cover_basis_jacobi_checks"] == 1000
    assert [row["degree"] for row in result["stages"]] == [3, 3, 2, 2, 2]
    assert sum(row["complete_label_tuples_checked"] for row in result["stages"]) == 5831
    assert all(row["positive_labels"] == 7 for row in result["stages"])
    assert all(row["records_with_zero_label"] > 0 for row in result["stages"])
    assert all(row["records_with_zero_scale"] > 0 for row in result["stages"])


def test_final_readout_recovers_tilt_not_only_abelianization(result):
    final = result["final_readout"]
    assert final["recovered_basis"] == [(1, 0, 0, 1, 0)]
    assert final["nonzero_frequencies"] == 2401
    assert final["total_probability"] == "1"
    assert final["frequencies_checked"] == 16807


def test_source_costs_are_not_hidden(result):
    ledger = result["one_terminal_state_resource_ledger"]
    assert ledger["lifted_source_copies"] == 432
    assert ledger["original_source_copies"] == 1296


def test_full_arity_active_targets_are_also_exercised(result):
    assert all(row["additional_all_active_witnesses"] == 1 for row in result["stages"])
    assert result["center_contained_control"]["additional_all_active_witnesses"] == 0


def test_no_quantum_or_novelty_admission(result):
    for key in ("quantum_circuit_executed", "generic_sde_implemented", "novelty_certified",
                "speedup_established_by_this_run"):
        assert result[key] is False


def test_wrong_order_and_early_abelianization_are_detected(result):
    negatives = result["negative_controls"]
    assert negatives["wrong_side_coset_product"] == "rejected"
    assert negatives["abelian_subtraction_before_grade_one"] == "rejected"
    assert negatives["base_dilation_on_tilted_hidden_subgroup"] == "rejected"
