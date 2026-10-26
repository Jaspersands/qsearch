"""Public group words checked against independent finite matrix exp/log."""
import random

import numpy as np
import pytest

from theorems.nil3_normal_word_bridge import (
    NormalWordLieBridge, controls, matvec, ut4_bridge, ut4_matrix, ut4_normal_word,
)


def matrix_log(matrix, p):
    x = matrix - np.eye(4, dtype=object)
    return (x - pow(2, -1, p)*(x @ x) + pow(3, -1, p)*(x @ x @ x)) % p


@pytest.mark.parametrize("p", [5, 7, 11])
def test_lazard_words_against_associative_matrix_logarithm(p):
    bridge, rng = ut4_bridge(p), random.Random(931)
    for _ in range(50):
        a, b = [tuple(rng.randrange(p) for _ in range(6)) for _ in range(2)]
        x, y = [matrix_log(ut4_matrix(w, p), p) for w in (a, b)]
        added = matrix_log(ut4_matrix(bridge.lie_add(a, b), p), p)
        bracket = matrix_log(ut4_matrix(bridge.lie_bracket(a, b), p), p)
        assert np.array_equal(added, (x+y) % p)
        assert np.array_equal(bracket, (x @ y - y @ x) % p)


def test_half_commutator_only_addition_is_wrong_in_class_three():
    bridge = ut4_bridge(5)
    a, b = (1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 0, 0)
    w = bridge.commutator(a, b)
    wrong = bridge.multiply(bridge.multiply(a, b), bridge.power(w, -pow(2, -1, 5)))
    expected = (matrix_log(ut4_matrix(a, 5), 5) + matrix_log(ut4_matrix(b, 5), 5)) % 5
    assert not np.array_equal(matrix_log(ut4_matrix(wrong, 5), 5), expected)
    assert np.array_equal(matrix_log(ut4_matrix(bridge.lie_add(a, b), 5), 5), expected)


def test_refined_flag_peeling_matches_matrix_log_coordinates():
    bridge, rng = ut4_bridge(7), random.Random(41)
    slots = [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3)]
    saw_different = False
    for _ in range(80):
        word = tuple(rng.randrange(7) for _ in range(6))
        coordinates = bridge.coordinates(word)
        matrix = matrix_log(ut4_matrix(word, 7), 7)
        assert coordinates == tuple(int(matrix[i, j]) for i, j in slots)
        assert bridge.element(coordinates) == word
        saw_different |= word != coordinates
    assert saw_different


def test_adapted_presentation_is_computed_from_collector_only():
    bridge, rng = ut4_bridge(11), random.Random(77)
    group, forward, inverse = bridge.adapted_presentation()
    assert (group.m, group.n) == (3, 3)
    for _ in range(60):
        a, b = [tuple(rng.randrange(11) for _ in range(6)) for _ in range(2)]
        av, bv = [matvec(inverse, bridge.coordinates(w), 11) for w in (a, b)]
        result = bridge.multiply(a, b)
        assert group.bch(av, bv) == matvec(inverse, bridge.coordinates(result), 11)
        assert bridge.element(matvec(forward, av, 11)) == a


def test_collector_really_uses_ordered_normal_words_not_bch_coordinates():
    word = (1, 1, 1, 1, 1, 1)
    matrix = ut4_matrix(word, 5)
    explicit = np.eye(4, dtype=object)
    for value, (i, j) in zip(word, [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3)]):
        elementary = np.eye(4, dtype=object)
        elementary[i, j] = value
        explicit = explicit @ elementary % 5
    assert np.array_equal(explicit, matrix)
    assert ut4_normal_word(matrix, 5) == word


def test_abelian_presentation_is_routed_separately():
    bridge = NormalWordLieBridge(5, 2, lambda a, b: tuple((x+y) % 5 for x, y in zip(a, b)))
    assert bridge.coordinates((3, 2)) == (3, 2)
    with pytest.raises(ValueError, match="abelian input"):
        bridge.adapted_presentation()


def test_peeling_needs_a_refined_flag_not_a_globally_central_flag():
    # Heisenberg normal words X^a Z^b Y^c. The tail <Y> is normal
    # in <Z,Y> but NOT in the whole group; Z is not the final generator.
    p = 5

    def collect(left, right):
        a, b, c = left
        x, y, z = right
        return (a+x) % p, (b+y-x*c) % p, (c+z) % p

    bridge = NormalWordLieBridge(p, 3, collect)
    assert bridge.commutator((1, 0, 0), (0, 0, 1)) == (0, 1, 0)
    for a in range(p):
        for b in range(p):
            for c in range(p):
                word = a, b, c
                coordinates = a, (b+a*c*pow(2, -1, p)) % p, c
                assert bridge.coordinates(word) == coordinates
                assert bridge.element(coordinates) == word
    group, forward, inverse = bridge.adapted_presentation()
    assert (group.m, group.n) == (2, 1)
    assert group.bracket((1, 0, 0), (0, 1, 0)) == (0, 0, 1)
    assert matvec(forward, (0, 0, 1), p) == (0, 1, 0)
    assert matvec(inverse, (0, 1, 0), p) == (0, 0, 1)


def test_invalid_characteristic_and_noncanonical_words_rejected():
    with pytest.raises(ValueError, match="p>3"):
        NormalWordLieBridge(3, 2, lambda a, b: a)
    bridge = ut4_bridge()
    with pytest.raises(ValueError, match="canonical"):
        bridge.coordinates((5, 0, 0, 0, 0, 0))


def test_live_bridge_report_does_not_claim_the_iss_recursion_was_executed():
    report = controls()
    assert report["failures"] == 0
    assert report["public_setup_collection_calls"] > 0
    assert report["normal_word_coordinates_are_not_logarithmic_coordinates"]
    assert not report["hidden_subgroup_or_oracle_accessed"]
    assert not report["iss_recursive_hsp_solver_executed"]
    assert not report["general_nil3_hsp_claim_admitted"]
