"""Bounded exact regression for a false finite-difference log linearization.

This is an easy factorization family, not a candidate or a stabilizer algorithm.
Only p=5,7,11 and four-variable polynomials of total degree at most p are
accepted. All arithmetic is formal, sparse, and modulo p; no PIT is used.
Running this module prints JSON to stdout and never writes a report file.
"""
from __future__ import annotations

from itertools import product
import json
from math import comb


CONTROL_PRIMES = (5, 7, 11)
MAX_CONTROL_PRIME = 11
BASIS_DIRECTIONS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
Monomial = tuple[int, int, int, int]
Polynomial = dict[Monomial, int]
Direction = tuple[int, int, int]


def _prime(p: int) -> None:
    if type(p) is not int or p not in CONTROL_PRIMES:
        raise ValueError("bounded regression requires p in (5, 7, 11); no override")


def _direction(direction, p: int) -> Direction:
    _prime(p)
    if (not isinstance(direction, (tuple, list)) or len(direction) != 3
            or any(type(a) is not int or not 0 <= a < p for a in direction)):
        raise ValueError("direction must contain three canonical F_p integers")
    return tuple(direction)


def _polynomial(poly: Polynomial, p: int) -> Polynomial:
    _prime(p)
    if not isinstance(poly, dict):
        raise ValueError("a sparse coefficient dictionary is required")
    result = {}
    for powers, coefficient in poly.items():
        if (not isinstance(powers, tuple) or len(powers) != 4
                or any(type(e) is not int or e < 0 for e in powers)
                or sum(powers) > p or type(coefficient) is not int):
            raise ValueError("four nonnegative integer exponents, degree <= p, "
                             "and integer coefficients are required")
        if coefficient % p:
            result[powers] = coefficient % p
    return result


def _add(left: Polynomial, right: Polynomial, p: int,
         scale: int = 1) -> Polynomial:
    result = left.copy()
    for powers, coefficient in right.items():
        value = (result.get(powers, 0) + scale * coefficient) % p
        if value:
            result[powers] = value
        else:
            result.pop(powers, None)
    return result


def _multiply(left: Polynomial, right: Polynomial, p: int) -> Polynomial:
    result = {}
    for a, coefficient_a in left.items():
        for b, coefficient_b in right.items():
            powers = tuple(x + y for x, y in zip(a, b))
            value = (result.get(powers, 0) + coefficient_a * coefficient_b) % p
            if value:
                result[powers] = value
            else:
                result.pop(powers, None)
    return result


def _power(poly: Polynomial, exponent: int, p: int) -> Polynomial:
    result = {(0, 0, 0, 0): 1}
    while exponent:
        if exponent & 1:
            result = _multiply(result, poly, p)
        exponent //= 2
        if exponent:
            poly = _multiply(poly, poly, p)
    return result


def _coordinates(p: int) -> tuple[Polynomial, Polynomial, Polynomial]:
    u = {(1, 0, 0, 0): 1, (0, 1, 0, 0): p - 1}
    v = {(0, 1, 0, 0): 1, (0, 0, 1, 0): p - 1}
    z = {(0, 0, 0, 1): 1}
    return u, v, z


def family_polynomial(p: int) -> Polynomial:
    """Expand F=(x-y)^(p-1)(y-w), only at the bounded control primes."""
    _prime(p)
    u, v, _ = _coordinates(p)
    return _multiply(_power(u, p - 1, p), v, p)


def _action(poly: Polynomial, direction: Direction, p: int) -> Polynomial:
    # Substitute into each monomial, independently of the displayed log formulas.
    result = {}
    for powers, coefficient in poly.items():
        terms = {powers: coefficient}
        for index, shift in enumerate(direction):
            if shift == 0:
                continue
            expanded = {}
            for exponents, value in terms.items():
                for j in range(exponents[index] + 1):
                    target = list(exponents)
                    target[index] -= j
                    target[3] += j
                    factor = comb(exponents[index], j) * pow(shift, j, p)
                    expanded = _add(expanded, {tuple(target): value * factor}, p)
            terms = expanded
        result = _add(result, terms, p)
    return result


def finite_action(poly: Polynomial, direction: Direction, p: int) -> Polynomial:
    """Return F(x+az,y+bz,w+cz,z) as a formal polynomial."""
    direction = _direction(direction, p)
    return _action(_polynomial(poly, p), direction, p)


def finite_difference(poly: Polynomial, direction: Direction, p: int) -> Polynomial:
    direction = _direction(direction, p)
    poly = _polynomial(poly, p)
    return _add(_action(poly, direction, p), poly, p, -1)


def finite_log(poly: Polynomial, direction: Direction, p: int) -> Polynomial:
    """Actually sum (-1)^(j+1)(T-I)^j F/j for 1 <= j < p.

    The recurrence acts on the previous difference polynomial, not on a
    derivative formula or a formula for this family. Numeric p is paid.
    """
    direction = _direction(direction, p)
    current = _polynomial(poly, p)
    result = {}
    for j in range(1, p):
        current = _add(_action(current, direction, p), current, p, -1)
        result = _add(result, current, p, (-1)**(j + 1) * pow(j, -1, p))
    return result


