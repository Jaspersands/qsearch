"""Exact controls for a native output-pinning obstruction, not a sampler."""

from fractions import Fraction as F
from math import factorial
from itertools import combinations

import sympy as sp


def physical_operators():
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    eye = sp.eye(2)
    return (
        sp.kronecker_product(x, eye, eye),
        sp.kronecker_product(z, x, eye),
        sp.kronecker_product(eye, z, x),
    )


def exact_algebra():
    a, b, c = physical_operators()
    h = a + b + c
    eye = sp.eye(8)
    d = a * c
    plus, minus = (eye + d) / 2, (eye - d) / 2
    return {
        "anticommute_ab": a * b == -b * a,
        "anticommute_bc": b * c == -c * b,
        "commute_ac": a * c == c * a,
        "central_d": d * h == h * d,
        "involution_d": d * d == eye,
        "square": h * h == 3 * eye + 2 * d,
        "plus_sector": h * h * plus == 5 * plus,
        "minus_sector": h * h * minus == minus,
        "word_sign": d * h == a + c - a * b * c,
    }


def closed_coefficient(order):
    """Coefficient of t**order in the complete unnormalized vector."""
    if type(order) is not int or order < 0:
        raise ValueError("order must be a nonnegative integer")
    out = [F(0)] * 8
    k = order // 2
    scale = F(1, factorial(order))
    if order % 2 == 0:
        out[0] = (5**k + 1) * scale / 2
        out[5] = (5**k - 1) * scale / 2
    else:
        out[1] = out[4] = -(5**k) * scale
        out[2] = -(5**k + 1) * scale / 2
        out[7] = (5**k - 1) * scale / 2
    return tuple(out)


def verify_taylor(max_order=16):
    a, b, c = physical_operators()
    h = a + b + c
    vector = sp.eye(8)[:, 0]
    for order in range(max_order + 1):
        expected = sp.Matrix([sp.Rational(x.numerator, x.denominator)
                              for x in closed_coefficient(order)])
        if vector != expected:
            return False
        vector = -h * vector / (order + 1)
    return True


def _positive_series(t, parity, sign, terms):
    # sign=None is s_5; otherwise coefficients are (5**k + sign)/2.
    def term(k):
        coefficient = F(5**k) if sign is None else F(5**k + sign, 2)
        power = 2 * k + parity
        return coefficient * t**power / factorial(power)

    lower = sum((term(k) for k in range(terms)), F(0))
    degree = 2 * terms + parity
    ratio = 6 * t * t / ((degree + 1) * (degree + 2))
    if ratio >= 1:
        raise ValueError("tail ratio is not contracting")
    return lower, lower + term(terms) / (1 - ratio)


def magnitude_intervals(beta, terms=10):
    if isinstance(beta, bool) or not isinstance(beta, (int, F)):
        raise TypeError("beta must be exact rational")
    if not 0 < beta <= F(1, 8):
        raise ValueError("control requires 0 < beta <= 1/8")
    if type(terms) is not int or terms < 2:
        raise ValueError("at least two terms are required")
    t = F(beta) / 2
    zero = (F(0), F(0))
    a = _positive_series(t, 1, None, terms)
    return (
        _positive_series(t, 0, 1, terms), a,
        _positive_series(t, 1, 1, terms), zero,
        a, _positive_series(t, 0, -1, terms), zero,
        _positive_series(t, 1, -1, terms),
    )


def certificate(beta):
    amplitudes = magnitude_intervals(beta)
    weights = [(lo * lo, hi * hi) for lo, hi in amplitudes]
    zlo = sum((lo for lo, _ in weights), F(0))
    zhi = sum((hi for _, hi in weights), F(0))
    alo, _ = amplitudes[1]
    _, chi = amplitudes[5]
    elo, _ = amplitudes[7]
    u = alo**2 / (alo**2 + chi**2)
    v = elo**2 / (chi**2 + elo**2)
    inclusions = {}
    for mask in range(1, 8):
        upper = sum((hi for word, (_, hi) in enumerate(weights)
                     if word & mask == mask), F(0)) / zlo
        bound = (F(beta) / 2)**(2 * mask.bit_count())
        inclusions[mask] = upper <= bound
    return {
        "u_lower": u,
        "v_lower": v,
        "row_sum_lower": 1 + u,
        "perron_polynomial_at_one": -2 * u * v,
        "positive_boundary_010_lower": weights[2][0] / zhi,
        "positive_boundary_111_lower": weights[7][0] / zhi,
        "all_inclusion_checks": all(inclusions.values()),
        "inclusion_checks": inclusions,
    }


def limiting_heat_bath():
    # Ordered support: 000, 100, 010, 001, 101, 111.
    return sp.Matrix([
        [1, 0, 0, 0, 0, 0],
        [F(1, 3), F(2, 3), 0, 0, 0, 0],
        [F(1, 3), 0, F(2, 3), 0, 0, 0],
        [F(1, 3), 0, 0, F(2, 3), 0, 0],
        [0, F(1, 3), 0, F(1, 3), F(1, 3), 0],
        [0, 0, 0, 0, F(1, 3), F(2, 3)],
    ])


def connected_extension_control():
    """Integer H**k|0> checks for the native L(K_4) graph, k<=8."""
    root_edges = [(0, 1), (1, 2), (2, 3), (0, 2), (0, 3), (1, 3)]
    anti_edges = [(i, j) for i, j in combinations(range(6), 2)
                  if set(root_edges[i]) & set(root_edges[j])]
    predecessors = [sum(1 << i for i, j in anti_edges if j == bit)
                    for bit in range(6)]
    vector = {0: 1}
    powers = []
    for _ in range(9):
        powers.append(vector)
        nxt = {}
        for word, value in vector.items():
            for bit, neighbors in enumerate(predecessors):
                sign = (-1)**((word & neighbors).bit_count())
                target = word ^ (1 << bit)
                nxt[target] = nxt.get(target, 0) + sign * value
        vector = {word: value for word, value in nxt.items() if value}
    return {
        "root_vertices": 4,
        "root_edges": len(root_edges),
        "cycle_rank": 3,
        "induced_path": ((0, 1) in anti_edges and (1, 2) in anti_edges
                         and (0, 2) not in anti_edges),
        "singleton_h_coefficient": powers[1][2],
        "nonadjacent_h2_coefficient": powers[2][5],
        "triple_h3_coefficient": powers[3][7],
        "adjacent_pairs_zero_through_order_8": all(
            power.get(3, 0) == power.get(6, 0) == 0 for power in powers),
        "every_odd_edge_word_zero_through_order_8": all(
            value == 0 for power in powers for word, value in power.items()
            if sum(bool(word & (1 << i)) and bool(word & (1 << j))
                   for i, j in anti_edges) % 2),
    }
