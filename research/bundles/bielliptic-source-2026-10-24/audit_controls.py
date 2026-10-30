"""Bounded arithmetic controls, never passed off as native surface inputs."""

from itertools import product

from sympy import Matrix, eye, zeros

from bielliptic import (
    SplitSextic, action, adjoint, alternating_form, analyze_pullback,
    classify_involution, column_basis, discover_involutions, mod, product_actions,
)
from controls import ArithmeticSource
from kernel_output import odd_maximal_order
from pullback import reconstruct_pullbacks
from residual_controls import lagrangians, space_key


def arithmetic_source(kind):
    order = odd_maximal_order(11)
    one, i, zero = order.unit, Matrix([0, 1, 0, 0]), zeros(4, 1)
    if kind == "mixing":
        phi = Matrix.vstack(one, 2*one, -2*one, one)
        gamma = Matrix.vstack(one, zero, zero, -one)
    elif kind == "stable_swap":
        phi = Matrix.vstack(one, 2*i, 2*i, one)
        gamma = Matrix.vstack(zero, one, one, zero)
    else:
        raise ValueError("unknown arithmetic control")
    return ArithmeticSource(11, 5, order, phi, (gamma,))


def run_arithmetic(kind):
    source = arithmetic_source(kind)
    reconstruction = reconstruct_pullbacks(
        source.order, source.ell, source.characteristic, source.norms(),
        source.levels(), source.split, source.observe, max_auxiliary_prime=47)
    result = analyze_pullback(source.order, source.ell, source.split(source.ell),
                              reconstruction.coordinates[0])
    return source, reconstruction, result


def sl2_elements(prime):
    if prime not in (3, 5):
        raise ValueError("exhaustive SL2 control limited to three and five")
    for entries in product(range(prime), repeat=4):
        matrix = Matrix(2, 2, entries)
        if int(matrix.det()) % prime == 1:
            yield matrix


def rank_census(prime):
    j = alternating_form(2)
    row = eye(4)[:, [0, 2]].T*j
    gamma = Matrix.diag(1, 1, -1, -1)
    counts = {0: 0, 1: 0, 2: 0}
    for plane in lagrangians(prime):
        transport = mod(plane*row, prime)
        a = mod(adjoint(transport)*gamma*transport, prime)
        if mod(a-adjoint(a), prime) != zeros(4):
            raise ArithmeticError("bad self-adjoint control")
        rank = column_basis(a, prime).cols
        counts[rank] += 1
    return counts


def curve_control(prime=13):
    points = tuple((x % prime, 1) for x in (1, -1, 2, -2, 3, -3))
    curve = SplitSextic.from_branches(prime, points)
    return curve, points, discover_involutions(curve, points)


def order_four_control():
    points = tuple((x, 1) for x in (1, 12, 2, 7, 3, 9))
    curve = SplitSextic.from_branches(13, points)
    lift = classify_involution(curve, Matrix([[0, 1], [1, 0]]))
    return curve, lift
