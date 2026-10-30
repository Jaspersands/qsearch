"""Exact elliptic identity controls, not the native matrix-only backend."""

from functools import lru_cache

import pytest
from flint import nmod_mat

from norm_completion import nullspace, rank, rows

P = 17


@lru_cache(None)
def monomials(degree):
    return tuple((a, b) for b in (0, 1) for a in range(2*degree+1)
                 if 2*a+3*b <= 4*degree)


def unit_space(degree):
    size = len(monomials(degree))
    return [[int(i == j) for j in range(size)] for i in range(size)]


def space(vectors):
    reduced, dimension = nmod_mat(vectors, P).rref()
    return rows(reduced)[:dimension]


def multiply(left, dl, right, dr):
    target = monomials(dl+dr)
    indices = {term: i for i, term in enumerate(target)}
    answer = [0]*len(target)
    for c, (a, b) in zip(left, monomials(dl)):
        for d, (u, v) in zip(right, monomials(dr)):
            terms = [(a+u, b+v, 1)] if b+v < 2 else [
                (a+u+3, 0, 1), (a+u+1, 0, 2), (a+u, 0, 2)]
            for x, y, factor in terms:
                answer[indices[x, y]] = (answer[indices[x, y]]+c*d*factor) % P
    return answer


def colon(dl, factors, dr, target):
    ann = nullspace(target, P)
    constraints = []
    for factor in factors:
        images = [multiply(unit, dl, factor, dr) for unit in unit_space(dl)]
        for j in range(len(ann[0])):
            constraints.append([sum(image[t]*ann[t][j] for t in range(len(ann))) % P
                                for image in images])
    if not constraints:
        return unit_space(dl)
    kernel = nullspace(constraints, P)
    return [[row[j] for row in kernel] for j in range(len(kernel[0]))]


def same_space(left, right):
    return rank(left, P) == rank(right, P) == rank(left+right, P)


def point_jets(degree, count):
    # Q=(0,6), x=t; implicit equation y^2=x^3+2x+2 has 2y(Q)!=0.
    y = [6]+[0]*(count-1)
    for j in range(1, count):
        rhs = (2 if j == 1 else 1 if j == 3 else 0)
        y[j] = (rhs-sum(y[i]*y[j-i] for i in range(1, j)))*pow(12, -1, P) % P
    result = []
    for order in range(count):
        result.append([int(order == a) if b == 0 else (y[order-a] if order >= a else 0)
                       for a, b in monomials(degree)])
    return result


def jet_kernel(degree, count):
    if count == 0:
        return unit_space(degree)
    kernel = nullspace(point_jets(degree, count), P)
    return [[row[j] for row in kernel] for j in range(len(kernel[0]))]


def ratio_mod_next(numerator, denominator, following):
    if rank(following+[denominator], P) == rank(following, P):
        raise ValueError("denominator has not reached its exact vanishing order")
    scalars = [c for c in range(P) if rank(following+[
        [(a-c*b) % P for a, b in zip(numerator, denominator)]], P) == rank(following, P)]
    if len(scalars) != 1:
        raise ValueError("ratio is not a regular one-dimensional quotient")
    return scalars[0]


def test_degree_eight_colon_filtration_matches_independent_jets():
    R4 = unit_space(4)
    U1 = jet_kernel(4, 1)
    current = R4
    for order in range(10):
        assert same_space(current, jet_kernel(4, order))
        F = colon(2, unit_space(2), 2, current)
        assert same_space(F, jet_kernel(2, order))
        if order == 0:
            current = U1
        elif order < 9:
            products = space([multiply(a, 4, b, 4) for a in current for b in U1])
            current = colon(4, R4, 4, products)


@pytest.mark.parametrize("pole_bound", [2, 3, 4])
def test_ratio_space_allows_extra_denominator_zeros(pole_bound):
    R2 = unit_space(2)
    sigma = [int(term == (2, 0)) for term in monomials(2)]
    Wj = [v for term, v in zip(monomials(2), R2)
          if 2*term[0]+3*term[1] <= 8-pole_bound]
    target = space([multiply(sigma, 2, v, 2) for v in R2])
    recovered = colon(2, Wj, 2, target)
    expected = []
    for term in monomials(1):
        if 2*term[0]+3*term[1] <= pole_bound:
            expected.append([int(t == (term[0]+2, term[1])) for t in monomials(2)])
    assert same_space(recovered, expected)


def test_common_zero_ratio_is_exact_and_frame_invariant():
    sigma = [int(term == (2, 0)) for term in monomials(2)]
    numerator = [(3*int(term == (2, 0))+5*int(term == (3, 0))) % P
                 for term in monomials(2)]
    # Both ordinary evaluations vanish. The order-two quotient returns 3.
    assert sum(a*b for a, b in zip(point_jets(2, 1)[0], sigma)) % P == 0
    assert sum(a*b for a, b in zip(point_jets(2, 1)[0], numerator)) % P == 0
    F3 = jet_kernel(2, 3)
    assert ratio_mod_next(numerator, sigma, F3) == 3
    for scale in range(1, P):
        assert ratio_mod_next([scale*x % P for x in numerator],
                              [scale*x % P for x in sigma], F3) == 3
    with pytest.raises(ValueError, match="exact vanishing"):
        ratio_mod_next(numerator, sigma, jet_kernel(2, 2))
    with pytest.raises(ValueError, match="regular"):
        ratio_mod_next(unit_space(2)[0], sigma, F3)
