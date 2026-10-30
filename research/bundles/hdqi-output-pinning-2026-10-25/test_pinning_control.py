from fractions import Fraction as F

import pytest
import sympy as sp

from pinning_control import (
    certificate, closed_coefficient, connected_extension_control, exact_algebra, limiting_heat_bath,
    magnitude_intervals, physical_operators, verify_taylor,
)


def test_physical_algebra():
    assert all(exact_algebra().values())


def test_whole_vector_taylor_identity():
    assert verify_taylor(16)
    assert closed_coefficient(3)[7] == F(1, 3)


def test_forbidden_words_have_exact_matrix_zeros():
    a, b, c = physical_operators()
    h = a + b + c
    # Cayley-Hamilton: powers 0,...,7 suffice for every analytic function.
    vec = sp.eye(8)[:, 0]
    for _ in range(8):
        assert vec[3] == vec[6] == 0
        vec = h * vec


@pytest.mark.parametrize("beta", [F(1, 16), F(1, 64), F(1, 256)])
def test_influence_certificate_inside_degree_scale(beta):
    result = certificate(beta)
    assert 3 * beta * beta < F(1, 64)
    assert result["positive_boundary_010_lower"] > 0
    assert result["positive_boundary_111_lower"] > 0
    assert result["row_sum_lower"] > 1
    assert result["perron_polynomial_at_one"] < 0
    assert result["all_inclusion_checks"]


def test_tail_enclosures_nested():
    coarse = magnitude_intervals(F(1, 16), terms=4)
    fine = magnitude_intervals(F(1, 16), terms=12)
    for (lo, hi), (flo, fhi) in zip(coarse, fine):
        assert lo <= flo <= fhi <= hi


def test_total_weight_normalization_coefficients():
    for order in range(17):
        actual = sum(
            (sum((a * b for a, b in zip(closed_coefficient(k),
                                        closed_coefficient(order-k))), F(0))
             for k in range(order + 1)), F(0)
        )
        expected = (2**order) * closed_coefficient(order)[0]
        assert actual == expected


def test_limiting_chain_has_positive_gap():
    chain = limiting_heat_bath()
    assert all(sum(chain.row(i)) == 1 for i in range(6))
    assert chain.eigenvals() == {sp.Integer(1): 1,
                                sp.Rational(2, 3): 4,
                                sp.Rational(1, 3): 1}


def test_limiting_chain_matches_physical_leading_powers():
    a, b, c = physical_operators()
    h = a + b + c
    vector = sp.eye(8)[:, 0]
    leading = {}
    for order in range(8):
        for word in range(8):
            if word not in leading and vector[word] != 0:
                leading[word] = (order, vector[word]**2)
        vector = -h * vector / (order + 1)
    support = [0, 4, 2, 1, 5, 7]
    chain = sp.zeros(6)
    for row, word in enumerate(support):
        for bit in (1, 2, 4):
            neighbor = word ^ bit
            if neighbor not in leading:
                jump = 0
            elif leading[neighbor][0] < leading[word][0]:
                jump = 1
            elif leading[neighbor][0] > leading[word][0]:
                jump = 0
            else:
                jump = leading[neighbor][1] / (leading[neighbor][1] + leading[word][1])
            if jump:
                chain[row, support.index(neighbor)] += sp.Rational(jump, 3)
            chain[row, row] += (1 - jump) / sp.Integer(3)
    assert chain == limiting_heat_bath()


def test_perron_lower_matrix_characteristic_polynomial():
    u, v, eigenvalue = sp.symbols("u v eigenvalue")
    matrix = sp.Matrix([[0, u, 1], [v, 0, v], [1, u, 0]])
    assert sp.expand(matrix.charpoly(eigenvalue).as_expr()) == sp.expand(
        (eigenvalue + 1) * (eigenvalue**2 - eigenvalue - 2*u*v))


def test_conditional_influence_uses_two_possible_boundaries():
    intervals = magnitude_intervals(F(1, 256))
    assert intervals[2][0] > 0 and intervals[7][0] > 0
    assert intervals[6] == intervals[3] == (0, 0)
    # Center=1, right=0 permits only 010; right=1 permits only 111.
    # Thus the left-bit probabilities are exactly zero and exactly one.
    assert (F(1, 512)**2) < 1


def test_connected_extensive_cycle_class_control():
    result = connected_extension_control()
    assert result["induced_path"]
    assert result["singleton_h_coefficient"] == 1
    assert result["nonadjacent_h2_coefficient"] == 2
    assert result["triple_h3_coefficient"] == -2
    assert result["adjacent_pairs_zero_through_order_8"]
    assert result["every_odd_edge_word_zero_through_order_8"]


@pytest.mark.parametrize("bad", [0, -1, F(1, 4)])
def test_reject_out_of_control_range(bad):
    with pytest.raises(ValueError):
        magnitude_intervals(bad)


def test_reject_float_certificate():
    with pytest.raises(TypeError):
        magnitude_intervals(0.0625)


def test_reject_one_term_difference_tail():
    with pytest.raises(ValueError):
        magnitude_intervals(F(1, 16), terms=1)


@pytest.mark.parametrize("bad", [-1, 0.5, True])
def test_reject_malformed_coefficient_order(bad):
    with pytest.raises(ValueError):
        closed_coefficient(bad)