def displayed_basis_logs(p: int) -> tuple[Polynomial, Polynomial, Polynomial]:
    """Closed formulas, used only as independent comparison targets."""
    _prime(p)
    u, v, z = _coordinates(p)
    first = _multiply(z, _multiply(_power(u, p - 2, p), v, p), p)
    second = _multiply(z, _power(u, p - 1, p), p)
    return (_add({}, first, p, -1),
            _add(_add(first, second, p), {(0, 0, 0, p): 1}, p),
            _add({}, second, p, -1))


def displayed_direction_log(p: int, direction: Direction) -> Polynomial:
    """Closed formula including the nonlinear degree-p directional carry."""
    a, b, c = _direction(direction, p)
    u, v, z = _coordinates(p)
    first = _multiply(_power(u, p - 2, p), v, p)
    second = _power(u, p - 1, p)
    derivative = _add(_add({}, first, p, b - a), second, p, b - c)
    carry = pow((a - b) % p, p - 1, p) * (b - c) % p
    return _add(_multiply(z, derivative, p), {(0, 0, 0, p): carry}, p)


def _terms(poly: Polynomial) -> list[dict]:
    return [{"powers": list(powers), "coefficient": coefficient}
            for powers, coefficient in sorted(poly.items())]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def module_length_control(p: int) -> dict:
    """Check all commuting generator-difference products of order p+1.

    I is generated by the three commuting T_i-I. Annihilating F with every
    such product also annihilates every translate, hence the whole orbit M.
    """
    _prime(p)
    poly = family_polynomial(p)
    layer = {(0, 0, 0): poly}
    nonzero_counts = [1]
    for order in range(1, p + 2):
        next_layer = {}
        for i in range(order + 1):
            for j in range(order - i + 1):
                counts = (i, j, order - i - j)
                index = next(k for k, count in enumerate(counts) if count)
                previous = list(counts)
                previous[index] -= 1
                value = layer[tuple(previous)]
                next_layer[counts] = _add(
                    _action(value, BASIS_DIRECTIONS[index], p), value, p, -1)
        layer = next_layer
        nonzero_counts.append(sum(bool(value) for value in layer.values()))
    witness = finite_difference(poly, BASIS_DIRECTIONS[2], p)
    for _ in range(p - 1):
        witness = finite_difference(witness, BASIS_DIRECTIONS[0], p)
    _require(witness == {(0, 0, 0, p): 1}, "order-p witness is not z^p")
    _require(nonzero_counts[p] > 0 and not any(layer.values()),
             "module action-length control failed")
    return {"action_length": p + 1, "I_power_p_nonzero": True,
            "I_power_p_plus_1_zero": True,
            "order_p_witness": _terms(witness),
            "order_p_plus_1_products_checked": len(layer),
            "nonzero_mixed_products_by_order": nonzero_counts}


def control(p: int) -> dict:
    """Exhaustive exact family control; fail closed on any disagreement."""
    _prime(p)
    poly = family_polynomial(p)
    logs = tuple(finite_log(poly, direction, p) for direction in BASIS_DIRECTIONS)
    _require(logs == displayed_basis_logs(p), "basis log formulas disagree")
    stabilizer = []
    linear_kernel = []
    for direction in product(range(p), repeat=3):
        invariant = finite_action(poly, direction, p) == poly
        actual_log = finite_log(poly, direction, p)
        _require(actual_log == displayed_direction_log(p, direction),
                 f"directional log formula disagrees at {direction}")
        _require((not actual_log) == invariant,
                 f"individual logarithm kernel disagrees at {direction}")
        if invariant:
            stabilizer.append(direction)
        linear_sum = {}
        for coefficient, value in zip(direction, logs):
            linear_sum = _add(linear_sum, value, p, coefficient)
        if not linear_sum:
            linear_kernel.append(direction)
    _require(stabilizer == [(a, a, a) for a in range(p)],
             "finite action disagrees with the full factorization stabilizer")
    _require(linear_kernel == [(0, 0, 0)], "linear-log kernel is not trivial")
    diagonal_sum = _add(_add(logs[0], logs[1], p), logs[2], p)
    _require(diagonal_sum == {(0, 0, 0, p): 1}, "diagonal false rejection lost")
    return {"p": p, "status": "EXACT_REGRESSION_PASS",
            "family_status": "EASY_FACTORIZATION_FAMILY",
            "matrix_dimension": 4, "group_class": 1,
            "group_order": p**3, "formal_degree": p,
            "finite_actions_checked": p**3, "direction_logs_checked": p**3,
            "individual_log_kernels_checked": p**3,
            "stabilizer": [list(a) for a in stabilizer],
            "linear_log_kernel": [list(a) for a in linear_kernel],
            "diagonal_finite_invariant": True, "diagonal_actual_log_zero": True,
            "diagonal_linear_log": _terms(diagonal_sum),
            "module_length": module_length_control(p)}


def report() -> dict:
    """Return only bounded exact controls, with no candidate promotion."""
    return {"status": "EXACT_REGRESSION_CONTROLS",
            "candidate": False, "hardness_evidence": False,
            "new_algorithm_claim": False, "general_stabilizer_solver": False,
            "uses_randomness": False, "max_control_prime": MAX_CONTROL_PRIME,
            "controls": [control(p) for p in CONTROL_PRIMES]}


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
